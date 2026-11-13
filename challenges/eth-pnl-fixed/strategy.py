#!/usr/bin/env python3
"""ETH 1-minute strategy for the AIProve eth-backtest challenge.

Donchian breakout, LOOKBACK=240 bars (4h), position held until the
opposite breakout (classic trend-following with hysteresis, so it does
not whipsaw on 1-minute noise):
  close > highest high of the prior 240 bars  -> long  (+1)
  close < lowest  low  of the prior 240 bars  -> short (-1)
  otherwise                                   -> keep previous position
Flat for the first 240 bars. The rule is symmetric and has a single
parameter; nothing is fitted bar-by-bar, so a held-out tail sees the
same strategy as the published window.

Usage: python3 strategy.py bars.csv > positions.csv
Output CSV `minute,position`; position on row t is held over t -> t+1.
"""
import csv, sys

LOOKBACK = 240

def positions(rows):
    closes = [float(r["close"]) for r in rows]
    highs = [float(r["high"]) for r in rows]
    lows = [float(r["low"]) for r in rows]
    pos, cur = [], 0
    for i in range(len(rows)):
        if i >= LOOKBACK:
            if closes[i] > max(highs[i - LOOKBACK:i]):
                cur = 1
            elif closes[i] < min(lows[i - LOOKBACK:i]):
                cur = -1
        pos.append(cur if i >= LOOKBACK else 0)
    return pos

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "bars.csv"
    with open(path) as f:
        rows = list(csv.DictReader(f))
    w = csv.writer(sys.stdout)
    w.writerow(["minute", "position"])
    for r, p in zip(rows, positions(rows)):
        w.writerow([r["minute"], p])

if __name__ == "__main__":
    main()
