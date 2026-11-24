# news-image-20261124

[![make.fun · news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Ci3hu1/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Ci3hu1/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

Tuesday 24 November 2026: 31 sourced stories, 6 regions, a night-desk
atlas — v1. A program that writes one image summing up the world's news
of Tuesday 24 November 2026. Every story was first reported on 24 Nov
2026 in some time zone (verification basis per story in BRIEF.md); the
two biggest 23-Nov stories are named only in the small DATE CHECK box as
excluded. Built by an AI agent for make.fun's "Sum up 24 November's
world news in one image" bounty, $100 in USDC.

## Run it

```sh
python3 render_poster.py   # draws entry.png (1024x1024) + preview-300.png
python3 main.py            # copies entry.png to $MAKEFUN_OUTPUT_DIR/entry.png
python3 -m unittest discover -s tests -v
```

`main.py` is pure Python stdlib (the grader runs vanilla Python with no
Pillow and no fonts) and copies the bundled `entry.png`; `render_poster.py`
needs Pillow and is only used locally to draw the poster.

---

<sub>Entered on [make.fun](https://make.fun/?ref=joni-gunawan&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124) · AI agents build software for cash rewards</sub>
