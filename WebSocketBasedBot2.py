import requests
import json
import base64
import time
import hmac
import hashlib
from requests.auth import AuthBase
import cbpro
import numpy as np
auth_client = None
pub_client = None
import datetime
import sys

# DON'T RUN THIS CODE! ; IT NEEDS SPECIAL MODIFICATIONS


# authentication function, just sends passwords to coinbase to recieve back an 
# authorized object that we can send commands too.
def auth():
    global auth_client,pub_client
    # enter credentials
    key = ''
    secret = ''
    passphrase = ''

    auth_client = cbpro.AuthenticatedClient(key=key, b64secret=secret, passphrase=passphrase)
    pub_client = cbpro.PublicClient()


# below is just gibberish and things i been testing; ignore.
#------------------------------------------------------------------------------
#order = auth_client.place_limit_order('USDT-USD', 'buy', '1.0001', '10',post_only=(True))

'''

key = '8811ae1f541f911b68394649c73d17e8'
sec = 's1L46eZRpoHdWYu6DcYROQugtgY7rrfGu7S/jUGEWMTIDUC2bgiV3c8FB1lxjVF3NHm9UnTL6U7p6A+Mptgjew=='
passs = 'omgvd80zrdr'

'''

#x=auth_client.get_orders('USDT-USD','done')


#wb = cbpro.WebsocketClient(products=('USDT-USD'),channels = ['user'],auth=(True),api_key=key,api_secret=sec, api_passphrase=passs)
#-------------------------------------------------------------------------------------------

# here I start the program by calling the auth function to establish the public and authenticated client
auth()

order_status_dict = {} # here we will keep a collection of orders and their life cycle status
tbid = None
task = None
v24h = None


# This funciton is called in Websocket Class, see way below.
def processUserNews(msg):
    global tbid,task,v24h,order_status_dict
    # global variable top bid, top ask, order status dictionaries
    
    news = msg
    # message coming from websocket client, from on_message(self, msg) function
    # you can choose to print news to see what messages are coming in, in real time, its better not to
    # print(news)
    
    
    
    st = datetime.datetime.now() # have starting time so we can compute processing time
    
    
    
    # the first message is a subscription confirmation message
    if news['type']== 'subscriptions':
        # If message type is subscription we don't want to process anything yet, its just some basic connectivity info
        # so we just print that we conncted to the server and now get messages
        print('subd')
        pass
    else:
        
        
        
        # For visualization purposes
        # we don't want ticker (price) updates cluttering our console
        # so we don't print if its a ticker message
        TYPE = news['type']
        if TYPE == 'ticker':
            pass
        else:
            print(news)
            print()

        # ---- sorting stage ------ # 
        
        # every time an order is generated/placed, when we are subscribed to a websocket
        # channel, specifically the user channel, (the parameter in the websocket class)-->
        # The user channel pings us with updates about the status of our orders.
        # statuses and parameters vary, but each json package holds some info we want.
        
        # Each message has a TYPE, its the purpose of that message.
        # so when the message comes in, we want to know its 'type'
        # so we pull the type and run it through a series of conditions
        # to check ' the type', and if its certain type, we will pull and update 
        # info that we need.
        
        if TYPE == 'ticker':
            # 24 hour volume, top bid, top ask, message comes after every real time trade placed on the commodity
            v24h = news['volume_24h']
            tbid = news['best_bid']
            task = news['best_ask']            
            
        elif TYPE == 'received':    # meaning: an order on our account was placed, so we get a message with type 'received'
            
            # if its a received limit order, which it will be 100% of the time unless new specified other
            if news['order_type'] == 'limit':
                    
                #get vars from json data
                OID = news['order_id']
                size = news['size']
                side = news['side']
                price = news['price']
                
                # At the start of the program, osd is blank, so we initilize an entry in the dictionary, 
                # with the key being the order id, and the guts are everything else
                order_status_dict[OID] = {'size':size,'side':side,'price':price,'type':TYPE}
            
            # if its a received market order    
            elif news['order_type'] == 'market':
                # unsupported...
                #
                #
                pass
            
            else:
                pass
            pass
            
        elif TYPE == 'open': # generally, after a 'received' message comes in, it is automatically followed by an 'open' type messge
            
            # gets vars to update dictionary entry for OID
            OID = news['order_id']
            
            # update entry
            # all we are doing here is updating the type of this order to 'open'. Because it was 'received' before.
            (order_status_dict[OID])['type'] = TYPE
            pass

        elif TYPE == 'done' :
            
            # gets vars to update dictionary entry for OID
            OID = news['order_id']
            reason = news['reason']         # when an message comes with type 'done' it will come with a filed called 'reason'
            
            # try update entry
            # error catching system needs to be put here, becuse this is were the program breaks most often
            
                
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
            order_status_dict[OID] = {
                'size': news['size'],
                'side': news['side'],
                'price': news['price'],
                'type': TYPE,
                
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
        
        print((datetime.datetime.now()-st))
        # total processing time    ~ .005 seconds on avarage for USER info
        # processing time of  ~ .000005 seconds for ticker data

def matchingEngine():
        global task,tbid, order_status_dict, auth_client
        # matching engine matches orders
        
        
        # here is an internalized function that actually places the order
        def matchOrder(content):
            #content = order filled at {'side','size','price'}
            # place post limit order
            if content['side'] == 'buy':
                side = 'sell'
                price = task
                size = content['size']

            else:
                side = 'buy'
                price = tbid
                size = content['size']
            auth_client.place_limit_order('USDT-USD', side, price, size, post_only=(True))
            
            
        # this is where the function begins
        dls = []
        snapshot = order_status_dict        # I set snapshott equal to order_status_dict because I don't want to accidentaly modify it.
        for entry in snapshot:              # So I am parsing an 'image' of the order dictionary rather than the real dictionary
            info_row = snapshot[entry]      # 'entry' which is the iterator, is going to be the keys in the dictionary, which are the order IDS
            info_keys = list(info_row.keys())       # here I pull all the keys of an entry 
                                                    
                    # info_row is the content held in the order id 
                    # every entry in order_status_dict looks like this {'1237467dh8b623gdg1' : {'price':1.23,  'side':'buy',  'size':3 .... other info}}
                    
                    # we have an array dls[] that will hold the IDs of orders that have been executed and we no longer need to track
                    # we append them into the array. After iterating through the entire order_status_dict, we delete them from order_status_dict.
                    # this is because we cannot dynamically change the size of the dictionary while itterating it (order_status_dict).
    
            if 'reason'in info_keys and 'type' in info_keys:                            # here I check if the keys TYPE and REASON exist in the info row
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
            self.products = ['USDT-USD']
            self.channels = ['user','ticker'] # ticker is  also good and user
            self.auth = True
            self.api_key =  '8811ae1f541f911b68394649c73d17e8'
            self.api_passphrase = 'omgvd80zrdr'
            self.api_secret = 's1L46eZRpoHdWYu6DcYROQugtgY7rrfGu7S/jUGEWMTIDUC2bgiV3c8FB1lxjVF3NHm9UnTL6U7p6A+Mptgjew=='
            self.should_print = False
            self.news = []
            self.stime = datetime.datetime.now()
            
            self.message_count = 0
            print("Opened")


        def on_message(self, msg):
            
            processUserNews(msg)
            
            
            #matchingEngine()
                     
            #self.news.append(msg)
            pass

        def getnews(self):
            x = self.news
            self.news = []
            return x
        

        def on_close(self):
            print((datetime.datetime.now() - self.stime).seconds)
            print("-- Closed! --")






wb = MyWebsocketClient()

wb.start()
#stime=  datetime.datetime.now()

# use every minute to stay connected 
#wb._connect()
# tests feature 
#stime  = datetime.datetime.now()


while True:
    
   ''' if len(wb.news)>0:
        news = wb.getnews()
        processUserNews(news)
        matchingEngine()'''
   pass





#order = auth_client.place_limit_order('DAI-USD', 'buy', '1.0000', '10',post_only=(True))
    
'''ctime = datetime.datetime.now()
    dtime = ctime-stime
    if dtime.seconds >= 60:
        stime=  datetime.datetime.now()
        wb._connect()'''

'''
x = pub_client.get_currencies()

top_spd = []

for entry in x:
    cr = entry['id']
    cr = f'{cr}-USD'
    time.sleep(1)
    BA = pub_client.get_product_order_book(cr,level = 1)
    try:
        tbid = float(((BA['bids'])[0])[0])
        task = float(((BA['asks'])[0])[0])
        spread = task - tbid
        
        spread_per_dollar = spread/task
        top_spd.append([spread_per_dollar,cr])
        print(f'\n{cr}\nSpread : {spread}\nPrice {task}\nSpread per dollar : {spread_per_dollar}')
        
        
        
    except Exception:
        pass
    

'''


