# GitHubブログ更新・引き継ぎ（2026-10-30）

## 目的と今回の依頼
新規認知からRELOHAのストア流入・ダウンロードにつなげる。GitHubブログに2記事追加し、一覧を魅力的に。Amebaの方向に合わせて、短い文章・多めの挿絵・簡単な手順を採用。

## 実装
- 新規 /guide/new-houseplant-first-day/：買った初日のラベル・葉裏・土・置き場所の確認。水・肥料・植え替えを一律に急がない判断。
- 新規 /guide/clean-houseplant-leaves/：葉のタイプ別の掃除。水と柔らかい布、毛のある葉のブラシ、洗剤を安易に足さない注意。
- 各記事はオリジナルAI生成の見出し画像＋本文画像2枚＋既存アプリ紹介画像。外部画像の転載なし。生成画像は診断証拠・実践写真として扱わず明示。
- 記事一覧は大きな新着2カードと既存記事の写真カード。クリーム・深緑・テラコッタで統一。悩み別の近道、カテゴリー、短い説明を配置。リンクはJSなしで利用可。
- 既存の植え替え・葉先の記事から新規記事へ内部リンク。
- 全19記事、XML/TXTサイトマップ22URLへ更新。canonical・Article・Breadcrumb・ItemList・既存analytics・記事別ストアリンクを維持。
- 本文の挿絵を検査できるよう既存チェッカーを拡張。一覧は記事カードと悩み別リンクを区別して重複を検査。

## 出典確認
2026-10-30に大学の公開原文を確認。本文末尾にリンクと参照範囲を掲載。直訳転載や体験談の捏造なし。
- https://extension.illinois.edu/houseplants/get-started
- https://extension.illinois.edu/houseplants/care
- https://extension.umd.edu/resource/watering-indoor-plants
- https://yardandgarden.extension.iastate.edu/faq/dust-has-accumulated-foliage-my-houseplants-how-can-i-clean-plants

## 検証・限界
生成・静的検査で19記事、22URLの整合・画像・参考リンク・内部リンク・単一H1・構造化データを確認。PC表示と390px iframeで一覧・新記事を目視、本文幅375pxで横はみ出しなし。不自然な一覧見出しの改行を修正。iPhone実機Safariは未確認。
公開の成否は対応コミットのPagesデプロイと公開URLで別途確認する。Googleへの登録成功、サイトマップ処理成功、検索順位、自然流入、ダウンロード増加はこの更新だけで断定しない。

## 今後の運用
記事は content/guides/*.json、一覧の枠は content/guide-index.template、一覧スタイルは assets/guide-index.css を編集。
python3 scripts/build-guides.py → python3 scripts/check-guides.py → python3 scripts/check-site.py。
画像追加時は幅・高さ・alt・AI生成の説明を入れ、画像は1200×800 WebPで軽量化する。
次に見る指標は記事別の検索表示・クリック・ストアクリック。ストアクリックはDLと別。Search Console/GA4認証が必要な確認は勝手に権限拡張しない。
課金・削除・外部連絡なし。既存トップ/モバイルトップの演出は変更なし。
