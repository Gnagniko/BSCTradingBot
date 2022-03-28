import logging
import queue
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from utils.queueHandler import QueueHandler
from utils.styling import *

"""
    This Class is responsible for polling
    messages from a logging queue and to display them in a scrolled text widget and errorLog file
"""
class ConsoleUi(object):
    def __init__(self, frame, logger):
        self.frame = frame
        self.logger = logger

        # Create a ScrolledText widget
        self.scrolled_text = ScrolledText(frame, state='disabled', height=30, width=100, bg=BG_COLOR)
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

        # Create a file handler
        formatter = logging.Formatter('%(asctime)s: %(message)s')
        self.file_handler = logging.FileHandler('error.log')
        self.file_handler.setFormatter(formatter)
        logger.addHandler(self.file_handler)

        # Create a logging handler using a queue
        self.log_queue = queue.Queue()
        self.queue_handler = QueueHandler(self.log_queue)
        self.queue_handler.setFormatter(formatter)
        self.logger.addHandler(self.queue_handler)

        # Start polling messages from the queue
        self.frame.after(100, self.poll_log_queue)

    def display(self, record):
        msg = self.queue_handler.format(record)
        self.scrolled_text.configure(state='normal')
        self.scrolled_text.insert(END, msg + '\n', record.levelname)
        self.scrolled_text.configure(state='disabled')
        # Autoscroll to the bottom
        self.scrolled_text.yview(END)

        # print msg to file log
        self.logger.debug(msg)

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


