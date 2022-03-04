# CoinBaseAPI
- Market Making Algorithms
- Providing Liquidity
---
## Background
Market making is essential in any trading commodity. For crypto- its common knowledge that there's high trading fee's on transactions. Though it varies from exchnage to exchnage, rates may be from .4% to .1%. This is eneough to move many algos away from running on defi pairs. However, to truely understand the market, we must first understand the fee structure. Its common to see exchnages offer fee reductions with higher volumes. But these reductions are minor and traders are expected to push 10-50 million dollars in volume in a 30 day period to see a pleasant reduction. This may seem like a daunting number, but there is an unsuspecting entry point into these volume tiers, that will be explored later. 

So how do we get away from these fees? While still running high frequency trading algorithems and avoiding the PDT (pattern day trading) rule for normal equity. 
We trade stable coins. Each currency pair has two trading sides, as does any universal commodity pair. Takers and makers. Takers demand, makers supply, in some sense. As a reward for supplying orders and providng liquiduty (on stable coins : USDT, UST, DAI, USDC). Makers, or "maker orders" get a 0% fill fee. Perfect. 

Back to market making, maker activity relies on two factors; that the market oscillates or it's non-trending. Trending markets will leave us holding unfavorable inventory quantities and oscillating markets/stable markets will allow us to consistently swap inventory positions from buy to sell-side and back. 

Utlizing the post order feature ('post' : posting to order book), we avoid fees and are free to conduct any trading activity, held back only at the discretion of our account balance and the order fill time. 

## Strategic Overview
The strategy of this program can be broken into several componenets. 
- Pric Time Volume Based Ordering
- Active Order Adjustment
- Empirical Placement
- Order Book Pressure Identification
- Inventory Turnover Calculation
### Price Volume Time (PVT) Ordering
- In an effort to find entry positions in an oscillating market, we look to capture market momentum and place orders over time. The benefit of such a strategy is it reduces the lumping of positions and increases price level diversity. It will organically place more orders at popularly resistive price points and less orders in extreme spike scenarios or during minor trends. In addition, several layers of order book and order flow analysis help determine optimal areas of caapitalization.
- 



