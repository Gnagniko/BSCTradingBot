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
from graphical_UIs.strategies_threads.buysniper_thread import BuySniperThread


class ChannelListner(threading.Thread):
    def __init__(self, wallet_address: str, private_key: str,
                 buy_quantity: float, sell_quantity, gas_amount: int, gas_price: str,
                 take_profit: float, stop_loss: float, logger: object):
        super().__init__()

        self.wallet_address = wallet_address
        self.private_key = private_key
        self.buy_quantity = buy_quantity
        self.sell_quantity = sell_quantity
        self.gas_amount = gas_amount
        self.gas_price = gas_price
        self.logger = logger
        self.take_profit = take_profit
        self.stop_loss = stop_loss

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

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        self.client = TelegramClient(self.username, self.api_id, self.api_hash)

        with self.client:
            self.client.loop.run_until_complete(self.main())

    async def main(self):
        print("line 24")
        await self.client.start()
        print("Client Created")
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
                    msg_split = msg.split('\n')
                    contract = msg_split[3].split(' ')[9]
                    if contract not in old_contracts:
                        level = logging.CRITICAL
                        self.logger.log(level, "New contract found")

                        buy_sniper = Buy(self.wallet_address, self.private_key, contract, self.buy_quantity,
                                         self.gas_amount, self.gas_price, self.logger)

                        # sell all token after reached X's set
                        sell_sniper = Sell(self.wallet_address, self.private_key, contract, self.sell_quantity,
                                           self.gas_amount, self.gas_price, self.logger)

                        # buy token with a thread
                        self.buy_sniper_thread = BuySniperThread(self.logger, buy_sniper, sell_sniper, self.take_profit,
                                                                 self.stop_loss)
                        self.buy_sniper_thread.start()

                        print("new bot started it runs until limit(stop loss or take profit) reached")

                        old_contracts.append(contract)

                        my_break = True
                    else:
                        level = logging.CRITICAL
                        self.logger.log(level, "no new Token yet")
                else:
                    level = logging.CRITICAL
                    self.logger.log(level, "no new Token yet")
                time.sleep(5)
