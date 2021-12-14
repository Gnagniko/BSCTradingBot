import logging
import threading
from bots.sell import Sell
import time


class SellThread(threading.Thread):
    def __init__(self, logger, sell: Sell):
        super().__init__()
        self.logger = logger
        self.sell = sell

    def run(self):
        """Sell if balance reached setted multiplier """
        try:
            level = logging.WARNING
            self.logger.log(level, "================================================================================")
            self.logger.log(level, "Sell Bot started... ")
            self.sell.get_balance()
            self.sell.approve_token()
            self.sell.sell_token()
        except Exception as e:
            print(e)
            level = logging.ERROR
            self.logger.log(level, str(e))

        self.logger.log(level, "Sell Bot Done")
