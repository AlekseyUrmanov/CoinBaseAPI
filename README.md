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

Assuming all 70 profitable instances, including outliers, the avarage profit for 100k in trading value of some commodity would be ~ 200$

## Talking Money
In perfect theory, 100k in volume would yield around 200$, but we are not bounded to that number, we can choose the most profitable instance to trade and be making 400$ - 1000$ per 100k in trading volume (50k buy 50k sell). The real question, is how often can we turnover 100k in trading volume, to actually make that profit.
And the answer is, fast, really fast. If you start with 10k USD, and you round trip 5 times on a commodity, thats 100k in volume. On high volume commodities, 1m - 10m per 24hours. We could turn 1-5m dollars per month in volume. That equates to thousands of dollars per day and millions of dollars per year. Additionaly, we would be paying more in fees, but we would also be paying lower fees in lower fee brackets.
My conlusion is simple, in practical theory, there is a massive opportunity in front of us. With a very conservative estimate, that includes risk and loss. We can easily do 50k volume per day, with just 5000 dollars (5 roundtrips, 70 commodities to choose from), adjusting for loss and dead inventory, our monthly profit could stand at 1000-3000$, and being the optimist I am, we could be making 10-20k per month in the near 1-2 years. 


