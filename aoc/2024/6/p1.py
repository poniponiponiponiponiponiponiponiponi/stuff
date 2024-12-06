ans = 0
m = []
pos = set()
for y, l in enumerate(open('input').read().strip().split('\n')):
    m.append(l.strip())
    if '^' in l:
        gx = l.index('^')
        gy = y
        print(y)

pos.add((gx, gy))        
quit = False
while not quit:
    for diff in ((0, -1), (1, 0), (0, 1), (-1, 0)):
        new_x = gx + diff[0]
        new_y = gy + diff[1]
        while new_x >= 0 and new_y >= 0 and new_x < len(m[0]) and new_y < len(m) and m[new_y][new_x] != '#':
            gx = new_x
            gy = new_y
            pos.add((gx, gy))
            new_x = gx + diff[0]
            new_y = gy + diff[1]
        if new_x < 0 or new_y < 0 or new_x >= len(m[0]) or new_y >= len(m):
            quit = True
            break
print(len(pos))
