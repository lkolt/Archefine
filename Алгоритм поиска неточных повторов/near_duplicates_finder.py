import simpleAPI2

class sent:
    def __init__(self, y, z, i):
        self.nGrams = y
        self.text = z
        self.index = i

class cl:
    def __init__(self, y, z):
        self.nGrams = y
        self.sents = z

def intersect(sent1, sent2):
    return [s for s in sent1 if s in sent2]

text = simpleAPI2.fileToSents("resources/sample.txt")
words = simpleAPI2.sentsToWords(text)
nGrams = simpleAPI2.wordsToTrigrams(words)

sents = [sent(ngram, line, i) for (i, (ngram, line)) in enumerate(zip(nGrams, text))]

classes = []

for curSent in sents:
    if len(curSent.nGrams) == 0:
        continue
    bestOverlap = 0
    bestClass = 0
    for j in range(len(classes)):
        curClass = classes[j]
        curIntersect = intersect(curSent.nGrams, curClass.nGrams)
        curOverlap = len(curIntersect) / len(curSent.nGrams)
        if curOverlap > bestOverlap:
            bestOverlap = curOverlap
            bestClass = j
    if bestOverlap < 0.5:
        classes.append(cl(curSent.nGrams, [curSent]))
    else:
        classes[bestClass].nGrams += curSent.nGrams
        classes[bestClass].sents.append(curSent)

with open("result.txt", "w") as file:
    for (i, curClass) in enumerate(classes):
        if len(curClass.sents) == 1:
            continue
        file.write("========================= CLASS #%d =============================\n" % i)
        file.write('\n'.join(["%d: %s" % (sent.index, sent.text) for sent in curClass.sents]))
        file.write("\n*****************************************************************\n")
