data = open('input').read().strip()

ans1 = 0
ans2 = 0
for line in data.split('\n'):
    numso = [int(n) for n in line.split()]

    diffs = []
    bigger = []
    smaller = []
    for a, b in zip(numso[::], numso[1::]):
        diffs.append(abs(a-b))
        bigger.append(a > b)
        smaller.append(a < b)
    if not (all(bigger) or all(smaller)):
        continue
    if not all(map(lambda n: n in range(1, 4), diffs)):
        continue
    ans1 += 1

for line in data.split('\n'):
    numso = [int(n) for n in line.split()]
    nums2 = [numso[:i] + numso[i+1:] for i in range(len(numso))]
    correct = 0
    for nums in nums2:
        diffs = []
        bigger = []
        smaller = []
        for a, b in zip(nums[::], nums[1::]):
            diffs.append(abs(a-b))
            bigger.append(a > b)
            smaller.append(a < b)
        if not (all(bigger) or all(smaller)):
            continue
        if not all(map(lambda n: n in range(1, 4), diffs)):
            continue
        correct += 1
    if correct > 0:
        ans2 += 1
print(ans1)
print(ans2)
    
