import time
import cbpro
import datetime
#import sys

auth_client = None
pub_client = None

def auth():
    global auth_client, pub_client
    key = '8811ae1f541f911b68394649c73d17e8'
    secret = 's1L46eZRpoHdWYu6DcYROQugtgY7rrfGu7S/jUGEWMTIDUC2bgiV3c8FB1lxjVF3NHm9UnTL6U7p6A+Mptgjew=='
    passphrase = 'omgvd80zrdr'

    auth_client = cbpro.AuthenticatedClient(key=key, b64secret=secret, passphrase=passphrase)
    pub_client = cbpro.PublicClient()


auth()

order_status_dict = {}  # dictionary of orders
order_book = {}  # dictionary of prices to volume
orders_at_price = {}  # dictionary of order sets

reduction_objects = []

tbid = None
task = None
v24h = None

def PositionManager(product): # can be run <10 times per second

    def bump(OID, direction):

        data = order_status_dict[OID]

        size = data['size']
        
        price = float(data['price'])

        keys = list(order_book.keys())
        
        keys.sort()

        iod = int(keys.index(price))

        if direction == 'up':
          
            nprice = str(keys[iod + 1])
            
        elif direction == 'down':
          
            nprice = str(keys[iod - 1])
            
        else:
          
            nprice = str(price)

        coin = data['product']
        
        side = data['side']

        auth_client.cancel_order(OID)
        
        auth_client.place_limit_order(coin, side, nprice, size, post_only=(True))


    # Step 1 : check for open positions at best bid/ask.

    BA = pub_client.get_product_order_book(product, level=1)

    # can't run at unlimited speed yet- because it polls public endpoint,
    
    # find a way to determine bid and ask through order book maintenance and construction

    task = float(((BA['asks'])[0])[0])
    
    tliquid = float(((BA['asks'])[0])[1])

    tbid = float(((BA['bids'])[0])[0])
    
    bliquid = float(((BA['bids'])[0])[1])

    orders_at_top_ask = orders_at_price[task]
    
    orders_at_top_bid = orders_at_price[tbid]

    amount_of_orders = len(order_status_dict)

    # preliminary bot; therefore; focus is just on avoiding bad entries

    # dynamically adjust spread based on order flow and order volume size flow factors
    # maybe I don't need to hold the tightest positions, I can hold triple spread which could be just as efficient

    if amount_of_orders == 0:
      
        # monitor spread and liquidity
        #print('no orders to analyze')
        pass
      
    else:

        adjustments = []

        if len(orders_at_top_bid) >0:
          
            for OID in orders_at_top_bid:
              
                current_liquid_ratio = tliquid/bliquid
                
                # ask liquidity out of bid liquidity
                
                position_liquid_ratio = ((order_status_dict[OID])['rliquidity'])/bliquid
                
                # remaining liquidity out of current liquidity
                
                if current_liquid_ratio <= 1: # ask amount is less than 100% of the bid amount
                  
                    # determine multiplier factor through a function of price - liquidity
                    # print(f'good liquidity :{current_liquid_ratio}')
                    
                    pass
                  
                elif current_liquid_ratio < 2: # ask size is larger than bid size, depending on the size, we can let it slide
                  
                    if position_liquid_ratio < 0.50:
                      
                        pass
                      
                    else:
                      
                        #bump down / more  analysis
                        # allow order to develop  and see how liquidity changes
                        pass
                      
                elif current_liquid_ratio > 2:
                  
                    if position_liquid_ratio < 0.05: # if i am within 5 % of execution
                      
                        pass
                      
                    else:
                      
                        adjustments.append([OID,'down'])
                        
                        #bump down / more  analysis
                        pass
                      
                else:
                  
                    pass

        else:
          
            pass

        buy_orders = 0
        sell_orders = 0

        bump_oids = []

        for order in order_status_dict:
          
            data = order_status_dict[order]

            if data['side'] == 'buy':
              
                if float(data['price']) == tbid:
                  
                    buy_orders += 1
                    
                    pass
                  
                else:
                  
                    plr = (data['rliquidity']) / float(order_book[float(data['price'])])
                    
                    buy_orders += 1
                    
                    if plr > 0.7:
                      
                        bump_oids.append(order)
                        
                    else:
                      
                        pass
            else:
                sell_orders += 1

        current_liquid_ratio = tliquid / bliquid
        
        if len(bump_oids) > 0 and current_liquid_ratio < 1:
          
            for OID in bump_oids:
              
                adjustments.append([OID,'up'])

        else:
          
            pass

        if len(adjustments) == 0:
          
            pass
          
        else:
          
            for adj in adjustments:
              
                bump(adj[0], adj[1])


    pass






def ProcessData(msg):
    news = msg

    if news['type'] == 'subscriptions':

        print('--sd--')
        pass
    else:

        TYPE = news['type']

        if TYPE == 'ticker':

            v24h = news['volume_24h']
            tbid = news['best_bid']
            task = news['best_ask']

        elif TYPE == 'snapshot':

            asks = news['asks']
            bids = news['bids']

            for ask in asks:
                order_book[float(ask[0])] = ask[1]
                orders_at_price[float(ask[0])] = set()
            for bid in bids:
                order_book[float(bid[0])] = bid[1]
                orders_at_price[float(bid[0])] = set()

            # 0.002 seconds processing time, ~ 15k entries, 1mb size data dpending on comodity

        elif 'user_id' in news:

            if news['user_id'] == '60243cfeb0ccd414b6290f32':

                if TYPE == 'received':

                    if news['order_type'] == 'limit':

                        # get vars
                        OID = news['order_id']
                        size = news['size']
                        side = news['side']
                        price = news['price']
                        product = news['product_id']

                        initial_liquidity = order_book[float(price)]

                        orders_at_price[float(price)].add(OID)

                        remaining_liquidity = float(initial_liquidity)

                        reduction_objects.append(ReductionObject(OID, price))

                        order_status_dict[OID] = {'size': size,
                                                  'side': side,
                                                  'price': price,
                                                  'type': TYPE,
                                                  'product': product,
                                                  'iliquidity': initial_liquidity,
                                                  'rliquidity': remaining_liquidity}

                    elif news['order_type'] == 'market':
                        pass

                    else:
                        pass
                    pass

                elif TYPE == 'open':

                    OID = news['order_id']

                    (order_status_dict[OID])['type'] = TYPE

                    pass

                elif TYPE == 'done':

                    OID = news['order_id']

                    reason = news['reason']

                    (order_status_dict[OID])['type'] = TYPE

                    (order_status_dict[OID])['reason'] = reason

                    matchingEngine(OID)

                    pass

                elif TYPE == 'match':

                    OID = news['maker_order_id']

                    if OID in order_status_dict:

                        (order_status_dict[OID])['type'] = TYPE

                    else:

                        OID = news['order_id']
                        size = news['size']
                        side = news['side']
                        price = news['price']
                        product = news['product_id']

                        initial_liquidity = order_book[float(price)]

                        orders_at_price[float(price)].add(OID)

                        remaining_liquidity = float(initial_liquidity)

                        reduction_objects.append(ReductionObject(OID, price))

                        order_status_dict[OID] = {'size': size,
                                                  'side': side,
                                                  'price': price,
                                                  'type': TYPE,
                                                  'product': product,
                                                  'iliquidity': initial_liquidity,
                                                  'rliquidity': remaining_liquidity}

                    pass
                else:
                    pass

        # data from full channel, used for reductions

        elif TYPE == 'received':

            OTYPE = news['order_type']

            if OTYPE == 'limit':

                price = news['price']
                OID = news['order_id']

                for r in reduction_objects:
                    r.add_id([OID, price])
            else:
                pass
            pass

        elif TYPE == 'open':

            pass

        elif TYPE == 'done':

            if 'reason' in news:
                if news['reason'] == 'canceled':

                    size = float(news['remaining_size'])
                    price = news['price']
                    ID = news['order_id']

                    for r in reduction_objects:

                        if r.PRICE == price:

                            if ID in r.void_ids:
                                # remeove that id from void ids to save storage
                                # increases processing time
                                # create effcient system
                                pass
                            else:

                                (order_status_dict[r.OID])['rliquidity'] -= size

                                pass
                        else:
                            pass
                else:
                    pass
            else:

                pass

            pass

        elif TYPE == 'match':

            price = float(news['price'])
            size = float(news['size'])

            OIDS = orders_at_price[price]

            if len(OIDS) == 0:
                pass
            else:
                for OID in OIDS:
                    (order_status_dict[OID])['rliquidity'] -= size

            pass

        elif TYPE == 'change':

            pass

        elif TYPE == 'activate':

            pass

        elif TYPE == 'l2update':

            changes = news['changes']
            for change in changes:
                order_book[float(change[1])] = change[2]

                if float(change[1]) in orders_at_price:
                    pass
                else:
                    orders_at_price[float(change[1])] = set()
        else:

            pass


def matchingEngine(OID):
    global order_status_dict, auth_client

    def new_price(x, y):

        x0 = int((x.split('.'))[0])
        x1 = int((x.split('.'))[1])

        y0 = int((y.split('.'))[0])
        y1 = int((y.split('.'))[1])

        d0 = y0 - x0
        d1 = y1 - x1

        new_price = f'{y0 + d0}' + '.' + f'{y1 + d1}'

        return new_price

    def matchOrder(content):

        coin = content['product']

        BA = pub_client.get_product_order_book(coin, level=1)

        task = ((BA['asks'])[0])[0]

        tbid = ((BA['bids'])[0])[0]

        if content['side'] == 'buy':

            side = 'sell'
            size = content['size']
            price = task

            if price == content['price']:
                price = new_price(tbid, task)

        else:

            side = 'buy'
            price = tbid
            size = content['size']

        auth_client.place_limit_order(coin, side, price, size, post_only=(True))

    content = order_status_dict[OID]

    if content['reason'] == 'canceled':

        p = float(content['price'])

        (orders_at_price[p]).remove(OID)

        del order_status_dict[OID]

        c = 0
        for r in reduction_objects:
            if r.OID == OID:
                del reduction_objects[c]
                break
            else:
                pass
            c += 1
        pass

    else:

        del order_status_dict[OID]

        p = float(content['price'])

        (orders_at_price[p]).remove(OID)

        c = 0
        for r in reduction_objects:
            if r.OID == OID:
                del reduction_objects[c]
                break
            else:
                pass
            c += 1
        pass

        matchOrder(content)


class ReductionObject():

    def __init__(self, OID, PRICE):
        self.PRICE = PRICE
        self.OID = OID
        self.void_ids = []

    def add_id(self, rPack):
        rprice = rPack[1]
        if rprice == self.PRICE:
            self.void_ids.append(rPack[0])
        else:
            pass


class MyWebsocketClient(cbpro.WebsocketClient):
    def on_open(self):
        self.url = "wss://ws-feed.pro.coinbase.com/"
        self.products = ['USDT-USD']
        self.channels = ['full', 'level2_50']  # 'user','ticker_1000','full','level2_50','level2_batch' is same as 50
        self.auth = True
        self.api_key = '8811ae1f541f911b68394649c73d17e8'
        self.api_passphrase = 'omgvd80zrdr'
        self.api_secret = 's1L46eZRpoHdWYu6DcYROQugtgY7rrfGu7S/jUGEWMTIDUC2bgiV3c8FB1lxjVF3NHm9UnTL6U7p6A+Mptgjew=='
        self.should_print = False
        self.stime = datetime.datetime.now()
        self.is_on = True

        print("--op--")

    def on_message(self, msg):
        ProcessData(msg)
        pass

    def on_close(self):
        print((datetime.datetime.now() - self.stime).seconds)
        self.is_on = False
        print("--cd--")


try:

    x = MyWebsocketClient()
    
    x.start()
    
    while True:
      
        time.sleep(3)
        PositionManager('USDT-USD')
        
        pass


finally:

    x.close()






