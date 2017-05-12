from tkinter import *


class Reviewer:
    def __init__(self):
        self.root = Tk()

        self.tx = Text(self.root, font=('times', 12), width=50, height=15, wrap=WORD)
        self.tx.pack(expand=YES, fill=BOTH)

    def start(self):
        self.root.mainloop()

    def insert(self, text):
        self.tx.insert(1.0, text)

    def insert_list(self, list):
        for word in list:
            self.tx.insert(END, word + "\n")

    def insert_sent(self, sents):
        for sent in sents:
            self.tx.insert(END, sent.sent)
            self.tx.insert(END, "\n")
