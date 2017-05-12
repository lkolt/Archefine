from tkinter import *
from TextReviwer import TextReviewer
import threading


class ContextFinder:
    def __init__(self, analyzer):
        self.analyzer = analyzer

        self.root = Tk()

        self.entry = Entry(self.root)
        self.entry.pack()

        self.but = Button(self.root)
        self.but["text"] = "Find context"
        self.but.bind("<Button-1>", self.find_context)
        self.but.pack()

        self.root.mainloop()

    def find_context(self, event):
        word = self.entry.get()
        ans = []

        for cur_sent in self.analyzer.text.sents:
            for cur_word in cur_sent.words:
                if word == cur_word:
                    ans.append(cur_sent)
                    break

        fnd = TextReviewer.Reviewer()
        threading.Thread(target=fnd.start)  # WHY NOT START?
        fnd.insert_sent(ans)
