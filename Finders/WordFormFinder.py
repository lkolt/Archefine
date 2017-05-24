from tkinter.filedialog import *
from TextReviwer import TextReviewer
import threading


class WordFormFinder:
    def __init__(self, analyzer):
        self.analyzer = analyzer

        self.root = Tk()
        self.root.geometry('200x100+80+200')
        self.root.title("Archefine from finder")

        self.label = Label(self.root)
        self.label["text"] = "Введите слово:"
        self.label.pack()

        self.entry = Entry(self.root, width=180)
        self.entry.pack()

        self.but = Button(self.root)
        self.but["text"] = "Найти формы слова"
        self.but.bind("<Button-1>", self.find_forms)
        self.but.pack()

        self.root.mainloop()

    def find_forms(self, event):
        word = self.entry.get()
        fnd = TextReviewer.Reviewer()
        threading.Thread(target=fnd.start)
        fnd.insert_list(self.analyzer.stc.get_forms(word))
