## Dev Updates 

### Update 1.001
Web Socket bot 1, was the first version of the new operation/trading type, its was clustrsome. Bot 2 has functions integrated directly into the class so it was far faster and more efficient, but it can only run one crypto. I have developed a neew program that can place orders on many different currencies at a time at different time intervals. So websocket bot 3 will be able to trade many currency that has had an order execute on it. And you will be able to specify which cryptos to not trade.

Bot3 almost complete; it can track and trade a variety of currencies. Now I am wokring on adding a 'smart' order matching function that prevents buying and selling at the same price. 

Ive got this idea that the projcet should not be one program, it should be a collection of 6-7 programs, that all work togther, but can work independantly too. 
The programs should be
- Order placing bot
- Trading Bot
- data collector
- data analyzer
- Risk manager
- Inventory manager
- Performance manager

So far, I have only written the trading bot and the order placing bot. 
