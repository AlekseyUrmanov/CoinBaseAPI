# CoinBaseAPI
- Market Making Algorithms
- Providing Liquidity
---
## Purpose and details
Market making is essential to any trading commodity. For crypto currency, there is a high trading fee on transactions. Though it varies from exchnage to exchnage, rates go from .4% to .1%. This factor alone, is eneough to defelct algos from running on crypto pairs. However, to truely understand the market, we must first understand the fee structure. Its common to see exchnages offer fee reductions with higher volumes. But these reductions are minor and traders are expected to push 10-50 million dollars in volume in a 30 day period. This may seem like a daunting number, but there is an unsuspecting entry point into these volume tiers, that will be explored later. 

So how do we get away from these fees, while still running high frequency trading algorithems and avoiding the PDT (pattern day trading) rule for normal equity. 
We trade stable coins. Each currency pair has two trading sides, as does any universal commodity pair. Takers and makers. Takers demand, makers supply, in some sense. As a reward for supplying orders and providng liquiduty (on stable coins : USDT, UST, DAI, USDC). Makers, or "maker orders" get a 0% fill fee. Perfect. 

Back to market making, for standard equity, maker activity relies on two factors; that the market oscillates or it's non-trending. Trending markets will leave us holding unfavorable inventory positions and oscillating markets/stable markets allows us to consistently swap inventory positions from buy to sell-side and back. 

Utlizing the post order feature ('post' : posting to order book), we avoid fees and are free to conduct any trading activity, held only at the discretion of our account balance and the order fill time. 

## Strategic Overview
The strategy of this program can be broken into several componenets. 
- Time Volume Based Ordering
- Active Order Adjustment
- Empirical Placement
- Order Book Pressure Identification
- Inventory Turnover Calculation




