import functools


stones = []
for n in open('input').read().strip().split():
    stones.append(int(n))

@functools.lru_cache(maxsize=9999999)
def f(n, d):
    if d == 0:
        return 1
    if n == 0:
        return f(1, d-1)
    if len(s := str(n)) % 2 == 0:
        return f(int(s[:len(s)//2]), d-1) + f(int(s[len(s)//2:]), d-1)
    return f(n*2024, d-1)

print(sum(f(n, 75) for n in stones))
