# some commonly used llibraries
import time
import requests
import pandas as pd
import json
import sys
import datetime
import base64



# specifically for coinbase api, u get 3 parameters for an api key
# skip this part for now
#1 the key
#2 the secret 
#3 the passphrase


# you can create two kinds of clients

#1 public client, for basic data requests

#2 authorized client, for placing trades and accesing account information


# these clients, that can be stored as variable names are basically objects.
# the imported coinbase pro package allows us to call methods that those
# objects have built into them
# coinbase api call has a throttle limit of 5 per second,
# so use time.sleep(<seconds>) between recursive calls to slow the process

print('sleeping...')
time.sleep(5)


# lets try the public client.
# import the cbpro dependancy, create the client, install cbpro with pip
import cbpro 

pub_client = cbpro.PublicClient()

# now everytime you type pub_client and put a dot afteer it you will see a menu of 
# functions that can be called with parameters


# here is an example of a price call for a coin

coin_price = pub_client.get_product_ticker('ETH-USD')

# when you put your cursor inside the parathenese u wil lsee the parameters that 
# need to be passed in 
# all coins are passed as pairs in thr format xxx-yyy, as strings
# some functions don't need alll the parameteres to be defined


#lets print the price of Ethereum

#print(coin_price)

# you will get a dictionary return from the coinbase server

# its formaated like this 

{'trade_id': 233743815, 'price': '2814.95',
 'size': '0.03429036', 'time': '2022-03-03T20:37:59.144976Z',
 'bid': '2814.91', 'ask': '2815.26', 'volume': '178852.46653024'}

# to access values in this dictionry, we use the array indexing methedology, 
# execept instead of number we used words, which are called dictionary keys
# this dictionary is stored in the variable we assigned it to, in the call





# so lets say we want the ASK PRICE or ETH

ask_price_eth = coin_price['ask']

#print(ask_price_eth)
# notice the key passed in is a string, 
# if we don't know the value that the dictionary posses we can call

eth_price_dic_keys = coin_price.keys()

#print(dic_keys)



#now we have an array of dictionary keys that we can store and use

# or we can use a basic for loop to parse throught the dictionary keys


for key in coin_price:
    
    #print(f'{key}  :  {coin_price[key]}')
    pass



# all calls will share similar formats
# for exmaple, here is call to get all the currencies on coinbase pro

all_currencies = pub_client.get_currencies()

#print(all_currencies)
# you get a massive text output of all pairs aand some info about them that we caan store
# and use to gain alpha and make trades


# some other calls include 

#pub_client.get_products()

# get orderbook, specify level and coin

# get trading volume

# get trades

# and so on


# these are good general call for basic crypto info. 
# the real sauce comes with authorization



# to authorize
# we create the credentials on coinbaase pro API tab
# by clicking create api key then doing veyrthing it requetst us to do



# to initilize our authorized client

# we need to establish three variabls, encode them, send tthem of, and receiev  client


key =''
secret = ''
passphrase =''

#encoded = json.dumps(secret).encode()
#b64secret = base64.b64encode(encoded)
#auth_client = cbpro.AuthenticatedClient(key=key, b64secret=secret, passphrase=passphrase)

#now we can use auth_client to make more advanced calls and access secure features














