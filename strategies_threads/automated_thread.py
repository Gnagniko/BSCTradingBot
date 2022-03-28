import logging
import threading
import time
from tkinter.scrolledtext import ScrolledText

import requests
from tkinter import *
from datetime import datetime

from utils.styling import BG_COLOR

"""
    For each time this class is created it:
        - it creates a new scroleted windows in the right frame for infos
        - then creates a Buy object to buy the token 
        - then monitors the price and if stop loss limit is reached it sells token with a Sell object 
"""


class AutomatedThread(threading.Thread):
    def __init__(self, r_frame, contract, take_profit, stop_loss, taxFee, buyFee, sellFee, id, threadLock,
                 sell_bot, buy_bot):
        super().__init__()
        self.buy_bot = buy_bot
        self.sell_bot = sell_bot
        self.stop_loss_actualizer = take_profit
        self.stop_loss = stop_loss

        self.contract = contract
        self.taxFee = float(taxFee)
        self.buyFee = float(buyFee)
        self.sell_slippage = float(sellFee)
        self.id = id
        self.r_frame = r_frame
        self.threadLock = threadLock

        # Create a ScrolledText widget (log_frame) for each thread
        self.scrolled_text = ScrolledText(self.r_frame, state='disabled', height=20, width=75, bg=BG_COLOR)
        self.scrolled_text.grid(row=id, column=0)
        self.scrolled_text.configure(font='TkFixedFont')

        self.scrolled_text.tag_config('INFO', foreground='green')
        self.scrolled_text.tag_config('WARNING', foreground='orange')
        self.scrolled_text.tag_config('ERROR', foreground='red')

    '''
       This method displays messages to the scrolled_text (log_frame) widget 
    '''
    def display(self, msg, level_name):
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(END, str(datetime.now()) + " " + msg + '\n', level_name)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(END)

    '''
        This method monitors the price and if stop loss limit is reached it sells token with a Sell object 
    '''
    def run(self):
        # Buy strategy: Try transaction over and over again until it succeed
        while True:
            try:
                self.buy_bot.buy()
                break
            except Exception as e:
                if str(e) != "execution reverted: PancakeLibrary: INSUFFICIENT_LIQUIDITY":
                    self.display("Thread: " + str(self.id) + " " + str(e), 'ERROR')
                    return
                self.display("Thread: " + str(self.id) +  " Liquidity is not added yet" , 'ERROR')

        self.display("Thread: " + str(self.id) + " Buy Bot Done", 'INFO')

        # SellSniper strategy: Sell if balance reached take_profit_lb or stop_loss
        try:
            time.sleep(20)  # wait for buy transaction to go through

            # approve token in the first place to save more time afterwards
            self.sell_bot.approve_token()

            level = logging.WARNING
            self.sell_bot.balance = self.sell_bot.get_balance()
            bl = self.sell_bot.get_token_value_usd(self.sell_bot.token_to_sell_address)
            first_bl = bl
            self.display("Thread: " + str(self.id) + "Account balance in USD " + str(bl), 'INFO')

            while True:
                balance = self.sell_bot.get_token_value_usd(self.sell_bot.token_to_sell_address)

                # if actualizer limit reached actualize the start balance
                if balance >= bl * float(self.stop_loss_actualizer):
                    bl = balance
                    self.display("Thread: " + str(self.id) + self.sell_bot.symbol + " balance in USD " + str(balance),
                                 'INFO')

                # if stop limit reached sell Token, display win made to scrolled_text and write win made to a file
                if balance <= bl * float(self.stop_loss):
                    self.sell_bot.sell_token()
                    self.display("Thread: " + str(self.id) + str(balance - bl) + "USD profit made",
                                 'INFO')

                    # print win made to file
                    self.threadLock.acquire()
                    with open("threads_output.txt", "a") as out:
                        print('INFO ' + str(datetime.now())
                              + " Contract: " + str(self.contract)
                              + " Win made: " + str(
                            bl * ((100 - float(self.sell_slippage + self.taxFee)) / 100) - first_bl) + " USD"
                              + '\n', file=out)
                        print("Tread " + str(self.id))
                    self.threadLock.release()
                    break
                time.sleep(1)

        except Exception as e:
            self.display("Thread: " + str(self.id) + str(e),
                         'ERROR')

        time.sleep(20)
        self.sell_bot.balance = self.sell_bot.get_balance()
        level = logging.CRITICAL
        self.logger.log(level, "Sell Bot Done\n")

