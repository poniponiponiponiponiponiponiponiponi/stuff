blocks = []
n = 0
gap = False
for c in open('input').read().strip():
    if not gap:
        blocks.extend([n] * int(c))
        gap = True
        n += 1
    elif gap:
        blocks.extend([None] * int(c))
        gap = False

        
l = 0
r = len(blocks)-1
while l < r:
    if blocks[l] is not None:
        l += 1
    elif blocks[r] is None:
        r -= 1
    else:
        blocks[l], blocks[r] = blocks[r], blocks[l]

print(sum(map(lambda p: p[0]*p[1], filter(lambda p: p[1] is not None, ((i, n) for i, n in enumerate(blocks))))))
