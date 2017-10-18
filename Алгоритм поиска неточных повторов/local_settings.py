# from .simpleAPI2 import *
from nltk import word_tokenize
import re

"""1) количество классов в документе
2) среднее количество предложений в классе(еще можно максимальное)
3) среднее количество слов в классе
4) среднее количество символов в классе"""
classes = 0
sents = 0
words = 0
symbols = 0
number = 0
####
All = 613423
####
with open('Linux_pres.txt', 'w', encoding='utf-8') as f:
    with open('Linux_Kernel_Documentation.pxml result.txt', 'r', encoding = 'utf-8') as file:
        for line in file:
            if re.fullmatch("========================= CLASS #\d+ =============================\n", line):
                classes += 1
            elif line == "*****************************************************************\n":
                continue
            elif line:

                ba = line.index("(")
                ea = line.index(")")

                ac = int(line[ba + 1:ea])

                bb = line.index("<")
                eb = line.index(">")
                bc  = int(line[bb + 1:eb])


                bf = line.index("{")
                ef = line.index("}")
                bs = line.index("[")
                es = line.index("]")
                fn = int(line[bf + 1:ef])
                sn = int(line[bs + 1:es])
                number += sn - fn + 1


                for i in range(ac, bc + 1):
                    f.write(str(i) + " ")

                sents += bc - ac + 1
                sent = line[line.index(": "):-1]
                words += len(word_tokenize(sent))
                symbols += len(sent)



print()
print("""1) количество классов в документе %d
2) среднее количество предложений в классе %f
3) среднее количество слов в классе %f
4) среднее количество символов в классе %f
5) количество предложений %f
6) количество символов, покрытых повторами %d
7) процент покрытия повторами %f""" % (classes, sents / classes, words / classes, symbols / classes, sents, number, number / All))
