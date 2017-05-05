from NDF import simpleAPI2


class Cl:
    def __init__(self, y, z):
        self.nGrams = y
        self.sents = z


class Node:
    def __init__(self, w, f, n):
        self.word = w
        self.forms = f
        self.count = n


def get_hash(word):
    ans = 0
    modulo = int(1e9 + 7)
    power = 239
    for ch in word:
        ans = (ans * power + ord(ch)) % modulo
    return ans


class StatisticCollector:
    def __init__(self):
        self.size = int(1e5 + 7)
        self.table = []
        self.count_words = 0
        self.count_stop_words = 0
        for i in range(self.size):
            self.table.append(Node("", set(), 0))

    def update(self):
        if self.count_words * 2 > self.size:
            elements = []
            for node in self.table:
                elements.append(node)
            self.table = []
            self.size *= 2
            for i in range(self.size):
                self.table.append(Node("", set(), 0))
            for node in elements:
                self.add_word(node.word, node.count)
                self.add_form(node.word)

    def get_pos(self, word):
        hash = get_hash(word)
        elem = hash % self.size
        while (self.table[elem].word != word) & (self.table[elem].word != ""):
            elem = (elem + 1) % self.size
        return elem

    def get_count(self, word):
        pos = self.get_pos(word)
        return self.table[pos].count

    def add_word(self, word, num):
        pos = self.get_pos(word)
        if self.table[pos].count == 0:
            self.count_words += 1
        if simpleAPI2.is_stop_word(word):
            self.count_stop_words += 1
        self.table[pos].word = word
        self.table[pos].count += num

    def add_form(self, word):
        init_form = simpleAPI2.word_to_stemmed(word)
        pos = self.get_pos(init_form)
        self.table[pos].forms.add(word)

    def get_forms(self, word):
        init_form = simpleAPI2.word_to_stemmed(word)
        pos = self.get_pos(init_form)
        return self.table[pos].forms

    def add_sent(self, sent):
        for word in sent.words:
            self.add_word(word, 1)
            self.add_form(word)
            self.update()

    def get_popularity(self):  # FIXME: wrong answer
        popular = []
        for i in range(self.size):
            if not self.table[i].count == 0:
                popular.append({self.table[i].count, self.table[i].word})
        popular.sort()
        return popular

    def statistic(self):
        print("Number words: " + str(self.count_words))
        print("Number stopWords " + str(self.count_stop_words))
        print(self.get_popularity())


class NearDuplicatesFinder:
    def __init__(self):
        self.classes = []

    def add_sent(self, curSent):
        best_overlap = 0
        best_class = 0
        for (j, curClass) in enumerate(self.classes):
            cur_intersect = curSent.nGrams & curClass.nGrams
            cur_overlap = sum(cur_intersect.values()) / sum(curSent.nGrams.values())

            if cur_overlap > best_overlap:
                best_overlap = cur_overlap
                best_class = j
        if best_overlap < 0.5:
            self.classes.append(Cl(curSent.nGrams, [curSent]))
        else:
            self.classes[best_class].nGrams += curSent.nGrams
            self.classes[best_class].sents.append(curSent)

    def print_classes(self, encoding, analyzer):
        szClasses = len(self.classes)
        with open("curRes.txt", "w", encoding=encoding) as file:
            for (cur, curClass) in enumerate(self.classes):
                if analyzer.stop == True:
                    return 2
                if len(curClass.sents) == 1:
                    continue
                file.write("========================= CLASS #%d =============================\n" % cur)
                file.write('\n'.join(
                    ["(%d) {%d} [%d]: %s" % (sent.index, sent.start, sent.end, sent.sent) for sent in curClass.sents]))
                file.write("\n*****************************************************************\n")
                analyzer.progress = 95 + 5 * cur / szClasses
        return 0


class Analyzer:
    def __init__(self, path, ID):
        self.name = path
        self.progress = 0
        self.stop = False
        self.ID = ID

    def get_id(self):
        return self.ID

    def set_progress(self, np):
        self.progress = np

    def get_progress(self):
        return self.progress

    def stop(self):
        self.stop = True

    def work(self):
        if (self.name == ''):
            self.progress = 0
            return 1

        text = simpleAPI2.Text(self.name, self)
        sents = text.sents
        szSents = len(sents)
        print(szSents)
        ndf = NearDuplicatesFinder()
        stc = StatisticCollector()
        for (i, curSent) in enumerate(sents):
            if self.stop == True:
                return 2
            stc.add_sent(curSent)
            if len(curSent.nGrams) == 0:
                continue
            ndf.add_sent(curSent)
            self.progress = 20 + 75 * i / szSents

        stc.statistic()
        return ndf.print_classes(text.encoding, self)
