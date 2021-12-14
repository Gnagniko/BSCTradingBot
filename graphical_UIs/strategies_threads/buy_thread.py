import logging
import threading
from bots.buy import Buy


class BuyThread(threading.Thread):
    def __init__(self, logger, buy_bot: Buy):
        super().__init__()
        self.logger = logger
        self.buy_bot = buy_bot

    def run(self):
        try:
            level = logging.WARNING
            self.logger.log(level, "================================================================================")
            self.logger.log(level, "Buy Bot started... ")
            self.buy_bot.get_balance()
            self.buy_bot.buy()
        except Exception as e:
            print(e)
            level = logging.ERROR
            self.logger.log(level, str(e))

        self.logger.log(level, "Buy Bot Done ")


