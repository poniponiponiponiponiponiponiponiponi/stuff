m = []
for l in open('input').read().strip().split('\n'):
    m.append(l.strip())

ans = 0
for letters in (
        ((0, 0), (0, 1), (0, 2), (0, 3)),
        ((0, 0), (1, 1), (2, 2), (3, 3)),
        ((0, 0), (1, 0), (2, 0), (3, 0)),
        ((0, 0), (1, -1), (2, -2), (3, -3))
):
    for i in range(len(m)):
        for j in range(len(m[0])):
            word = ""
            try:
                for pos in letters:
                    if i+pos[0] < 0:
                        continue
                    if j+pos[1] < 0:
                        continue
                    word += m[i+pos[0]][j+pos[1]]
                if word == "XMAS" or word == "SAMX":
                    print(i, j)
                    ans += 1
            except IndexError:
                pass
print(ans)


ans = 0
for letters in (
        ((-1, -1), (0, 0), (1, 1), (1, -1), (0, 0), (-1, 1)),
        ((-1, -1), (0, 0), (1, 1), (-1, 1), (0, 0), (1, -1))
):
    for i in range(len(m)):
        for j in range(len(m[0])):
            word = ""
            try:
                for pos in letters:
                    if i+pos[0] < 0:
                        continue
                    if j+pos[1] < 0:
                        continue
                    word += m[i+pos[0]][j+pos[1]]
                if word == "MASMAS" or word == "SAMSAM":
                    print(i, j)
                    ans += 1
            except IndexError:
                pass
print(ans)
