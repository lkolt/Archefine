from tkinter import ttk
from tkinter.filedialog import *
from NDF import near_duplicates_finder as ndf
from Finders import Finder
import threading
import time


class UserInterface:
    def __init__(self):
        self.popular_word = Label(root)
        self.popular_word.pack()

        self.number_stop_words = Label(root)
        self.number_stop_words.pack()

        self.number_words = Label(root)
        self.number_words.pack()

        self.but = Button(root)
        self.but["text"] = "Choose"
        self.but.bind("<Button-1>", self.worker)
        self.but.pack()

        self.cancel = Button(root)
        self.cancel["text"] = "Cancel"
        self.cancel.bind("<Button-1>", self.stop)
        self.cancel.pack()

        self.mpb = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
        self.mpb.pack()
        self.mpb["maximum"] = 100
        self.mpb["value"] = 0

        self.isWork = False
        self.curID = 0

        self.work_with_results = Button()
        self.work_with_results["text"] = "Work with results"
        self.work_with_results.bind("<Button-1>", self.to_finder)
        self.work_with_results["state"] = "disabled"
        self.work_with_results.pack()

    def to_finder(self, event):
        if self.work_with_results["state"] == "normal":
            Finder.FinderForm(self.analyzer)

    def update_fields(self, set):
        progress = self.analyzer.get_progress()
        self.mpb["value"] = progress
        self.popular_word["text"] = (self.analyzer.get_most_popular_word())[1]
        self.number_words["text"] = self.analyzer.get_count_words()
        self.number_stop_words["text"] = self.analyzer.get_count_stop_words()

    def set_progress_bar(self):
        last = self.analyzer.get_id()
        while self.isWork & (last == self.analyzer.get_id()):
            Tk.update(root)
            self.update_fields(False)
            time.sleep(0.1)

    def do_analyze(self):
        last = self.analyzer.get_id()
        result = self.analyzer.work()
        print("WORKER: " + str(self.analyzer.get_id()) + " ended with " + str(result))
        if self.analyzer.get_id() == last:
            self.mpb["value"] = 0
            if self.isWork:
                self.update_fields(True)
                self.work_with_results["state"] = "normal"
            self.isWork = False
            self.but["state"] = "normal"

    def worker(self, event):
        if self.but["state"] == "disabled":
            return
        op = askopenfilename()
        self.work_with_results["state"] = "disabled"
        self.analyzer = ndf.Analyzer(op, self.curID)
        self.curID += 1
        self.but["state"] = "disabled"
        self.isWork = True
        th1 = threading.Thread(target=self.do_analyze)
        th2 = threading.Thread(target=self.set_progress_bar)
        th2.start()
        th1.start()

    def stop(self, event):
        if self.isWork:
            self.isWork = False
            self.analyzer.stop_work()

root = Tk()
root.geometry('500x400+300+200')
obj = UserInterface()

root.mainloop()
