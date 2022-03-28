import asyncio
import json
import logging
import threading
import time

from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)

from bots.buy import Buy
from bots.sell import Sell
from strategies_threads.automated_thread import AutomatedThread

"""
    This class listens to a telegram Channel.
    For a new message in the channel it checks:
        - if contract of new msg is the newest 
            - verifies seted limits (Fees) and then buys the token with a new Thread 
"""


class ChannelListner(threading.Thread):
    def __init__(self, wallet_address: str, private_key: str,
                 buy_quantity: float, sell_quantity, gas_amount: int, gas_price: str,
                 take_profit: float, stop_loss: float, max_tax_fee: float, max_liquidity_fee: float,
                 max_buy_slippage: float, max_sell_slippage: float, logger: object, r_frame,
                 threadlock):

        super().__init__()

        self.wallet_address = wallet_address
        self.private_key = private_key
        self.buy_quantity = buy_quantity
        self.sell_quantity = sell_quantity
        self.gas_amount = gas_amount
        self.gas_price = gas_price
        self.main_logger = logger
        self.take_profit = take_profit
        self.stop_loss = stop_loss
        self.max_tax_fee = max_tax_fee
        self.max_liquidity_fee = max_liquidity_fee
        self.max_buy_slippage = max_buy_slippage
        self.max_sell_slippage = max_sell_slippage
        self.r_frame = r_frame

        self.threadLock = threadlock

        with open("config.json") as jsonfile:
            data = json.load(jsonfile)

            for key, value in data.items():
                if key == "api_id":
                    self.api_id = value
                if key == "api_hash":
                    self.api_hash = value
                if key == "phone":
                    self.phone = value
                if key == "username":
                    self.username = value
                if key == "channel_url":
                    self.channel_url = value

        self.client = TelegramClient(self.username, self.api_id, self.api_hash)

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        with self.client:
            self.client.loop.run_until_complete(self.main())


    async def main(self):
        await self.client.start()
        # Ensure you're authorized
        if await self.client.is_user_authorized() == False:
            await self.client.send_code_request(self.phone)
            try:
                await self.client.sign_in(self.phone, input('Enter the code: '))
            except SessionPasswordNeededError:
                await self.client.sign_in(password=input('Password: '))

        user_input_channel = self.channel_url

        if user_input_channel.isdigit():
            entity = PeerChannel(int(user_input_channel))
        else:
            entity = user_input_channel

        my_channel = await self.client.get_entity(entity)

        offset_id = 0
        limit = 1
        old_contracts = []


        my_break = False

        counter = 1
        while not my_break:
            history = await self.client(GetHistoryRequest(
                peer=my_channel,
                offset_id=offset_id,
                offset_date=None,
                add_offset=0,
                limit=limit,
                max_id=0,
                min_id=0,
                hash=0
            ))
            if not history.messages:
                print("No history messages found")
                break

            messages = history.messages

            for message in messages:
                msg = message.message

                if msg is not None and msg[0] == "🔴":
                    """ On new alert check Token fees and Slippage then by token """

                    msg_split = msg.split('\n')

                    buy_slippage = int(msg_split[7].split(' ')[11].split('%')[0])
                    sell_slippage = int(msg_split[8].split(' ')[11].split('%')[0])

                    if buy_slippage <= int(self.max_buy_slippage) and sell_slippage <= int(self.max_sell_slippage):

                        contract = msg_split[3].split(' ')[9]
                        if contract not in old_contracts:
                            level = logging.CRITICAL
                            self.main_logger.log(level, "New contract found")

                            # sell all token after reached X's set
                            try:
                                sell_bot = Sell(self.wallet_address, self.private_key, contract, self.sell_quantity,
                                                self.gas_amount, self.gas_price, self.main_logger)
                                buy_bot = Buy(self.wallet_address, self.private_key, contract, self.sell_quantity,
                                              self.gas_amount, self.gas_price, self.main_logger)
                            except Exception as e:
                                print(e)
                                level = logging.ERROR
                                self.logger.log(level, "Bot inputs have incorrect form !!!")

                            try:
                                # get fees
                                tax_fees = sell_bot.sellTokenContract.functions._taxFee().call()
                                print("_taxFee: "+str(tax_fees))

                                if tax_fees <= self.max_tax_fee:
                                    # buy token with a thread

                                    self.automated_thread = AutomatedThread(self.r_frame, contract,
                                                                            self.take_profit,
                                                                            self.stop_loss,
                                                                            tax_fees,
                                                                            buy_slippage,
                                                                            sell_slippage,
                                                                            counter, self.threadLock,
                                                                            sell_bot, buy_bot)
                                    self.automated_thread.start()


                                else:
                                    level = logging.CRITICAL
                                    self.main_logger.log(level, "Fees to high,  Tax Fees: " + str(tax_fees))
                                    self.main_logger.log(level, "Looking for a new Token")

                            except Exception as e:
                                # buy token with a thread
                                self.automated_thread = AutomatedThread(self.r_frame, contract,
                                                                        self.take_profit,
                                                                        self.stop_loss,
                                                                        self.max_tax_fee,
                                                                        buy_slippage,
                                                                        sell_slippage,
                                                                        counter,
                                                                        self.threadLock, sell_bot,
                                                                        buy_bot)
                                self.automated_thread.start()

                            counter = counter + 1
                            old_contracts.append(contract)

                        else:
                            level = logging.CRITICAL
                            self.main_logger.log(level, "no new Token yet")
                            time.sleep(5)

                    else:
                        level = logging.CRITICAL
                        self.main_logger.log(level, "Slippage to high,  Buy Slippage: " + str(buy_slippage) +
                                        ", Sell Slippage: " + str(sell_slippage))
                        self.main_logger.log(level, "Looking for a new Token")
                        time.sleep(5)

                else:
                    level = logging.CRITICAL
                    self.main_logger.log(level, "no new Token yet")
                    time.sleep(5)

