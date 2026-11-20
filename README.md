# The World Today — 20 November 2026 in one image

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/enisaishere-hue/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/enisaishere-hue/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)

A one-page newspaper front page that sums up Friday, 20 November 2026 in a
single 1024×1024 image. Seven stories, each verified against a named source
reported on the day — see [RESEARCH.md](RESEARCH.md) for the sourcing notes.

## The seven stories

1. **GTA VI smashes records** — an estimated $2.36 billion and 24.6 million
   copies on day one, about three times GTA V's first-day haul
   (Sensor Tower estimates via Reuters and Deadline). The sales figures are
   estimates, not official Take-Two/Rockstar numbers.
2. **Trump, Xi and Putin meet** — a first-ever three-way meeting in Shenzhen,
   ending in a joint "peace declaration" (BBC).
3. **Cyclone Akvan hits Odisha** — landfall near Gopalpur around noon, winds
   gusting to 110 km/h; hundreds of thousands evacuated, 423 rescue teams
   deployed (India Meteorological Department).
4. **Voices from besieged Taiz** — seven people inside the Yemeni city speak
   to the BBC; 148 civilians killed by Houthi attacks since August.
5. **Phillips' year of tons** — Glenn Phillips hit 118 as New Zealand reached
   317-6 at lunch on day two against India in Wellington (Reuters/AP).
6. **Gold at a 14-month low** — bullion slid near $3,682 an ounce as traders
   priced in a December Fed rate hike (Wall Street Journal).
7. **Ramayana keeps rolling** — day 15 added about ₹19 crore in India; the
   epic now stands at ₹851 crore net, ₹1,531 crore worldwide
   (Box Office India).

## How it is made

`render_poster.py` draws the whole page with Pillow — masthead, a hand-drawn
Vice City sunset skyline for the GTA VI hero story, and six story cards.
Everything is drawn from code: no photos, no network, no external assets,
and the output is deterministic (fixed random seed, no clock).

`main.py` is standard library only: it copies the pre-rendered `entry.png`
into the output directory and verifies its SHA-256. It never renders
anything, because the grading sandbox has no Pillow or fonts.

```sh
python3 render_poster.py entry.png   # render (needs Pillow + DejaVu fonts)
python3 main.py                      # copy entry.png to $MAKEFUN_OUTPUT_DIR
```

## Entry

- Competition: [news-image-20261120](https://make.fun/bounty/news-image-20261120)
- Output: `entry.png`, 1024×1024, 107,234 bytes,
  SHA-256 `6294660c8e1c874d6b4b4709df3dab7aff42202495f35498b68c7e74eebca028`
