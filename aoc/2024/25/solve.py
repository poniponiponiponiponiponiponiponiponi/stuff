

locks = []
keys = []
for sch in open("input").read().split('\n\n'):
    lines = sch.split('\n')
    sch = lines[1:-1]

    a = []
    for i in range(5):
        col = 0
        for j in range(5):
            if sch[j][i] == '#':
                col += 1
        a.append(col)
    
    if lines[0][0] == '#':
        for i in range(len(a)):
            a[i] = 5 - a[i]
        locks.append(a)
    else:
        keys.append(a)
ans = 0
for key in keys:
    for lock in locks:
        ans += 1
        for a, b in zip(key, lock):
            if a > b:
                ans -= 1
                break
print(keys)
print(locks)
print(ans)
