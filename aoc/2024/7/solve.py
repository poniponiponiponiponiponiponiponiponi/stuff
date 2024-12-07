ans = 0

def test(nums, now, wynik):
    if len(nums) == 0:
        return now == wynik
    return test(nums[1:], now+nums[0], wynik) or \
        test(nums[1:], now*nums[0], wynik) or \
        test(nums[1:], int(str(now)+str(nums[0])), wynik)



for l in open('input').read().strip().split('\n'):
    wynik, l = l.split(':')
    wynik = int(wynik)
    nums = [int(n) for n in l.strip().split()]
    if test(nums[1:], nums[0], wynik):
        ans += wynik
print(ans)    
