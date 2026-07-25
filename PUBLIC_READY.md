# PUBLIC_READY — 公開判定メモ

対象: `nexus-ai-2045/heic-convert` / 判定日: 2026-07-20 (ローカル整備時点)

## ローカル確認済み

- [x] **機能検証**: 合成 HEIC (EXIF 付き / 大文字拡張子 / サブフォルダ) と実写真 15 枚で変換成功、
      EXIF 引き継ぎ・非破壊 (元ファイル無変更)・既存出力スキップを実測確認 (backend: pillow)。
- [x] **依存欠如経路**: pillow-heif 不在時にインストール案内を出して exit 1 することを実測確認。
      (macOS sips フォールバックはコードパス分岐まで確認。実機 macOS での実行検証は未実施 — 既知の残課題)
- [x] **ネットワークアクセスなしの突合**: `grep -rhoE 'https?://[a-zA-Z0-9.-]+' scripts/` → 0 件。
      SECURITY.md の宣言と実装が一致。
- [x] **identity 検査**: 個人名義・個人アカウント識別子の内容 grep (所定パターン一式) 0 件 /
      個人ローカルパス 0 件 / git identity は `nexus_ai <273569186+nexus-ai-2045@users.noreply.github.com>`。
- [x] **履歴の清潔さ**: 初回 commit から個人パス・個人名義を含まない
      (toc-engine の「初期 commit に個人パス混入 → 履歴作り直し」教訓の予防)。
- [x] **ライセンス**: コードは MIT (Copyright (c) 2026 nexus_ai)。外部データのミラーなし。
      依存 (Pillow: MIT-CMU / pillow-heif: BSD-3-Clause) は同梱せず利用者インストール方式。
- [x] SECURITY.md / LICENSE / README (ライセンスと出典セクション) 配置済み。

## GitHub 側 (未検証 / 公開前に要実施)

- [ ] private repo 作成 + push 後、`gh api -X PUT repos/nexus-ai-2045/heic-convert/private-vulnerability-reporting`
      → GET で `enabled=true` を実測。
- [ ] secret scanning / push protection の有効化確認 (公開後に audit-public-repo-lockdown が監視)。
- [ ] push_gate 登録: `github-account-repo-map.md` + `push_gate.sh` の `PUBLIC_PUSH_ALLOWLIST` 追記 (CEO 承認 / Type1)。
- [ ] CEO による内容の目視レビュー。
- [ ] **public 化 (visibility 変更) — CEO 明示承認が gate。ここまでは一切実施しない。**

## 残課題 (公開ブロッカーではない)

- macOS 実機での sips フォールバック実行検証 (1 枚試し変換で足りる)。
- canonical skill registry (`nexus-ai-2045/nexus-ai-skills`) への登録は、同 repo の
  migration hold (duplicate checkout / behind 32) 解消後に実施。
