from tkinter.filedialog import *
from TextReviwer import TextReviewer
import threading


class WordFormFinder:
    def __init__(self, analyzer):
        self.analyzer = analyzer

        self.root = Tk()

        self.entry = Entry(self.root)
        self.entry.pack()

        self.but = Button(self.root)
        self.but["text"] = "Find forms"
        self.but.bind("<Button-1>", self.find_forms)
        self.but.pack()

        self.label = Label(self.root)
        self.label.pack()

        self.root.mainloop()

    def find_forms(self, event):
        word = self.entry.get()
        fnd = TextReviewer.Reviewer()
        threading.Thread(target=fnd.start)
        fnd.insert_list(self.analyzer.stc.get_forms(word))
