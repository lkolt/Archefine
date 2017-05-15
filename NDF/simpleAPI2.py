from collections import Counter
from typing import List, Set

from nltk.tokenize import sent_tokenize as nltk_sent_tokenize
from nltk.corpus import stopwords
from nltk import word_tokenize as nltk_word_tokenize
from nltk.util import trigrams  # skipgrams(_, n, k); n - deg, k - skip dist
from nltk.stem.snowball import RussianStemmer as RusStemmer
from nltk.stem.snowball import EnglishStemmer as EngStemmer

import re


class LangDiff:
    def __init__(self, lang):
        # This can be varied
        self.language = 'english'.lower() if lang == 2 else 'russian'.lower()
        self.removeStops = True  # `= set()` for not removing stopwords
        self.puncts = set('.,!?')
        self.default_encodings = ["utf-8", "cp1251"]

        # language dispatch
        self.sent_tokenize = lambda text: nltk_sent_tokenize(text, self.language)
        self.word_tokenize = lambda text: nltk_word_tokenize(text, self.language)
        self.stopwords = set(stopwords.words(self.language)) if self.removeStops else set()
        self.stemmer = RusStemmer() if lang == 1 else EngStemmer()


# Remove unnecessary tokens
def remove_sth(seq: List[str], sth: Set[str]) -> List[str]:
    """ Generic function for removal """
    return [x for x in seq if x not in sth]


# Kernel classes
class Sentence:
    def __init__(self, index: int, sent: str, start: int, end: int, lang: LangDiff):
        self.lang = lang
        self.index = index
        self.sent = sent
        self.words = self.remove_puncts(self.lang.word_tokenize(sent))
        self.nGrams = Counter(trigrams(self.sent_to_words()))
        self.start = start
        self.end = end

    def sent_to_words(self) -> List[str]:
        # FIXME: remove_stops . remove_puncts ~> remove_sth(_, stops | puncts)
        return self.words_to_stemmed(
            self.remove_stops(
                self.remove_puncts(
                    self.lang.word_tokenize(self.sent))))

    def remove_puncts(self, seq: List[str]) -> List[str]:
        return remove_sth(seq, self.lang.puncts)

    def remove_stops(self, seq: List[str]) -> List[str]:
        return remove_sth(seq, self.lang.stopwords)

    def words_to_stemmed(self, sent: List[str]) -> List[str]:
        return [self.lang.stemmer.stem(word) for word in sent]


class Text:
    def __init__(self, filename: str, analyzer):
        self.encoding = None
        self.lang = LangDiff(analyzer.language)
        self.sents = self.file_to_sents(filename, analyzer)

    def file_to_sents(self, filename: str, analyzer) -> List[str]:
        def decode(sth: bytes, codings: List[str]) -> str:
            for coding in codings:
                try:
                    self.encoding = coding
                    return sth.decode(encoding=coding)
                except UnicodeDecodeError:
                    pass
            raise UnicodeDecodeError

        with open(filename, mode='rb') as file:
            text = decode(file.read(), self.lang.default_encodings).replace('\n', ' ')
            # text = re.sub("\s+", ' ', text)  # "hi     man" ~> "hi man"
        sents = self.lang.sent_tokenize(text)
        index = 0
        sz = len(sents)
        lst = list()
        for (num, sent) in enumerate(sents):
            index = text.find(sent, index)
            lst.append(Sentence(num, re.sub("\s+", ' ', sent), index, index + len(sent), self.lang))
            analyzer.set_progress(20 * num / sz)
            if analyzer.stop:
                return

        return lst

    def word_to_stemmed(self, word):
        return self.lang.stemmer.stem(word)

    def is_stop_word(self, word):
        return word in self.lang.stopwords
