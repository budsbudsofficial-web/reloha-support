"""Build researched guide pages from content/guides/*.json (standard library only)."""
from pathlib import Path
import json, html
ROOT=Path(__file__).resolve().parents[1]
BASE='https://budsbudsofficial-web.github.io/reloha-support/'
def esc(s): return html.escape(s,quote=True)
for path in sorted((ROOT/'content/guides').glob('*.json')):
    a=json.loads(path.read_text()); slug=a['slug']; url=BASE+'guide/'+slug+'/'
    image=BASE+'assets/guide/'+slug+'.webp'
    article={'@context':'https://schema.org','@type':'Article','headline':a['title'],'description':a['description'],'inLanguage':'ja','mainEntityOfPage':url,'image':image,'dateModified':'2026-10-23','author':{'@type':'Organization','name':'RELOHA編集部'},'publisher':{'@type':'Organization','name':'RELOHA','url':BASE}}
    crumbs={'@context':'https://schema.org','@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'RELOHA','item':BASE},{'@type':'ListItem','position':2,'name':'植物ガイド','item':BASE+'guide/'},{'@type':'ListItem','position':3,'name':a['title'],'item':url}]}
    toc=''.join(f'<li><a href="#{esc(s["id"])}">{esc(s["title"])}</a></li>' for s in a['sections'])
    sections=''.join(f'<section class="section" id="{esc(s["id"])}"><h2>{esc(s["title"])}</h2>{s["body"]}</section>' for s in a['sections'])
    faq=''.join(f'<details><summary>{esc(q)}</summary><p>{ans}</p></details>' for q,ans in a['faq'])
    refs=''.join(f'<li id="source-{i}"><a href="{esc(s["url"])}">{esc(s["name"])}</a><span>{esc(s["scope"])}</span></li>' for i,s in enumerate(a['sources'],1))
    related=''.join(f'<a href="../{esc(s)}/">{esc(t)}<span aria-hidden="true">↗</span></a>' for s,t in a['related'])
    lead=esc(a['lead'])
    if a.get('lead_tail'):
        tail=esc(a['lead_tail'])
        assert lead.endswith(tail)
        lead=lead[:-len(tail)]+'<span class="phrase">'+tail+'</span>'
    text=f'''<!doctype html>
<html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(a['title'])}｜RELOHA植物ガイド</title>
<meta name="description" content="{esc(a['description'])}"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="theme-color" content="#f7f5ef">
<link rel="canonical" href="{url}"><link rel="stylesheet" href="../../assets/guide-editorial.css">
<meta property="og:type" content="article"><meta property="og:locale" content="ja_JP"><meta property="og:title" content="{esc(a['title'])}"><meta property="og:description" content="{esc(a['description'])}"><meta property="og:url" content="{url}"><meta property="og:image" content="{image}"><meta property="og:image:alt" content="{esc(a['image_alt'])}">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps(article,ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(crumbs,ensure_ascii=False)}</script>
<script defer src="/reloha-support/assets/analytics.js"></script></head>
<body><a class="skip" href="#answer">本文へ移動</a><header><a class="logo" href="../../">RELOHA</a><a class="nav" href="../">植物ガイド一覧 <span aria-hidden="true">↗</span></a></header>
<main><nav class="breadcrumbs" aria-label="パンくず"><a href="../../">RELOHA</a><span>/</span><a href="../">植物ガイド</a><span>/</span><span>{esc(a['category'])}</span></nav>
<div class="hero"><div><p class="eyebrow">RELOHA JOURNAL / {esc(a['category'])}</p><h1>{a['heading']}</h1><p class="lead">{lead}</p><p class="byline">RELOHA編集部 · <time datetime="2026-10-23">2026年10月23日 更新</time></p></div><figure><img src="../../assets/guide/{slug}.webp" alt="{esc(a['image_alt'])}" width="1200" height="800" fetchpriority="high"><figcaption>AI生成によるイメージ。症状や虫を同定する写真ではありません。</figcaption></figure></div>
<article class="content"><aside class="answer" id="answer"><p class="eyebrow">まず、結論</p><p>{a['answer']}</p></aside>
<section class="quick"><h2>今日やることは、この3つ</h2><ol>{''.join('<li>'+s+'</li>' for s in a['quick'])}</ol></section>
<nav class="toc" aria-label="この記事の目次"><p>この記事でわかること</p><ol>{toc}<li><a href="#faq">よくある質問</a></li></ol></nav>
{sections}<section class="section faq" id="faq"><h2>よくある質問</h2>{faq}</section>
<aside class="feature"><img src="../../mobile/screens/home.png" alt="RELOHAの実際のホーム画面" width="390" height="844" loading="lazy"><div><p class="eyebrow">変化を、見比べられるように</p><h2>{esc(a['cta_title'])}</h2><p>{esc(a['cta'])}</p><a class="button" href="https://apps.apple.com/jp/app/reloha/id6813563330?utm_source=reloha_site&amp;utm_medium=organic&amp;utm_campaign=guide_{slug}">App StoreでRELOHAを見る <span aria-hidden="true">↗</span></a><p class="small">iPhone向けの植物成長記録アプリです。虫や病気の自動診断機能ではありません。</p></div></aside>
<section class="section related"><h2>あわせて読みたい</h2>{related}<a href="../">植物ガイドをすべて見る<span aria-hidden="true">↗</span></a></section>
<section class="section sources"><h2>参考情報と編集方針</h2><p>園芸団体・大学・メーカーの公開情報を確認し、家庭での観察と判断の順序をRELOHA編集部が整理しました。植物ごとの管理条件は、購入時のラベルや生産者の案内を優先してください。</p><ol>{refs}</ol><p class="small">確認日：2026年10月23日。参考情報にある海外の薬剤・資材の使用条件を、そのまま日本向けに推奨していません。</p></section>
<footer><a href="../../">RELOHA公式サイト</a><a href="../../privacy.html">プライバシーポリシー</a><a href="mailto:budsbuds.official@gmail.com">お問い合わせ</a><span>© RELOHA</span></footer></article></main></body></html>'''
    out=ROOT/'guide'/slug/'index.html';out.write_text(text)
    print(f'Built {out.relative_to(ROOT)}')
