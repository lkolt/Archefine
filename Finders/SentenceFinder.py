from tkinter import *
from TextReviwer import TextReviewer
from NDF import simpleAPI2
import threading


class ExactDuplicateSentenceFinder:
    def __init__(self, analyzer):
        self.analyzer = analyzer

        self.root = Tk()
        self.root.geometry('520x100+300+60')
        self.root.title("Archefine exact duplicate sentence finder")

        self.label = Label(self.root)
        self.label["text"] = "Введите предложение:"
        self.label.pack()

        self.entry = Entry(self.root, width=480)
        self.entry.pack()

        self.but = Button(self.root)
        self.but["text"] = "Найти предложение"
        self.but.bind("<Button-1>", self.find_sentence)
        self.but.pack()

        self.answer = Label(self.root)
        self.answer.pack()

        self.root.mainloop()

    def find_sentence(self, event):
        sent = self.entry.get()
        ans = 0

        for cur_sent in self.analyzer.text.sents:
            if sent == cur_sent.sent:
                ans += 1

        self.answer["text"] = "Предложение встречается в тексте " + str(ans) + " раз\n"


class NearDuplicateSentenceFinder:
    def __init__(self, analyzer):
        self.analyzer = analyzer

        self.root = Tk()
        self.root.geometry('520x80+300+80')
        self.root.title("Archefine near duplicate sentence finder")

        self.label = Label(self.root)
        self.label["text"] = "Введите предложение:"
        self.label.pack()

        self.entry = Entry(self.root, width=480)
        self.entry.pack()

        self.but = Button(self.root)
        self.but["text"] = "Найти похожие предложения"
        self.but.bind("<Button-1>", self.find_near_duplicate)
        self.but.pack()

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
