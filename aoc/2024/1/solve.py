import math

data = open('input').read().strip()

total = 0
a = []
b = []
for line in data.split('\n'):
    n1, n2 = (int(x) for x in line.split())
    a.append(n1)
    b.append(n2)
a.sort()
b.sort()
ans = sum(abs(n1-n2) for n1, n2 in zip(a, b))
print(ans)

ans = sum(b.count(n1)*n1 for n1 in a)
print(ans)
