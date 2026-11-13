// ETH perpetual PnL backtest — corrected implementation.
// The broken spec this replaces made three errors:
//  1) Leverage ignored: PnL was computed on margin, not on notional
//     (margin x leverage). Fixed: notional = margin * leverage.
//  2) Liquidation threshold wrong: a long is liquidated when the price
//     drop wipes the margin, i.e. drop >= 1/leverage (less maintenance),
//     not at a flat y% for every leverage. Fixed per-position below.
//  3) Funding sign flipped: with positive funding, LONGS PAY shorts.
//     The broken spec credited longs. Fixed: pnl -= funding for longs.
//
// Prices: array of ETH prices, one per hour. Funding: rate per 8h,
// applied at every 8th step. Returns { pnl, liquidated, liquidationStep }.
function backtest({ margin, leverage, entry, prices, fundingRate8h, maintenance = 0.005, side = 1 }) {
  const notional = margin * leverage;
  const qty = notional / entry;
  let pnl = 0;
  for (let i = 0; i < prices.length; i++) {
    const price = prices[i];
    const unreal = side * qty * (price - entry);
    if (unreal <= -(margin - maintenance * notional)) {
      return { pnl: -margin, liquidated: true, liquidationStep: i };
    }
    if ((i + 1) % 8 === 0) {
      // longs pay when funding > 0; shorts receive (side flips the sign)
      pnl -= side * fundingRate8h * qty * price;
    }
  }
  const finalPrice = prices[prices.length - 1];
  pnl += side * qty * (finalPrice - entry);
  return { pnl, liquidated: false, liquidationStep: null };
}
module.exports = { backtest };
