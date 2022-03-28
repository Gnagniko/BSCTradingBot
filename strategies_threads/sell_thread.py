import logging
import threading
from bots.sell import Sell
import time

"""
    This class creates a new sell object and sell the token with the Sell object 
"""


class SellThread(threading.Thread):
    def __init__(self, logger, wallet_address, private_key, token_to_buy, quantity, gas_amount, gas_price, ):
        super().__init__()
        self.logger = logger
        self.wallet_address = wallet_address
        self.private_key = private_key
        self.token_to_buy = token_to_buy
        self.quantity = quantity
        self.gas_amount = gas_amount
        self.gas_price = gas_price

    '''
        This method sells a token with the Sell object 
    '''
    def run(self):
        """Sell if balance reached setted multiplier """
        try:
            sell_bot = Sell(self.wallet_address, self.private_key, self.token_to_buy, self.quantity,
                                 self.gas_amount, self.gas_price, self.logger)
        except Exception as e:
            print(e)
            level = logging.ERROR
            self.logger.log(level, "Bot inputs have incorrect form !!!")
            return

        try:
            level = logging.WARNING
            self.logger.log(level, "================================================================================")
            self.logger.log(level, "Sell Bot started... ")
            sell_bot.get_bnb_balance()
            sell_bot.approve_token()
            sell_bot.sell_token()
        except Exception as e:
            print(e)
            level = logging.ERROR
            self.logger.log(level, str(e))

        self.logger.log(level, "Sell Bot Done")
