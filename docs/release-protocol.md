# Sonagi: Website Release Protocol & Non-Regression Check

**Created:** 2026-05-12
**Owner:** Asma + whichever Claude session is shipping a change
**Status:** Mandatory, every website change runs this protocol before deploy
**Purpose:** prevent the kind of regression that happened when manual Netlify uploads drifted git out of sync with production, and the kind of "I confirmed I saved it but didn't" gap that lost the prior protocol.

---

## 0. Source-of-truth rule (read first)

**The LIVE site at sonagibeauty.com is the source of truth, not git.** Git history is incomplete because the site has been deployed manually via Netlify (uploads from local `files/` directory) and several HTML pages exist only on disk.

Any change starts with:
1. Fetch the live page via `curl -s https://sonagibeauty.com/<page> -o /tmp/live-<page>` and compare to local. NEVER assume `origin/main` matches production.
2. Use `C:\Users\marou\sonagi-beauty\files\` as the working source, it is the closest mirror of live (within ~520 bytes of difference at last check).

---

## 1. Pre-flight checklist (before touching any file)

- [ ] `git status` clean OR pending changes documented in a TODO log
- [ ] `git fetch --all --prune` ran without errors
- [ ] Live homepage HTML size noted (`curl -s https://sonagibeauty.com/ | wc -c`)
- [ ] Verify which Netlify deploy method is active:
  - `netlify status` if Netlify CLI installed, OR
  - Netlify dashboard → site → Deploys tab: latest deploy source = git auto / manual upload / CLI
- [ ] Confirm Netlify site ID matches `.netlify/state.json` (currently `545b559c-e99f-4a48-9b39-d03fffc2529e`)
- [ ] Note: if the latest deploy is "manual upload" or "CLI", git auto-deploy from `main` would OVERWRITE the manually-uploaded content. **Do not push main without confirming.**

---

## 2. Work in an isolated worktree, never on the user's main working tree

```bash
# Create a clean isolated workspace
git worktree add -B claude/release-<YYYY-MM-DD>-<short-desc> /c/Users/marou/sonagi-release \
  claude/cleanup-2026-05-12        # base off the most-recent cleanup branch, not main

# OR, if working from live: copy the working tree (preserves all 19 production HTML files)
mkdir -p /c/Users/marou/sonagi-release
cp -r /c/Users/marou/sonagi-beauty/files/. /c/Users/marou/sonagi-release/
```

Never edit `/c/Users/marou/sonagi-beauty/files/` directly until the user explicitly approves a write-back.

---

## 3. Apply changes: one atomic commit per logical change

Atomic means: theme-color sweep = 1 commit. Section reorder = 1 commit. BreadcrumbList = 1 commit. Hero CTA fix = 1 commit. Each commit must be revertable independently.

Commit message format:
```
<type>(<scope>): <imperative description>

<paragraph explaining what and why>

Non-regression check: <pass/fail>
  Tag balance: ✓
  Section markers preserved: ✓
  Size delta: +<bytes> (expected: <reason>)
  Hero/CTA/links manually verified: ✓
```

---

## 4. Non-regression check: run BEFORE every commit

A small script lives at `scripts/non-regression-check.sh` (TODO: write this). Until then, run manually:

### 4.1 Structural tag balance
```bash
ORIG=/c/Users/marou/sonagi-beauty/files/<page>.html
NEW=/c/Users/marou/sonagi-release/<page>.html
for tag in section div script style head body article main; do
  o_open=$(grep -oE "<$tag[ >]" "$ORIG" | wc -l)
  o_close=$(grep -oE "</$tag>" "$ORIG" | wc -l)
  n_open=$(grep -oE "<$tag[ >]" "$NEW" | wc -l)
  n_close=$(grep -oE "</$tag>" "$NEW" | wc -l)
  echo "$tag: orig $o_open/$o_close → new $n_open/$n_close"
done
```
Pass criterion: all 8 tag counts in NEW match ORIG (deltas only acceptable when the change is explicitly adding/removing those elements).

### 4.2 Section marker preservation
For homepage `index.html`, check that every key section class still exists exactly once:
- `carousel-wrap`, `marquee-wrap`, `section-wrap`, `quiz-banner`, `brand-belt-section`, `concerns-wrap`, `reviews-section`, `blog-section`, `inf-section`, `events-section`, `insta-section`, `newsletter`, `points-section`

For product `produit.html`:
- `prod-layout`, `prod-gallery`, `prod-tabs-bar`, `related-section`

For catalog (`skincare.html`, `maquillage.html`, `haircare.html`):
- `cat-banner`, `filter-strip`, `prods-grid`

### 4.3 Link/href integrity
```bash
# All hrefs that should resolve to existing HTML pages
grep -oE 'href="[^"]+\.html"' "$NEW" | sort -u | while read href; do
  url=$(echo "$href" | sed -E 's/href="([^"]+)"/\1/')
  [ -f "$NEW/../$url" ] || [ -f "files/$url" ] || echo "BROKEN: $url"
done
```

### 4.4 JSON-LD validity
Every `<script type="application/ld+json">` block must parse as valid JSON:
```bash
python -c "
import re, json, sys
for blk in re.findall(r'<script type=\"application/ld\\+json\">(.*?)</script>', open('$NEW').read(), re.DOTALL):
    try: json.loads(blk)
    except json.JSONDecodeError as e: print('INVALID JSON-LD:', e); sys.exit(1)
print('all JSON-LD blocks parse OK')
"
```

### 4.5 Mobile-vs-desktop scope check
If the change is mobile-only, scan that no desktop-breakpoint CSS was modified:
```bash
git diff <ORIG_REF> <NEW_REF> -- files/css/sonagi.css | \
  grep -E "^[+-]" | grep -vE "max-width|@media\s*\(max-width" | head -20
```

### 4.6 Lighthouse smoke check (manual or scripted)
Before deploy, run Lighthouse on the preview URL for the home + product + journal pages.
Targets: LCP < 2.5s, CLS < 0.1, performance ≥ 85. Regressions = block deploy.

---

## 5. Preview URL: always required before deploy

```bash
cd /c/Users/marou/sonagi-release
python -m http.server 8765 > /tmp/sonagi-server.log 2>&1 &
npx --yes localtunnel --port 8765 --subdomain sonagi-preview-asma > /tmp/sonagi-lt.log 2>&1 &
sleep 12
cat /tmp/sonagi-lt.log    # → "your url is: https://sonagi-preview-asma.loca.lt"
curl -s https://ipv4.icanhazip.com  # → tunnel-password for the localtunnel gate
```

User browses the preview on desktop + mobile + iPad. Reviews every page on the change list.

---

## 6. Deploy: only after explicit user "go" + non-regression check passes

### 6a. If site auto-deploys from `main`:
```bash
git checkout main
git merge --no-ff claude/release-<date>-<desc>
git push origin main
# Netlify auto-rebuilds and deploys
```

### 6b. If site is deployed via Netlify CLI from local:
```bash
# 1. Sync the release branch back to working tree
rsync -a /c/Users/marou/sonagi-release/ /c/Users/marou/sonagi-beauty/files/
# 2. Deploy via CLI (requires netlify login + site link)
cd /c/Users/marou/sonagi-beauty
netlify deploy --dir=files --prod --message="release <date>, <short-desc>"
# 3. Verify deploy URL
netlify status
```

### 6c. If site is deployed via Netlify drag-drop UI:
Bundle the directory:
```bash
cd /c/Users/marou/sonagi-release
zip -r /tmp/sonagi-release-<date>.zip . -x "*.git/*"
# User uploads the zip via app.netlify.com/sites/.../deploys
```

---

## 7. Post-deploy verification (within 10 minutes of deploy)

- [ ] `curl -sI https://sonagibeauty.com/<changed-page>` returns 200
- [ ] Page size is in expected range (within ±5% of preview)
- [ ] Visual smoke on desktop (incognito) + mobile (iOS Safari + Android Chrome if possible)
- [ ] Test the critical conversion paths: hero CTA → quiz, quiz → results, results → product, add-to-cart → cart, cart → checkout
- [ ] Verify schema with [Google Rich Results Test](https://search.google.com/test/rich-results) for at least the homepage + a product page + a glossary page
- [ ] Note the live deploy ID + timestamp in `docs/deploy-log.md`

---

## 8. Rollback procedure (if regression detected post-deploy)

### If deployed via git → Netlify auto-deploy:
```bash
git revert <bad-commit-sha> --no-edit
git push origin main
# Netlify auto-redeploys the previous good state
```

### If deployed via Netlify CLI/drag-drop:
- Open Netlify dashboard → site → Deploys tab
- Find the previous good deploy
- Click "Publish deploy", instant rollback (no rebuild)

---

## 9. Logging: what gets persisted

Every release appends an entry to `docs/deploy-log.md`:
```
## 2026-MM-DD: <short-desc>
- Branch: claude/release-<date>-<desc>
- Commits: <list>
- Files changed: <list>
- Preview URL (if still up): <url>
- Live deploy URL: https://sonagibeauty.com, Netlify deploy ID: <id>
- Non-regression check: pass (link to commit message)
- Post-deploy smoke: pass / fail-and-rolled-back
```

---

## 10. Known gotchas (from past sessions)

1. **Git can be a phantom copy of production.** Always verify against `curl https://sonagibeauty.com/` not against `git show origin/main:files/`.
2. **The 12-vs-19 HTML page trap.** `origin/main` has 12 HTML files; production has 19. The 7 extras (about, faq, glossaire, cgv, cookies, mentions-legales, politique-confidentialite) live ONLY on disk + production. Always work from 19, never 12.
3. **The script tag imbalance is normal.** `<script src="…">` self-closing tags appear in `<script>` count but not `</script>`. Expect roughly +1 open vs close. Not a regression.
4. **Don't kill `node.exe` or `python.exe` indiscriminately.** Doing so kills the claude-mem worker (port 37777), losing access to past-session memory. Use PID-targeted `taskkill /F /PID <pid>` instead.
5. **Localtunnel sessions die when Claude Code session ends.** For persistent previews, deploy a Netlify branch deploy URL instead (one-time setup in Netlify dashboard).

---

End of protocol. This document is mandatory reading at session start when any website work is on the agenda.
