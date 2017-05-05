from collections import Counter
from typing import Iterator, List, Set

from nltk.tokenize import sent_tokenize as nltk_sent_tokenize
from nltk.corpus import stopwords
from nltk import word_tokenize as nltk_word_tokenize
from nltk.util import trigrams  # skipgrams(_, n, k); n - deg, k - skip dist

import re


# This can be varied
language = 'russian'.lower()  # FIXME PLIZZZZZ
removeStops = True  # `= set()` for not removing stopwords
puncts = set('.,!?')
default_encodings = ["utf-8", "cp1251"]


# language dispatch
sent_tokenize = lambda text: nltk_sent_tokenize(text, language)
word_tokenize = lambda text: nltk_word_tokenize(text, language)
stopwords = set(stopwords.words(language)) if removeStops else set()
if language == 'russian':
    from nltk.stem.snowball import RussianStemmer as Stemmer
else:
    from nltk.stem.snowball import EnglishStemmer as Stemmer


# Remove unnecessary tokens
def remove_sth(seq: Iterator[str], sth: Set[str]) -> Iterator[str]:
    """ Generic function for removal """
    return filter(lambda x: x not in sth, seq)


def remove_puncts(seq: Iterator[str]) -> Iterator[str]:
    return remove_sth(seq, puncts)


def remove_stops(seq: Iterator[str]) -> Iterator[str]:
    return remove_sth(seq, stopwords)


def words_to_stemmed(sent: Iterator[str]) -> List[str]:
    return [Sentence.stemmer.stem(word) for word in sent]


def word_to_stemmed(word):
    return Stemmer().stem(word)


def is_stop_word(word):
    return word in stopwords


# Kernel classes
class Sentence:
    stemmer = Stemmer()

    def __init__(self, index: int, sent: str, start: int, end: int):
        self.index = index
        self.sent = sent
        self.words = remove_puncts(word_tokenize(sent))
        self.nGrams = Counter(trigrams(self.sent_to_words()))
        self.start = start
        self.end = end

    def sent_to_words(self) -> List[str]:
        # FIXME: remove_stops . remove_puncts ~> remove_sth(_, stops | puncts)
        return words_to_stemmed(
            remove_stops(
                remove_puncts(
                    word_tokenize(self.sent))))


class Text:
    def __init__(self, filename: str, analyzer):
        self.encoding = None
        self.sents = list(self.file_to_sents(filename, analyzer))

    def file_to_sents(self, filename: str, analyzer) -> List[str]:
        def decode(sth: bytes, codings: List[str] = default_encodings) -> str:
            for coding in codings:
                try:
                    self.encoding = coding
                    return sth.decode(encoding=coding)
                except UnicodeDecodeError:
                    pass
            raise UnicodeDecodeError

        with open(filename, mode='rb') as file:
            text = decode(file.read()).replace('\n', ' ')
            # text = re.sub("\s+", ' ', text)  # "hi     man" ~> "hi man"
            sents = sent_tokenize(text)
            index = 0
            sz = len(sents)
            for (num, sent) in enumerate(sents):
                index = text.find(sent, index)
                yield Sentence(num, re.sub("\s+", ' ', sent), index, index + len(sent))
                analyzer.set_progress(20 * num / sz)
                if analyzer.stop:
                    return
