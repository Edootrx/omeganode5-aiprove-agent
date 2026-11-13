#!/usr/bin/env python3
"""Replay strategy.py over bars.csv with a stated cost model.

Capital 1.0, 1x exposure. Bar PnL = position[t] * (close[t+1]/close[t] - 1).
On every position change, cost = |delta_pos| * (TAKER + SLIPPAGE*|delta_pos|)
of notional, TAKER=5bps, SLIPPAGE=2bps. Prints net return and max drawdown.
"""
import csv
from strategy import positions

TAKER, SLIPPAGE = 0.0005, 0.0002

def main():
    with open("bars.csv") as f:
        rows = list(csv.DictReader(f))
    closes = [float(r["close"]) for r in rows]
    pos = positions(rows)
    eq, peak, maxdd, trades, prev = 1.0, 1.0, 0.0, 0, 0
    for t in range(len(closes) - 1):
        if pos[t] != prev:
            d = abs(pos[t] - prev)
            eq -= d * (TAKER + SLIPPAGE * d)
            trades += 1
            prev = pos[t]
        eq *= 1.0 + pos[t] * (closes[t + 1] / closes[t] - 1.0)
        peak = max(peak, eq)
        maxdd = max(maxdd, 1.0 - eq / peak)
    print(f"net_return={eq - 1.0:.4%} final_equity={eq:.6f} max_drawdown={maxdd:.4%} position_changes={trades}")

if __name__ == "__main__":
    main()
