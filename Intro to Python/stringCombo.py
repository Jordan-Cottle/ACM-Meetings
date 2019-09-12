from itertools import permutations

*words, target = input().split()

validPairs = []
for combo in permutations(words, 2):
    if target in ''.join(combo):
        validPairs.append(combo)

if not len(validPairs):
    print('not found')
else:
    for pair in validPairs:
        print(*pair)
