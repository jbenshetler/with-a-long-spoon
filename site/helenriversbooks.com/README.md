# site/helenriversbooks.com

Static author site — plain HTML/CSS, no build step, no JavaScript.

```
index.html          the whole page
style.css           palette taken from the cover (plum, brass, the one red accent)
images/cover.jpg    1000×1600 web copy of images/cover.png
images/cover-500.jpg  half-size, served to phones via srcset
```

## Deploy

```
site/helenriversbooks.com/deploy.sh
```

Wraps `wrangler pages deploy` for the `helen-rivers-site` project, and
regenerates the web cover copies first if `images/cover.png` (the master
symlink) is newer. First run opens a browser to log in to Cloudflare; after
that it is non-interactive. Live at <https://helen-rivers-site.pages.dev> —
the per-deployment hash URL wrangler prints has no TLS certificate, so ignore it.

Dashboard drag-and-drop and the folder picker are both broken in Chrome on
Cinnamon/Mint; `/tmp` zip upload is the fallback if wrangler is unavailable.

Custom domains are attached in the dashboard under the project's **Custom
domains** (`helenriversbooks.com`, `www.helenriversbooks.com`) — Cloudflare
writes the DNS records and issues the certificates itself.

`.assetsignore` keeps this README off the public site.

## Copy source

The blurb, tagline, and comp line are the **Test-epub blurb** from
`meta/meta-blurb.md`. That doc is authoritative — edit it there first, then
mirror the change here. The page obeys the same craft discipline as every other
blurb surface (warmth leads, one dark cue, no happily-ever-after language).

## Not here yet

- **Newsletter signup** — `index.html` has a commented placeholder in the News
  section; paste the provider's embed snippet there once a list service is chosen.
- **Buy links** — add when the book is listed; the `.status` line becomes the
  retail link.
- **Favicon** — a cropped detail of the brass emblem would do it.
