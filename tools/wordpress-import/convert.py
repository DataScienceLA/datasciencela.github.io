"""Convert the WordPress JSON export (from extract.py) into Hugo page bundles.

usage: convert.py WP_JSON UPLOADS_DIR SITE_DIR CACHE_DIR [slug,slug,...]
"""
import csv, hashlib, html, io, json, os, re, shutil, sys, time, urllib.parse, urllib.request
from bs4 import BeautifulSoup, NavigableString, Comment
from markdownify import MarkdownConverter
from PIL import Image, ImageOps

WP_JSON, UPLOADS, SITE, CACHE = sys.argv[1:5]
ONLY = set(sys.argv[5].split(',')) if len(sys.argv) > 5 and sys.argv[5] else None
SITE_HOST = re.compile(r'^(?:https?:)?//(?:www\.)?datascience\.la', re.I)
MAX_IMG_W = 1600
SKIP = {'join-membership', 'subscription-confirmation'}  # membership sign-up pages of the live site
os.makedirs(CACHE, exist_ok=True)
REPORT = []  # (slug, message) for things a human should look at


# ---------------------------------------------------------------- network (cached)

def cached_json(key, url, headers=None):
    path = os.path.join(CACHE, hashlib.sha1(key.encode()).hexdigest() + '.json')
    if os.path.exists(path):
        return json.load(open(path))
    req = urllib.request.Request(url, headers={'User-Agent': 'dsla-archive-converter', **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = {'ok': True, 'status': r.status, 'body': json.loads(r.read().decode())}
    except urllib.error.HTTPError as e:
        data = {'ok': False, 'status': e.code, 'body': None}
    except Exception as e:  # network errors are not cached
        return {'ok': False, 'status': None, 'body': None, 'error': str(e)}
    json.dump(data, open(path, 'w'))
    time.sleep(0.2)
    return data


def youtube_info(vid):
    d = cached_json('yt:' + vid, 'https://www.youtube.com/oembed?format=json&url=' +
                    urllib.parse.quote(f'https://www.youtube.com/watch?v={vid}'))
    return d['body'] if d['ok'] else None


def speakerdeck_info(url):
    d = cached_json('sd:' + url, 'https://speakerdeck.com/oembed.json?url=' + urllib.parse.quote(url))
    if not d['ok']:
        return None
    b = d['body']
    m = re.search(r'/player/([0-9a-f]+)', b.get('html', ''))
    return dict(id=m.group(1), title=b.get('title', ''), w=b.get('width') or 710, h=b.get('height') or 532) if m else None


def gist_info(gid):
    d = cached_json('gist:' + gid, f'https://api.github.com/gists/{gid}')
    return d['body'] if d['ok'] else None


# ---------------------------------------------------------------- placeholders

class Placeholders:
    """Opaque tokens that survive HTML->Markdown conversion and are swapped for final Markdown at the end."""
    def __init__(self):
        self.items = {}

    def block(self, md):
        k = f'DSLAPH{len(self.items):04d}X'
        self.items[k] = md
        return f'\n\n<p>{k}</p>\n\n'

    def restore(self, md):
        for k, v in self.items.items():
            md = re.sub(r'(?m)^[ \t]*' + k + r'[ \t]*$', lambda _: v, md)
            md = md.replace(k, v)
        return md


def sc_attr(attrs, name):
    for rx in (r'"([^"]*)"', '[\u201c\u201d]([^\u201c\u201d]*)[\u201c\u201d]', r"'([^']*)'"):
        m = re.search(name + r'\s*=\s*' + rx, attrs)
        if m:
            return m.group(1)
    return ''


def q(s):
    """Quote a value for a Hugo shortcode parameter."""
    return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'


# ---------------------------------------------------------------- embeds

YT_URL = re.compile(r'https?://(?:www\.|m\.)?(?:youtube\.com/(?:watch\?\S*?v=|embed/)|youtu\.be/)([\w-]{11})\S*', re.I)
SD_URL = re.compile(r'https?://(?:www\.)?speakerdeck\.com/[\w-]+/[\w-]+', re.I)
TW_URL = re.compile(r'https?://(?:www\.|mobile\.)?twitter\.com/(\w+)/status(?:es)?/(\d+)\S*', re.I)


def embed_youtube(url, ph, slug):
    m = YT_URL.match(url)
    vid = m.group(1)
    t = re.search(r'[?&#](?:t|start)=(\d+)', url)
    info = youtube_info(vid)
    if not info:
        REPORT.append((slug, f'YouTube video unavailable: {vid}'))
        return ph.block(f'{{{{< youtube-lite id={q(vid)} unavailable="true" >}}}}')
    args = f'id={q(vid)} title={q(info.get("title", ""))}' + (f' start="{t.group(1)}"' if t else '')
    return ph.block(f'{{{{< youtube-lite {args} >}}}}')


def embed_speakerdeck(url, ph, slug):
    info = speakerdeck_info(url)
    if not info:
        REPORT.append((slug, f'Speaker Deck unavailable: {url}'))
        return ph.block(f'Slides: <{url}>')
    return ph.block(f'{{{{< speakerdeck id={q(info["id"])} url={q(url)} title={q(info["title"])} '
                    f'ratio="{info["w"]}/{info["h"]}" >}}}}')


def embed_tweet(url, item, ph, slug):
    m = TW_URL.match(url)
    tid = m.group(2)
    for h in item['oembed']:
        if tid in h and 'twitter-tweet' in h:
            soup = BeautifulSoup(h, 'html.parser')
            bq = soup.find('blockquote')
            text = md_inline(str(bq.find('p'))) if bq.find('p') else ''
            links = bq.find_all('a')
            date = links[-1].get_text() if links else ''
            byline = bq.get_text().rsplit('—', 1)[-1].replace(date, '').strip() if '—' in bq.get_text() else ''
            return ph.block(f'{{{{< tweet-archive url={q(url)} author={q(byline)} date={q(date)} >}}}}\n'
                            f'{text}\n{{{{< /tweet-archive >}}}}')
    REPORT.append((slug, f'Tweet not in cache, left as link: {url}'))
    return ph.block(f'<{url}>')


def embed_url(url, item, ph, slug):
    url = html.unescape(url.strip())
    if YT_URL.match(url):
        return embed_youtube(url, ph, slug)
    if SD_URL.match(url):
        return embed_speakerdeck(url, ph, slug)
    if TW_URL.match(url):
        return embed_tweet(url, item, ph, slug)
    return None


def embed_gist(gid, ph, slug):
    g = gist_info(gid)
    if not g:
        REPORT.append((slug, f'Gist unavailable: {gid}'))
        return ph.block(f'Code: <https://gist.github.com/{gid}>')
    out = []
    for fname, f in g['files'].items():
        lang = (f.get('language') or '').lower().replace('shell', 'bash')
        code = f['content'].rstrip('\n')
        fence = '````' if '```' in code else '```'
        out.append(f'{fence}{lang}\n{code}\n{fence}')
    owner = (g.get('owner') or {}).get('login', '')
    out.append(f'<small>Source: [gist {gid[:7]}]({g["html_url"]})' + (f' by {owner}' if owner else '') + '</small>')
    return ph.block('\n\n'.join(out))


# ---------------------------------------------------------------- shortcodes & raw text

def easy_table(attrs, body):
    body = html.unescape(re.sub(r'<br\s*/?>', '\n', body)).strip('\n')
    rows = [r for r in csv.reader(io.StringIO(body)) if any(c.strip() for c in r)]
    if not rows:
        return ''
    head = ''.join(f'<th>{html.escape(c.strip())}</th>' for c in rows[0])
    trs = ''.join('<tr>' + ''.join(f'<td>{html.escape(c.strip())}</td>' for c in r) + '</tr>' for r in rows[1:])
    return f'\n\n<table><thead><tr>{head}</tr></thead><tbody>{trs}</tbody></table>\n\n'


def preprocess(item, ph):
    """Replace WordPress shortcodes, block comments and standalone embed URLs."""
    slug, t = item['slug'], item['content'].replace('\r\n', '\n').replace('\r', '\n')
    t = t.replace('<!--more-->', ph.block('<!--more-->'))
    # Gutenberg embed blocks: keep only the URL
    t = re.sub(r'<figure class="wp-block-embed[^"]*"[^>]*>\s*<div class="wp-block-embed__wrapper">\s*(\S+?)\s*</div>'
               r'(?:\s*<figcaption>(.*?)</figcaption>)?\s*</figure>',
               lambda m: '\n\n' + m.group(1) + '\n\n' + (f'<p><em>{m.group(2)}</em></p>' if m.group(2) else ''), t, flags=re.S)
    t = re.sub(r'<!--\s*/?wp:.*?-->', '', t, flags=re.S)
    t = re.sub(r'\[embed[^\]]*\](.*?)\[/embed\]',
               lambda m: embed_url(m.group(1), item, ph, slug) or f'\n\n<{m.group(1).strip()}>\n\n', t, flags=re.S)
    t = re.sub(r'\[speakerdeck([^\]]*)\]', lambda m: embed_speakerdeck(sc_attr(m.group(1), 'url'), ph, slug), t)
    t = re.sub(r'\[gist\s+(?:id=)?["\']?(?:https://gist\.github\.com/(?:[\w-]+/)?)?([0-9a-f]+)["\']?\s*\]',
               lambda m: embed_gist(m.group(1), ph, slug), t)
    t = re.sub(r'\[caption([^\]]*)\](.*?)\[/caption\]', lambda m: caption_to_figure(m.group(2)), t, flags=re.S)
    t = re.sub(r'\[symple_heading([^\]]*)\]', lambda m: f'\n\n<h2>{sc_attr(m.group(1), "title")}</h2>\n\n', t)
    t = re.sub(r'\[symple_divider[^\]]*\]', '\n\n<hr />\n\n', t)
    t = re.sub(r'\[symple_column([^\]]*)\]', lambda m: f'\n\n<div class="wpcol-{sc_attr(m.group(1), "size")}">\n\n', t)
    t = re.sub(r'\[/symple_column\]', '\n\n</div>\n\n', t)
    t = re.sub(r'\[table([^\]]*)\](.*?)\[/table\]', lambda m: easy_table(m.group(1), m.group(2)), t, flags=re.S)
    # standalone URLs on their own line (WordPress auto-embeds)
    t = re.sub(r'(?m)^[ \t]*(?:<p>)?\s*(https?://[^\s<]+)\s*(?:</p>)?[ \t]*$',
               lambda m: embed_url(m.group(1), item, ph, slug) or m.group(0), t)
    leftover = re.findall(r'\[/?[a-z_]+(?:\s[^\]]*)?\]', t)
    leftover = [s for s in leftover if not re.fullmatch(r'\[\d+\]', s) and re.match(r'\[/?(symple|gist|embed|caption|table|speakerdeck|slideshare|wp_|video|audio)', s)]
    if leftover:
        REPORT.append((slug, f'unhandled shortcodes: {sorted(set(leftover))[:5]}'))
    return t


def caption_to_figure(inner):
    soup = BeautifulSoup(inner, 'html.parser')
    img = soup.find('img')
    if not img:
        return inner
    media = img.find_parent('a') or img
    media.extract()
    cap = str(soup).strip()
    return f'\n\n<figure>{media}<figcaption>{cap}</figcaption></figure>\n\n'


ALLBLOCKS = (r'(?:table|thead|tfoot|caption|col|colgroup|tbody|tr|td|th|div|dl|dd|dt|ul|ol|li|pre|form|map|area|'
             r'blockquote|address|math|style|p|h[1-6]|hr|fieldset|legend|section|article|aside|hgroup|header|footer|'
             r'nav|figure|figcaption|details|menu|summary|iframe)')


def wpautop(t):
    """Port of WordPress' wpautop(): blank lines become paragraphs, single newlines become <br>."""
    if not t.strip():
        return ''
    pres = {}

    def keep(m):
        k = f'<pre wp-pre-tag-{len(pres)}></pre>'
        pres[k] = m.group(0)
        return k
    t = re.sub(r'<pre[\s>].*?</pre>', keep, t, flags=re.S | re.I)
    t = re.sub(r'<[^>]*>', lambda m: m.group(0).replace('\n', ' '), t)  # newlines inside tags
    t += '\n'
    t = re.sub(r'<br\s*/?>\s*<br\s*/?>', '\n\n', t)
    t = re.sub(r'(<' + ALLBLOCKS + r'[\s/>])', r'\n\n\1', t)
    t = re.sub(r'(</' + ALLBLOCKS + r'>)', r'\1\n\n', t)
    t = re.sub(r'\n\n+', '\n\n', t)
    parts = [p for p in re.split(r'\n\s*\n', t) if p.strip()]
    t = ''.join('<p>' + p.strip('\n') + '</p>\n' for p in parts)
    t = re.sub(r'<p>\s*</p>', '', t)
    t = re.sub(r'<p>([^<]+)</(div|address|form)>', r'<p>\1</p></\2>', t)
    t = re.sub(r'<p>\s*(</?' + ALLBLOCKS + r'[^>]*>)\s*</p>', r'\1', t)
    t = re.sub(r'<p>(<li.+?)</p>', r'\1', t)
    t = re.sub(r'<p><blockquote([^>]*)>', r'<blockquote\1><p>', t, flags=re.I)
    t = t.replace('</blockquote></p>', '</p></blockquote>')
    t = re.sub(r'<p>\s*(</?' + ALLBLOCKS + r'[^>]*>)', r'\1', t)
    t = re.sub(r'(</?' + ALLBLOCKS + r'[^>]*>)\s*</p>', r'\1', t)
    t = re.sub(r'(?<!<br />)\s*\n', '<br />\n', t)
    t = re.sub(r'(</?' + ALLBLOCKS + r'[^>]*>)\s*<br />', r'\1', t)
    t = re.sub(r'<br />(\s*</?(?:p|li|div|dl|dd|dt|th|pre|td|ul|ol)[^>]*>)', r'\1', t)
    t = re.sub(r'\n</p>$', '</p>', t)
    for k, v in pres.items():
        t = t.replace(k, v)
    return t


# ---------------------------------------------------------------- media

def local_upload(url):
    """Map an uploads URL to (relative path under uploads/, absolute file) preferring the full-size original."""
    u = SITE_HOST.sub('', url.strip())
    if not u.startswith('/wp-content/uploads/'):
        return None
    rel = urllib.parse.unquote(u[len('/wp-content/uploads/'):].split('?')[0])
    orig = re.sub(r'-\d+x\d+(\.\w+)$', r'\1', rel)
    for cand in (orig, rel):
        f = os.path.join(UPLOADS, cand)
        if os.path.isfile(f):
            return cand, f
    return None


def copy_media(src_file, dest_dir, name=None):
    name = name or os.path.basename(src_file)
    dest = os.path.join(dest_dir, name)
    ext = name.lower().rsplit('.', 1)[-1]
    if ext in ('jpg', 'jpeg', 'png'):
        try:
            im = Image.open(src_file)
            im = ImageOps.exif_transpose(im)
            if im.width > MAX_IMG_W:
                im = im.resize((MAX_IMG_W, round(im.height * MAX_IMG_W / im.width)), Image.LANCZOS)
            if ext == 'png':
                im.save(dest, optimize=True)
            else:
                im.convert('RGB').save(dest, quality=82, optimize=True, progressive=True)
            if os.path.getsize(dest) > os.path.getsize(src_file) and im.width <= MAX_IMG_W:
                shutil.copyfile(src_file, dest)
            return name
        except Exception:
            pass
    shutil.copyfile(src_file, dest)
    return name


# ---------------------------------------------------------------- HTML cleanup

KEEP_ATTRS = {'a': ['href'], 'img': ['src', 'alt', 'title'], 'td': ['colspan', 'rowspan'], 'th': ['colspan', 'rowspan'],
              'ol': ['start'], 'pre': ['class'], 'code': ['class'], 'iframe': ['src']}
BLOCK_TAGS = {'p', 'div', 'ul', 'ol', 'li', 'table', 'blockquote', 'pre', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr',
              'figure', 'iframe', 'dl'}


def clean_html(h, slug, bundle, ph, slugs):
    soup = BeautifulSoup(h, 'html.parser')
    for c in soup.find_all(string=lambda s: isinstance(s, Comment)):
        c.extract()
    for t in soup.find_all(['script', 'style', 'noscript', 'meta', 'link']):
        t.decompose()
    for t in soup.find_all(['span', 'font', 'u', 'o:p', 'center', 'section', 'small', 'big', 'abbr', 'cite']):
        t.unwrap()
    # anchors used as in-page targets: keep them as heading ids
    for a in soup.find_all('a'):
        if not a.get('href') and (a.get('id') or a.get('name')):
            target = a.get('id') or a.get('name')
            hd = a.find_parent(re.compile(r'^h[1-6]$'))
            if hd is not None:
                hd.append(f' DSLAANCHOR{target}X')
            a.unwrap()
    # team-page columns: avatar beside bio
    for col in soup.find_all('div', class_=re.compile(r'^wpcol-')):
        img = col.find('img') if 'sixth' in col['class'][0] and col['class'][0].startswith('wpcol-one') else None
        if img is not None:
            res = local_upload((img.find_parent('a') or {}).get('href', '') or img['src']) or local_upload(img['src'])
            name = copy_media(res[1], bundle) if res else img['src']
            col.replace_with(BeautifulSoup(ph.block(f'{{{{< avatar src={q(name)} >}}}}'), 'html.parser'))
    # iframes (maps etc.)
    for f in soup.find_all('iframe'):
        src = f.get('src', '')
        f.replace_with(BeautifulSoup(ph.block(f'{{{{< iframe src={q(src)} >}}}}'), 'html.parser') if src else '')
    # images
    for img in soup.find_all('img'):
        src = img.get('src', '')
        a = img.find_parent('a')
        res = None
        if a is not None and a.get('href') and re.search(r'\.(jpe?g|png|gif|webp)$', a['href'], re.I):
            res = local_upload(a['href'])
            if res or not SITE_HOST.match(a['href']):
                a.unwrap()
        res = res or local_upload(src)
        if res:
            img['src'] = copy_media(res[1], bundle)
        elif SITE_HOST.match(src):
            REPORT.append((slug, f'missing image {src}'))
        alt = img.get('alt', '')
        if re.fullmatch(r'[\w\-.]+', alt or '') and ('_' in alt or '-' in alt or alt.lower().startswith(('img', 'screen'))):
            img['alt'] = ''
    for fig in soup.find_all('figure'):
        img = fig.find('img')
        cap = fig.find('figcaption')
        if img is None:
            fig.unwrap()
            continue
        caption = md_inline(cap.decode_contents()) if cap else ''
        link = img.find_parent('a')
        args = f'src={q(img["src"])}' + (f' alt={q(img.get("alt",""))}' if img.get('alt') else '') + \
               (f' caption={q(caption)}' if caption else '') + (f' link={q(link["href"])}' if link else '')
        fig.replace_with(BeautifulSoup(ph.block(f'{{{{< figure {args} >}}}}'), 'html.parser'))
    # links
    for a in soup.find_all('a', href=True):
        href = a['href'] = re.sub(r'^(?:%20|\s)+', '', a['href']).strip()  # some WordPress links start with an encoded space
        if SITE_HOST.match(href) or href.startswith('/category/'):
            path = SITE_HOST.sub('', href) or '/'
            res = local_upload(href)
            if res:
                a['href'] = copy_media(res[1], bundle)
            elif path.startswith('/wp-content/'):
                REPORT.append((slug, f'link to missing upload {href}'))
            else:
                path = re.sub(r'^/category/(?:[^/]+/)+?([^/]+)/?$', r'/category/\1/', path)  # WordPress nested categories
                a['href'] = path
                s = path.strip('/').split('/')[0]
                if s and s not in slugs and s not in ('category', 'author', 'tag', 'feed', 'page'):
                    REPORT.append((slug, f'internal link to unknown page {path}'))
    # divs: innermost first; div with only inline content becomes a paragraph
    for d in reversed(soup.find_all('div')):
        if any(getattr(c, 'name', None) in BLOCK_TAGS for c in d.children):
            d.unwrap()
        else:
            d.name = 'p'
    # nested <p> (from div->p) is invalid: unwrap the outer one
    for p in soup.find_all('p'):
        if p.find('p'):
            p.unwrap()
    for tag in soup.find_all(True):
        keep = KEEP_ATTRS.get(tag.name, [])
        tag.attrs = {k: v for k, v in tag.attrs.items() if k in keep}
    for h1 in soup.find_all('h1'):
        h1.name = 'h2'
    for p in soup.find_all('p'):
        if not p.get_text(strip=True) and not p.find(['img', 'iframe']):
            p.decompose()
    for t in soup.find_all(string=lambda x: '<' in x or '>' in x):
        if not t.find_parent(['pre', 'code']) and not isinstance(t, Comment):
            t.replace_with(t.replace('<', 'DSLALTX').replace('>', 'DSLAGTX'))
    return str(soup)


# ---------------------------------------------------------------- HTML -> Markdown

class MD(MarkdownConverter):
    def convert_pre(self, el, text, parent_tags):
        cls = ' '.join(el.get('class', []) + (el.code.get('class', []) if el.code else []))
        m = re.search(r'(?:sourceCode|language-|lang-|brush:\s*)\s*([\w+#-]+)', cls)
        lang = (m.group(1) if m else '').lower()
        lang = '' if lang in ('sourcecode', 'none', 'text') else lang
        code = el.get_text().strip('\n')
        fence = '````' if '```' in code else '```'
        return f'\n\n{fence}{lang}\n{code}\n{fence}\n\n'

    def convert_br(self, el, text, parent_tags):
        return '\\\n' if '_inline' not in parent_tags else ' '


def md(h):
    return MD(heading_style='ATX', bullets='-', escape_underscores=False, escape_misc=False,
              table_infer_header=True).convert(h)


def md_inline(h):
    return re.sub(r'\s+', ' ', md(h)).strip()


def finalize(text, ph):
    text = ph.restore(text)
    text = re.sub(r' DSLAANCHOR(.+?)X\s*$', r' {#\1}', text, flags=re.M)
    text = text.replace('DSLALTX', '&lt;').replace('DSLAGTX', '&gt;')
    text = re.sub(r'(?m)^(?:\\[*\u2022\-]|\u2022|\u2013) (.*?)\\?$', r'- \1', text)
    text = re.sub(r'\\\n(?=- )', '\n', text)  # no hard line break right before a list item
    text = re.sub(r'[ \t]+$', '', text, flags=re.M)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip() + '\n'


# ---------------------------------------------------------------- front matter

def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)


def front_matter(item, authors, featured, hide_featured, wp_type):
    fm = [f'title: {yaml_str(html.unescape(item["title"]))}',
          f'date: {item["date"].replace(" ", "T")}',
          f'lastmod: {item["modified"].replace(" ", "T")}',
          f'slug: {yaml_str(item["slug"])}']
    if wp_type == 'post':
        fm += [f'authors: [{yaml_str(item["author"])}]',
               'categories: [' + ', '.join(yaml_str(c['slug']) for c in item['categories'] if c['slug'] != 'uncategorized') + ']',
               'tags: [' + ', '.join(yaml_str(t['slug']) for t in item['tags']) + ']']
    else:
        fm += ['showDate: false', 'showReadingTime: false', 'showAuthor: false']
    desc = item['seo_desc'] or item['excerpt']
    if desc:
        fm.append(f'description: {yaml_str(html.unescape(re.sub(r"<[^>]+>", "", desc)).strip())}')
    if featured and hide_featured:
        fm.append('showHero: false  # featured image also appears in the post body')
    if item['comments']:
        fm += [f'archivedComments: {len(item["comments"])}', 'showComments: true']
    fm.append(f'wpID: {item["id"]}')
    return '---\n' + '\n'.join(fm) + '\n---\n\n'


# ---------------------------------------------------------------- main

def convert_comments(item, bundle, ph, slugs):
    out = []
    for c in item['comments']:
        text = html.escape(c['content'], quote=False) if '<' not in c['content'] else c['content']
        text = re.sub(r'(?<![="\'>/])\b(https?://[^\s<>"\']+[^\s<>"\'.,;:!?)\]])', r'<a href="\1">\1</a>', text)
        h = clean_html(wpautop(text), item['slug'], bundle, ph, slugs)
        body = BeautifulSoup(h, 'html.parser')
        for t in body.find_all(True):
            if t.name not in ('p', 'br', 'a', 'em', 'strong', 'b', 'i', 'code', 'pre', 'blockquote', 'ul', 'ol', 'li'):
                t.unwrap()
        for a in body.find_all('a'):
            a['rel'] = 'nofollow ugc noopener'
        out.append(dict(id=c['id'], parent=c['parent'], author=html.unescape(c['author']).strip(),
                        date=c['date'].replace(' ', 'T'), html=str(body).strip()))
    return out


def team_photos(data, authors):
    """Copy each author's Team page photo to assets/img/authors/<slug>.<ext>; returns {slug: asset path}."""
    team = next((i for i in data['items'] if i['slug'] == 'team'), None)
    out = {}
    if not team:
        return out
    by_name = {re.sub(r'[^a-z]', '', html.unescape(a['name']).lower()): s for s, a in authors.items()}
    by_slug = set(authors)
    dest = os.path.join(SITE, 'assets', 'img', 'authors')
    os.makedirs(dest, exist_ok=True)
    for m in re.finditer(r'<h4>(?:<a id="([^"]*)"></a>)?(.*?)</h4>.*?<img[^>]+src="([^"]+)"', team['content'], re.S):
        anchor, name, src = m.groups()
        key = re.sub(r'[^a-z]', '', html.unescape(re.sub(r'<[^>]+>', '', name)).lower())
        slug = by_name.get(key) or (anchor if anchor in by_slug else None)
        if not slug:
            # match on first + last word of the name (e.g. "Eduardo Arino de la Rubia" vs "Eduardo Ariño de la Rubia")
            words = re.sub(r'<[^>]+>', '', name).lower().split()
            slug = next((s for s, a in authors.items() if words and a['name'].lower().split()[:1] == words[:1]
                         and a['name'].lower().split()[-1:] == words[-1:]), None)
        res = local_upload(src)
        if slug and res:
            ext = res[1].rsplit('.', 1)[-1].lower()
            copy_media(res[1], dest, f'{slug}.{ext}')
            out[slug] = f'img/authors/{slug}.{ext}'
    return out


def main():
    data = json.load(open(WP_JSON))
    authors = {a['slug']: a for a in data['authors'].values()}
    items = [i for i in data['items'] if (not ONLY or i['slug'] in ONLY) and i['slug'] not in SKIP]
    slugs = {i['slug'] for i in data['items']}
    used_authors, used_cats, used_tags, cat_parents = set(), {}, {}, {}
    for item in items:
        slug = item['slug']
        wp_type = item['type']
        bundle = os.path.join(SITE, 'content', 'posts' if wp_type == 'post' else '', slug)
        shutil.rmtree(bundle, ignore_errors=True)
        os.makedirs(bundle)
        ph = Placeholders()
        t = preprocess(item, ph)
        if '<!-- wp:' not in item['content']:  # classic editor content has no <p> tags
            t = wpautop(t)
        h = clean_html(t, slug, bundle, ph, slugs)
        body = finalize(md(h), ph)
        featured, hide = None, False
        if item['featured']:
            res = local_upload(item['featured'])
            if res:
                ext = res[1].rsplit('.', 1)[-1].lower()
                featured = copy_media(res[1], bundle, 'feature.' + ext)
                stem = re.sub(r'-\d+x\d+$', '', os.path.splitext(os.path.basename(res[0]))[0])
                hide = stem in item['content']
            else:
                REPORT.append((slug, f'featured image missing {item["featured"]}'))
        with open(os.path.join(bundle, 'index.md'), 'w') as f:
            f.write(front_matter(item, authors, featured, hide, wp_type) + body)
        if item['comments']:
            json.dump(convert_comments(item, bundle, ph, slugs), open(os.path.join(bundle, 'comments.json'), 'w'),
                      indent=1, ensure_ascii=False)
        if wp_type == 'post':
            used_authors.add(item['author'])
            for c in item['categories']:
                used_cats[c['slug']] = c['name']
                if c.get('parent'):
                    cat_parents[c['slug']] = c['parent']
            for t in item['tags']:
                used_tags[t['slug']] = t['name']
        print(f'{slug}: {len(body)} chars, {len(os.listdir(bundle)) - 1} files')
    # taxonomy term pages: keep WordPress slugs, show WordPress names
    photos = team_photos(data, authors)
    for s in used_authors:
        a = authors[s]
        d = os.path.join(SITE, 'content', 'authors', s)
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, '_index.md'), 'w').write(
            f'---\ntitle: {yaml_str(a["name"])}\nslug: {yaml_str(s)}\naliases: ["/author/{s}/"]\n---\n\n{a["bio"].strip()}\n')
        dd = os.path.join(SITE, 'data', 'authors')
        os.makedirs(dd, exist_ok=True)
        info = {'name': a['name'], 'bio': a['bio'].strip()}
        if s in photos:
            info['image'] = photos[s]
        json.dump(info, open(os.path.join(dd, s + '.json'), 'w'), ensure_ascii=False, indent=1)
    for (tax, s), name in [(('categories', k), v) for k, v in used_cats.items()] + \
                          [(('tags', k), v) for k, v in used_tags.items()]:
        if s == 'uncategorized':
            continue
        d = os.path.join(SITE, 'content', tax, s)
        os.makedirs(d, exist_ok=True)
        alias = f'aliases: ["/category/{cat_parents[s]}/{s}/"]\n' if tax == 'categories' and s in cat_parents else ''
        open(os.path.join(d, '_index.md'), 'w').write(f'---\ntitle: {yaml_str(html.unescape(name))}\nslug: {yaml_str(s)}\n{alias}---\n')
    print('\n'.join(f'REVIEW {s}: {m}' for s, m in REPORT) or 'nothing to review')


if __name__ == '__main__':
    main()
