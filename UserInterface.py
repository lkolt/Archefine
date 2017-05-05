from tkinter import ttk
from tkinter.filedialog import *
from NDF import near_duplicates_finder as ndf
import threading
import time


class UserInterface:
    def __init__(self):
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

    def set_progress_bar(self):
        last = self.analyzer.get_id()
        while self.isWork & (last == self.analyzer.get_id()):
            Tk.update(root)
            progress = self.analyzer.get_progress()
            self.mpb["value"] = progress
            time.sleep(0.1)

    def do_analyze(self):
        last = self.analyzer.get_id()
        result = self.analyzer.work()
        print("WORKER: " + str(self.analyzer.get_id()) + " ended with " + str(result))
        if self.analyzer.get_id() == last:
            self.mpb["value"] = 0
            if self.isWork:
                self.mpb["value"] = 100
            self.isWork = False
            self.but["state"] = "normal"

    def worker(self, event):
        if self.but["state"] == "disabled":
            return
        op = askopenfilename()
        self.analyzer = ndf.Analyzer(op, self.curID)
        self.curID += 1
        self.but["state"] = "disabled"
        self.isWork = True
        th1 = threading.Thread(target=self.do_analyze)
        th2 = threading.Thread(target=self.set_progress_bar)
        th2.start()
        th1.start()

    def stop(self, event):
        if self.isWork == True:
            self.isWork = False
            self.analyzer.stop()

root = Tk()
root.geometry('500x400+300+200')
obj = UserInterface()

root.mainloop()
