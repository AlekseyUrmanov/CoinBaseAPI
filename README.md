# CoinBaseTrading
- Market Making Algorithms
- Providing Liquidity
- Automating Entrance Opportunities

## Understanding Profitability
 As a foundation, this project will begin in market making stable coins, they have huge volume, low risk, and zero fees. 
 However, moving forward, we will look to enter high volume based fee reduction brackets, and market make standard commodities. 
 - *Factors of Profit*
   - Trade Cost
   - Trade Gain
   - Trade Profit

### Fee structure
<img width="433" alt="Screen Shot 2022-03-11 at 1 08 00 PM" src="https://user-images.githubusercontent.com/94999268/157925277-2681004a-0d17-4e89-abed-9a341d787138.png">

Look at the maker fees, I'll point out that the best bracket is 100k - 1M, its diminishing returns after that. 
In order to get into this bracket, you would only pay 215$ in transaction fees. And boom! You have yourself a 0.1% maker fee, thats 4 times less than the starting fee (we can be 4 times more profitable). To stay in this bracket you will only pay 100$ in fees for every 100k you trade in volume. Crazy.

### Trade Cost
- Trade cost is the base fee, we will define the cost of a trade to be the total cost of a roundtrip (buy and sell). We calculate this cost by taking the value in USD of our position, multiplying it by the fee rate, than doubling it to get the total cost of a roundtrip trade. Trade costs will vary based on the size of our position, but it is not dependant on the price of the commoditity. 

### Trade Gain
- The trade gain we make, is the spread between the best ask and best bid. For simplicity, we assume the spread to be some constant avarage value, though it does fluctuate. Our trade gain will be the size of our position in currency multiplied by the spread we aare able to capture. 

### Trade Profit
- Profit will be the difference between the trade gain and trade cost. We can look at profit this way, the lower the fees the more opportunitis we will see in which we can make a profit, but we also need to analyze the spread per dollar that we can capture. A large spread may be misleading if the price of a commodity is in the thousands, but if spread is large (0.01 - 0.001) and price is low, that is our special sauce. 

## Identifying Opportunity
As a basic example of finding opportunity, assume this code:

<img width="395" alt="Screen Shot 2022-03-11 at 1 30 48 PM" src="https://user-images.githubusercontent.com/94999268/157930359-802065c2-dfa9-4983-8d0e-a4dd0b1e24c4.png">

We run through every currency pair trading in USD. 
We than calculate the profit of of a rountrip trade with a 100 USD value, and some fee rate. 
### Fee Rate Profits
- Disregarding stable coins
  - At .004, we can turn a profit in **14** instances
  - At .001, we can turn a profit in **70** instances

Assuming all 70 profitable instances, including outliers, the avarage profit for 100k in trading value of some commodity would be ~ 200$, with highs around 1400$, and lows at 10$. 

## Opportunities

If we 'draw' out the fee structure, per one dollar, we can assume we pay a fee equal to the decimal of the percentage fee. We pay this fee twice, on entry and exit of a position. SPD (spread per dollar) is simply the spread of the commodity, divided by the price. To see on how many instances we can become profitable on trades we multiply the fee decimal per dollar by two, and look for commodities that have a greater spread per dollar than that value. Here is a table of how opportunities increase based on the fee bracket, and the spread per dollar. Noteably, the most valuable bracket is the  .001 fee. But that does not exactly indicate valuable opportunites, as some of these are quite literally shit coins with low liquidity. 
Looking at this situation, intutition tells us that we can trade small volume of many different cryptos rather than large volume on a few, and still get the same results. 

<img width="380" alt="Screen Shot 2022-03-14 at 2 02 52 PM" src="https://user-images.githubusercontent.com/94999268/158234911-bdd2907f-72d2-4f6d-a17c-f1c3cc35c605.png">
 *Fee column is not in %*


