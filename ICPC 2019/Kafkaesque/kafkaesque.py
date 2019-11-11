n = int(input())

needed = {i: int(input()) for i in range(n)}
passes = 1
cur = 0
for i in range(n):
    pos = needed[i]
    if pos < cur:
        passes += 1
    cur = pos

print(passes)
