---
name: heic-convert
description: >-
  HEIC/HEIF 画像を JPG または PNG に変換するスキル (Windows / macOS / Linux 対応)。同梱の Python
  スクリプトで単発・複数・フォルダ一括の変換を非破壊 (元ファイル保持・EXIF/ICC 引き継ぎ・回転補正付き) で行う。
  「HEICをjpgにして」「iPhoneの写真を変換して」「この画像が開けない (.heic)」「HEIF を PNG に」
  「写真フォルダをまとめて変換」など、HEIC/HEIF 形式の変換・閲覧不能トラブルに関する依頼が来たら、
  明示的に「スキル」と言われなくても必ずこのスキルを使う。
compatibility: >-
  Python 3.9+ / pillow + pillow-heif 推奨 (macOS は未導入でも標準 sips に自動フォールバック)。
  Claude Code / Codex / その他 AGENTS.md 系エージェント共通。
---

# heic-convert — HEIC/HEIF → JPG/PNG 変換

## 実行方法

スクリプトは本スキルディレクトリの `scripts/convert_heic.py`。
ユーザーが渡したパス (ファイル / フォルダ / glob) をそのまま渡せばよい:

```
<python> <このスキルのディレクトリ>/scripts/convert_heic.py <パス>... [オプション]
```

`<python>` は OS ごとに選ぶ:

| OS | interpreter |
|---|---|
| Windows | インストール済み Python のフルパス推奨 (素の `python`/`python3` は Store スタブに解決される罠あり) |
| macOS / Linux | `python3` |

依存: `pillow` + `pillow-heif`。未導入で import に失敗したら `<python> -m pip install pillow pillow-heif`。
macOS では pillow-heif が無くてもスクリプトが標準の `sips` コマンドに自動フォールバックするので、そのまま実行してよい。

| オプション | 意味 | デフォルト |
|---|---|---|
| `--to jpg\|png` | 出力形式 | `jpg` |
| `--quality N` | JPG 品質 (1-100) | `92` |
| `--out-dir DIR` | 出力先フォルダ | 元ファイルと同じ場所 |
| `--recursive` | フォルダ指定時にサブフォルダも対象 | off |
| `--overwrite` | 既存出力を上書き | off (スキップ) |

実行後、スクリプトが出す「変換 N 件 / スキップ N 件 / 失敗 N 件」のサマリと出力先をユーザーに報告する。
失敗があった場合はエラーメッセージを添える。

## 使い分けの目安

- 写真 (iPhone 撮影など) → `jpg` (デフォルト)。ファイルサイズが小さく汎用性が高い。
- 透過が必要 / 無劣化にしたい → `--to png`。
- ユーザーが形式を指定しない場合は jpg で進めてよい (報告時に「PNG も可能」と一言添える)。

## クラウド同期フォルダ (iCloud / OneDrive / Dropbox) の入力を渡された時

- 変換は読み取り専用なので元の写真にリスクはない。
- ただし**出力先を同期フォルダ内にすると変換後の jpg/png がクラウドへ同期アップロードされる**。
  意図しない重複を避けるため、`--out-dir` で同期フォルダの外 (例: `~/Pictures/HEIC_converted`) に出力する。
- 「オンラインのみ」状態のファイルは開いた瞬間に OS が自動ダウンロードする (無害だが時間がかかることがある)。

## 設計上の性質 (ユーザーに聞かれたら説明する)

- **非破壊**: 元の HEIC は削除・変更しない。
- **メタデータ**: EXIF (撮影日時・位置情報など) と ICC プロファイルは出力に引き継ぐ。
  位置情報を落としたい要望があれば、その時だけ `exif` を外す改造を提案する。
- **回転**: EXIF Orientation はピクセルに反映してから保存するので、どのビューアでも正しい向きになる。
- **安全な再実行**: 既存出力はデフォルトでスキップするため、同じフォルダに何度かけても壊れない。
- **バックエンド**: Pillow (全 OS) → sips (macOS フォールバック) の順で自動選択。サマリ末尾に使用 backend を表示。

## トラブルシューティング

- `ModuleNotFoundError` → `<python> -m pip install pillow pillow-heif` (macOS はそのまま再実行でも sips で動く)。
- 「ファイルが見つからない」→ スペースや日本語を含むパスは `"..."` で囲んで渡す。引用符自体はスクリプト側で除去する。
- sips バックエンドは JPG 品質指定のみ対応。細かい制御が必要なら pillow-heif を導入する。
