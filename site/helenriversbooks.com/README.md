# site/helenriversbooks.com

Static author site — plain HTML/CSS, no build step, no JavaScript.

```
index.html          the whole page
style.css           palette taken from the cover (plum, brass, the one red accent)
images/cover.jpg    1000×1600 web copy of images/cover.png
images/cover-500.jpg  half-size, served to phones via srcset
```

## Deploy (Cloudflare)

Dashboard → **Workers & Pages** → **Create** → **Pages** tab → **Upload assets**.
Drag **this directory** in (not the repo root). Then, in the project's
**Custom domains**, add `helenriversbooks.com` and `www.helenriversbooks.com`.

Updating later: drag the directory in again — each upload is a new deployment,
and old ones stay available for rollback.

## Regenerating the cover images

After a cover change, re-derive both sizes from the master symlink:

```
convert images/cover.png -resize 1000x1600 -quality 86 site/helenriversbooks.com/images/cover.jpg
convert images/cover.png -resize 500x800  -quality 86 site/helenriversbooks.com/images/cover-500.jpg
```

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
