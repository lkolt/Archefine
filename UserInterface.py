from tkinter import ttk
from tkinter.filedialog import *
from NDF import near_duplicates_finder as ndf
import threading
import time

class But_analyzer:
    def __init__(self):
        self.but = Button(root)
        self.but["text"] = "Choose"
        self.but.bind("<Button-1>", self.worker)
        self.but.pack()
        self.cancel = Button(root)
        self.cancel["text"] = "Cancel"
        self.cancel.bind("<Button-1>", self.Stop)
        self.cancel.pack()
        self.mpb = ttk.Progressbar(root, orient="horizontal", length=200, mode="determinate")
        self.mpb.pack()
        self.mpb["maximum"] = 100
        self.mpb["value"] = 0
        self.isWork = False
        self.curID = 0

    def setProgressBar(self):
        last = self.analyzer.getID()
        while ((self.isWork == True) & (last == self.analyzer.getID())):
            Tk.update(root)
            progress = self.analyzer.getProgress()
            self.mpb["value"] = progress
            time.sleep(0.1)

    def doAnalyze(self):
        print("WORKER: " + str(self.analyzer.getID()) + " ended with " + str(self.analyzer.work()))
        self.mpb["value"] = 0
        if self.isWork == True:
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
        th1 = threading.Thread(target = self.doAnalyze)
        th2 = threading.Thread(target = self.setProgressBar)
        th2.start()
        th1.start()

    def Stop(self, event):
        if self.isWork == True:
            self.isWork = False
            self.analyzer.Stop()



root = Tk()
root.geometry('500x400+300+200')
obj = But_analyzer()

root.mainloop()