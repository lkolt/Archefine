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
    ans = []
    for s in sent1:
        if (s in sent2):
            ans.append(s)
    return ans

def add(sent1, sent2):
    ans = sent2
    for s in sent1:
        ans.append(s)
    return ans

text = simpleAPI2.fileToSents("resources/SVNBook.pxml")
words = simpleAPI2.sentsToWords(text)
nGrams = simpleAPI2.wordsToTrigrams(words)

sents = []
for i in range(len(text)):
    sents.append(sent(nGrams[i], text[i]))

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
        classes[bestClass].nGrams = add(curSent.nGrams, classes[bestClass].nGrams)
        classes[bestClass].sents.append((curSent, i))

with open("result.txt", "w") as file:
    for i in range(len(classes)):
        if (len(classes[i].sents) == 1):
            continue
        print("========================= CLASS #" + str(i) + " =============================", file=file)
        for j in range(len(classes[i].sents)):
            print(str(classes[i].sents[j][1]) + ": ", file=file, sep='', end = '')
            print(*classes[i].sents[j][0].text, file=file, sep='')
        print("*****************************************************************", file=file)
