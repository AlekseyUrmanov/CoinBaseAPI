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

def auth():
    global auth_client,pub_client
    key = '8811ae1f541f911b68394649c73d17e8'
    secret = 's1L46eZRpoHdWYu6DcYROQugtgY7rrfGu7S/jUGEWMTIDUC2bgiV3c8FB1lxjVF3NHm9UnTL6U7p6A+Mptgjew=='
    passphrase = 'omgvd80zrdr'

    auth_client = cbpro.AuthenticatedClient(key=key, b64secret=secret, passphrase=passphrase)
    pub_client = cbpro.PublicClient()



#order = auth_client.place_limit_order('USDT-USD', 'buy', '1.0001', '10',post_only=(True))

'''

key = '8811ae1f541f911b68394649c73d17e8'
sec = 's1L46eZRpoHdWYu6DcYROQugtgY7rrfGu7S/jUGEWMTIDUC2bgiV3c8FB1lxjVF3NHm9UnTL6U7p6A+Mptgjew=='
passs = 'omgvd80zrdr'

'''

#x=auth_client.get_orders('USDT-USD','done')


#wb = cbpro.WebsocketClient(products=('USDT-USD'),channels = ['user'],auth=(True),api_key=key,api_secret=sec, api_passphrase=passs)




class MyWebsocketClient(cbpro.WebsocketClient):
        def on_open(self):
            self.url = "wss://ws-feed.pro.coinbase.com/"
            self.products = ['ADA-USD']
            self.channels = ['user','ticker'] # ticker is  also good
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
            
            if msg['type'] == 'ticker':
                pass
            
            else:
                pass            
            
            
            self.news.append(msg)
            

        def getnews(self):
            x = self.news
            self.news = []
            return x
        

        def on_close(self):
            print((datetime.datetime.now() - self.stime).seconds)
            print("-- Closed! --")


auth()

order_status_dict = {}
tbid = None
task = None
v24h = None

def processUserNews(msg):
    global tbid,task,v24h,order_status_dict
    news = msg[0]
    if news['type']== 'subscriptions':
        print('subed')
        pass
    else:
        # the type of message
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
                
                # create entry
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
        
        

def matchingEngine():
        global task,tbid, order_status_dict, auth_client
        
        
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
            auth_client.place_limit_order('ADA-USD', side, price, size, post_only=(True))
            
            
        
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
        
        




wb = MyWebsocketClient()

wb.start()
#stime=  datetime.datetime.now()

# use every minute to stay connected 
#wb._connect()
# tests feature 
#stime  = datetime.datetime.now()

while True:
    
    if len(wb.news)>0:
        news = wb.getnews()
        processUserNews(news)
        matchingEngine()









#order = auth_client.place_limit_order('DAI-USD', 'buy', '1.0000', '10',post_only=(True))
    
'''ctime = datetime.datetime.now()
    dtime = ctime-stime
    if dtime.seconds >= 60:
        stime=  datetime.datetime.now()
        wb._connect()'''



