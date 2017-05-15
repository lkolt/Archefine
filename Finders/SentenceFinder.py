from tkinter import *
from TextReviwer import TextReviewer
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
        fnd = TextReviewer.Reviewer()
        ans = []
#
#        for cur_sent in self.analyzer.text.sents:
#            if sent == cur_sent:
#                ans.append(cur_sent)
#                break

#        threading.Thread(target=fnd.start)
#        fnd.insert_list(self.analyzer.stc.get_forms(word))