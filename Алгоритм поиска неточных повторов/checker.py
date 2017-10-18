was = []
used = []
for i in range(10000):
    was.append(False)
    used.append(False)


with open('Linux_pres_1.txt', 'r', encoding='utf-8') as f1:
    A = f1.read().split(' ')

    for i in range(len(A)):
        if A[i] != '':
            was[int(A[i])] = True


with open('Linux_pres_2.txt', 'r', encoding='utf-8') as f2:
    A = f2.read().split(' ')

    for i in range(len(A)):
        if A[i] != '':
            used[int(A[i])] = True

cnt1 = 0
cnt2 = 0
cntAll = 0
for i in range(10000):
    if (was[i] and used[i]):
        cntAll += 1

    if (was[i] and (not used[i])):
        print(str(i) + " is in multi")
        cnt1 += 1

    if (used[i] and (not was[i])):
        print(str(i) + " is in only")
        cnt2 += 2

print(str(cnt1) + " " + str(cnt2))
print(str(cntAll) + " together")
print(str(cnt1 + cntAll) + " all multi")
print(str(cnt2 + cntAll) + " all only")