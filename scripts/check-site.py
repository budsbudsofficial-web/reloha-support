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
        super().__init__(); self.links=[]; self.canon=[]; self.scripts=[]; self.structured=[]; self.capture=False; self.buffer=''; self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
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
for url in locations:
    rel=url.removeprefix(BASE);p=ROOT/rel
    if p.is_dir():p=p/'index.html'
    if not p.is_file():errors.append(f'sitemap target missing: {url}');continue
    page=Page(p.read_text())
    if page.canon != [url]:errors.append(f'sitemap canonical mismatch: {url}')
print(json.dumps({'pages':pages,'sitemap_urls':len(locations),'errors':errors},ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
