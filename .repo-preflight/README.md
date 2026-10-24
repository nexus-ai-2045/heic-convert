# 名義検査

許可名義は allowed-identities.json のみ。検査時に --allowed-identities で明示指定する。

repo-preflight はローカルの固定済み検査ツールを使用する。pre-commit はステージ内容・名義・秘密、commit-msg は本文を検査する。
