from itertools import combinations

nums = [n for n in map(int, input().split()) if n != 0]

k = int(input())

if k > len(nums):
    print(0)
else:
    total = 0
    for combo in combinations(nums, k):
        options = 1
        for num in combo:
            options *= num
        total += options
    print(total)
