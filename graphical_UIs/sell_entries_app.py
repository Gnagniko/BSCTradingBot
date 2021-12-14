import json
import logging
from tkinter import *
from bots.sell import Sell
from graphical_UIs.strategies_threads.sell_thread import SellThread
from styling import *


class SellEntriesApp(object):
    def __init__(self, master, list_box_app, logger,**kwargs):
        self.master = master
        self.list_box_app = list_box_app
        self.logger = logger
        self.sell_thread = None

        label1 = Label(self.master, text="Token to sell address: ", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
        label1.grid(row=0)

        label2 = Label(self.master, text="Quantity of token in %: ", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
        label2.grid(row=1)

        # Entries
        self.entry1 = Entry(self.master, width=67, fg=FG_COLOR,
                            insertbackground=FG_COLOR, bg=BG_COLOR_2, highlightthickness=False)
        self.entry1.grid(row=0, column=1)

        self.entry2 = Entry(self.master, width=67, fg=FG_COLOR,
                            insertbackground=FG_COLOR, bg=BG_COLOR_2, highlightthickness=False)
        self.entry2.grid(row=1, column=1)

        start_bot_button = Button(self.master, text="Sell Token", command=self.start_bot_command, font=GLOBAL_FONT,
                          bg=BG_COLOR_2, fg=FG_COLOR)
        start_bot_button.grid(row=5, column=1)

    def start_bot_command(self,):
        wallet_address = None
        private_key = None
        gas_price = None
        gas_amount = None

        with open("config.json") as jsonfile:
            data = json.load(jsonfile)

            for key, value in data.items():
                if key == "Wallet Address":
                    wallet_address = value
                if key == "Private Key":
                    private_key = value
                if key == "Gasprice":
                    gas_price = value
                if key == "Gas amount":
                    gas_amount = value

        token_to_buy = self.entry1.get()
        try:
            quantity = float(self.entry2.get())
        except ValueError:
            level = logging.ERROR
            self.logger.log(level, "Bot inputs have incorrect form !!!")
            return

        sell_bot = Sell(wallet_address, private_key, token_to_buy, quantity, gas_amount, gas_price, self.logger, False)

        if self.sell_thread is not None and self.sell_thread.is_alive():
            self.sell_thread.join()
            return

        self.sell_thread = SellThread(self.logger, sell_bot)
        self.sell_thread.start()
