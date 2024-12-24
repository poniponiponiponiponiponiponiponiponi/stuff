blocks = []
n = 0
gap = False
for c in open('input').read().strip():
    if not gap:
        blocks.append((n, int(c)))
        gap = True
        find = n
        n += 1
    elif gap:
        blocks.append((None, int(c)))
        gap = False


r = len(blocks)-1
while 0 < r:
    if blocks[r][0] is None:
        r -= 1
    elif blocks[r][0] == find:
        find -= 1
        fit = blocks[r]
        for l in range(0, r):
            gap = blocks[l]
            if gap[0] is not None:
                gap = None
                continue
            if fit[1] <= gap[1]:
                break
        if gap is not None and fit[1] <= gap[1]:
            gap = (None, gap[1] - fit[1])
            blocks[r] = (None, fit[1])
            blocks = blocks[:l] + [fit] + [gap] + blocks[l+1:]
            r += 1
    else:
        r -= 1

ans = 0
i = 0
print(blocks)
for n, l in blocks:
    for _ in range(0, l):
        if n != None:
            ans += n * i
        i += 1
print(ans)
