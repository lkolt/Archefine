from tkinter.filedialog import *
from TextReviwer import TextReviewer
from threading import *


class WordCountFinder:
    def __init__(self, analyzer):
        self.analyzer = analyzer

        self.root = Tk()
        self.root.geometry('250x120+620+540')
        self.root.title("Archefine word count finder")

        self.label = Label(self.root)
        self.label["text"] = "Введите слово"
        self.label.pack()

        self.entry = Entry(self.root, width=80)
        self.entry.pack()

        self.but = Button(self.root)
        self.but["text"] = "Найти количество вхождений в текст"
        self.but.bind("<Button-1>", self.find_count)
        self.but.pack()

        self.answer = Label(self.root)
        self.answer.pack()

        self.popular = Button(self.root)
        self.popular["text"] = "Список встречаемости слов"
        self.popular.bind("<Button-1>", self.button_popular)
        self.popular.pack()

        self.root.mainloop()

    def find_count(self, event):
        word = self.entry.get()
        self.answer["text"] = "Слово встречается " + str(self.analyzer.stc.get_count(word)) + " раз"

    def button_popular(self, event):
        fnd = TextReviewer.Reviewer()
        fnd.insert_popularity(self.analyzer.get_popularity())
        Thread(target=fnd.start)
