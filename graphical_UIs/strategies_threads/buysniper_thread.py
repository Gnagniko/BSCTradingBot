import logging
import threading
import time

from bots.buy import Buy
from bots.sell import Sell


class BuySniperThread(threading.Thread):
    def __init__(self, logger, buy_sniper: Buy, sell_sniper: Sell, take_profit, stop_loss):
        super().__init__()
        self.logger = logger
        self.buy_sniper = buy_sniper
        self.sell_sniper = sell_sniper
        self.take_profit = take_profit
        self.stop_loss = stop_loss

        level = logging.CRITICAL
        self.logger.log(level, "================================================================================")
        self.logger.log(level, "Sniper Bot running..., it runs until transaction is successful")
        self.buy_sniper.get_balance()

    def run(self):
        # BuySniper strategy: Try transaction over and over again until it succeed
        while True:
            try:
                self.buy_sniper.buy()
                break
            except Exception as e:
                if str(e) != "execution reverted: PancakeLibrary: INSUFFICIENT_LIQUIDITY":
                    level = logging.ERROR
                    self.logger.log(level, str(e))
                    print(str(e))
                    return
                level = logging.ERROR
                self.logger.log(level, "Liquidity is not added yet")

        level = logging.CRITICAL
        self.logger.log(level, "Snipe Bot Done\n")

        # SellSniper strategy: Sell if balance reached take_profit or stop_loss
        try:
            level = logging.CRITICAL
            self.logger.log(level, "================================================================================")
            self.logger.log(level, "Sell Bot running... , token will be sell after balance reach setted multiplier")

            time.sleep(20)  # wait for buy transaction to go through

            level = logging.WARNING
            self.sell_sniper.balance = self.sell_sniper.get_balance()
            start_bl = self.sell_sniper.get_token_value_usd(self.sell_sniper.token_to_sell_address)
            self.logger.log(level, "Account balance in USD " + str(start_bl))

            if self.take_profit == "-1" and self.take_profit == "-1":
                #  no Take profit and no Stop loss set
                print("no Take profit and no Stop loss set")
                self.sell_sniper.approve_token()
                self.sell_sniper.sell_token()

            elif self.take_profit != '-1' and self.stop_loss == '-1':
                # only take_profit is activated
                print("only take_profit is activated")
                while True:
                    balance = self.sell_sniper.get_token_value_usd(self.sell_sniper.token_to_sell_address)
                    self.logger.log(level, self.sell_sniper.symbol + " balance in USD " + str(balance))
                    if balance >= start_bl * float(self.take_profit):
                        self.sell_sniper.approve_token()
                        self.sell_sniper.sell_token()
                        self.logger.log(level, str(balance - start_bl) + "USD profit made")
                        break
                    time.sleep(5)

            elif self.take_profit == '-1' and self.stop_loss != '-1':
                # only stop_loss is activated
                print("only stop_loss is activated")
                while True:
                    balance = self.sell_sniper.get_token_value_usd(self.sell_sniper.token_to_sell_address)
                    self.logger.log(level, self.sell_sniper.symbol + " balance in USD " + str(balance))
                    if balance <= start_bl - start_bl * float(self.stop_loss):
                        self.sell_sniper.approve_token()
                        self.sell_sniper.sell_token()

                        self.logger.log(level, str(balance - start_bl) + "USD profit made")
                        break
                    time.sleep(5)
            else:
                # take_profit and stop_loss activated
                print("take_profit and stop_loss activated")
                while True:
                    balance = self.sell_sniper.get_token_value_usd(self.sell_sniper.token_to_sell_address)
                    self.logger.log(level, self.sell_sniper.symbol + " balance in USD " + str(balance))
                    if balance >= start_bl * float(self.take_profit) or balance <= start_bl * float(self.stop_loss):
                        self.sell_sniper.approve_token()
                        self.sell_sniper.sell_token()
                        self.logger.log(level, str(balance - start_bl) + "USD profit made")
                        break
                    time.sleep(5)

        except Exception as e:
            print(e)
            level = logging.ERROR
            self.logger.log(level, str(e))

        time.sleep(20)
        self.sell_sniper.balance = self.sell_sniper.get_balance()
        level = logging.CRITICAL
        self.logger.log(level, "Sell Bot Done\n")

