import copy

ans = 0
m = []
for y, l in enumerate(open('input').read().strip().split('\n')):
    m.append(list(l.strip()))
    if '^' in l:
        gx = l.index('^')
        gy = y

sx, sy = gx, gy
for (ox, oy) in ((x, y) for y in range(len(m)) for x in range(len(m[0]))):
    if m[oy][ox] == '#' or (ox, oy) == (sx, sy):
        continue
    gx, gy = sx, sy
    oldm = copy.deepcopy(m)
    quit = False
    lines = []
    m[oy][ox] = '#'
    while not quit:
        for diff in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            sp = (gx, gy)
            new_x = gx + diff[0]
            new_y = gy + diff[1]
            while new_x >= 0 and new_y >= 0 and new_x < len(m[0]) and new_y < len(m) and m[new_y][new_x] != '#':
                gx = new_x
                gy = new_y
                new_x = gx + diff[0]
                new_y = gy + diff[1]
            if new_x < 0 or new_y < 0 or new_x >= len(m[0]) or new_y >= len(m):
                quit = True
                break
            ep = (gx, gy)
            if (sp, ep) in lines:
                ans += 1
                print(ans)
                quit = True
                break
            lines.append((sp, ep))
    m = oldm
print(ans)
