import statistics
import time
import cbpro
import datetime

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

order_status_dict = {}
order_book = {}
orders_at_price = {}
bid_ask_order_book = {}
void_orders_at_price = {}

order_sizes = []
median_order_size = 0
mean_order_size = 0

tbid = None
task = None
v24h = None

dynamic_bid_index = 0


def get_bid_ask():

    global dynamic_bid_index, bid_ask_order_book
    book = bid_ask_order_book
    keys = sorted(book)

    bid = 0
    ask = 0

    for price in keys[dynamic_bid_index:]:
        if book[price] == 'sell':
            dynamic_bid_index = (keys.index(price))-20
            ask = price
            break
        else:
            bid = price

    # 0.001 - .0007s
    return bid, ask


def position_manager():

    pass


def update_liquidity(size, price, order_id=None):

    global order_status_dict, orders_at_price

    try:
        orders = orders_at_price[float(price)]
    except KeyError:
        orders_at_price[float(price)] = set()
        orders = orders_at_price[float(price)]

    if len(orders) == 0:
        pass
    else:
        if order_id is None:

            for order_id in orders:
                order_status_dict[order_id]['rliquidity'] -= float(size)
        else:

            for open_order in void_orders_at_price[float(price)]:
                if order_id in void_orders_at_price[float(price)][open_order]:
                    pass
                else:
                    for open_order_id in orders:
                        order_status_dict[open_order_id]['rliquidity'] -= float(size)
            pass
        pass


def update_order_flow(size):
    global median_order_size, order_sizes, mean_order_size
    order_sizes.append(float(size))
    median_order_size = statistics.median(order_sizes)
    mean_order_size = statistics.mean(order_sizes)


def process_data(msg):
    news = msg

    if news['type'] == 'subscriptions':

        print('--sd--')
        pass
    else:

        msg_type = news['type']

        if msg_type == 'snapshot':

            asks = news['asks']
            bids = news['bids']

            for ask in asks:
                order_book[float(ask[0])] = ask[1]
                orders_at_price[float(ask[0])] = set()
                bid_ask_order_book[float(ask[0])] = 'sell'

            for bid in bids:
                order_book[float(bid[0])] = bid[1]
                orders_at_price[float(bid[0])] = set()
                bid_ask_order_book[float(bid[0])] = 'buy'

        elif 'user_id' in news:

            if news['user_id'] == '60243cfeb0ccd414b6290f32':

                if msg_type == 'received':

                    if news['order_type'] == 'limit':

                        identity = news['order_id']
                        size = news['size']
                        side = news['side']
                        price = news['price']
                        product = news['product_id']

                        try:

                            initial_liquidity = order_book[float(price)]

                            orders_at_price[float(price)].add(identity)

                            remaining_liquidity = float(initial_liquidity)

                            if float(price) in void_orders_at_price:

                                (void_orders_at_price[float(price)])[identity] = []

                            else:

                                void_orders_at_price[float(price)] = {identity: []}

                        except KeyError:

                            initial_liquidity = '0'

                            order_book[float(price)] = initial_liquidity

                            remaining_liquidity = float(initial_liquidity)

                            if float(price) in void_orders_at_price:

                                (void_orders_at_price[float(price)])[identity] = []

                            else:

                                void_orders_at_price[float(price)] = {identity: []}

                        order_status_dict[identity] = {'size': size,
                                                          'side': side,
                                                          'price': price,
                                                          'type': msg_type,
                                                          'product': product,
                                                          'iliquidity': initial_liquidity,
                                                          'rliquidity': remaining_liquidity}

                    elif news['order_type'] == 'market':
                        pass

                    else:
                        pass
                    pass

                elif msg_type == 'open':

                    identity = news['order_id']

                    (order_status_dict[identity])['type'] = msg_type

                    pass

                elif msg_type == 'done':

                    identity = news['order_id']

                    reason = news['reason']

                    try:

                        (order_status_dict[identity])['type'] = msg_type

                        (order_status_dict[identity])['reason'] = reason

                        trading_engine(identity)

                    except KeyError:
                        # Order canceled that was not on logs when program started
                        pass

                elif msg_type == 'match':

                    identity = news['maker_order_id']

                    if identity in order_status_dict:

                        (order_status_dict[identity])['type'] = msg_type

                    else:

                        OID = news['order_id']
                        size = news['size']
                        side = news['side']
                        price = news['price']
                        product = news['product_id']

                        initial_liquidity = order_book[float(price)]

                        orders_at_price[float(price)].add(OID)

                        remaining_liquidity = float(initial_liquidity)

                        void_orders_at_price[float(price)] = []

                        order_status_dict[OID] = {'size': size,
                                                  'side': side,
                                                  'price': price,
                                                  'type': msg_type,
                                                  'product': product,
                                                  'iliquidity': initial_liquidity,
                                                  'rliquidity': remaining_liquidity}

                    pass
                else:
                    pass

        elif msg_type == 'received':

            if news['order_type'] == 'limit':

                price = news['price']
                order_id = news['order_id']

                if float(price) in void_orders_at_price:

                    for open_order in void_orders_at_price[float(price)]:
                        void_orders_at_price[float(price)][open_order].append(order_id)

                else:

                    pass

        elif msg_type == 'open':

            pass

        elif msg_type == 'done':

            if 'reason' in news and news['reason'] == 'canceled':
                price = news['price']
                size = news['remaining_size']
                order_id = news['order_id']

                update_liquidity(size, price, order_id)

            else:
                pass

        elif msg_type == 'match':

            price = news['price']
            size = news['size']

            update_liquidity(size, price)
            update_order_flow(size)

        elif msg_type == 'change':

            pass

        elif msg_type == 'activate':

            pass

        elif msg_type == 'l2update':

            changes = news['changes']
            for change in changes:
                order_book[float(change[1])] = change[2]
                bid_ask_order_book[float(change[1])] = change[0]

                if float(change[1]) in orders_at_price:
                    pass
                else:
                    orders_at_price[float(change[1])] = set()
        else:

            pass


def trading_engine(order_id):

    order_data = order_status_dict[order_id]
    original_price = order_data['price']

    if order_data['reason'] == 'filled':

        size = order_data['size']
        side = order_data['side']
        coin = order_data['product']

        bid, ask = get_bid_ask()

        new_side = 'sell' if side == 'buy' else 'buy'

        price = bid if new_side == 'buy' else ask

        auth_client.place_limit_order(coin, new_side, price, size, post_only=(True))

    else:
        pass

    del order_status_dict[order_id]
    orders_at_price[float(original_price)].remove(order_id)
    del void_orders_at_price[float(original_price)][order_id]


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
        process_data(msg)
        pass

    def on_close(self):
        print((datetime.datetime.now() - self.stime).seconds)
        self.is_on = False
        print("--cd--")


try:

    x = MyWebsocketClient()
    x.start()

    while True:
        time.sleep(1)
        pass

finally:

    x.close()






