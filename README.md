# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/iqbalcokk8-crypto/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/iqbalcokk8-crypto/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One-page newspaper front page summing up the world news of Saturday, 21 November 2026: seven verified stories, drawn entirely with code.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=xvbs15t0&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>

## About the image

`entry.png` (1024×1024, PNG) is a newspaper-style front page. The lead story is
Iran saying it struck U.S. bases in Bahrain, with Bahrain reporting a civilian
site burned, no one hurt, and its air defences intercepting the rest. The six
other stories cover Mexico's capture of FBI most-wanted cartel boss
"El Chapo Isidro", a Russian missile strike on Zelenskyy's hometown Kryvyi
Rih, the COP31 climate talks in Antalya running past their deadline, the AI
stock sell-off erasing the Nasdaq's 2026 gains, a Russian cargo ship ablaze
in the Gulf of Finland after a drone strike, and a hopeful note from Brazil,
where specially bred mosquitoes cut dengue in children by about 69%. Every
fact on the image was checked against at least two independent reports — see
`RESEARCH.md` for the sources and verification notes. The image is drawn by
`gen_image.py` (Python PIL, no AI image generator, no copyrighted images);
`main.ts` copies the finished PNG to the output directory and verifies it.
