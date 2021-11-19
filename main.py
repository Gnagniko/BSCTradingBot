from tkinter import *
from buysniper import BuySniper


class EntryApp(object):
    def __init__(self, master, **kwargs):
        self.master = master

        # Frames
        self.entry_frame = Frame(self.master, width=400)
        self.entry_frame.grid(row=0, column=0,  pady=30)

        self.list_box_frame = Frame(self.master)
        self.list_box_frame.grid(row=1, column=0, pady=10, padx=20)

        # Labels
        label1 = Label(self.entry_frame, text="Wallet address: ")
        label1.grid(row=0)

        label2 = Label(self.entry_frame, text="Privatekey: ")
        label2.grid(row=1)

        label3 = Label(self.entry_frame, text="Token to buy address: ")
        label3.grid(row=2)

        label4 = Label(self.entry_frame, text="Quantity: ")  # TODO only accept  float values
        label4.grid(row=3)

        label5 = Label(self.entry_frame, text="Gasprice: ")  # TODO only accept  float values
        label5.grid(row=4)

        # Entries
        self.entry1 = Entry(self.entry_frame, width=50)
        self.entry1.grid(row=0, column=1)

        self.entry2 = Entry(self.entry_frame, width=50)
        self.entry2.grid(row=1, column=1)

        self.entry3 = Entry(self.entry_frame, width=50)
        self.entry3.grid(row=2, column=1)

        self.entry4 = Entry(self.entry_frame, width=50)
        self.entry4.grid(row=3, column=1)

        self.entry5 = Entry(self.entry_frame, width=50)
        self.entry5.grid(row=4, column=1)

        start_bot_button = Button(self.entry_frame, text="Start Bot", command=self.start_bot_command)
        start_bot_button.grid(row=5, column=1)

        self.list_box = Listbox(self.list_box_frame, width=90, height=30)
        self.list_box.grid(row=7, column=1)

    def update_listbox(self, data: str):
        self.list_box.insert(END, "=================================================================")
        self.list_box.insert(END, data)
        self.list_box.insert(END, " ")


    def start_bot_command(self,):
        wallet_address = self.entry1.get()
        private_key = self.entry2.get()
        token_to_buy = self.entry3.get()
        try:
            quantity = float(self.entry4.get())
        except ValueError:
            print("Not a number")

        gas_price = self.entry5.get()

        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.entry4.delete(0, END)
        self.entry5.delete(0, END)

        print(wallet_address)
        print(private_key)
        print(token_to_buy)
        print(quantity)
        print(gas_price)

        BuySniper(wallet_address, private_key, token_to_buy, quantity, gas_price, self)


root = Tk()
root.title("Sniper Bot")
root.geometry("800x800")
app = EntryApp(root)
root.mainloop()