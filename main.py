from tkinter import *
from buysniper import BuySniper
from sellsniper import SellSniper


class BuyEntriesApp(object):
    def __init__(self, master, list_box_app, **kwargs):
        self.master = master
        self.list_box_app = list_box_app

        # Labels
        label1 = Label(self.master, text="Wallet address: ")
        label1.grid(row=0)

        label2 = Label(self.master, text="Privatekey: ")
        label2.grid(row=1)

        label3 = Label(self.master, text="Token to buy address: ")
        label3.grid(row=2)

        label4 = Label(self.master, text="Quantity: ")  # TODO only accept  float values
        label4.grid(row=3)

        label5 = Label(self.master, text="Gasprice: ")  # TODO only accept  float values
        label5.grid(row=4)

        # Entries
        self.entry1 = Entry(self.master, width=40)
        self.entry1.grid(row=0, column=1)

        self.entry2 = Entry(self.master, width=40)
        self.entry2.grid(row=1, column=1)

        self.entry3 = Entry(self.master, width=40)
        self.entry3.grid(row=2, column=1)

        self.entry4 = Entry(self.master, width=40)
        self.entry4.grid(row=3, column=1)

        self.entry5 = Entry(self.master, width=40)
        self.entry5.grid(row=4, column=1)

        start_bot_button = Button(self.master, text="Start Bot", command=self.start_bot_command)
        start_bot_button.grid(row=5, column=1)

    def start_bot_command(self,):
        wallet_address = self.entry1.get()
        private_key = self.entry2.get()
        token_to_buy = self.entry3.get()
        try:
            quantity = float(self.entry4.get())
        except ValueError:
            print("Not a number")

        gas_price = self.entry5.get()

        BuySniper(wallet_address, private_key, token_to_buy, quantity, gas_price, self.list_box_app)


class ListBoxApp(object):
    def __init__(self, master, **kwargs):
        self.master = master

        self.list_box = Listbox(self.master, width=90, height=25)
        self.list_box.grid(row=7, column=1)

    def update_listbox(self, data: str):
        self.list_box.insert(END, "=================================================================")
        self.list_box.insert(END, data)


class SellEntriesApp(object):
    def __init__(self, master, list_box_app, **kwargs):
        self.master = master
        self.list_box_app = list_box_app

        # Labels
        label1 = Label(self.master, text="Wallet address: ")
        label1.grid(row=0)

        label2 = Label(self.master, text="Privatekey: ")
        label2.grid(row=1)

        label3 = Label(self.master, text="Token to sell address: ")
        label3.grid(row=2)

        label4 = Label(self.master, text="Amount of token to sell: ")  # TODO only accept  float values
        label4.grid(row=3)

        label5 = Label(self.master, text="Gasprice: ")  # TODO only accept  float values
        label5.grid(row=4)

        # Entries
        self.entry1 = Entry(self.master, width=40)
        self.entry1.grid(row=0, column=1)

        self.entry2 = Entry(self.master, width=40)
        self.entry2.grid(row=1, column=1)

        self.entry3 = Entry(self.master, width=40)
        self.entry3.grid(row=2, column=1)

        self.entry4 = Entry(self.master, width=40)
        self.entry4.grid(row=3, column=1)

        self.entry5 = Entry(self.master, width=40)
        self.entry5.grid(row=4, column=1)

        start_bot_button = Button(self.master, text="Sell Token", command=self.start_bot_command)
        start_bot_button.grid(row=5, column=1)

    def start_bot_command(self,):
        wallet_address = self.entry1.get()
        private_key = self.entry2.get()
        token_to_buy = self.entry3.get()
        try:
            quantity = float(self.entry4.get())
        except ValueError:
            print("Not a number")

        gas_price = self.entry5.get()

        SellSniper(wallet_address, private_key, token_to_buy, quantity, gas_price, self.list_box_app)




if __name__ == '__main__':
    root = Tk()
    root.title("Sniper Bot")
    root.geometry("800x800")

    # Frames
    entries_frame = Frame(root, width=400)
    entries_frame.grid(row=0, column=0)

    buy_entries_frame = Frame(entries_frame, width=200)
    buy_entries_frame.grid(row=0, column=0, pady=30)

    sell_entries_frame = Frame(entries_frame, width=200)
    sell_entries_frame.grid(row=0, column=1, pady=30)

    list_box_frame = Frame(root, width=400)
    list_box_frame.grid(row=1, column=0, pady=10, padx=20)

    list_box_app = ListBoxApp(list_box_frame)
    buy_entries_app = BuyEntriesApp(buy_entries_frame, list_box_app)
    sell_entries_app = SellEntriesApp(sell_entries_frame, list_box_app)

    root.mainloop()