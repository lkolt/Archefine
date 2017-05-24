from tkinter import *
from TextReviwer import TextReviewer
import threading


class ContextFinder:
    def __init__(self, analyzer):
        self.analyzer = analyzer

        self.root = Tk()
        self.root.geometry('200x100+840+200')
        self.root.title("Archefine context finder")

        self.label = Label(self.root)
        self.label["text"] = "Введите слово:"
        self.label.pack()

        self.entry = Entry(self.root)
        self.entry.pack()

        self.but = Button(self.root)
        self.but["text"] = "Найти контекст"
        self.but.bind("<Button-1>", self.find_context)
        self.but.pack()

        self.root.mainloop()

    def find_context(self, event):
        word = self.entry.get()
        ans = []

        for cur_sent in self.analyzer.text.sents:
            if word in cur_sent.words:
                ans.append(cur_sent)

        fnd = TextReviewer.Reviewer()
        threading.Thread(target=fnd.start)  # WHY NOT START?
        fnd.insert_sent(ans)
