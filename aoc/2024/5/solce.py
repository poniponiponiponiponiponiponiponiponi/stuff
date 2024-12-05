from collections import defaultdict

ans1 = 0
ans2 = 0
before = defaultdict(lambda : [])
in1, in2 = open('input').read().strip().split('\n\n')

for line in in1.strip().split('\n'):
    line = line.strip()
    a, b = [int(n) for n in line.split('|')]
    before[b].append(a)

for line in in2.strip().split('\n'):
    nums = [int(n) for n in line.strip().split(',')]
    bad = False
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            n = nums[i]
            m = nums[j]
            b = before.get(n, None)
            if b is None:
                continue
            if m in b:
                bad = True
    if not bad:
        mid = nums[len(nums)//2]
        ans1 += mid
        
    bad = False
    for i in range(len(nums)):
        for j in range(i+1, len(nums)):
            n = nums[i]
            m = nums[j]
            b = before.get(n, None)
            if b is None:
                continue
            if m in b:
                nums[i], nums[j] = nums[j], nums[i]
                bad = True
    if bad:
        mid = nums[len(nums)//2]
        ans2 += mid
    
print(ans1)
print(ans2)
