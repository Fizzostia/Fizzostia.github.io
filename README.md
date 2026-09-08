# fizzostia.github.io

The Fizzostia studio site: home, games, and a press kit for each game.

## Building

```
python build.py
```

`build.py` holds every fact shown on the site and generates all the HTML. Edit the data at
the top of that file, rerun it, commit. Do not hand-edit the generated `.html` files, the
next build overwrites them. `assets/style.css` is hand-written and is not generated.

## Facts

Everything on this site is verified against the live Steam pages, or for
RoboSquare: Recharged against `Marketing/BRAND.md` in the game repo. The verification date
is set by `VERIFIED` in `build.py` and printed in the site footer. Re-check before changing it.

## The pitch deck

`build.py` also renders the RoboSquare: Recharged publishing pitch to an unlisted path
(`PITCH_SLUG`). It is `noindex`, excluded in `robots.txt` and linked from nowhere on the
site, so it is reachable only by someone given the URL. The deck itself lives in the game
repo at `Marketing/press-kit/pitch-deck-aggro-crab.html`; this build wraps it for hosting.
