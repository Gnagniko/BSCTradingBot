import logging
from tkinter import *
from graphical_UIs.buy_entries_app import BuyEntriesApp
from graphical_UIs.sell_entries_app import SellEntriesApp
from graphical_UIs.console_app import ConsoleUi
from styling import *


if __name__ == '__main__':
    root = Tk()
    root.title("BSCSniper")
    root.geometry("1129x800")
    # root.resizable(0, 0)

    # Frames
    entries_frame = Frame(root, width=800, height=800, bg=BG_COLOR)
    entries_frame.grid(row=1, column=0)

    buy_entries_frame = Frame(entries_frame, width=400, bg=BG_COLOR)
    buy_entries_frame.grid(row=1, column=0, pady=10)

    sell_entries_frame = Frame(entries_frame, width=400, bg=BG_COLOR)
    sell_entries_frame.grid(row=1, column=1, pady=10,)

    list_box_frame = Frame(root, width=800, bg=BG_COLOR)
    list_box_frame.grid(row=2, column=0, pady=2)

    logger = logging.getLogger(__name__)

    list_box_app = ConsoleUi(list_box_frame, logger)
    buy_entries_app = BuyEntriesApp(buy_entries_frame,
                                    entries_frame, list_box_app, logger)
    sell_entries_app = SellEntriesApp(sell_entries_frame, list_box_app, logger)

    root.mainloop()