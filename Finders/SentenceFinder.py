from tkinter import *
from TextReviwer import TextReviewer
from NDF import simpleAPI2
import threading


class ExactDuplicateSentenceFinder:
    def __init__(self, analyzer):
        self.analyzer = analyzer

        self.root = Tk()

        self.entry = Entry(self.root)
        self.entry.pack()

        self.but = Button(self.root)
        self.but["text"] = "Find sentence"
        self.but.bind("<Button-1>", self.find_sentence)
        self.but.pack()

        self.label = Label(self.root)
        self.label.pack()

        self.root.mainloop()

    def find_sentence(self, event):
        sent = self.entry.get()
     #   fnd = TextReviewer.Reviewer()
        ans = []

        for (i, cur_sent) in enumerate(self.analyzer.text.sents):
            if sent == cur_sent.sent:
                ans.append(i)
                break

      #  threading.Thread(target=fnd.start)
       # fnd.insert_list(self.analyzer.stc.get_forms(word))
        print(ans)


class NearDuplicateSentenceFinder:
    def __init__(self, analyzer):
        self.analyzer = analyzer

        self.root = Tk()

        self.entry = Entry(self.root)
        self.entry.pack()

        self.but = Button(self.root)
        self.but["text"] = "Find near duplicate"
        self.but.bind("<Button-1>", self.find_near_duplicate)
        self.but.pack()

        self.label = Label(self.root)
        self.label.pack()

        self.root.mainloop()

    def find_near_duplicate(self, event):
        sent = simpleAPI2.Sentence(0, self.entry.get(), 0, 0, self.analyzer.language)
        fnd = TextReviewer.Reviewer()
        ans = []

        if not sum(sent.nGrams.values()) == 0:
            for cur_sent in self.analyzer.text.sents:
                cur_intersect = cur_sent.nGrams & sent.nGrams
                cur_overlap = sum(cur_intersect.values()) / sum(sent.nGrams.values())
                if cur_overlap > 0.5:
                    ans.append(cur_sent)

        threading.Thread(target=fnd.start)
        fnd.insert_sent(ans)
