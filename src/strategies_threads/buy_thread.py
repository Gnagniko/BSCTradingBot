import logging
import threading
from src.bots.buy import Buy

"""
    This class creates a new Buy object and buys the token with the Buy object 
"""


class BuyThread(threading.Thread):
    def __init__(self, logger, wallet_address, private_key, token_to_buy, quantity, gas_amount, gas_price):
        super().__init__()
        self.logger = logger
        self.wallet_address = wallet_address
        self.private_key = private_key
        self.token_to_buy = token_to_buy
        self.quantity = quantity
        self.gas_amount = gas_amount
        self.gas_price = gas_price

    '''
       This method buys a token with the Buy object 
    '''
    def run(self):
        try:
            buy_bot = Buy(self.wallet_address, self.private_key, self.token_to_buy, self.quantity, self.gas_amount,
                               self.gas_price, self.logger)
        except Exception as e:
            print(e)
            level = logging.ERROR
            self.logger.log(level, "Bot inputs have incorrect form !!!")

        try:
            level = logging.WARNING
            self.logger.log(level, "================================================================================")
            self.logger.log(level, "Buy Bot started... ")
            buy_bot.get_bnb_balance()
            buy_bot.buy()
        except Exception as e:
            print(e)
            level = logging.ERROR
            self.logger.log(level, str(e))

        self.logger.log(level, "Buy Bot Done ")


