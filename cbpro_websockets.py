import coinbase
import json

from coinbase.wallet.client import Client
import coinbasepro as cbp
import time
import cbpro
import pandas as pd

#bs6644
import base64
import requests
import numpy as np
import matplotlib.pyplot as plt
import datetime

c = cbpro.PublicClient()
pr = None
ch =None


class BasicWebSock(cbpro.WebsocketClient):
    
    def on_open(self):
        self.url = "wss://ws-feed.pro.coinbase.com"
        self.products = [pr]#['USDT-USD']
        self.channels = [ch]#['level2']#,'ticker', 'matches'
        self.data = []
        self.message_count = 0
        self.buy_volume = 0
        self.sell_volume = 0
        self.start_time = datetime.datetime.now()
        
        self.min_buy_vol = []
        self.min_sell_vol = []
        
        
        
    def on_message(self,msg):
        self.message_count+=1
        print(msg)
        if self.message_count <=2:
            pass
        else:
            t = datetime.datetime.now()
            
            if ((t - self.start_time).seconds) <=60:
                
                data = msg
                side = data['side']
                size = float(data['size'])
                
                if side == 'buy':
                    self.buy_volume += size
                else:
                    self.sell_volume += size
                    
            else:
                 self.start_time =  datetime.datetime.now()
                 self.min_buy_vol.append((self.buy_volume))
                 self.min_sell_vol.append(self.sell_volume)
                 
                 self.buy_volume = 0
                 self.sell_volume = 0
                 
                 data = msg
                 side = data['side']
                 size = float(data['size'])
                
                 if side == 'buy':
                        self.buy_volume += size
                 else:
                        self.sell_volume += size
                 
                
            # watch volume grow as a sequence
            # watch volume flow through intervals
            
            
                
            '''
            
            try:
                if len(self.data) ==50:
                    self.data.pop(len(self.data)-1)
                    self.data.append(msg)
                else:
                    self.data.append(msg)
            except KeyError:
                    pass'''
                
                
    def pull_data(self):
        x = self.data
        self.data = []
        return x
        
    def on_close(self):
        print('--Closed Web Sock--')
        pass

def create_wbsc(product,channel):
    global pr
    global ch
    
    pr = product
    ch = channel
    
    some_web_socket = BasicWebSock()
    return some_web_socket


bwsc = create_wbsc('USDT-USD','matches')
bwsc.start()

time.sleep(1200)
print('\n'*3)


buyVOL = bwsc.min_buy_vol
sellVOL = bwsc.min_sell_vol


bwsc.close()

plt.plot(buyVOL)
plt.plot(sellVOL)







