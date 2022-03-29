import logging
import tkinter as tk

from src.graphical_UIs.entries_app import EntriesApp
from src.graphical_UIs.console_app import ConsoleUi
from src.utils.styling import *

def createScrollbarFrame(frame):

    r_frame = tk.LabelFrame(frame, width=625, bg=BG_COLOR)
    r_frame.pack(side=tk.LEFT, fill=tk.BOTH)

    # Create Canvas
    my_canvas = tk.Canvas(r_frame, width=625)
    my_canvas.pack(side=tk.LEFT, fill=tk.BOTH)

    # Add A Scrollbar to the Canvas
    my_scrollbar = tk.Scrollbar(r_frame, orient=tk.VERTICAL, command=my_canvas.yview)
    my_scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

    # Configure the Canvas
    my_canvas.configure(yscrollcommand=my_scrollbar.set)

    # Create another Frame inside the Canvas
    second_frame = tk.Frame(my_canvas, width=625)
    second_frame.pack(side=tk.RIGHT, fill=tk.BOTH)
    second_frame.bind("<Configure>", lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

    # Add that New frame to a Window in the Canvas
    my_canvas.create_window((0,0), window=second_frame, anchor="nw")

    return second_frame

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Automated Trading Protocol")
    root.geometry("1525x780")
    root.resizable(0, 0)

    # Separates the root component in two blocks

    # left side
    _left_frame = tk.LabelFrame(root, bg=BG_COLOR)
    _left_frame.pack(side=tk.LEFT)

    parent_bots_fm = tk.Frame(_left_frame, width=100, bg=BG_COLOR)
    parent_bots_fm.grid(row=1, column=0)

    list_box_frame = tk.Frame(_left_frame, width=100, bg=BG_COLOR)
    list_box_frame.grid(row=2, column=0, pady=2)

    logger = logging.getLogger(__name__)

    console_ui = ConsoleUi(list_box_frame, logger)

    # right side
    _right_frame = createScrollbarFrame(root)

    bots_entries_app = EntriesApp(parent_bots_fm, parent_bots_fm, console_ui, logger, _right_frame)

    root.mainloop()