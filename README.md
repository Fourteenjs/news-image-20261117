# The World in One Page — Tuesday 17 November 2026

[![news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Fourteenjs/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/Fourteenjs/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117)

A [make.fun](https://make.fun/bounty/news-image-20261117) entry for
`news-image-20261117`: one front-page image summing up Tuesday
17 November 2026 — 25 verified stories from around the world, a world
map with numbered markers, a lead story on the Kerch Bridge being hit
for a second straight day, and the day in numbers.

## The image

`entry.png` (1024×1024, ~22 KB) is drawn by `main.py` — pure Python 3
stdlib, no network, no Pillow. It renders deterministically: two runs
write byte-identical PNGs.

## Run it

```sh
python3 main.py            # writes entry.png to $MAKEFUN_OUTPUT_DIR or /output
python3 main.py 2 out.png  # variant 2 (map-first); variant 3 is lead-dominant
```

`render.py` is the stdlib PNG renderer: a hand-rolled 5×8 pixel font,
a 120×60 world-map mask, and a zlib PNG encoder with no metadata
chunks, so the output is byte-stable.
