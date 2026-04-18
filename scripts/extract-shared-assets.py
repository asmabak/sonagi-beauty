# -*- coding: utf-8 -*-
"""
Extract inline shared CSS / QUIZ_IMGS / shared JS from all 12 HTML files
and replace with <link> + <script src> tags pointing to the canonical
extracted files in files/css/ and files/js/.

Pixel-perfect parity rules:
- The first 614 lines of every page's inline <style> are byte-identical (verified)
  and live entirely in files/css/sonagi.css (which now also includes the 12-line
  tail block: rev-stars-top, rev-footer, rev-city, the @media inf-video tweak,
  and .c-slide-bg-1/2/3).  So every full inline <style> is fully covered.
  -> Replace the entire <style>...</style> with <link rel="stylesheet">
     + a SMALL inline <style> for any page-specific delta lines (lines 626..N-1
     of the original block, where present).
- window.QUIZ_IMGS = {...} block is byte-identical and lives in
  files/js/sonagi-quiz-imgs.js.  Replace its <script>...</script> wrapper
  with <script src="js/sonagi-quiz-imgs.js" defer></script>.
- The "SHARED JS v4 (clean rebuild)" portion of the second <script> block is
  byte-identical across all pages and lives in files/js/sonagi-app.js.
  Replace it (header through DOMContentLoaded init) with
  <script src="js/sonagi-app.js" defer></script>.  KEEP the rest of the
  second <script> (the SONAGI ADVISOR v2 block + handleCheckout note).
"""
import os
import re
import io

PAGES = [
    'index.html', 'skincare.html', 'haircare.html', 'maquillage.html',
    'marques.html', 'produit.html', 'panier.html', 'compte.html',
    'journal.html', 'masterclasses.html', 'rewards.html', 'confirmation.html',
]

FILES_DIR = os.path.join(os.path.dirname(__file__), '..', 'files')
FILES_DIR = os.path.normpath(FILES_DIR)


def read(path):
    with io.open(path, 'r', encoding='utf-8', newline='') as f:
        return f.read()


def write(path, txt):
    with io.open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(txt)


def transform(src, fname):
    # Detect line ending used (CRLF on Windows here) and use it everywhere
    EOL = '\r\n' if '\r\n' in src[:200] else '\n'
    out = src

    # ── 1) Replace inline <style>...</style> with <link> + page-specific delta ─
    # The shared CSS is exactly the first 614 LINES (not chars) of the inline
    # style.  Anything from line 615 (1-indexed) of the inline block onward is
    # page-specific delta (or for index.html, just the c-slide-bg helper line
    # which we already migrated to sonagi.css).
    eol_re = re.escape(EOL)
    m = re.search(r'<style>' + eol_re + r'(.*?)' + eol_re + r'</style>', out, re.S)
    assert m, fname + ': no <style> block found'
    css_body = m.group(1)
    css_lines = css_body.split(EOL)
    # css_lines[0..613] (614 lines) = shared, byte-identical to sonagi.css head
    # css_lines[614..] = page-specific delta
    delta_lines = css_lines[614:]
    delta_text = '\n'.join(delta_lines).strip()

    # Index page's only delta is the c-slide-bg-1/2/3 line which is now in
    # sonagi.css.  Detect that and emit nothing.
    is_index_only_delta = (
        delta_text == ''
        or delta_text == '.c-slide-bg-1{background:var(--cream)}.c-slide-bg-2{background:#fdf9f5}.c-slide-bg-3{background:#fdf8f2}'
    )

    if is_index_only_delta:
        replacement = '<link rel="stylesheet" href="css/sonagi.css">'
    else:
        replacement = (
            '<link rel="stylesheet" href="css/sonagi.css">' + EOL
            + '<style>' + EOL + delta_text + EOL + '</style>'
        )

    out = out[:m.start()] + replacement + out[m.end():]

    # ── 2) Replace QUIZ_IMGS inline <script>...</script> with src tag ──
    # Pattern: <script>\nwindow.QUIZ_IMGS = {  ... };\n</script>
    m2 = re.search(
        r'<script>' + eol_re
        + r'window\.QUIZ_IMGS\s*=\s*\{.*?' + eol_re
        + r'\};' + eol_re + r'</script>',
        out, re.S
    )
    assert m2, fname + ': no QUIZ_IMGS <script> block found'
    out = (
        out[:m2.start()]
        + '<script src="js/sonagi-quiz-imgs.js" defer></script>'
        + out[m2.end():]
    )

    # ── 3) Replace inline shared JS (inside the second <script>) with src tag ──
    # The shared JS spans from the comment header
    #   "SONAGI BEAUTY — SHARED JS v4 (clean rebuild)"
    # through the closing of the DOMContentLoaded init "});" on its own line.
    # Everything AFTER (the SONAGI ADVISOR v2 block + Stripe Checkout comment)
    # stays inline.
    #
    # The inline shared JS lives inside:
    #   <script>\n  ...HEADER...  ...DOMContentLoaded });\n  /* ADVISOR v2 ... */
    #
    # Strategy: find the second <script> block.  Inside it, replace the prefix
    # from the SHARED JS comment header through the first ADVISOR v2 marker
    # with nothing, and place a separate <script src> tag right BEFORE that
    # second <script> (in body, not head — defer ordering not critical because
    # the advisor calls only fire on user interaction).
    shared_header_re = re.compile(
        r'/\* '
        + re.escape('══════════════════════════════════════════════════════')
        + r'\s*' + eol_re + r'\s*SONAGI BEAUTY — SHARED JS v4 \(clean rebuild\)'
    )
    # Find first occurrence
    sh_match = shared_header_re.search(out)
    assert sh_match, fname + ': no SHARED JS v4 header found'
    sh_start = sh_match.start()

    # Find the line containing the first '/* ══ SONAGI ADVISOR v2' AFTER sh_start
    adv_match = re.search(r'/\* ══ SONAGI ADVISOR v2', out[sh_start:])
    assert adv_match, fname + ': no SONAGI ADVISOR v2 marker found'
    adv_pos = sh_start + adv_match.start()

    # The shared JS to remove is out[sh_start:adv_pos] (header + body up to
    # the start of the advisor block).  We want to replace it with the empty
    # line that lets the advisor block keep its own context.

    # Locate the opening "<script>\n" right BEFORE sh_start to insert the
    # external <script src> tag right before it (so external loads first).
    script_open_marker = '<script>' + EOL
    script_open = out.rfind(script_open_marker, 0, sh_start)
    assert script_open != -1, fname + ': could not locate enclosing <script> tag'

    # Build the new content:
    # 1) keep everything before <script>
    # 2) insert <script src="js/sonagi-app.js" defer></script>\n
    # 3) keep the existing <script>\n (we still need its contents — just the advisor)
    # 4) drop everything from sh_start to adv_pos (the shared JS)
    # 5) keep everything from adv_pos onward (advisor + closing </script>)

    new = (
        out[:script_open]
        + '<script src="js/sonagi-app.js" defer></script>' + EOL
        + out[script_open:sh_start]
        + out[adv_pos:]
    )
    out = new

    return out


def main():
    backups = []
    for p in PAGES:
        path = os.path.join(FILES_DIR, p)
        before = os.path.getsize(path)
        src = read(path)
        try:
            new_src = transform(src, p)
        except AssertionError as e:
            print('SKIP %s: %s' % (p, e))
            continue
        write(path, new_src)
        after = os.path.getsize(path)
        print('%-22s  %8d -> %8d  (-%d, -%.1f%%)' % (
            p, before, after, before - after, 100.0 * (before - after) / before
        ))


if __name__ == '__main__':
    main()
