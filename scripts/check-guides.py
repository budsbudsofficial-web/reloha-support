"""Validate published guides: navigation, sources, accessible structure and assets."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote, parse_qs
import json

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://budsbudsofficial-web.github.io/reloha-support/'

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids=[]; self.links=[]; self.images=[]; self.h1=0
        self.tables=0; self.faq=0; self.feed(text)
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.append(a['id'])
        if tag=='a':self.links.append(a.get('href',''))
        if tag=='img':self.images.append(a)
        if tag=='h1':self.h1+=1
        if tag=='table':self.tables+=1
        if tag=='details':self.faq+=1

errors=[]; report=[]
for data in sorted((ROOT/'content/guides').glob('*.json')):
    a=json.loads(data.read_text()); slug=a['slug']
    path=ROOT/'guide'/slug/'index.html'; text=path.read_text(); page=Page(text)
    url=BASE+'guide/'+slug+'/'
    duplicates=[k for k,n in Counter(page.ids).items() if n>1]
    if duplicates:errors.append(f'{slug}: duplicate IDs {duplicates}')
    if page.h1!=1 or page.tables<1 or page.faq<3:errors.append(f'{slug}: heading/table/FAQ structure')
    if len(a['quick'])!=3:errors.append(f'{slug}: expected three immediate actions')
    if len(a['sources'])<2:errors.append(f'{slug}: missing reference context')
    source_urls={s['url'] for s in a['sources']}
    if not source_urls.issubset(set(page.links)):errors.append(f'{slug}: reference link missing')
    for link in page.links:
        dest=urlsplit(urljoin(url,link))
        if dest.netloc=='apps.apple.com' and dest.path.endswith('/id6813563330'):
            if parse_qs(dest.query).get('utm_campaign')!=['guide_'+slug]:errors.append(f'{slug}: article attribution missing')
        if dest.netloc!='budsbudsofficial-web.github.io' or not dest.path.startswith('/reloha-support/'):continue
        target=ROOT/unquote(dest.path.removeprefix('/reloha-support/'))
        if target.is_dir():target=target/'index.html'
        if not target.is_file():errors.append(f'{slug}: missing link {link}');continue
        if dest.fragment and target.suffix=='.html':
            ids=page.ids if target==path else Page(target.read_text()).ids
            if unquote(dest.fragment) not in ids:errors.append(f'{slug}: missing fragment {link}')
    if len(page.images)!=2:errors.append(f'{slug}: expected hero and common promotion')
    for image in page.images:
        for key in ['src','alt','width','height']:
            if not image.get(key):errors.append(f'{slug}: image missing {key}')
        dest=urlsplit(urljoin(url,image.get('src','')))
        image_path=ROOT/dest.path.removeprefix('/reloha-support/')
        if not image_path.is_file():errors.append(f'{slug}: missing image {dest.path}')
    if not any(i.get('src','').endswith('/reloha-promotion.webp') for i in page.images):errors.append(f'{slug}: inconsistent promotion artwork')
    if 'AI生成' not in text:errors.append(f'{slug}: missing contextual image disclosure')
    report.append({'slug':slug,'sections':len(a['sections']),'references':len(source_urls),'faq':page.faq})

published={p.parent.name for p in (ROOT/'guide').glob('*/index.html')}
configured={json.loads(p.read_text())['slug'] for p in (ROOT/'content/guides').glob('*.json')}
if published!=configured:errors.append('Published articles and content inputs differ')
print(json.dumps({'guides':len(report),'errors':errors},ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
