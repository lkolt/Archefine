import simpleAPI2

class sent:
    def __init__(self, y, z):
        self.nGrams = y
        self.text = z

class cl:
    def __init__(self, y, z):
        self.nGrams = y
        self.sents = z

def intersect(sent1, sent2):
    return [s for s in sent1 if s in sent2]

text = simpleAPI2.fileToSents("resources/sample.txt")
words = simpleAPI2.sentsToWords(text)
nGrams = simpleAPI2.wordsToTrigrams(words)

sents = [sent(ngram, line) for (ngram, line) in zip(nGrams, text)]
classes = []

for i in range(len(sents)):
    curSent = sents[i]
    if (len(curSent.nGrams) == 0):
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
        classes.append(cl(curSent.nGrams, [(curSent, i)]))
    else:
        classes[bestClass].nGrams += curSent.nGrams
        classes[bestClass].sents.append((curSent, i))

with open("result.txt", "w") as file:
    for i in range(len(classes)):
        if (len(classes[i].sents) == 1):
            continue
        print("========================= CLASS #" + str(i) + " =============================", file=file)
        for j in range(len(classes[i].sents)):
            print(str(classes[i].sents[j][1]), file=file, end=": ")
            print(*classes[i].sents[j][0].text, file=file, sep='')
        print("*****************************************************************", file=file)
