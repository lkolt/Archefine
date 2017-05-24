from tkinter import *
from TextReviwer import TextReviewer
from NDF import simpleAPI2
import threading


class AchetypeFinder:
    def __init__(self, analyzer):
        self.analyzer = analyzer

        self.root = Tk()

        self.entry = Entry(self.root)
        self.entry.pack()

        self.but = Button(self.root)
        self.but["text"] = "Find sentences by archetype"
        self.but.bind("<Button-1>", self.find_archetype)
        self.but.pack()

        self.label = Label(self.root)
        self.label.pack()

        self.root.mainloop()

    def find_archetype(self, event):
        sent = simpleAPI2.Sentence(0, self.entry.get(), 0, 0, self.analyzer.language)
        fnd = TextReviewer.Reviewer()
        ans = []

        for cur_sent in self.analyzer.text.sents:
            cur_intersect = cur_sent.nGrams & sent.nGrams
            cur_overlap = sum(cur_intersect.values()) / sum(sent.nGrams.values())
            if cur_overlap > 0.5:
                ans.append(cur_sent)

        threading.Thread(target=fnd.start)
        fnd.insert_sent(ans)
