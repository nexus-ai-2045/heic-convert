# PUBLIC_READY — 公開判定メモ

対象: `nexus-ai-2045/heic-convert`
状態: **公開済み** (2026-07-29 public 化) / 機能検証 2026-07-20 / 判定 2026-07-25 / 最終確認 2026-08-04

## ローカル確認済み

- [x] **機能検証**: 合成 HEIC (EXIF 付き / 大文字拡張子 / サブフォルダ) と実写真 15 枚で変換成功、
      EXIF 引き継ぎ・非破壊 (元ファイル無変更)・既存出力スキップを実測確認 (backend: pillow)。
- [x] **依存欠如経路**: pillow-heif 不在時にインストール案内を出して exit 1 することを実測確認。
      (macOS sips フォールバックはコードパス分岐まで確認。実機 macOS での実行検証は未実施 — 既知の残課題)
- [x] **ネットワークアクセスなしの突合**: `grep -rhoE 'https?://[a-zA-Z0-9.-]+' scripts/` → 0 件。
      SECURITY.md の宣言と実装が一致。
- [x] **identity 検査**: 個人名義・個人アカウント識別子の内容 grep (所定パターン一式) 0 件 /
      個人ローカルパス 0 件 / git identity は nexus noreply 名義。
- [x] **履歴の清潔さ**: 初回 commit から個人パス・個人名義を含まない
      （個人パス混入を防ぐための履歴作り直し）。
- [x] **ライセンス**: コードは MIT (Copyright (c) 2026 nexus-ai-2045)。外部データのミラーなし。
      依存 (Pillow: MIT-CMU / pillow-heif: BSD-3-Clause) は同梱せず利用者インストール方式。
- [x] SECURITY.md / LICENSE / README (ライセンスと出典セクション) 配置済み。

## GitHub 側 (公開完了 / 2026-07-29 実施・2026-08-04 最終確認)

- [x] repo 作成 (`nexus-ai-2045/heic-convert`)。
- [x] **public 化** — CEO 明示承認のうえ visibility を変更。API で `visibility=public` を実測。
- [x] Private Vulnerability Reporting — 有効化後 GET で `enabled=true` を実測。
      (private repo では同 API が 404 を返す = 本機能は public repo 限定であることを実測確認済み)
- [x] secret scanning / push protection — 公開直後は両方 disabled だったため有効化し、`enabled` を実測。
- [x] lockdown 監査 — `audit-public-repo-lockdown.ps1` 実行。全 public repo PASS。本 repo は
      public_ready / readme / license / security すべて True、secret 検出 0、個人パス scan clean。
- [x] 内容の目視レビュー (CEO)。
- [x] repo↔account map への登録 — Projects PR #486 として merge 済み (2026-08-02)。
      当初予定していた `push_gate.sh` の `PUBLIC_PUSH_ALLOWLIST` 追記は、2026-07-26 の identity
      registry 移行で同 allowlist 自体が廃止されたため不要と判断して取り下げた
      (owner=nexus-ai-2045 は公開 lane identity として自動導出される)。

## 残課題 (公開ブロッカーではない)

- macOS 実機での sips フォールバック実行検証 (1 枚試し変換で足りる)。
- canonical skill registry （共通スキル管理リポ） への登録は、同 repo の
  migration hold (duplicate checkout / behind 32) 解消後に実施。
