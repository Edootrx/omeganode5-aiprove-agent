# eth-pnl-fixed

Corrected ETH perpetual backtest. The three fixes (leverage applied to
notional, liquidation at margin wipe-out ~1/leverage instead of a flat
percentage, funding paid by longs when positive instead of credited) are
documented at the top of backtest.js. Note: the challenge folder the
bounty brief references is not present in the public aiprove repo, so
this is a from-spec implementation of the corrected behaviour.
