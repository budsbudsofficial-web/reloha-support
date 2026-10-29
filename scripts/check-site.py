"""Check local public URLs, metadata, structured data, and analytics wiring."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, unquote
import json
import xml.etree.ElementTree as ET
BASE = 'https://budsbudsofficial-web.github.io/reloha-support/'
ROOT = Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(); self.links=[]; self.article_links=[]; self.canon=[]; self.scripts=[]; self.structured=[]; self.capture=False; self.buffer=''; self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='a' and 'item' in a.get('class','').split():self.article_links.append(a['href'])
        if tag in ('a','img','script','iframe'):
            val=a.get('href') if tag=='a' else a.get('src')
            if val:self.links.append(val)
        if tag=='link' and a.get('rel')=='canonical':self.canon.append(a['href'])
        if tag=='script':
            if a.get('src'):self.scripts.append(a['src'])
            self.capture=a.get('type')=='application/ld+json';self.buffer=''
    def handle_data(self, data):
        if self.capture:self.buffer+=data
    def handle_endtag(self, tag):
        if tag=='script' and self.capture:self.structured.append(json.loads(self.buffer));self.capture=False
errors=[]; pages=0
for path in ROOT.rglob('*.html'):
    if '.git' in path.parts or path.name.startswith('google') or path.relative_to(ROOT).parts[:2] == ('docs', 'qa'):continue
    rel=path.relative_to(ROOT).as_posix(); url=BASE+(rel[:-10] if rel.endswith('index.html') else rel)
    text=path.read_text(); page=Page(text);pages+=1
    if len(page.canon)!=1:errors.append(f'{rel}: expected one canonical')
    if page.scripts.count('/reloha-support/assets/analytics.js')!=1:errors.append(f'{rel}: expected one analytics loader')
    if 'googletagmanager.com/gtag/js' in text:errors.append(f'{rel}: inline duplicate GA tag')
    for link in page.links:
        target=urlsplit(urljoin(url,link))
        if target.netloc!='budsbudsofficial-web.github.io' or not target.path.startswith('/reloha-support/'):continue
        local=ROOT/unquote(target.path[len('/reloha-support/'):])
        if local.is_dir():local=local/'index.html'
        if not local.is_file():errors.append(f'{rel}: missing {link}')
locations=[e.text for e in ET.parse(ROOT/'sitemap.xml').iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
if len(locations)!=len(set(locations)):errors.append('duplicate sitemap URL')
if (ROOT/'sitemap.txt').read_text().splitlines()!=locations:
    errors.append('XML and TXT sitemap URLs differ')
inputs=[json.loads(p.read_text()) for p in (ROOT/'content/guides').glob('*.json')]
expected_guides={BASE+'guide/'+a['slug']+'/' for a in inputs}
if expected_guides!={u for u in locations if u.startswith(BASE+'guide/') and u!=BASE+'guide/'}:
    errors.append('sitemap and article inputs differ')
index_text=(ROOT/'guide/index.html').read_text()
index=Page(index_text)
index_links=[urljoin(BASE+'guide/',u) for u in index.links]
article_links=[urljoin(BASE+'guide/',u) for u in index.article_links]
for a in inputs:
    url=BASE+'guide/'+a['slug']+'/'
    if article_links.count(url)!=1:errors.append(f'index must contain one article card for {a["slug"]}')
    if a['title'] not in index_text or a['description'] not in index_text:
        errors.append(f'index metadata out of sync: {a["slug"]}')
if index_text.count('<nav ')!=index_text.count('</nav>'):
    errors.append('guide index navigation is not closed')
lists=[s for s in index.structured if s.get('@type')=='ItemList']
if len(lists)!=1 or [i['url'] for i in lists[0]['itemListElement']]!=article_links:
    errors.append('index ItemList differs from visible article links')
for url in locations:
    rel=url.removeprefix(BASE);p=ROOT/rel
    if p.is_dir():p=p/'index.html'
    if not p.is_file():errors.append(f'sitemap target missing: {url}');continue
    page=Page(p.read_text())
    if page.canon != [url]:errors.append(f'sitemap canonical mismatch: {url}')
print(json.dumps({'pages':pages,'sitemap_urls':len(locations),'errors':errors},ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
