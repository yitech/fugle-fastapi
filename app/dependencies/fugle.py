import schedule
import time
from threading import Thread
from configparser import ConfigParser
from fugle_trade.sdk import SDK
from fugle_trade.order import OrderObject
from app.models.fugle import OrderResult, NotifyAck
from app.core.config import settings
import logging

FUGLE_TRADE_CONFIG = settings.fugle_trade_config

class TraderSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TraderSingleton, cls).__new__(cls)
            cls._instance._initialize()
            cls._instance._start_scheduler()
        return cls._instance

    def _initialize(self):
        self.config = ConfigParser()
        self.config.read(FUGLE_TRADE_CONFIG)
        self.trader = SDK(self.config)
        self.trader.login()

        self.orders: dict[str, OrderResult] = self._get_order_results()
        self._connect_websocket() 

    def _login(self):
        print("Logging in again...")
        self.trader.login()

    def _start_scheduler(self):
        # Schedule the login to happen every day at midnight
        schedule.every().day.at("00:00").do(self._login)

        # Run the scheduler in a separate thread
        scheduler_thread = Thread(target=self._run_scheduler, daemon=True)
        scheduler_thread.start()
        

    def _run_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def get_trader(self):
        return self
    
    def place_order(self, order: OrderObject):
        return self.trader.place_order(order)
            
    
    def cancel_order(self, ord_no: str):
        if ord_no not in self.orders:
            raise ValueError(f"Order number {ord_no} not found")
        order_result = self.orders[ord_no]
        logging.info(f"Cancelling order {order_result}")
        res = self.trader.cancel_order(order_result.model_dump())
        logging.info(f"Order {res} cancelled")
    
    def get_order_results(self):
        return list(self.orders.values())
    
    def _get_order_results(self):
        try:
            order_results = self.trader.get_order_results()
        except ValueError as e:
            raise ValueError(str(e))
        except Exception as e:
            raise Exception(str(e))
        
        res : dict[str, OrderResult] = {}
        for result in filter(lambda res: res["celable"] == "1", order_results):
            order_result = OrderResult(**result)
            if order_result.ord_id == '':
                print("Error: Could not find order number")
            else:
                res[order_result.ord_id] = order_result
        return res
    
    def _connect_websocket(self):
        @self.trader.on("order")
        def on_order(data: dict):
            ack = NotifyAck(**data)
            logging.info(f"On NotifyAck: {ack}")
            self.on_order(ack)

        @self.trader.on("dealt")
        def on_dealt(data):
            self.on_dealt(data)

        @self.trader.on("error")
        def on_error(data):
            self.on_error(data)

        websocket_thread = Thread(target=self.trader.connect_websocket, daemon=True)
        websocket_thread.start()

    def on_order(self, ack: NotifyAck):
        try:
            if ack.cel_type == '2':  # Cannot cancel, remove from orders
                del self.orders[ack.ord_id]
            elif ack.cel_type == '1':
                ack_update = ack.model_dump()
                ack_update.update({'org_qty_share': int(ack.org_qty * 1000),
                                   'mat_qty_share': int(ack.mat_qty * 1000),
                                   'cel_qty_share': int(ack.cel_qty * 1000)})
                if ack.ord_id in self.orders:
                    self.orders[ack.ord_id].update(ack_update)
                else:
                    ack_update.update({'avg_price': 0.0,
                                       'celable': '1',
                                       'ord_date': ack.work_date,
                                       'ord_time': ack.ret_time})
                    self.orders[ack.ord_id] = OrderResult(**ack_update)
            else:
                print(f"Cannot handle ack type {ack.cel_type}")
                raise ValueError(f"Cannot handle ack type {ack.cel_type}")
        except Exception as e:
            print(f"An exception occurred: {e}")

    def on_dealt(self, data):
        print(data)

    def on_error(self, data):
        print(data)
    
    

# Function to get the trader instance
def get_trader():
    return TraderSingleton().get_trader()

