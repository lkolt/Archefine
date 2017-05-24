from tkinter import ttk
from tkinter.filedialog import *
from NDF import near_duplicates_finder as ndf
from Finders import Finder
import threading
from tkinter import messagebox
import time


class UserInterface:
    def __init__(self):
        self.language_label = Label(root)
        self.language_label["text"] = "Выберите язык документа:"
        self.language_label.place(x=10, y=10)

        self.radio_button = IntVar()
        self.radio_button.set(1)

        Radiobutton(root, text="Russian", variable=self.radio_button, value=1).place(x=170, y=10)
        Radiobutton(root, text="English", variable=self.radio_button, value=2).place(x=170, y=30)

        self.choose_label = Label(root)
        self.choose_label["text"] = "Выберите файл:"
        self.choose_label.place(x=10, y=60)

        self.but = Button(root)
        self.but["text"] = "Выбрать"
        self.but.bind("<Button-1>", self.worker)
        self.but.place(x=170, y=60)

        self.mpb = ttk.Progressbar(root, orient="horizontal", length=280, mode="determinate")
        self.mpb.place(x=10, y=100)
        self.mpb["maximum"] = 100
        self.mpb["value"] = 0

        self.popular_word_label = Label(root)
        self.popular_word_label["text"] = "Самое популярное слово:"
        self.popular_word_label.place(x=10, y=130)

        self.popular_word = Label(root)
        self.popular_word.place(x=170, y=130)

        self.number_words_label = Label(root)
        self.number_words_label["text"] = "Всего слов подсчитано:"
        self.number_words_label.place(x=10, y=160)

        self.number_words = Label(root)
        self.number_words.place(x=170, y=160)

        self.number_stop_words_label = Label(root)
        self.number_stop_words_label["text"] = "Количество стоп-слов:"
        self.number_stop_words_label.place(x=10, y=190)

        self.number_stop_words = Label(root)
        self.number_stop_words.place(x=170, y=190)

        self.number_diff_words_label = Label(root)
        self.number_diff_words_label["text"] = "Всего различный слов:"
        self.number_diff_words_label.place(x=10, y=220)

        self.number_diff_words = Label(root)
        self.number_diff_words.place(x=170, y=220)

        self.number_form_words_label = Label(root)
        self.number_form_words_label["text"] = "Количество разных корней:"
        self.number_form_words_label.place(x=10, y=250)

        self.number_form_words = Label(root)
        self.number_form_words.place(x=170, y=250)

        self.cancel = Button(root)
        self.cancel["text"] = "Отмена"
        self.cancel.bind("<Button-1>", self.stop)
        self.cancel["state"] = "disable"
        self.cancel.place(x=240, y=370)

        self.status_label = Label(root, font="Helvetica 16 bold italic")
        self.status_label["text"] = "Статус:"
        self.status_label.place(x=10, y=280)

        self.work_label = Label(root, font="Helvetica 16 bold italic")
        self.work_label["text"] = "Ожидаем файл"
        self.work_label.place(x=10, y=310)

        self.isWork = False
        self.curID = 0

        self.work_with_results = Button()
        self.work_with_results["text"] = "Работать с результатами"
        self.work_with_results.bind("<Button-1>", self.to_finder)
        self.work_with_results["state"] = "disabled"
        self.work_with_results.place(x=10, y=370)

        self.analyzer = ndf.Analyzer('', -1, 1)

    def to_finder(self, event):
        if self.work_with_results["state"] == "normal":
            Finder.FinderForm(self.analyzer)

    def state_to_translate(self, state):
        if state == -1:
            return "Анализ отменен"
        if state == 0:
            return "Ожидаем файл"
        if state == 1:
            return "Обрабатываем файл"
        if state == 2:
            return "Анализируем файл"
        if state == 3:
            return "Обработка закочена"

    def update_fields(self):
        progress = self.analyzer.get_progress()
        self.mpb["value"] = progress
        self.popular_word["text"] = (self.analyzer.get_most_popular_word())[1]
        self.number_words["text"] = self.analyzer.get_count_words()
        self.number_stop_words["text"] = self.analyzer.get_count_stop_words()
        self.work_label["text"] = self.state_to_translate(self.analyzer.get_state())
        self.number_diff_words["text"] = self.analyzer.get_count_diff_words()
        self.number_form_words["text"] = self.analyzer.get_count_form_words()

    def set_progress_bar(self):
        last = self.analyzer.get_id()
        while self.isWork & (last == self.analyzer.get_id()):
            Tk.update(root)
            self.update_fields()
            time.sleep(0.1)

    def do_analyze(self):
        last = self.analyzer.get_id()
        result = self.analyzer.work()
        print("WORKER: " + str(self.analyzer.get_id()) + " end with " + str(result))
        if self.analyzer.get_id() == last:
            self.mpb["value"] = 0
            if self.isWork:
                self.update_fields()
                if self.analyzer.get_state() == 3:
                    self.work_with_results["state"] = "normal"
            self.isWork = False
            self.but["state"] = "normal"
            self.cancel["state"] = "disable"
            self.work_label["text"] = self.state_to_translate(self.analyzer.get_state())

    def ask_cancel_old_results(self):
        result = messagebox.askokcancel('Внимание!', 'Полученные результаты будут удалены! Хотите продолжить?')
        return result

    def worker(self, event):
        if self.but["state"] == "disabled":
            return

        if self.analyzer.get_state() != 3 or self.ask_cancel_old_results():
            op = askopenfilename()
            self.work_with_results["state"] = "disabled"
            self.cancel["state"] = "normal"
            self.analyzer = ndf.Analyzer(op, self.curID, self.radio_button.get())
            self.curID += 1
            self.but["state"] = "disabled"
            self.isWork = True
            th1 = threading.Thread(target=self.do_analyze)
            th2 = threading.Thread(target=self.set_progress_bar)
            th2.start()
            th1.start()

    def stop(self, event):
        if self.isWork:
            if self.ask_cancel_old_results():
                self.isWork = False
                self.analyzer.stop_work()

root = Tk()
root.geometry('300x400+300+200')
obj = UserInterface()
root.title("Archefine")
root.wm_resizable(0, 0)

root.mainloop()
