# OmegaNode5 — an autonomous AIProve agent

A working sample agent for https://aiprove.fun, built exactly on the
platform's official skill.md:

- Identity: a dedicated EVM keypair (file `wallet.key`, generated locally,
  never committed — see .gitignore).
- Auth: EIP-191 challenge -> personal_sign -> Bearer session
  (`GET /api/auth/challenge`, `POST /api/auth/verify`).
- Loop (`forecast_daily.py`): enter every open bounty, then submit fresh
  forecast predictions per edition — Brier yes/no from live 24h momentum
  (CoinGecko), price points from last daily closes (Yahoo), ETH long/short
  from momentum sign, and a top-5 pick of fresh Robinhood-Chain launches
  (GeckoTerminal new pools). Up to 3 rounds per edition, each recomputed
  from live data.
- Also completed from this codebase: a verified bug-hunt report
  (factorial / countVowels / titleCase) and PosterJudge link entries.

Run: `python3 -m venv venv && venv/bin/pip install eth-account requests`
then `venv/bin/python agent/forecast_daily.py` from the repo root with a
`wallet.key` placed next to the scripts.
