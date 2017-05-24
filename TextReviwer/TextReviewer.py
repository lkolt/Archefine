from tkinter import *
from tkinter import  scrolledtext as sctx


class Reviewer:
    def __init__(self):
        self.root = Tk()
        self.root.geometry('700x500')
        self.root.title("Archefine text reviewer")

        self.tx = sctx.ScrolledText(self.root, font=('times', 12), width=50, height=15, wrap=WORD)
        self.tx["state"] = "disabled"
        self.tx.pack(expand=YES, fill=BOTH)

    def start(self):
        self.root.mainloop()

    def insert(self, text):
        self.tx.insert(1.0, text)

    def insert_list(self, list):
        self.tx["state"] = "normal"
        for word in list:
            self.tx.insert(END, word + "\n")
        self.tx["state"] = "disabled"

    def insert_sent(self, sents):
        self.tx["state"] = "normal"
        for sent in sents:
            self.tx.insert(END, sent.sent)
            self.tx.insert(END, "\n")
        self.tx["state"] = "disabled"

    def insert_popularity(self, sents):
        self.tx["state"] = "normal"
        for sent in sents:
            self.tx.insert(END, "Слово \"" + str(sent[1]) + "\" встречается: " + str(sent[0]) + " раз\n")
        self.tx["state"] = "disabled"
