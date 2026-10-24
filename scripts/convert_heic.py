#!/usr/bin/env python3
"""HEIC/HEIF → JPG/PNG 一括変換スクリプト (Windows / macOS / Linux)。

使い方:
    python convert_heic.py <file|dir|glob>... [--to jpg|png] [--quality N]
                           [--out-dir DIR] [--recursive] [--overwrite]

- 元ファイルは削除しない (非破壊)
- EXIF / ICC プロファイルは可能な限り引き継ぐ
- 回転情報 (Orientation) はピクセルに反映してから保存する (二重回転防止)
- 既存の出力ファイルはデフォルトでスキップ (--overwrite で上書き)

変換バックエンドは自動選択:
    1. Pillow + pillow-heif (全 OS / 推奨)
    2. sips (macOS 標準コマンド / pillow-heif 未導入時のフォールバック)
"""

from __future__ import annotations

import argparse
import glob
import shutil
import subprocess
import sys
from pathlib import Path

# バックエンド判定: pillow-heif が無い macOS では sips に自動フォールバック
try:
    from PIL import Image, ImageOps
    from pillow_heif import register_heif_opener

    register_heif_opener()
    BACKEND = "pillow"
except ImportError:
    if sys.platform == "darwin" and shutil.which("sips"):
        BACKEND = "sips"
    else:
        print(
            "依存ライブラリがありません。次でインストールしてください:\n"
            "  python3 -m pip install pillow pillow-heif\n"
            "(macOS は未導入でも標準の sips で動きますが、この環境では見つかりませんでした)",
            file=sys.stderr,
        )
        sys.exit(1)

HEIC_EXTS = {".heic", ".heif", ".hif"}


def collect_targets(inputs: list, recursive: bool) -> list:
    """入力 (ファイル / ディレクトリ / glob) から HEIC ファイル一覧を作る。"""
    targets = []
    for raw in inputs:
        p = Path(raw.strip('"')).expanduser()
        if p.is_dir():
            pattern = "**/*" if recursive else "*"
            targets.extend(
                f for f in sorted(p.glob(pattern))
                if f.is_file() and f.suffix.lower() in HEIC_EXTS
            )
        elif p.is_file():
            targets.append(p)
        else:
            # glob パターンとして解釈 (PowerShell はワイルドカードを展開しないため)
            matched = [Path(m) for m in glob.glob(str(p), recursive=True)]
            heics = [m for m in matched if m.is_file() and m.suffix.lower() in HEIC_EXTS]
            if heics:
                targets.extend(sorted(heics))
            else:
                print(f"[warn] 見つかりません: {raw}", file=sys.stderr)
    # 重複除去 (順序維持)
    seen = set()
    unique = []
    for t in targets:
        r = t.resolve()
        if r not in seen:
            seen.add(r)
            unique.append(t)
    return unique


def convert_pillow(src: Path, dest: Path, fmt: str, quality: int) -> None:
    """Pillow + pillow-heif での変換 (EXIF/ICC 引き継ぎ・回転補正)。"""
    with Image.open(src) as img:
        # Orientation をピクセルに反映 (EXIF の回転タグは除去される)
        img = ImageOps.exif_transpose(img)
        exif = img.info.get("exif")
        icc = img.info.get("icc_profile")
        save_kwargs = {}
        if exif:
            save_kwargs["exif"] = exif
        if icc:
            save_kwargs["icc_profile"] = icc
        if fmt == "jpg":
            if img.mode not in ("RGB", "L"):
                img = img.convert("RGB")
            save_kwargs.update(quality=quality, optimize=True)
            img.save(dest, "JPEG", **save_kwargs)
        else:  # png
            img.save(dest, "PNG", **save_kwargs)


def convert_sips(src: Path, dest: Path, fmt: str, quality: int) -> None:
    """macOS 標準 sips での変換 (追加インストール不要)。"""
    sips_fmt = "jpeg" if fmt == "jpg" else "png"
    cmd = ["sips", "-s", "format", sips_fmt]
    if fmt == "jpg":
        cmd += ["-s", "formatOptions", str(quality)]
    cmd += [str(src), "--out", str(dest)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())


def convert_one(src: Path, fmt: str, quality: int, out_dir, overwrite: bool) -> str:
    """1 ファイル変換。結果を 'converted' / 'skipped' / 'error' で返す。"""
    dest_dir = out_dir if out_dir else src.parent
    dest = dest_dir / (src.stem + "." + fmt)
    if dest.exists() and not overwrite:
        print(f"[skip] 既に存在: {dest}")
        return "skipped"
    try:
        if BACKEND == "pillow":
            convert_pillow(src, dest, fmt, quality)
        else:
            convert_sips(src, dest, fmt, quality)
        print(f"[ok]   {src.name} -> {dest}")
        return "converted"
    except Exception as e:  # 1 枚の失敗で全体を止めない
        print(f"[error] {src}: {e}", file=sys.stderr)
        return "error"


def main() -> int:
    ap = argparse.ArgumentParser(description="HEIC/HEIF を JPG/PNG に変換する")
    ap.add_argument("inputs", nargs="+", help="HEIC ファイル / ディレクトリ / glob パターン")
    ap.add_argument("--to", choices=["jpg", "png"], default="jpg", help="出力形式 (default: jpg)")
    ap.add_argument("--quality", type=int, default=92, help="JPG 品質 1-100 (default: 92)")
    ap.add_argument("--out-dir", type=Path, default=None, help="出力先ディレクトリ (default: 元と同じ場所)")
    ap.add_argument("--recursive", action="store_true", help="ディレクトリ指定時にサブフォルダも対象にする")
    ap.add_argument("--overwrite", action="store_true", help="既存の出力ファイルを上書きする")
    args = ap.parse_args()

    targets = collect_targets(args.inputs, args.recursive)
    if not targets:
        print("変換対象の HEIC ファイルが見つかりませんでした。", file=sys.stderr)
        return 1

    if args.out_dir:
        args.out_dir.mkdir(parents=True, exist_ok=True)

    counts = {"converted": 0, "skipped": 0, "error": 0}
    for src in targets:
        counts[convert_one(src, args.to, args.quality, args.out_dir, args.overwrite)] += 1

    print(f"\n完了: 変換 {counts['converted']} 件 / スキップ {counts['skipped']} 件 / 失敗 {counts['error']} 件 (backend: {BACKEND})")
    return 0 if counts["error"] == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
