import logging
import queue
from datetime import datetime
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from graphical_UIs.queueHandler import QueueHandler
from styling import *


class ConsoleUi(object):
    """Poll messages from a logging queue and display them in a scrolled text widget"""

    def __init__(self, frame, logger):
        self.frame = frame
        # Create a ScrolledText widget
        self.scrolled_text = ScrolledText(frame, state='disabled', height=35, width=140, bg=BG_COLOR)
        self.scrolled_text.grid(row=0, column=0, sticky=(N, S, W, E))
        self.scrolled_text.configure(font='TkFixedFont')

        # WARNING used as INFO
        # CRITICAL used as WARNING
        # ERROR used as ERROR
        self.scrolled_text.tag_config('INFO', foreground=FG_COLOR_2)
        self.scrolled_text.tag_config('DEBUG', foreground='orange')
        self.scrolled_text.tag_config('WARNING', foreground='green')
        self.scrolled_text.tag_config('ERROR', foreground='red')
        self.scrolled_text.tag_config('CRITICAL', foreground='orange')
        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        formatter = logging.Formatter('%(asctime)s: %(message)s')
        self.queue_handler.setFormatter(formatter)
        logger.addHandler(self.queue_handler)
        # Start polling messages from the queue
        self.frame.after(100, self.poll_log_queue)

    def display(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(END)

    def poll_log_queue(self):
        # Check every 100ms if there is a new message in the queue to display
        while True:
            try:
                record = self.log_queue.get(block=False)
            except queue.Empty:
                break
            else:
                self.display(record)
        self.frame.after(100, self.poll_log_queue)


