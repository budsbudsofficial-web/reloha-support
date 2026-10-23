# RELOHA 販促・編集運用の追加作業 — 2026-10-23

この記録は同日の `RELOHA_WORK_HANDOFF_2026-10-23.md` に続く追加実施記録。従来の14記事の公開、計測受信、Search Consoleの切り分けは同引き継ぎを参照。

## 公開した内容

- `holiday-plant-care`：旅行・帰省時の不在期間と普段の乾き方を照合する記事。日数別の準備表、器具の事前確認、家族向けの架空の引き継ぎメモ、帰宅後の確認。日数・給水器具での成功を保証しない。
- `wilting-after-repotting`：植え替え後のしおれを作業履歴、根鉢・用土、排水、光・温度から確認。追加の水・追肥・根の触り直しを急がない条件と相談の判断。回復期間は保証しない。
- 記事本文は各 `content/guides/*.json` が正本。既存共通CSS・記事構造と指定宣伝画像を使用。新規記事ごとにFAQ5問、参考資料、記事別App Storeリンクを設定。
- `watering-when`、`plant-care-multiple`、`repotting-signs`、`drooping-leaves` の関連リンクから新記事へ接続。
- 記事数は14→16、サイトマップURL数は17→19。従来のURLは維持。
- 公式トップ・モバイル公式・演出・プライバシー・analytics.jsは変更していない。

## 参照と素材

本文根拠はMaryland大学Extension、RHS、ハイポネックスの一次情報を確認。以下の確認範囲を記事末尾へ記載。

- https://extension.umd.edu/resource/watering-indoor-plants — 乾湿・重さ・排水、過湿でもしおれる点。
- https://www.rhs.org.uk/plants/types/houseplants/holiday-care — 不在期間・季節、給水方式と失敗要因、長期の世話依頼。
- https://www.rhs.org.uk/plants/types/houseplants/how-to-help-a-poorly-houseplant — 光・水・温度の確認。
- https://extension.umd.edu/resource/potting-and-repotting-indoor-plants — 初回の水やりと、その後の追加の区別。
- https://www.hyponex.co.jp/plantia/plantia-6847/ — 元気のない観葉植物の環境確認、種類と時期による根鉢の扱い。
- https://www.hyponex.co.jp/plantia/plantia-14846/ — 植え替え直後の追肥への注意。

競合検索は検索意図の定性的な確認であり、検索需要・順位・難易度の定量測定ではない。本文と表・確認順序・架空メモは独自編集。RHSの英国の季節条件や海外資材の推奨を日本へ一律転用していない。

画像は既存の `indoor-collection.webp` と `repotting-care.webp` をテーマイメージとして再利用。生成来歴は既存 `GUIDE_IMAGE_PROVENANCE_2026-10-23.json`。症例・旅行中の成功・成長比較の証拠として使っていない。新しい外部写真の転載や新規生成は行っていない。

## 維持方法

`python scripts/build-guides.py` は記事に加え、一覧・XML/TXT・QA選択肢を更新する。

- 一覧テンプレート：`content/guide-index.template`。HTML拡張子にはせず、公開記事に混同しない。
- 一覧の順序：`content/guide-order.json`。記事を1本追加したら同時に1回だけ登録する。未登録・重複はビルド時に停止。
- 一覧のタイトル・説明は記事JSONから生成。画面上の順序と一致する `ItemList` を生成。
- 一覧にあった不一致の閉じタグを修正。
- 新規記事ディレクトリはビルドで作成。
- `check-site.py` が全原稿と一覧リンク・サイトマップの一致、XML/TXTの一致、一覧構造化データとリンク順序の一致を検査。
- QAページは `docs/qa/all-guides.html?v=<revision>` で記事iframeにバージョンを付けられる。古い本文がブラウザキャッシュに残る場合に利用。QA親はnoindex,nofollow、iframe内のGA4除外は従来のまま。

## 検証記録

- 内容コミット：`3d3016eadd38661e1b19b1a69776c44962b4f7ee`。Pages run `39946947209` 成功。
- 見出し・App Store紹介の狭幅調整：`c036a25c5319d1c94e6df4d4d1a5ba7f00818b81`。Pages run `39947632218` 成功。
- バージョン付きQAの追加：`cec9872a51c9f226f71ccaa3cc44a2fab1ecf6c8`。
- 32公開ファイルの200応答とローカル一致：`PUBLIC_PROMOTION_VERIFICATION_2026-10-23.json`。
- 16記事×320/390pxの32表示で本文横はみ出しなし。スクロールバーを除く本文幅は305/375px。
- 初回に画像読込中だった11表示は8記事の再確認で全て読込成功。初回記録を成功に書き換えていない。
- 新2記事のFAQ開閉、目次移動、表の横スクロール領域、宣伝画像の読込・縦横比、記事別App Store URLを確認。リンク遷移の自己テストは増やしていない。
- 最終見出しと紹介文はバージョン付きQAで実際の反映と横はみ出しなしを再確認。古いブラウザキャッシュ上の表示を最終版の検証と混同しない。
- 公開サイトで検証。実機iPhone Safari確認は依然未実施。
- `python scripts/check-site.py`：21公開HTML、19サイトマップURL、エラーなし。
- `python scripts/check-guides.py`：16記事、エラーなし。
- `node scripts/check-analytics.cjs`：成功。
- `git diff --check`：成功。再生成の冪等性を確認。

## 計測・検索掲載の確認

GA4の「今日」を指定したページ別通常レポート・流入元レポート・イベントレポートで集計を確認。既定期間が当日を除く場合があるので、初日を確認するときは期間に注意。前回の自己テストが含まれるため、自然送客・実ダウンロード獲得の成果とは扱わない。具体的な閲覧・参照元の数値や管理画面の証跡は公開リポジトリに保存していない。

Search ConsoleではXML/TXTの「取得できませんでした」が継続。XML詳細は「サイトマップを読み込めませんでした」で、原因を特定する通信詳細は確認できない。既存水やり記事は確認時点でもGoogle未認識。ライブテスト成功の過去記録から掲載完了を推測しない。

新記事追加で19URLへ更新したXMLを一度だけ通知し、送信受付を確認。取得成功は未確認。TXT再送信や、同じ既存記事の登録依頼は行っていない。旅行記事の個別登録依頼は受付・優先クロールキュー追加を確認。植え替え後の記事は初回の依頼で一時的な送信エラーが出た。再試行結果は本記録の最終追記を参照。

## 保留と次の作業

- Search Consoleの通常取得、Google掲載完了、自然検索流入、App Store Connectの実DLは別に追う。
- 実機Safari検証は未実施として残す。
- ホスト直下の別リポジトリ作成や所有権設定、ドメイン購入、DNS変更は行っていない。エラー原因未確定のまま大きな構成変更をしない。
- 課金、重要データ削除、大幅デザイン変更、外部への連絡は行っていない。
- 承認が必要な操作を見切り発車で行っていない。通常の編集・検証・公開は委任範囲で実施。

## 最終追記

植え替え後の記事の個別登録依頼は、時間を空けた一度の再試行でも同じ送信エラーが表示された。これ以上の連続試行は行わず保留。旅行記事の受付済みと混同しない。エラー文は「インデックス登録リクエストの送信中に問題が発生しました。しばらくしてからもう一度お試しください。」。CAPTCHA操作や認証回避はしていない。

表示確認の要約と初回画像読込中・再確認・最終コピー確認の区別は `BROWSER_PROMOTION_VERIFICATION_2026-10-23.json` を参照。
