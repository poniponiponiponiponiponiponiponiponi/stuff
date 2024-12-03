ans = 0

inp = open('input').read().strip()
inp = inp.split("don't()")
new_inp = inp[0]
for l in inp:
    try:
        new_inp += ''.join(l.split("do()")[1:])
    except IndexError:
        continue
for cand in new_inp.split('mul('):
    try:
        cand = cand.split(')')[0]
        x, y = (int(n) for n in cand.split(','))
        ans += x * y
    except:
        continue

print(ans)
