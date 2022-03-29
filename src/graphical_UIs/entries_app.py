import json
import logging
import threading
import tkinter
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import StringVar
from tkinter import OptionMenu
from src.bots.buy import Buy
from src.bots.sell import Sell
from src.graphical_UIs.console_app import ConsoleUi
from src.strategies_threads.buy_thread import BuyThread
from src.strategies_threads.automated_thread import AutomatedThread
from src.strategies_threads.channelListner_thread import ChannelListner
from src.strategies_threads.sell_thread import SellThread
from src.utils.styling import *

"""
    This class is creates parameter entries for different Bots.
    Then gets inputs for a specific Bot and starts the Bot with a new Thread.
"""


class EntriesApp:
    def __init__(self, master, entries_frame, console_ui: ConsoleUi, logger, r_frame):
        self.master = master
        self.entries_master_frame = entries_frame
        self.console_ui = console_ui
        self.logger = logger
        self.r_frame = r_frame

        # Thread for each bot type
        self.buy_sniper_thread = None
        self.buy_thread = None
        self.channel_listner = None
        self.sell_thread = None

        self.token_txt = tkinter.StringVar()
        self.token_txt.set("Token to buy address: ")
        self.token_address_lb = Label(self.master, textvariable=self.token_txt, bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
        self.token_address_lb.grid(row=1)

        self.quantity_txt = tkinter.StringVar()
        self.quantity_txt.set("Quantity: ")
        self.quantity_lb = Label(self.master, textvariable=self.quantity_txt, bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
        self.quantity_lb.grid(row=2)

        self.take_profit_lb = Label(self.master, text="SL actualizer: ", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
        self.take_profit_lb.grid(row=3)

        self.stop_loss_lb = Label(self.master, text="Stop loss: ", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
        self.stop_loss_lb.grid(row=4)

        self.sell_quantity_lb = Label(self.master, text="Sell Quantity: ", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
        self.sell_quantity_lb.grid(row=5)

        self.tax_fee_lb = Label(self.master, text="max TaxFee: ", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
        self.tax_fee_lb.grid(row=6)

        self.liquidity_fee_lb = Label(self.master, text="max LiquidityFee: ", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
        self.liquidity_fee_lb.grid(row=7)

        self.buy_slippage_lb = Label(self.master, text="max Buy Slippage: ", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
        self.buy_slippage_lb.grid(row=8)

        self.sell_slippage_lb = Label(self.master, text="max sell Slippage: ", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
        self.sell_slippage_lb.grid(row=9)

        # Entries
        self.entry1 = Entry(self.master, width=67, fg=FG_COLOR,
                            insertbackground=FG_COLOR, bg=BG_COLOR_2, highlightthickness=False)
        self.entry1.grid(row=1, column=1)

        self.entry2 = Entry(self.master, width=67, fg=FG_COLOR,
                            insertbackground=FG_COLOR, bg=BG_COLOR_2, highlightthickness=False)
        self.entry2.grid(row=2, column=1)

        self.entry3 = Entry(self.master, width=67, fg=FG_COLOR,
                            insertbackground=FG_COLOR, bg=BG_COLOR_2, highlightthickness=False)
        self.entry3.grid(row=3, column=1)

        self.entry4 = Entry(self.master, width=67, fg=FG_COLOR,
                            insertbackground=FG_COLOR, bg=BG_COLOR_2, highlightthickness=False)
        self.entry4.grid(row=4, column=1)

        self.entry5 = Entry(self.master, width=67, fg=FG_COLOR,
                            insertbackground=FG_COLOR, bg=BG_COLOR_2, highlightthickness=False)
        self.entry5.grid(row=5, column=1)

        self.tax_fee_entry = Entry(self.master, width=67, fg=FG_COLOR,
                           insertbackground=FG_COLOR, bg=BG_COLOR_2, highlightthickness=False)
        self.tax_fee_entry.grid(row=6, column=1)

        self.liquidity_fee_entry = Entry(self.master, width=67, fg=FG_COLOR,
                                   insertbackground=FG_COLOR, bg=BG_COLOR_2, highlightthickness=False)
        self.liquidity_fee_entry.grid(row=7, column=1)

        self.buy_slippage_entry = Entry(self.master, width=67, fg=FG_COLOR,
                                         insertbackground=FG_COLOR, bg=BG_COLOR_2, highlightthickness=False)
        self.buy_slippage_entry.grid(row=8, column=1)

        self.sell_slippage_entry = Entry(self.master, width=67, fg=FG_COLOR,
                                        insertbackground=FG_COLOR, bg=BG_COLOR_2, highlightthickness=False)
        self.sell_slippage_entry.grid(row=9, column=1)

        # Dropdown menu, choose which bot to use
        self.bot_chosen = StringVar()
        self.bot_chosen.set("Automated")
        drop = OptionMenu(self.entries_master_frame, self.bot_chosen, "Automated", "Snipe",
                          "Buy", "Sell", command=self.initialise_bot_command)
        drop.grid(row=0, column=0, padx=30)

        self.start_bot_btn = Button(self.master, text="Start " + self.bot_chosen.get(),
                                    command=self.start_bot_command, font=GLOBAL_FONT,
                                    bg=BG_COLOR_2, fg=FG_COLOR)
        self.start_bot_btn.grid(row=10, column=1)

        self.entry3_4_and_5_destroyed = False
        self.fees_entries_destroyed = False

        self.threadLock = threading.Lock()

    '''
    This method set the entries for a specific  Bot (Sniper, Buy_&_Sell, Automated)
    It deletes entries that current bot do not need
    :return:
    '''
    def initialise_bot_command(self, choice):

        self.start_bot_btn.config(text="Start " + self.bot_chosen.get())

        level = logging.WARNING
        self.logger.log(level, str(self.bot_chosen.get()) + " Bot selected")
        print(str(self.bot_chosen.get()) + " Bot selected")

        if str(self.bot_chosen.get()) == 'Buy' or str(self.bot_chosen.get()) == 'Sell':
            self.take_profit_lb.destroy()
            self.entry3.destroy()

            self.stop_loss_lb.destroy()
            self.entry4.destroy()

            self.sell_quantity_lb.destroy()
            self.entry5.destroy()

            self.entry3_4_and_5_destroyed = True

            self.tax_fee_lb.destroy()
            self.tax_fee_entry.destroy()

            self.liquidity_fee_lb.destroy()
            self.liquidity_fee_entry.destroy()

            self.sell_slippage_lb.destroy()
            self.sell_slippage_entry.destroy()

            self.buy_slippage_lb.destroy()
            self.buy_slippage_entry.destroy()

            self.fees_entries_destroyed = True

            if str(self.bot_chosen.get()) == 'Sell':
                self.token_txt.set("Token to Sell address: ")
                self.quantity_txt.set("Quantity of token in %")

            if str(self.bot_chosen.get()) == 'Buy':
                self.token_txt.set("Token to buy address: ")
                self.quantity_txt.set("Quantity")

        elif str(self.bot_chosen.get()) == "Snipe" or str(self.bot_chosen.get()) == "Automated":

            if self.entry3_4_and_5_destroyed:
                # if entry3,4,5 are destroyed from Sell or Buy Bot
                # set them back

                self.token_txt.set("Token to buy address: ")
                self.quantity_txt.set("Quantity")

                self.take_profit_lb = Label(self.master, text="SL actualizer", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
                self.take_profit_lb.grid(row=3)

                self.entry3 = Entry(self.master, width=67, fg=FG_COLOR,
                                    insertbackground=FG_COLOR, bg=BG_COLOR_2, highlightthickness=False)
                self.entry3.grid(row=3, column=1)

                self.stop_loss_lb = Label(self.master, text="Stop Loss", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
                self.stop_loss_lb.grid(row=4)

                self.entry4 = Entry(self.master, width=67, fg=FG_COLOR,
                                    insertbackground=FG_COLOR, bg=BG_COLOR_2, highlightthickness=False)
                self.entry4.grid(row=4, column=1)

                self.sell_quantity_lb = Label(self.master, text="Sell Quantity: ", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
                self.sell_quantity_lb.grid(row=5)

                self.entry5 = Entry(self.master, width=67, fg=FG_COLOR,
                                    insertbackground=FG_COLOR, bg=BG_COLOR_2, highlightthickness=False)
                self.entry5.grid(row=5, column=1)

                self.entry3_4_and_5_destroyed = False

            """if str(self.bot_chosen.get()) == "Snipe":

                self.tax_fee_lb.destroy()
                self.tax_fee_entry.destroy()

                self.liquidity_fee_lb.destroy()
                self.liquidity_fee_entry.destroy()

                self.sell_slippage_lb.destroy()
                self.sell_slippage_entry.destroy()

                self.buy_slippage_lb.destroy()
                self.buy_slippage_entry.destroy()

                self.fees_entries_destroyed = True 
            """

            if str(self.bot_chosen.get()) == "Automated" and self.fees_entries_destroyed:
                # Automated need also to set tax_fee and liquidity_fee entries back

                self.tax_fee_lb = Label(self.master, text="max TaxFee: ", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
                self.tax_fee_lb.grid(row=6)

                self.liquidity_fee_lb = Label(self.master, text="max LiquidityFee: ", bg=BG_COLOR, fg=FG_COLOR,
                                              font=BOLD_FONT)
                self.liquidity_fee_lb.grid(row=7)

                self.buy_slippage_lb = Label(self.master, text="max Buy Slippage: ", bg=BG_COLOR, fg=FG_COLOR,
                                             font=BOLD_FONT)
                self.buy_slippage_lb.grid(row=8)

                self.sell_slippage_lb = Label(self.master, text="max sell Slippage: ", bg=BG_COLOR, fg=FG_COLOR,
                                              font=BOLD_FONT)
                self.sell_slippage_lb.grid(row=9)

                self.tax_fee_entry = Entry(self.master, width=67, fg=FG_COLOR,
                                           insertbackground=FG_COLOR, bg=BG_COLOR_2, highlightthickness=False)
                self.tax_fee_entry.grid(row=6, column=1)

                self.liquidity_fee_entry = Entry(self.master, width=67, fg=FG_COLOR,
                                                 insertbackground=FG_COLOR, bg=BG_COLOR_2, highlightthickness=False)
                self.liquidity_fee_entry.grid(row=7, column=1)

                self.buy_slippage_entry = Entry(self.master, width=67, fg=FG_COLOR,
                                                insertbackground=FG_COLOR, bg=BG_COLOR_2, highlightthickness=False)
                self.buy_slippage_entry.grid(row=8, column=1)

                self.sell_slippage_entry = Entry(self.master, width=67, fg=FG_COLOR,
                                                 insertbackground=FG_COLOR, bg=BG_COLOR_2, highlightthickness=False)
                self.sell_slippage_entry.grid(row=9, column=1)

                self.fees_entries_destroyed = False

    '''
    This method creates the Object for a selected Bot and run it in an extern Thread
    '''
    def start_bot_command(self):
        wallet_address = None
        private_key = None
        gas_amount = None
        gas_price = None

        with open("src/config.json") as jsonfile:
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
            if not self.entry3_4_and_5_destroyed:
                take_profit = self.entry3.get()
                stop_loss = self.entry4.get()
                sell_quantity = float(self.entry5.get())

            if not self.fees_entries_destroyed:
                max_tax_fee = self.tax_fee_entry.get()
                max_liquidity_fee = self.liquidity_fee_entry.get()
                max_buy_slippage = self.buy_slippage_entry.get()
                max_sell_slippage = self.sell_slippage_entry.get()

        except ValueError:
            print("Not a number")
            level = logging.ERROR
            self.logger.log(level, "Bot inputs have incorrect form !!!")
            return

        # depending one which bot is selected start bots (--> run bot functions)
        if str(self.bot_chosen.get()) == 'Snipe':
            try:
                buy_bot = Buy(wallet_address, private_key, token_to_buy, quantity, gas_amount, gas_price, self.logger)
            except Exception as e:
                # mini validation. If BuySniper inputs do not have the correct form, output errors to log
                print(e)
                level = logging.ERROR
                self.logger.log(level, "Bot inputs have incorrect form !!!")
                return

            if self.buy_sniper_thread is not None and self.buy_sniper_thread.is_alive():
                self.buy_sniper_thread.join()
                return

            # sell all token after reached X's set
            sell_bot = Sell(wallet_address, private_key, token_to_buy, sell_quantity, gas_amount, gas_price, self.logger)

            # buy token with a thread
            self.buy_sniper_thread = AutomatedThread(self.r_frame, token_to_buy,
                                                                        take_profit,
                                                                        stop_loss,
                                                                        max_tax_fee,
                                                                        max_buy_slippage,
                                                                        max_sell_slippage,
                                                                        0,
                                                                        self.threadLock, sell_bot,
                                                                        buy_bot)
            self.buy_sniper_thread.start()

        elif str(self.bot_chosen.get()) == 'Automated':
            try:
                self.channel_listner = ChannelListner(wallet_address, private_key, quantity, sell_quantity, gas_amount,
                                                      gas_price, take_profit, stop_loss, max_tax_fee, max_liquidity_fee,
                                                      max_buy_slippage, max_sell_slippage, self.logger, self.r_frame,
                                                      self.threadLock)
            except Exception as e:
                # mini validation. If BuySniper inputs do not have the correct form, output errors to log
                print(e)
                level = logging.ERROR
                self.logger.log(level, "Bot inputs have incorrect form !!!")
                return

            if self.channel_listner is not None and self.channel_listner.is_alive():
                self.channel_listner.join()

            self.channel_listner.start()

        elif str(self.bot_chosen.get()) == 'Sell':

            # if thread already exists kill it before creating a new one
            if self.sell_thread is not None and self.sell_thread.is_alive():
                self.sell_thread.join()
                return

            self.sell_thread = SellThread(self.logger, wallet_address, private_key, token_to_buy, quantity,
                                          gas_amount, gas_price)
            self.sell_thread.start()

        else:

            # if thread already exists kill it before creating a new one
            if self.buy_thread is not None and self.buy_thread.is_alive():
                self.buy_thread.join()
                return

            self.buy_thread = BuyThread(self.logger, wallet_address, private_key, token_to_buy, quantity, gas_amount,
                                        gas_price)
            self.buy_thread.start()






