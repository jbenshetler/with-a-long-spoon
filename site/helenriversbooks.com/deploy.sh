#!/usr/bin/env bash
# Deploy the author site to Cloudflare Pages.
#
#   site/helenriversbooks.com/deploy.sh
#
# Run from anywhere; paths resolve relative to this script. Requires a browser
# login on first use (wrangler opens one), or CLOUDFLARE_API_TOKEN in the env.

set -euo pipefail

SITE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT="helen-rivers-site"
LIVE_URL="https://helen-rivers-site.pages.dev"

# Refresh the web copies of the cover from the master symlink, if it has moved.
REPO_ROOT="$(cd "$SITE_DIR/../.." && pwd)"
MASTER="$REPO_ROOT/images/cover.png"
if [[ -f "$MASTER" ]] && command -v convert >/dev/null 2>&1; then
  if [[ "$MASTER" -nt "$SITE_DIR/images/cover.jpg" ]]; then
    echo "cover master is newer — regenerating web copies"
    convert "$MASTER" -resize 1000x1600 -quality 86 "$SITE_DIR/images/cover.jpg"
    convert "$MASTER" -resize 500x800  -quality 86 "$SITE_DIR/images/cover-500.jpg"
  fi
fi

# Stage only the public files. `wrangler pages deploy` uploads everything in the
# directory it is given — .assetsignore is a Workers-assets feature and is NOT
# honoured by Pages — so anything not meant to be public must be excluded here.
STAGE="$(mktemp -d)"
trap 'rm -rf "$STAGE"' EXIT

rsync -a \
  --exclude 'README.md' \
  --exclude '.assetsignore' \
  --exclude 'deploy.sh' \
  --exclude '.wrangler' \
  --exclude '.*.swp' \
  "$SITE_DIR"/ "$STAGE"/

echo "deploying (staged copy of $SITE_DIR) -> $PROJECT"
echo "  files:"; (cd "$STAGE" && find . -type f | sed 's|^\./|    |' | sort)

npx wrangler pages deploy "$STAGE" \
  --project-name="$PROJECT" \
  --commit-dirty=true

echo
echo "live: $LIVE_URL"
echo "(the per-deployment hash URL has no TLS cert — use the one above)"
