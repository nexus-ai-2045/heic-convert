# heic-convert

HEIC/HEIF 画像を JPG / PNG に一括変換する Python スクリプトと、AI コーディングエージェント
(Claude Code / Codex など) 用の SKILL 定義のセットです。

- **非破壊**: 元の HEIC/HEIF ファイルは削除・変更しません
- **メタデータ引き継ぎ**: EXIF (撮影日時など) と ICC プロファイルを出力に保持します
- **回転補正**: EXIF Orientation をピクセルに反映してから保存するため、どのビューアでも正しい向きになります
- **安全な再実行**: 既存の出力ファイルはデフォルトでスキップします (`--overwrite` で上書き)
- **クロスプラットフォーム**: Windows / macOS / Linux。macOS では pillow-heif 未導入でも標準の `sips` に自動フォールバックします
- **ネットワークアクセスなし**: 完全にローカルで動作します

## 使い方

```bash
# 依存 (推奨。macOS は省略しても sips で動作)
python3 -m pip install pillow pillow-heif

# 単発
python3 scripts/convert_heic.py photo.heic

# フォルダ一括 → PNG、出力先指定、サブフォルダ含む
python3 scripts/convert_heic.py ~/Pictures --to png --out-dir ~/Pictures/converted --recursive
```

> Windows では素の `python` / `python3` が Microsoft Store のスタブに解決されることがあります。
> その場合はインストール済み Python のフルパスで実行してください。

| オプション | 意味 | デフォルト |
|---|---|---|
| `--to jpg\|png` | 出力形式 | `jpg` |
| `--quality N` | JPG 品質 (1-100) | `92` |
| `--out-dir DIR` | 出力先ディレクトリ | 元ファイルと同じ場所 |
| `--recursive` | ディレクトリ指定時にサブフォルダも対象 | off |
| `--overwrite` | 既存出力を上書き | off (スキップ) |

## クラウド同期フォルダ (iCloud / OneDrive / Dropbox) の注意

変換は読み取り専用なので元の写真は安全ですが、**出力先を同期フォルダ内にすると変換後の
jpg/png がクラウドへ同期アップロードされます**。意図しない重複を避けたい場合は
`--out-dir` で同期フォルダの外を指定してください。

## AI エージェントでの利用

[`SKILL.md`](./SKILL.md) は Claude Code などの skill 形式の定義です。
skill ディレクトリ (例: `~/.claude/skills/heic-convert/`) にこの repo の内容を配置すると、
「HEIC を jpg にして」のような依頼で自動発火します。

## ライセンスと出典

- コード・ドキュメント: [MIT License](./LICENSE) (Copyright (c) 2026 nexus_ai)
- 依存ライブラリ: [Pillow](https://python-pillow.org/) (MIT-CMU) /
  [pillow-heif](https://github.com/bigcat88/pillow_heif) (BSD-3-Clause)。
  いずれも本 repo には同梱せず、利用者が各自インストールします。
- 外部データのミラー・再配布は含みません。
