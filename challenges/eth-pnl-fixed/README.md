# eth-pnl-fixed — ETH backtest strategy

Dataset: `bars.csv` — the frozen 1,440-bar ETH/USDT 1-minute set published
in the official challenge repo (challenges/eth-backtest), window ending
2026-11-13 12:17 UTC. ETH trends down ~3.4% across the window.

Strategy (`strategy.py`): Donchian breakout with a 240-bar (4h) channel
and hysteresis — go long on a close above the prior 240-bar high, short
on a close below the prior 240-bar low, otherwise hold the current
position. One parameter, fully symmetric, no per-bar fitting, so the
held-out tail sees exactly the same rule. On this window it enters short
early and holds, changing position only twice.

Local replay (`backtest.py`; cost model: 5 bps taker + 2 bps size-scaled
slippage per unit of position change, 1x exposure):
net_return=+3.2798%, max_drawdown=2.4521%, position_changes=2
(printed by the script itself; re-run to verify).

Run: `python3 strategy.py bars.csv > positions.csv && python3 backtest.py`
