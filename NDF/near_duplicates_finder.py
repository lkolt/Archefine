from tkinter import ttk
from tkinter.filedialog import *
from NDF import simpleAPI2


class cl:
    def __init__(self, y, z):
        self.nGrams = y
        self.sents = z


class Analyzer:
    def __init__(self, path, ID):
        self.name = path
        self.progress = 0
        self.stop = False
        self.ID = ID

    def getID(self):
        return self.ID

    def setProgress(self, np):
        self.progress = np

    def getProgress(self):
        return self.progress

    def Stop(self):
        self.stop = True

    def work(self):
        if (self.name == ''):
            self.progress = 0
            return 1

        text = simpleAPI2.Text(self.name, self)
        sents = text.sents
        classes = []
        szSents = len(sents)

        for (i, curSent) in enumerate(sents):
            if self.stop == True:
                return 2
            if len(curSent.nGrams) == 0:
                continue
            bestOverlap = 0
            bestClass = 0
            for (j, curClass) in enumerate(classes):
                curIntersect = curSent.nGrams & curClass.nGrams
                curOverlap = sum(curIntersect.values()) / sum(curSent.nGrams.values())

                if curOverlap > bestOverlap:
                    bestOverlap = curOverlap
                    bestClass = j
            if bestOverlap < 0.5:
                classes.append(cl(curSent.nGrams, [curSent]))
            else:
                classes[bestClass].nGrams += curSent.nGrams
                classes[bestClass].sents.append(curSent)
            self.progress = 20 + 75 * i / szSents

        szClasses = len(classes)
        with open("curRes.txt", "w", encoding=text.encoding) as file:
            for (cur, curClass) in enumerate(classes):
                if self.stop == True:
                    return 2
                if len(curClass.sents) == 1:
                    continue
                file.write("========================= CLASS #%d =============================\n" % cur)
                file.write('\n'.join(["(%d) {%d} [%d]: %s" % (sent.index, sent.start, sent.end, sent.sent) for sent in curClass.sents]))
                file.write("\n*****************************************************************\n")
                self.progress = 95 + 5 * cur / szClasses
        return 0