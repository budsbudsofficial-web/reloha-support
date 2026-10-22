# RELOHA 公式サイト制作 引き継ぎ（2026-10-12）

> 最新の編集・計測・未解決事項は [2026-10-23 Work引き継ぎ](RELOHA_WORK_HANDOFF_2026-10-23.md) を参照。この文書は実施時点の記録です。

## 確定した方向性
RELOHA公式サイトは **1ページの連続したスクロール体験** とする。別ページ「New Experience」に移動する構成は不採用。植物写真 → 立体的な写真の集合 → 実際のアプリUIを表示したiPhone → コピー → 既存の公式サイト本編、という流れをクリックなしで自然につなぐ。現在の統合版をベースに、今後は追加と微調整を重ねる。既存の演出・サポート・プライバシーを勝手に大きく変えない。

## リポジトリとURL
- GitHub: `budsbudsofficial-web/reloha-support`（main）
- 公式サイト: https://budsbudsofficial-web.github.io/reloha-support/
- 演出単独: https://budsbudsofficial-web.github.io/reloha-support/experience/
- ルート: `index.html`、演出: `experience/index.html`、ルート `.nojekyll` 確認済み
- Apple App Reviewに関係する公式サポートURLは維持する。

## ここまでの経緯
1. プレミアムな植物スクロール演出を制作。3枚の異なる写真、iPhoneの本物UI、ステータスバーなし、立体感を重視。
2. PHOTO/JOURNAL/REPLAYの紹介やCTAを追加。
3. GitHub Pagesに公開。文字だけ表示される問題があったが、その後正常表示を確認。
4. スクロール終盤のiPhoneとコピーの重なりを修正（commit `df2fae04f2aa0d760bcc26ae65ec48b610191319`）。
5. 一度、既存サイトから「New Experience ↗」への別ページリンクを追加したが、ユーザーが不採用とした。
6. 公式サイトの先頭に演出を組み込み、既存サイト本編へスクロールで連続させる方式に変更（commit `2b1c6820827f4ce92537d3a3a708921f3587a135`）。ユーザーが「そうそう、このイメージ、あとはこれをベースに追加と調整」と承認。

## 現在の実装
- ルートの `index.html` 冒頭に `#reloha-intro-scroll`（初期650vh）と `#reloha-intro-frame` iframeを配置。
- iframeは同一オリジンの `./experience/` を読み込み、親スクロールをiframeに同期。
- iframe内の `#reloha-product` は非表示にして、既存公式サイトの本編につなぐ。
- 導入中は既存ナビゲーションを隠し、終わると表示。
- 既存 `#support` と `#privacy` は保持。
- **注意**：iframe同期は暫定実装。Safari・スマホ・リサイズ・境界の自然さなどの実機検証は未完了。GitHub書き込み成功と公開サイトのブラウザ検証は区別する。

## 次回の開始
1. この統合版を正式なベースとして扱う。別ページ方式に戻さない。
2. ユーザーの希望する追加・調整を聞く。指定がなければスクロール境界の自然さ、モバイル、同期、アニメーションの調整を提案。
3. GitHubプラグインで最新ファイルとSHAを確認してから最小限の修正を行う。
4. ルート `index.html` は約2.8MBで `fetch_file` が空を返すことがある。その場合 `fetch_blob` にblob SHAを渡すと全文を取得できた。演出HTMLは約509KB。
5. 既存のサポート・プライバシーを維持し、変更内容と公開確認の有無を明示する。

## 再開の一言
「RELOHAの公式サイト、前回の統合版をベースに続きをやろう」
