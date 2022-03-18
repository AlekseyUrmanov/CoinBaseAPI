import time
import cbpro
auth_client = None
pub_client = None
import datetime
import sys

def auth():
    global auth_client,pub_client
    key = '8811ae1f541f911b68394649c73d17e8'
    secret = 's1L46eZRpoHdWYu6DcYROQugtgY7rrfGu7S/jUGEWMTIDUC2bgiV3c8FB1lxjVF3NHm9UnTL6U7p6A+Mptgjew=='
    passphrase = 'omgvd80zrdr'

    auth_client = cbpro.AuthenticatedClient(key=key, b64secret=secret, passphrase=passphrase)
    pub_client = cbpro.PublicClient()

auth()

order_status_dict = {}  # dictionary of orders
order_book = {} # dictionary of prices to volume
orders_at_price = {} # dictionary of order sets

tbid = None
task = None
v24h = None

def ProcessData(msg):
    global tbid,task,v24h,order_status_dict
    
    news = msg    
    
    if news['type']== 'subscriptions':
        
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
                            
                        #get vars
                        OID = news['order_id']
                        size = news['size']
                        side = news['side']
                        price = news['price']
                        product = news['product_id']
                        
                        
                        initial_liquidity = order_book[float(price)]
                        
                        orders_at_price[float(price)].add(OID)
                        
                        remaining_liquidity = float(initial_liquidity)
                        
                        
                        order_status_dict[OID] = {'size':size,
                                                  'side':side,
                                                  'price':price,
                                                  'type':TYPE,
                                                  'product':product,
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
        
                elif TYPE == 'done' :
                    
                    OID = news['order_id']
                    
                    reason = news['reason']
                    
                    (order_status_dict[OID])['type'] = TYPE
                    
                    (order_status_dict[OID])['reason'] = reason
                    
                    matchingEngine(OID)
        
                    pass
                
                elif TYPE == 'match':
                    
                    OID = news['maker_order_id']
                    
                    if OID in order_status_dict:
                        
                        (order_status_dict[OID])['type'] =  TYPE
                        
                    else:
                        
                        OID = news['order_id']
                        size = news['size']
                        side = news['side']
                        price = news['price']
                        product = news['product_id']
                        
                        initial_liquidity = order_book[float(price)]
                        
                        orders_at_price[float(price)].add(OID)
                    
                        remaining_liquidity = float(initial_liquidity)
                        
                        order_status_dict[OID] = {'size':size,
                                                  'side':side,
                                                  'price':price,
                                                  'type':TYPE,
                                                  'product':product,
                                                  'iliquidity': initial_liquidity,
                                                  'rliquidity': remaining_liquidity}
                    
                    pass
                else:
                    pass
                
        # data from full channel, used for reductions
        
        elif TYPE == 'received':
            pass
            
        elif TYPE == 'open':
            
            pass

        elif TYPE == 'done' :
           

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
                    
            
            
            # maybe if i add my order ids to the orerbook dictionary at 
            # their correspoing prices.
            # i can acces the order ids at that price.
            # and reduce them in order status dictionary
            
            
            
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
        
        
        def new_price(x,y):
                
            x0 = int((x.split('.'))[0])
            x1 = int((x.split('.'))[1])
                
            y0 = int((y.split('.'))[0])
            y1 = int((y.split('.'))[1])
        
            d0 = y0-x0
            d1 = y1-x1
            
            new_price = f'{y0+d0}'+ '.'+f'{y1+d1}'
            
            return new_price
          
        def matchOrder(content):
            
            coin = content['product']
            
            BA = pub_client.get_product_order_book(coin,level = 1)
            
            task = ((BA['asks'])[0])[0]
            
            tbid = ((BA['bids'])[0])[0]
            
            
            if content['side'] == 'buy':
                
                side = 'sell'
                size = content['size']
                price = task
                
                if price == content['price']:
                                        
                    price = new_price(tbid,task)
                    
            else:
                
                side = 'buy'
                price = tbid
                size = content['size']
                
            auth_client.place_limit_order(coin, side, price, size, post_only=(True))
            
        content = order_status_dict[OID]
        matchOrder(content)
        del order_status_dict[OID]
        
    
class MyWebsocketClient(cbpro.WebsocketClient):
        def on_open(self):
            self.url = "wss://ws-feed.pro.coinbase.com/"
            self.products = ['USDT-USD']
            self.channels = ['full','level2_50','user']   #'user','ticker_1000','full','level2_50',
            self.auth = True
            self.api_key =  '8811ae1f541f911b68394649c73d17e8'
            self.api_passphrase = 'omgvd80zrdr'
            self.api_secret = 's1L46eZRpoHdWYu6DcYROQugtgY7rrfGu7S/jUGEWMTIDUC2bgiV3c8FB1lxjVF3NHm9UnTL6U7p6A+Mptgjew=='
            self.should_print = False
            self.stime = datetime.datetime.now()
            self.is_on = True
            
            print("--op--")

    
        def on_message(self, msg):
            ProcessData(msg)
            # processes 50 kilobytes per minute
        

        def on_close(self):
            print((datetime.datetime.now() - self.stime).seconds)
            self.is_on = False
            print("--cd--")
            

try:
        
    x = MyWebsocketClient()
    x.start()
    while True:
        pass
        time.sleep(10)
    
    

    
finally:
   x.close() 





