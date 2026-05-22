# Sumi Browser 開発ガイド

## プロジェクト概要
Firefox fork ベースのミニマルブラウザ。薄いコア + プラグイン拡張。

## 技術スタック
- Firefox (Gecko エンジン) — `engine/` に展開
- surfer (`@zen-browser/surfer`) — Firefox fork ビルドツール
- パッチベースの改変 — `src/` にパッチ、`engine/` にFirefox本体

## ビルドコマンド
```bash
npm run init          # Firefox DL + bootstrap + パッチ適用（初回のみ）
npm run build         # フルビルド
npm run build:ui      # UI変更のみの高速ビルド
npm start             # ビルド済みブラウザを起動
npm run import        # パッチを engine/ に適用
npm run export <file> # engine/ の変更をパッチとして保存
npm run status        # engine/ の変更状況を表示
npm run reset         # engine/ をFirefox元の状態に戻す
```

## ディレクトリ構成
```
sumi-browser/
├── engine/          # Firefox ソース（git管理外）
├── src/             # Sumi のパッチ・カスタムコード
│   ├── browser/     # Firefox browser/ へのパッチ
│   └── sumi/        # Sumi 固有の機能
│       ├── common/       # 共通ユーティリティ
│       ├── sidebar/      # 縦タブサイドバー
│       └── command-palette/ # コマンドパレット
├── prefs/           # 設定ファイル (YAML)
├── configs/         # ビルド設定
├── surfer.json      # surfer 設定（ブランド、バージョン）
└── package.json     # npm スクリプト
```

## engine/ パッチ（surfer reset 後に再適用が必要）
`surfer reset` や `surfer download --force` 後は以下を実行:
```bash
python scripts/apply-engine-patches.py
```
パッチ内容:
1. `mozconfig.py` — 日本語 Windows での UTF-8 デコードエラー修正
2. `data.py` — Unified ファイル名の切り詰めロジック修正（WebRTC ビルドエラー回避）

## 開発ワークフロー
1. `engine/` 内のファイルを編集
2. `npm run status` で変更確認
3. `npm run export <変更したファイルのパス>` でパッチ化
4. `npm run build:ui` で高速リビルド
5. `npm start` で確認
6. パッチファイルをgit commit

## 設計思想
- `project_sumi_browser.md` を参照
- Anti-Bloat: 困る人が1人でもいる機能は入れない
- 外部化: コアは薄く、拡張はコミュニティに委ねる
- 寛容さ: UI根幹まで変えるプラグインも受け入れる
