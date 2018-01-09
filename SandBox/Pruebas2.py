import copy
from pyllist import dllist

class Event(object):
    pass

class TickEvent(Event):
    def __init__(self, instrument, time, bid, ask):
        self.type = 'TICK'
        self.instrument = instrument
        self.time = time
        self.bid = bid
        self.ask = ask

    def __str__(self):
        return "Type: %s, Instrument: %s, Time: %s, Bid: %s, Ask: %s" % (
            str(self.type), str(self.instrument),
            str(self.time), str(self.bid), str(self.ask)
        )

class SignalEvent(Event):
    def __init__(self, instrument, order_type, side, time):
        self.type = 'SIGNAL'
        self.instrument = instrument
        self.order_type = order_type
        self.side = side
        self.time = time

    def __str__(self):
        return "Type: %s, Instrument: %s, Order Type: %s, Side: %s" % (
            str(self.type), str(self.instrument),
            str(self.order_type), str(self.side)
        )

class OrderEvent(Event):
    def __init__(self, instrument, units, order_type, side):
        self.type = 'ORDER'
        self.instrument = instrument
        self.units = units
        self.order_type = order_type
        self.side = side

class Strategy(object):
    pass

class TestRandomStrategy(Strategy):
    def __init__(self, instrument, events):
        self.instrument = instrument
        self.events = events
        self.ticks = 0
        self.invested = False

    def calculate_signals(self, event):
        if event.type == 'TICK':
            self.ticks += 1
            if self.ticks % 5 == 0:
                if self.invested == False:
                    signal = SignalEvent(event.instrument, "AtMarket", "true", event.time)
                    self.events.put(signal)
                    self.invested = True
                else:
                    signal = SignalEvent(event.instrument, "AtMarket", "false", event.time)
                    self.events.put(signal)
                    self.invested = False


class MovingAverageCrossStrategy(Strategy):
    def __init__(
        self, pairs, events,
        short_window = 10, long_window = 50
    ):
        self.pairs = pairs
        self.pairs_dict = self.create_pairs_dict()
        self.events = events
        self.short_window = short_window
        self.long_window = long_window

    def create_pairs_dict(self):
        attr_dict = {
            "ticks": 0,
            "invested": False,
            "short_sma": None,
            "long_sma": None
        }
        pairs_dict = {}
        for p in self.pairs:
            pairs_dict[p] = copy.deepcopy(attr_dict)
        return pairs_dict

    def calc_rolling_sma(self, sma_m_1, window, price):
        return ((sma_m_1 * (window - 1)) + price) / window

    def calculate_signals(self, event):
        if event.type == 'TICK':
            pair = event.instrument
            price = event.bid
            pd = self.pairs_dict[pair]
            if pd["ticks"] == 0:
                pd["short_sma"] = price
                pd["long_sma"] = price
            else:
                pd["short_sma"] = self.calc_rolling_sma(
                    pd["short_sma"], self.short_window, price
                )
                pd["long_sma"] = self.calc_rolling_sma(
                    pd["long_sma"], self.long_window, price
                )
            # Only start the strategy when we have created an accurate short window
            if pd["ticks"] > self.short_window:
                if pd["short_sma"] > pd["long_sma"] and not pd["invested"]:
                    signal = SignalEvent(pair, "AtMarket", "true", event.time)
                    self.events.put(signal)
                    pd["invested"] = True
                if pd["short_sma"] < pd["long_sma"] and pd["invested"]:
                    signal = SignalEvent(pair, "AtMarket", "false", event.time)
                    self.events.put(signal)
                    pd["invested"] = False
            pd["ticks"] += 1
            #print(str(pd["short_sma"]) + " & " + str(pd["long_sma"]))


class BollingerBandStrategy(Strategy):
    '''
    * Middle Band = 20-day simple moving average (SMA)
    * Upper Band = 20-day SMA + (20-day standard deviation of price x 2)
    * Lower Band = 20-day SMA - (20-day standard deviation of price x 2)
    '''
    def __init__(
        self, pairs, events,
        sma_window = 20
    ):
        self.pairs = pairs
        self.pairs_dict = self.create_pairs_dict()
        self.events = events
        self.sma_window = sma_window
        self.list = dllist()

    def create_pairs_dict(self):
        attr_dict = {
            "ticks": 0,
            "invested_long": False,
            "invested_short": False,
            "lower_band": None,
            "middle_band": None,
            "upper_band" : None
        }
        pairs_dict = {}
        for p in self.pairs:
            pairs_dict[p] = copy.deepcopy(attr_dict)
        return pairs_dict

    def calc_rolling_sma(self, sma_m_1, window, price):
        return ((sma_m_1 * (window - 1)) + price) / window

    def calc_rolling_st(self, list, average):
        st_dev = 0
        for price in list:
            result = price - average
            result = result*result
            st_dev = st_dev + result
        st_dev = st_dev/20
        return st_dev

    def calculate_signals(self, event):
        if event.type == 'TICK':
            pair = event.instrument
            price = event.bid
            pd = self.pairs_dict[pair]
            if pd["ticks"] < self.sma_window:
                pd["middle_band"] = price
                pd["lower_band"] = price
                pd["upper_band"] = price
                self.list.appendleft(price)
            else:
                pd["middle_band"] = self.calc_rolling_sma(
                    pd["middle_band"], self.sma_window, price
                )
                self.list.popright()
                self.list.appendleft(price)
                st_dev = self.calc_rolling_st(self.list, pd["middle_band"])
                pd["upper_band"] = pd["middle_band"] + 20*st_dev
                pd["lower_band"] = pd["middle_band"] - 20*st_dev
            # Only start the strategy when we have created an accurate short window
            if pd["ticks"] > self.sma_window:
                if price >= pd["upper_band"] and not pd["invested_short"]:
                    signal = SignalEvent(pair, "AtMarket", "false", event.time)
                    self.events.put(signal)
                    pd["invested_short"] = True
                if price <= pd["lower_band"] and not pd["invested_long"]:
                    signal = SignalEvent(pair, "AtMarket", "true", event.time)
                    self.events.put(signal)
                    pd["invested_long"] = True
                if price <= pd["middle_band"] and pd["invested_short"]:
                    signal = SignalEvent(pair, "AtMarket", "true", event.time)
                    self.events.put(signal)
                    pd["invested_short"] = False
                if price >= pd["middle_band"] and pd["invested_long"]:
                    signal = SignalEvent(pair, "AtMarket", "false", event.time)
                    self.events.put(signal)
                    pd["invested_long"] = False
            #print(price)
            print(str(pd["lower_band"]) + "," + str(pd["middle_band"]) + "," + str(pd["upper_band"]))
            pd["ticks"] += 1


class DonchianChannelStrategy(Strategy):
    '''
    * Upper Band = 20-day high
    * Lower Band = 20-day low
    '''
    def __init__(
        self, pairs, events,
        sma_window = 20
    ):
        self.pairs = pairs
        self.pairs_dict = self.create_pairs_dict()
        self.events = events
        self.sma_window = sma_window
        self.list = dllist()

    def create_pairs_dict(self):
        attr_dict = {
            "ticks": 0,
            "invested_long": False,
            "invested_short": False,
            "lower_band": None,
            "upper_band" : None
        }
        pairs_dict = {}
        for p in self.pairs:
            pairs_dict[p] = copy.deepcopy(attr_dict)
        return pairs_dict

    def calc_rolling_sma(self, sma_m_1, window, price):
        return ((sma_m_1 * (window - 1)) + price) / window

    def calc_upper(self, list):
        high = 0
        for price in list:
            if price > high:
                high = price
        return high


    def calc_lower(self, list):
        low = 999999999
        for price in list:
            if price < low:
                low = price
        return low

    def calculate_signals(self, event):
        if event.type == 'TICK':
            pair = event.instrument
            price = event.bid
            pd = self.pairs_dict[pair]
            if pd["ticks"] < self.sma_window:
                pd["middle_band"] = price
                pd["lower_band"] = price
                pd["upper_band"] = price
                self.list.appendleft(price)
            else:
                pd["middle_band"] = self.calc_rolling_sma(
                    pd["middle_band"], self.sma_window, price
                )
                self.list.popright()
                self.list.appendleft(price)
                pd["upper_band"] = self.calc_upper(self.list)
                pd["lower_band"] = self.calc_lower(self.list)
            # Only start the strategy when we have created an accurate short window
            if pd["ticks"] > self.sma_window:
                if price >= pd["upper_band"] and not pd["invested_long"]:
                    signal = SignalEvent(pair, "AtMarket", "true", event.time)
                    self.events.put(signal)
                    pd["invested_long"] = True
                if price <= pd["lower_band"] and not pd["invested_short"]:
                    signal = SignalEvent(pair, "AtMarket", "false", event.time)
                    self.events.put(signal)
                    pd["invested_short"] = True
                if price < pd["upper_band"] and price > pd["lower_band"] and pd["invested_long"]:
                    signal = SignalEvent(pair, "AtMarket", "false", event.time)
                    self.events.put(signal)
                    pd["invested_long"] = False
                if price < pd["upper_band"] and price > pd["lower_band"] and pd["invested_short"]:
                    signal = SignalEvent(pair, "AtMarket", "true", event.time)
                    self.events.put(signal)
                    pd["invested_short"] = False
            #print(self.list)
            #print(price)
            print(str(pd["lower_band"])+","+str(pd["middle_band"])+","+str(pd["upper_band"]))
            pd["ticks"] += 1
