from tkinter.filedialog import *
from TextReviwer import TextReviewer
import threading


class WordCountFinder:
    def __init__(self, analyzer):
        self.analyzer = analyzer

        self.root = Tk()

        self.entry = Entry(self.root)
        self.entry.pack()

        self.but = Button(self.root)
        self.but["text"] = "Find count"
        self.but.bind("<Button-1>", self.find_count)
        self.but.pack()

        self.label = Label(self.root)
        self.label.pack()

        self.root.mainloop()

    def find_count(self, event):
        word = self.entry.get()
        fnd = TextReviewer.Reviewer()
        threading.Thread(target=fnd.start)
        fnd.insert(self.analyzer.stc.get_count(word))
        #self.label["text"] = str(self.analyzer.stc.get_count(word))
