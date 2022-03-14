import time
import cbpro
auth_client = None
pub_client = None
import datetime


def auth():
    global auth_client,pub_client
    key = '8811ae1f541f911b68394649c73d17e8'
    secret = 's1L46eZRpoHdWYu6DcYROQugtgY7rrfGu7S/jUGEWMTIDUC2bgiV3c8FB1lxjVF3NHm9UnTL6U7p6A+Mptgjew=='
    passphrase = 'omgvd80zrdr'

    auth_client = cbpro.AuthenticatedClient(key=key, b64secret=secret, passphrase=passphrase)
    pub_client = cbpro.PublicClient()



auth()

order_status_dict = {} 
tbid = None
task = None
v24h = None

def processUserNews(msg):
    global tbid,task,v24h,order_status_dict,coin
    
    news = msg
    
    
    #st = datetime.datetime.now() 
    
    if news['type']== 'subscriptions':
        
        print('subed')
        pass
    else:
        
        
        
        TYPE = news['type']
        if TYPE == 'ticker':
            pass
        else:
            print(news)
            print()

        if TYPE == 'ticker':
            # 24 hour volume, top bid, top ask, message comes after every trade
            v24h = news['volume_24h']
            tbid = news['best_bid']
            task = news['best_ask']            
            
        elif TYPE == 'received':
            
            # if its a received limit order
            if news['order_type'] == 'limit':
                    
                #get vars
                OID = news['order_id']
                size = news['size']
                side = news['side']
                price = news['price']
                product = news['product_id']
                # create entry
                order_status_dict[OID] = {'size':size,
                                          'side':side,
                                          'price':price,
                                          'type':TYPE,
                                          'product':product}
            
            # if its a received market order    
            elif news['order_type'] == 'market':
                # unsupported...
                #
                #
                pass
            
            else:
                pass
            pass
            
        elif TYPE == 'open':
            
            # gets vars to update dictionary entry for OID
            OID = news['order_id']
            
            # update entry
            (order_status_dict[OID])['type'] = TYPE
            pass

        elif TYPE == 'done' :
            
            # gets vars to update dictionary entry for OID
            OID = news['order_id']
            reason = news['reason']
            
            # try update entry
            
                
            (order_status_dict[OID])['type'] = TYPE
                
            # order may have not been on the book before it was cancelled/filled
            # this order cannot be matched by matching engine bc it does not
            # come with a price or a size



            # update reason for message | can be filled or cancelled
            (order_status_dict[OID])['reason'] = reason
            pass
        elif TYPE == 'match':
            # sometime instead of a received msg you get a match message before
            # a done message, breaking the algo.
            # creating entry
            OID = news['maker_order_id']
            
            
            if OID in order_status_dict:
                (order_status_dict[OID])['type'] =  TYPE
            else:
                order_status_dict[OID] = {
                    'size': news['size'],
                    'side': news['side'],
                    'price': news['price'],
                    'type': TYPE,
                    'product': news['product_id']
                    }
            
            pass
        elif TYPE == 'change':
            
            # not yet neccesary, figure out how to change live order sizes
            
            pass
        elif TYPE == 'activate':
            
            # also unneccesary but will be implemented in future
            pass
        
        else:
            pass
        
        #print((datetime.datetime.now()-st))
        # total processing time    ~ .005 seconds on avarage for USER info
        # processing time of  ~ .000005 seconds for ticker data





def matchingEngine():
        global order_status_dict, auth_client
        
        
        def new_price(x,y):
            #adds spread difference to top ask, without using floats to avoid rounding error
                
            x0 = int((x.split('.'))[0])
            x1 = int((x.split('.'))[1])
                
            y0 = int((y.split('.'))[0])
            y1 = int((y.split('.'))[1])
        
            d0 = y0-x0
            d1 = y1-x1
            
            new_price = f'{y0+d0}'+ '.'+f'{y1+d1}'
            return new_price
          
        def matchOrder(content):
            #content = order filled at {'side','size','price','coin'}
            # place post limit order
            coin = content['product']
            BA = pub_client.get_product_order_book(coin,level = 1)
            task = ((BA['asks'])[0])[0]
            tbid = ((BA['bids'])[0])[0]
            
            
            if content['side'] == 'buy':
                side = 'sell'
                size = content['size']
                price = task
                
                if price == content['price']:
                    
                    print('prices matched')
                    price = new_price(tbid,task)
                    
            else:
                side = 'buy'
                price = tbid
                size = content['size']
            auth_client.place_limit_order(coin, side, price, size, post_only=(True))
            
        
        dls = []
        snapshot = order_status_dict
        for entry in snapshot:
            info_row = snapshot[entry]
            info_keys = list(info_row.keys())
    
            if 'reason'in info_keys and 'type' in info_keys:
                if info_row['reason'] == 'filled' and info_row['type'] == 'done':
                    dls.append(entry) # adds entry Order ID to dls 'deletables array' for futuree deletion
                    matchOrder(info_row)
                elif info_row['reason'] == 'canceled':
                    dls.append(entry)
                    pass
                else:
                    pass
                
        for entry in dls:
            del order_status_dict[entry]
        
        
class MyWebsocketClient(cbpro.WebsocketClient):
        def on_open(self):
            self.url = "wss://ws-feed.pro.coinbase.com/"
            self.products = ['RBN-USD']
            self.channels = ['user','ticker'] # ticker is  also good and user
            self.auth = True
            self.api_key =  '8811ae1f541f911b68394649c73d17e8'
            self.api_passphrase = 'omgvd80zrdr'
            self.api_secret = 's1L46eZRpoHdWYu6DcYROQugtgY7rrfGu7S/jUGEWMTIDUC2bgiV3c8FB1lxjVF3NHm9UnTL6U7p6A+Mptgjew=='
            self.should_print = False
            self.stime = datetime.datetime.now()
            self.is_on = True
            print("Opened")

    
        def on_message(self, msg):
            processUserNews(msg)
            matchingEngine()
        

        def on_close(self):
            print((datetime.datetime.now() - self.stime).seconds)
            self.is_on = False
            print("-- Closed! --")
            

wb = MyWebsocketClient()
wb.start()
while True:
    
        if wb.is_on:
            pass
        else:
            wb.start()
   
    




