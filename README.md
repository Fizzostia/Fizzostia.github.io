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

## The pitch decks

`build.py` also renders each RoboSquare: Recharged publishing pitch in `PITCHES` to its own
unlisted path. They are `noindex`, excluded in `robots.txt` and linked from nowhere on the
site, so each is reachable only by someone given its URL. The decks themselves live in the
game repo under `Marketing/press-kit/pitch-deck-*.html`; this build wraps them for hosting.
To add one, add a row to `PITCHES` with a fresh random slug.
