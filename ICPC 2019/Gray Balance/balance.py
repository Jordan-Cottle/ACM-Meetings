n = int(input())

grid = [input() for _ in range(n)]


def checkRow(i):
    row = grid[i]
    count = 0
    reps = 0
    last = ''
    for c in row:
        if c == 'B':
            count += 1
        else:
            count -= 1

        if c != last:
            reps = 1
            last = c
        else:
            reps += 1

        if reps == 3:
            return False

    if count != 0:
        return False

    return True


def checkCol(i):
    count = 0
    reps = 0
    last = ''
    for row in grid:
        c = row[i]
        if c == 'B':
            count += 1
        else:
            count -= 1

        if c != last:
            reps = 1
            last = c
        else:
            reps += 1

        if reps == 3:
            return False

    if count != 0:
        return False

    return True


for i in range(n):
    if not(checkRow(i) and checkCol(i)):
        print(0)
        break
else:
    print(1)