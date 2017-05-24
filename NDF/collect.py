import re

files = [open("%d.txt" % i, 'w') for i in range(1, 4)]

with open("Zend_Manual.nocode.pxml resultChoose.txt") as file:
    curFileIndex = -1
    for line in file.readlines():
        if re.fullmatch("^\d========================= CLASS #\d+ =============================\n", line):
            curFileIndex = int(line[0]) - 1
            files[curFileIndex].write(line[1:])
        else:
            files[curFileIndex].write(line)

for file in files:
    file.close()

