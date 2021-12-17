import json
import logging
from tkinter import Label, CENTER
from tkinter import Entry
from tkinter import Button
from tkinter import StringVar
from tkinter import OptionMenu
from bots.buy import Buy
from bots.sell import Sell
from graphical_UIs.console_app import ConsoleUi
from graphical_UIs.strategies_threads.buy_thread import BuyThread
from graphical_UIs.strategies_threads.buysniper_thread import BuySniperThread
from graphical_UIs.strategies_threads.channelListner_thread import ChannelListner
from styling import *


class BuyEntriesApp:
    def __init__(self, master, entries_frame, console_ui: ConsoleUi, logger, **kwargs):
        self.master = master
        self.entries_master_frame = entries_frame
        self.console_ui = console_ui
        self.logger = logger

        self.buy_sniper_thread = None
        self.buy_thread = None
        self.channel_listner = None

        self.label1 = Label(self.master, text="Token to buy address: ", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
        self.label1.grid(row=1)

        self.label2 = Label(self.master, text="Quantity: ", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
        self.label2.grid(row=2)

        self.label3 = Label(self.master, text="Take profit: ", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
        self.label3.grid(row=3)

        self.label4 = Label(self.master, text="Stop loss: ", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
        self.label4.grid(row=4)

        self.label5 = Label(self.master, text="Sell Quantity: ", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
        self.label5.grid(row=5)

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

        # Dropdown menu, choose which bot to use
        self.bot_chosen = StringVar()
        self.bot_chosen.set("Snipe")
        drop = OptionMenu(self.entries_master_frame, self.bot_chosen, "Snipe",
                          "Buy", "Automated", command=self.initialise_bot_command)
        drop.grid(row=0, column=0, padx=30)

        self.start_bot_button = Button(self.master, text="Start " + self.bot_chosen.get(),
                                       command=self.start_bot_command, font=GLOBAL_FONT,
                                       bg=BG_COLOR_2, fg=FG_COLOR)
        self.start_bot_button.grid(row=7, column=1)

        self.entry3_4_and_5_destroyed = False

    def initialise_bot_command(self, choice):
        """
        This method set the entries for a specific  Bot (Sniper, Buy_&_Sell, Automated)
        It deletes entries that current bot do not need
        :return:
        """

        self.start_bot_button.config(text="Start " + self.bot_chosen.get())

        level = logging.WARNING
        self.logger.log(level, str(self.bot_chosen.get()) + " Bot selected")
        print(str(self.bot_chosen.get()) + " Bot selected")

        if str(self.bot_chosen.get()) == 'Buy':
            self.label3.destroy()
            self.entry3.destroy()

            self.label4.destroy()
            self.entry4.destroy()

            self.label5.destroy()
            self.entry5.destroy()

            self.entry3_4_and_5_destroyed = True

        elif str(self.bot_chosen.get()) == "Snipe" or str(self.bot_chosen.get()) == "Automated":
            if self.entry3_4_and_5_destroyed:
                self.label3 = Label(self.master, text="Take profit", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
                self.label3.grid(row=3)

                self.entry3 = Entry(self.master, width=67, fg=FG_COLOR,
                                    insertbackground=FG_COLOR, bg=BG_COLOR_2, highlightthickness=False)
                self.entry3.grid(row=3, column=1)

                self.label4 = Label(self.master, text="Stop loss", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
                self.label4.grid(row=4)

                self.entry4 = Entry(self.master, width=67, fg=FG_COLOR,
                                    insertbackground=FG_COLOR, bg=BG_COLOR_2, highlightthickness=False)
                self.entry4.grid(row=4, column=1)

                self.label5 = Label(self.master, text="Sell Quantity: ", bg=BG_COLOR, fg=FG_COLOR, font=BOLD_FONT)
                self.label5.grid(row=5)

                self.entry5 = Entry(self.master, width=67, fg=FG_COLOR,
                                    insertbackground=FG_COLOR, bg=BG_COLOR_2, highlightthickness=False)
                self.entry5.grid(row=5, column=1)

                self.entry3_4_and_5_destroyed = False

    def start_bot_command(self):
        wallet_address = None
        private_key = None
        gas_amount = None
        gas_price = None

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
            if not self.entry3_4_and_5_destroyed:
                take_profit = self.entry3.get()
                stop_loss = self.entry4.get()
                sell_quantity = float(self.entry5.get())
        except ValueError:
            print("Not a number")
            level = logging.ERROR
            self.logger.log(level, "Bot inputs have incorrect form !!!")
            return

        if str(self.bot_chosen.get()) == 'Snipe':
            try:
                buy_sniper = Buy(wallet_address, private_key, token_to_buy, quantity, gas_amount, gas_price, self.logger)
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
            sell_sniper = Sell(wallet_address, private_key, token_to_buy, sell_quantity, gas_amount, gas_price, self.logger)

            # buy token with a thread
            self.buy_sniper_thread = BuySniperThread(self.logger, buy_sniper, sell_sniper, take_profit, stop_loss)
            self.buy_sniper_thread.start()

        elif str(self.bot_chosen.get()) == 'Automated':
            try:
                self.channel_listner = ChannelListner(wallet_address, private_key, quantity, sell_quantity, gas_amount, gas_price
                                             , take_profit, stop_loss, self.logger)
            except Exception as e:
                # mini validation. If BuySniper inputs do not have the correct form, output errors to log
                print(e)
                level = logging.ERROR
                self.logger.log(level, "Bot inputs have incorrect form !!!")
                return

            if self.channel_listner is not None and self.channel_listner.is_alive():
                self.channel_listner.join()

            self.channel_listner.start()

        else:
            try:
                buy_bot = Buy(wallet_address, private_key, token_to_buy, quantity, gas_amount, gas_price, self.logger)
            except Exception as e:
                print(e)
                level = logging.ERROR
                self.logger.log(level, "Bot inputs have incorrect form !!!")
                return

            if self.buy_thread is not None and self.buy_thread.is_alive():
                self.buy_thread.join()
                return

            self.buy_thread = BuyThread(self.logger, buy_bot)
            self.buy_thread.start()



