# DataScience.LA archive

A read-only archive of [DataScience.LA](https://datasciencela.github.io/), the blog of the Los Angeles
data science community (2014–2021): meetup talks, useR! 2014 interviews, benchmarks and essays.

The site is a static [Hugo](https://gohugo.io/) site using the [Blowfish](https://blowfish.page/) theme,
deployed to GitHub Pages by GitHub Actions on every push to `master`.

## Layout

| Path | What |
|---|---|
| `content/posts/<slug>/` | One page bundle per post: `index.md`, its images, and `comments.json` (archived comments) |
| `content/team/`, `content/join-membership/` | Pages |
| `content/authors/`, `content/categories/`, `content/tags/` | Term pages (names, slugs, WordPress URL aliases) |
| `data/authors/` | Author names, bios and photos used by Blowfish |
| `layouts/` | Site templates: archived comments, link handling, embed shortcodes |
| `assets/` | Logo, author photos, CSS overrides (`assets/css/custom.css`) |
| `config/_default/hugo.toml` | Site configuration |
| `themes/blowfish` | Theme (git submodule, pinned) |
| `tools/wordpress-import/` | Scripts that generated `content/` from the WordPress database dump |

URLs match the original WordPress site: posts at `/<slug>/`, categories at `/category/<slug>/`,
tags at `/tag/<slug>/`; author pages are at `/authors/<slug>/` with redirects from `/author/<slug>/`.

## Building locally

```sh
git clone --recurse-submodules git@github.com:DataScienceLA/datasciencela.github.io.git
cd datasciencela.github.io
hugo server            # http://localhost:1313/ — needs Hugo extended ≥ 0.157
hugo build --gc --minify   # output in public/
```

## Shortcodes

| Shortcode | Use |
|---|---|
| `{{< youtube-lite id="…" title="…" >}}` | YouTube video, loaded (from youtube-nocookie.com) only when clicked |
| `{{< speakerdeck id="…" url="…" title="…" >}}` | Speaker Deck slides |
| `{{< tweet-archive url="…" author="…" date="…" >}}text{{< /tweet-archive >}}` | A tweet, preserved as text |
| `{{< iframe src="…" >}}` | Other embeds (maps) |
| `{{< avatar src="…" >}}` | Round photo on the Team page |

## How the content was produced

`content/` was generated from the WordPress database dump of the original site (not included in this
repository) with the scripts in `tools/wordpress-import/`:

1. `extract.py` reads the SQL dump and writes published posts, pages, authors, categories, tags and approved
   comments to JSON (no e-mail addresses or other private data).
2. `convert.py` turns each post into a Hugo page bundle: WordPress paragraph formatting, shortcodes
   (captions, Symple columns/headings, Easy Table, Speaker Deck, gists), auto-embedded YouTube/Speaker Deck/Twitter
   URLs, images (full-size originals, resized to ≤1600 px) and comments.

Embedded GitHub gists were copied into the posts as code blocks. Tweets were preserved from WordPress' oEmbed cache.
Posts can be edited directly as Markdown now; the scripts are kept for reference.

Videos and slides that were no longer available when the archive was made (shown as a note with the original link):
YouTube `AQ0EjOJnu9Q`, `5_vpPJPA9UQ`, `a6VRHvSapYQ`, `8x3nVP9B0hQ`, `DZ0Y7fbipXs`, `6DcUNKBdHiQ` (deleted),
`H_YtvFxD8ig`, `d0aVup0QuuI`, `lZ6q1Orwtug` (private), and the Speaker Deck deck
`szilard/machine-learning-meetup-febr-2017`.
