"""Extract published posts/pages, authors, terms, comments and media from the WP SQL dump into JSON."""
import sys, json, re, os
sys.path.insert(0, os.path.dirname(__file__))
from parse_sql import load

src, out = sys.argv[1], sys.argv[2]
T, C = load(src)
rows = lambda t: [dict(zip(C[t], r)) for r in T.get(t, [])]
P = rows('wp_posts'); M = rows('wp_postmeta'); U = rows('wp_users'); UM = rows('wp_usermeta')
terms = {t['term_id']: t for t in rows('wp_terms')}
tax = {t['term_taxonomy_id']: t for t in rows('wp_term_taxonomy')}
rel = rows('wp_term_relationships')
meta = {}
for m in M: meta.setdefault(m['post_id'], {}).setdefault(m['meta_key'], []).append(m['meta_value'])
umeta = {}
for m in UM: umeta.setdefault(m['user_id'], {})[m['meta_key']] = m['meta_value']
byid = {p['ID']: p for p in P}

def attached_file(aid):
    v = meta.get(aid, {}).get('_wp_attached_file')
    return '/wp-content/uploads/' + v[0] if v else None

authors = {}
for u in U:
    um = umeta.get(u['ID'], {})
    authors[u['ID']] = dict(login=u['user_login'], slug=u['user_nicename'], name=u['display_name'],
                            url=u['user_url'] or '', bio=um.get('description', '') or '',
                            first=um.get('first_name', ''), last=um.get('last_name', ''))

comments = {}
for c in rows('wp_comments'):
    if c['comment_approved'] != '1' or c['comment_type'] not in ('comment', ''): continue
    comments.setdefault(c['comment_post_ID'], []).append(dict(
        id=c['comment_ID'], parent=c['comment_parent'], author=c['comment_author'],
        url=c['comment_author_url'] or '', date=c['comment_date'], content=c['comment_content']))

items = []
for p in P:
    if p['post_type'] not in ('post', 'page') or p['post_status'] != 'publish': continue
    cats, tags = [], []
    for r in rel:
        if r['object_id'] == p['ID'] and r['term_taxonomy_id'] in tax:
            t = tax[r['term_taxonomy_id']]; term = terms[t['term_id']]
            parent = tax.get(next((k for k, v in tax.items() if v['term_id'] == t['parent']), None))
            (cats if t['taxonomy'] == 'category' else tags if t['taxonomy'] == 'post_tag' else []).append(
                dict(name=term['name'], slug=term['slug'],
                     parent=terms[parent['term_id']]['slug'] if parent and t['parent'] != '0' else None))
    thumb = meta.get(p['ID'], {}).get('_thumbnail_id', [None])[0]
    items.append(dict(id=p['ID'], type=p['post_type'], slug=p['post_name'], title=p['post_title'],
        date=p['post_date'], modified=p['post_modified'], author=authors.get(p['post_author'], {}).get('slug'),
        excerpt=p['post_excerpt'], content=p['post_content'], categories=cats, tags=tags,
        featured=attached_file(thumb) if thumb else None,
        seo_desc=(meta.get(p['ID'], {}).get('_aioseop_description') or [''])[0],
        oembed=[v[0] for k, v in meta.get(p['ID'], {}).items()
                if k.startswith('_oembed_') and not k.startswith('_oembed_time_') and v[0] and v[0] != '{{unknown}}'],
        comments=sorted(comments.get(p['ID'], []), key=lambda c: c['date'])))
items.sort(key=lambda x: x['date'])
json.dump(dict(authors=authors, items=items), open(out, 'w'), indent=1, ensure_ascii=False)
print('items', len(items), 'authors', len(authors), 'comments', sum(len(i['comments']) for i in items))
