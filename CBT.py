import json
import cbpro
import base64
import time
import sys
import datetime
auth_client = None
pub_client = None



def auth():
    global auth_client,pub_client
    key = '8811ae1f541f911b68394649c73d17e8'
    secret = 's1L46eZRpoHdWYu6DcYROQugtgY7rrfGu7S/jUGEWMTIDUC2bgiV3c8FB1lxjVF3NHm9UnTL6U7p6A+Mptgjew=='
    passphrase = 'omgvd80zrdr'
    
    encoded = json.dumps(secret).encode()
    b64secret = base64.b64encode(encoded)
    auth_client = cbpro.AuthenticatedClient(key=key, b64secret=secret, passphrase=passphrase)
    pub_client = cbpro.PublicClient()


class trader():
    def __init__(self,crypto,cash):
        self.crypto =   str(crypto)
        self.cash = float(cash)
        self.portions = int((self.cash *.95)/10)
        self.trading_status = None
        self.profit = 0
        self.trades = 0
        self.price_tiers = []
        self.bid_ask = []
        self.my_order_book = {}
        self.waiting_fill = []
        self.filled_orders = {}
        self.start_time = datetime.datetime.now()
        
        self.stage_one_orders = []
        
        self.past_trades = []
        
    
    def disp_info(self,disp_type):
        if disp_type == 0:
            info_string = f'Trading {self.crypto} |'+f' Cash {self.cash}$'
            y = len(info_string)
            print('-'*y)
            print(info_string)
            print('-'*y)
            print()
            edit_params = input('Would You Like To Edit Parameters (yes/no)\n')
            if edit_params == 'yes':
                edCash = float(input('Set Cash : '))
                edCrypto = str(input('Set Crypto : '))
                self.cash = edCash
                self.crypto = edCrypto
                self.portions = int((self.cash *.95)/10)
                
            else:
                pass
            start_input = input('Type <start> To Run Trader\n')
            if start_input == 'start':
                pass
            else:
                print('Program Did Not Start')
                sys.exit()
                pass
            
            
            
        elif disp_type == 1:
            info_string = f'Trading {self.crypto} |'+f' Profit {self.profit}$'
            y = len(info_string)
            print('-'*y)
            print(info_string)
            print('-'*y)            
            TIME = datetime.datetime.now()
            print(f'Time Passed : {TIME -self.start_time}\n')
            
        elif disp_type == 2:
            print('-----Inventory-----')
            for order in self.my_order_book:
                content = self.my_order_book[order]
                print(f'Order : {content}\n')
            
        else:
            pass

  



    def set_bid_ask(self):
        order_book = pub_client.get_product_order_book(f'{self.crypto}', level = 1)
        bid = float(((order_book['bids'])[0])[0])
        ask = float(((order_book['asks'])[0])[0])
        self.bid_ask=[bid,ask]
        
    def set_containers(self):
        
        with open('CBT_CMDS.csv','r+') as file:
            file.truncate(0)
        
        print(datetime.datetime.now())

        order_book = pub_client.get_product_order_book(f'{self.crypto}', level = 1)
        bid = float(((order_book['bids'])[0])[0])
        ask = float(((order_book['asks'])[0])[0])
        self.bid_ask = [bid,ask]
       
        self.trading_status = 'Green'
        self.disp_info(0)
    
    
    def  order_processing(self):
        now_time = float((datetime.datetime.now()).timestamp())
        
        orders_to_place = []
        
        if (self.stage_one_orders[len(self.stage_one_orders)-1])['type'] == 'placed':
            pass
        else:
            for order in self.stage_one_orders:
                if order['type'] == 'stage1' and now_time > float(order['executiontime']):
                    
                    print('A Stage 1 Order Was Placed')
                    order['type'] = 'placed'
                    self.set_bid_ask()
                    bid = (self.bid_ask)[0]
                    (order['order'])['price'] = str(bid)
                    orders_to_place.append(order)
                    break
                else:
                    
                    pass
        
        deletables = []
        for order_id in self.my_order_book:
            time.sleep(.5)
            order_content = auth_client.get_order(order_id)
            status = order_content['status']
            if status == 'done':
                # add to deletables and orders to place
                matched_order = self.match_order(self.my_order_book[order_id])
                deletables.append(order_id)
                orders_to_place.append(matched_order)
                print('created matched order')
                
            else:
                print('order pending...')
        
        
        orders_waiting_fill = []
        for order in orders_to_place:
            content = order['order']
            returned_order = self.place_postlimit_order(content)
            print('placed matched order')
            order['order'] = returned_order
            order['type'] = 'waitingfill'
            print(order)
            orders_waiting_fill.append(order)
        
        
        for OID in deletables:
            del self.my_order_book[OID]
            print('deleted filled orders from my orderbook')

        
        
        self.mod_my_order_book(orders_waiting_fill)
        
        
  
        pass
        
    
    
    
    def place_postlimit_order(self,order):
        
        
        SIDE = order['side']
        SIZE = order['size']
        PRICE = order['price']
        
        placed_order = auth_client.place_limit_order(product_id =self.crypto,
                                                     side =SIDE,
                                                     price = PRICE,
                                                     size = SIZE,
                                                     post_only='True')
        
        #try order id, invalid order will give KeyError send to order sorting path error
        Order_Id =  placed_order['id']
        order['id'] = Order_Id
        
        return order
        
        
        pass
    
    
    def mod_my_order_book(self,orders):
        
        for order in orders:
            content = order['order']
            BookKey = content['id']
            del (order['order'])['id']
            self.my_order_book[BookKey]  = order['order']
            print('added order waiting to fill to my order book')

            
        pass
        
    
    def match_order(self,order):
        # {'price': '1.0003', 'size': '5', 'side': 'buy'}
        
        PRICE = order['price']
        SIZE = order['size']
        SIDE = order['side']
        
        self.set_bid_ask()
        spread = float((self.bid_ask[1]))   - float((self.bid_ask[0])) 
        if SIDE == 'buy':  # buy ---> sell
            ask = str((self.bid_ask)[1])
            if PRICE== ask:
                PRICE = float(PRICE) +spread
            else:  
                PRICE = ask
            PRICE = str(PRICE)
            
            match_order = {'type':'match','order':{'price':PRICE,'size':SIZE,'side':'sell'}}
            self.past_trades.append(order)
            return match_order
        else: # sell --> buy
            self.profit += (spread * float(SIZE))
            PRICE = str((self.bid_ask)[0])
            match_order = {'type':'match','order':{'price':PRICE,'size':SIZE,'side':'buy'}}
            self.past_trades.append(order)
            return match_order
       
        pass
    
    

    
    def unsettled_orders(self,order):
        Order_Id = order['id']
        del order['path']
        del order['id']
        self.waiting_fill[Order_Id] = order        
        pass
    
    def order_sorting(self,order):
        #types initilize, send to inventory, send to matching
        if isinstance(order, list):
            sOrder = order[0]
            if sOrder['type'] == 'stage1':
                self.stage_one_orders = order
            else:
                pass
            pass
        else:
           
            path = order['path']
            if path == 'init':
                self.initilize_order(order)
                
                
            elif path == 'inv':
                self.inventory(order)
                
                
            elif path == 'match':
                self.match_order(order)
                
                
            elif path == 'unset':
                self.unsettled_orders(order)
                
                
            else:
                self.errors(order)
        
    def cancel_all_orders(self):
        auth_client.cancel_all(self.crypto)
        pass
    
    def stage_one_trade(self,order_sizes,amount_of_orders,time_interval):
        self.set_bid_ask()
        order_list = []
        now_time = ((datetime.datetime.now()).timestamp())
        for i in range(amount_of_orders): # how many orders you want to place = range
            execution_time = str(now_time +(time_interval*(i)))  # time intervals
            order  = {'type':'stage1','order':{'price':'tbd','size':f'{order_sizes}','side':'buy'},'executiontime':execution_time,'path':'op'}
            order_list.append(order)
        
        self.order_sorting(order_list)
        
        pass
        
def read_exit_file(obj):
     with open('CBT_CMDS.csv','r+') as file:
        x = file.read()
        print(x)
        command = x.split(' ')        
        if command[0] == 'exit':
            file.truncate(0)
            return 'exit'
        elif command[0] == 'print' and command[1] == 'vars':
            
            print(vars(obj))
            file.truncate(0)
            pass
            
        elif command[0] == 'inventory':
            obj.disp_info(2)
            file.truncate(0)
            pass
            
        elif command[0] == 'cancel' and command[1] == 'all' and command[2] == 'orders':
            obj.cancel_all_orders()
            print('Cancelled and Exited')
            file.truncate(0)
            return 'exit'
            pass
        
        elif command[0] == 'add' and command[1] == 'order':
                for entry in command:
                    try:
                        SIZE = int(entry)
                    except ValueError:
                        try:
                            PRICE = float(entry)
                        except ValueError:
                            pass
                        pass
                
                # add cmd stops for improper price or improper sizes
                
                order = {'price':f'{PRICE}','size':f'{SIZE}','side':'buy'}
                placed_order = obj.place_postlimit_order(order)
                into_mod_order = [{'type':'waitingfill','order':placed_order}]
                obj.mod_my_order_book(into_mod_order)
                file.truncate(0)
                pass
            
        elif command[0] == 'remove' and command[1] == 'order':
            # remove order sell 1.0004 10
            open_orders= obj.my_order_book
            if len(open_orders) == 0:
                print('No matured orders\nStage1 orders cannot be removed')
                pass
            
            else:
                
                order_to_delete = None
                for entry in command:
                        try:
                            SIZE = int(entry)
                        except ValueError:
                            try:
                                PRICE = float(entry)
                            except ValueError:
                                pass
                            pass
                
                
                print(f'removed order --> {PRICE} {SIZE} {command[2]}')
                
                for key in open_orders:
                    order_content = open_orders[key]
                    if order_content['side'] == command[2]:
                        if order_content['price'] == str(PRICE) and order_content['size'] == str(SIZE):
                            order_id = key
                            print(order_id)
                            break
                        else:
                            pass
                    else:
                        pass
                
                auth_client.cancel_order(order_id)
                del obj.my_order_book[order_id]
            file.truncate(0)

            pass
        
            
        elif command[0] == 'past' and command[1] == 'trades':
            pt = obj.past_trades
            for trade in pt:
                print(trade)
            file.truncate(0)
            pass

        else:
                file.truncate(0)
                pass


def runMM():
    auth()
    x = trader('USDT-USD',100)
    x.set_containers()
    x.stage_one_trade(10,8,3600)
    while True:
        x.order_processing()
        x.disp_info(1)
        dec= read_exit_file(x)
        if dec == 'exit':
            break
        time.sleep(10)


runMM()


