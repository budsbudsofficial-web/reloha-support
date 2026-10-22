# RELOHA 植物記事の重点改善（2026-10-23）

## 対象と実装
- fungus-gnats / brown-tips / winter-watering の3記事を、検索意図と具体的な判断手順に沿って全面的に書き直した。URLは維持。
- 冒頭の結論、今日の3行動、目次、原因・状態の比較表、実施順序、FAQ、関連記事、出典を用意。
- 写真・メモで変化を振り返るという実機能に沿って、記事ごとのRELOHA紹介を作成。アプリに自動診断があるような説明はしない。
- ArticleとBreadcrumbListを生成。確認した更新日のみをdateModifiedへ反映し、未確認の公開日・専門家監修は追加しない。FAQPageによる検索表示の保証は行わない。
- 既存トップ・PCスクロール演出・スマホ版の実装は変更しない。
- content/guides/*.json を編集し、python scripts/build-guides.py で3ページを再生成する。共通CSSは assets/guide-editorial.css。
- docs/qa/guide-layout.html はnoindexの390px幅iframeによる開発用確認ページ。実機Safariの検証ではない。iframe内は既存のanalyticsガードで計測しない。QA親ページにも計測を設置しない。

## 調査と編集上の判断
- コバエ：KINCHO園芸は発生源と種類の違いを整理している。UC IPM・RHS・Cornellの情報と照合し、成虫の捕獲と土内の段階への管理を分ける。虫の種類・効果・対策日数を断定しない。薬剤や自己流の混合物の処方はしない。
- 葉先：Iowa State UniversityとUC IPMでは、水の過不足・肥料由来の塩類・湿度など複数の要因が示される。RELOHAでは「茶色＝水不足」としない確認表、切除と原因対策の違い、同じ葉の前後比較を重視する。
- 冬：園芸ネット・RHS・University of Marylandを照合。冷える室内を想定した固定回数だけを一般化せず、暖房、生育状態、鉢の重さ、用土内部の湿り気を分けて説明。冬に育つ種類・鉢底穴のない容器などへの一律適用を避ける。
- 検索結果の調査は時点・地域・検索環境で変化する。検索需要・順位・流入増の実測結果ではない。競合の表現をコピーせず、家庭での観察と判断の順序を独自に構成した。
- 国内の参考情報には種類や条件を広く一般化した説明もあるため、植物名・生育状態・ラベルを優先する。この記事自体も個別診断や専門家による実体験の報告ではない。

## 画像とプロンプト
組み込みのimagegenを使用。イメージ用の生成画像であり、実写の症状写真や虫の同定画像としては使わない。各figureにAI生成と明記。1536×1024の出力から1200×800 WebPへ形式・サイズを最適化。

保存先：assets/guide/fungus-gnats.webp、assets/guide/brown-tips.webp、assets/guide/winter-watering.webp。

プロンプトの要点：
1. photorealistic-natural / premium Japanese houseplant magazine / 3:2 / healthy pothos in pale clay pot, textured potting mix, small plain yellow sticky card, hand holds pot rim, diffuse morning window light, cream and sage palette. No drawn insects, no text/logo/watermark. Context illustration, not diagnostic evidence.
2. photorealistic-natural / 3:2 / healthy compact dracaena marginata in matte ivory pot on oak table, natural red margins, close view of leaf textures, soft Japanese interior and side light. No people, insects, disease, text/logo/watermark. Context image, not symptom photograph.
3. photorealistic-natural / 3:2 / quiet winter Japanese apartment, healthy rubber plant and fern inward from window with leaves away from glass, ivory watering can not pouring, folded wool throw, cool daylight and warm oak textures. No people, indoor snow, condensation, heater, text/logo/watermark. Context illustration.

## 検証の区別
ローカルのリンク・canonical・構造化JSON・analytics参照、目次と出典のフラグメント、単一H1、再生成の一致を検査。公開後のレイアウトとアセット配信は別途確認する。Googleへの掲載、GA4受信、実機Safariはコード検査と混同しない。

## 公開後の確認結果
- commit ca63c07e718e5917a2f62315b2f54abe9073d5b3 のPagesビルド・デプロイ成功を確認。
- 公開3記事の390px iframeで本文の横はみ出しなし（デスクトップのスクロールバー分を除いた本文viewportは375px）。見出し・各hero画像を表示できた。
- 3記事とも目次からFAQへ移動でき、アプリ画面の遅延読込を確認。コバエ記事でFAQの開閉を確認。
- コバエ記事の比較表はコンテナ内でキーボードによる横スクロールが動作（scrollLeft 40px）し、本文の横幅を押し広げていない。
- 公開PC表示を目視確認。導入文にtext-wrap:pretty / word-break:auto-phraseを追加し、日本語の不自然な分割を抑える。
- これらはデスクトップChromeでのPC表示および狭幅iframeの検証であり、iPhone実機Safariの確認は未実施。
- Search Consoleを再確認したところXML/TXTとも取得エラーが継続。今回の品質改善によって検索順位やインデックスが改善したという確認はまだない。
