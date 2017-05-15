from tkinter.filedialog import *
from Finders import WordFormFinder
from Finders import ContextFinder
from Finders import WordCountFinder
from threading import *
from TextReviwer import TextReviewer


class FinderForm:
    def __init__(self, analyzer):
        self.analyzer = analyzer

        self.root = Tk()
        self.root.geometry('500x400+300+200')

        self.form_finder = Button(self.root)
        self.form_finder["text"] = "Form finder"
        self.form_finder.bind("<Button-1>", self.button_form_finder)
        self.form_finder.pack()

        self.word_count_finder = Button(self.root)
        self.word_count_finder["text"] = "Word count finder"
        self.word_count_finder.bind("<Button-1>", self.button_word_count)
        self.word_count_finder.pack()

        self.context_finder = Button(self.root)
        self.context_finder["text"] = "Context finder"
        self.context_finder.bind("<Button-1>", self.button_context_finder)
        self.context_finder.pack()

        self.open_text = Button(self.root)
        self.open_text["text"] = "Open all text"
        self.open_text.bind("<Button-1>", self.button_open_text)
        self.open_text.pack()

        self.root.mainloop()

    def button_form_finder(self, event):
        WordFormFinder.WordFormFinder(self.analyzer)

    def button_word_count(self, event):
        WordCountFinder.WordCountFinder(self.analyzer)

    def button_context_finder(self, event):
        ContextFinder.ContextFinder(self.analyzer)

    def button_open_text(self, event):
        fnd = TextReviewer.Reviewer()
        Thread(target=fnd.start)  # WHY NOT START?
        fnd.insert_sent(self.analyzer.text.sents)