from tkinter.filedialog import *
from Finders import WordFormFinder
from Finders import ContextFinder
from Finders import WordCountFinder
from threading import *
from Finders import SentenceFinder
from TextReviwer import TextReviewer


class FinderForm:
    def __init__(self, analyzer):
        self.analyzer = analyzer

        self.root = Tk()
        self.root.geometry('200x290+620+200')
        self.root.title("Archefine finders")
        self.root.wm_resizable(0, 0)

        self.form_finder = Button(self.root)
        self.form_finder["text"] = "Поиск форм слова"
        self.form_finder.bind("<Button-1>", self.button_form_finder)
        self.form_finder.place(x=10, y=10, height=30, width=180)

        self.word_count_finder = Button(self.root)
        self.word_count_finder["text"] = "Количество вхождений слова"
        self.word_count_finder.bind("<Button-1>", self.button_word_count)
        self.word_count_finder.place(x=10, y=40, height=30, width=180)

        self.context_finder = Button(self.root)
        self.context_finder["text"] = "Поиск контекста"
        self.context_finder.bind("<Button-1>", self.button_context_finder)
        self.context_finder.place(x=10, y=70, height=30, width=180)

        self.open_text = Button(self.root)
        self.open_text["text"] = "Открыть весь текст"
        self.open_text.bind("<Button-1>", self.button_open_text)
        self.open_text.place(x=10, y=100, height=30, width=180)

        self.near_duplicate = Button(self.root)
        self.near_duplicate["text"] = "Найти похожие предложения"
        self.near_duplicate.bind("<Button-1>", self.button_near_duplicate)
        self.near_duplicate.place(x=10, y=130, height=30, width=180)

        self.exact_duplicate = Button(self.root)
        self.exact_duplicate["text"] = "Найти предложения"
        self.exact_duplicate.bind("<Button-1>", self.button_exact_duplicate)
        self.exact_duplicate.place(x=10, y=160, height=30, width=180)

        self.list_stop_words = Button(self.root)
        self.list_stop_words["text"] = "Список стоп-слов"
        self.list_stop_words.bind("<Button-1>", self.button_list_stop_words)
        self.list_stop_words.place(x=10, y=190, height=30, width=180)

        self.show_results = Button(self.root)
        self.show_results["text"] = "Группы похожих предложний"
        self.show_results.bind("<Button-1>", self.button_show_results)
        self.show_results.place(x=10, y=220, height=30, width=180)

        self.save_results = Button(self.root)
        self.save_results["text"] = "Сохранить результаты"
        self.save_results.bind("<Button-1>", self.button_save_results)
        self.save_results.place(x=10, y=250, height=30, width=180)

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

    def button_near_duplicate(self, event):
        SentenceFinder.NearDuplicateSentenceFinder(self.analyzer)

    def button_exact_duplicate(self, event):
        SentenceFinder.ExactDuplicateSentenceFinder(self.analyzer)

    def button_list_stop_words(self, event):
        fnd = TextReviewer.Reviewer()
        Thread(target=fnd.start)
        fnd.insert_popularity(self.analyzer.get_stop_words())

    def button_show_results(self, event):
        fnd = TextReviewer.Reviewer()
        fnd.insert_list(self.analyzer.get_groups())
        Thread(target=fnd.start())

    def button_save_results(self, event):
        op = askopenfilename()
        if op != '':
            Thread(target=self.analyzer.print_groups(op))
