class Node:
    def __init__(self):
        self._content = 0
        self.nopes = set()

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if value == self.content:
            return

        if value in self.nopes:
            raise ValueError(f'{value} in nopes!')
        
        self._content = value
        self.nopes.add(value)
    
    def __str__(self):
        return f'{self.content}: {self.nopes}'

class World:
    def __init__(self, size, clues):
        self.items = [[Node() for c in range(size)] for r in range(size)]
        self.clues = clues
        self.size = size

        for i, clue in enumerate(self.clues):
            div = i // size
            if div == 0:
                direction = (1, 0)
                startRow = 0
                startCol = i
            elif div == 1:
                direction = (0, -1)
                startRow = i - 4
                startCol = 3
            elif div == 2:
                direction = (-1, 0)
                startRow = 3
                startCol = 11 - i
            elif div == 3:
                direction = (0, 1)
                startRow = 15 - i
                startCol = 0

            start = (startRow, startCol)
            self.parseClue(start, direction, clue)

    def parseClue(self, start, direction, clue):
        if clue == 1:
            self[start] = self.size
        elif clue == 2:
            self[start].nopes.add(self.size)
            pos = (start[0] + direction[0], start[1] + direction[1])
            print(start, pos)
            self[pos].nopes.add(self.size-1)
        elif clue == self.size:
            for i in range(self.size):
                xDiff = direction[0] * i
                yDiff = direction[1] * i

                pos = (start[0] + xDiff, start[1] + yDiff)
                self[pos] = i+1
        else:
            for i in range(clue-1):
                xDiff = direction[0] * i
                yDiff = direction[1] * i
                pos = (start[0] + xDiff, start[1] + yDiff)
                for j in range((clue-1)-i):
                    self[pos].nopes.add(self.size-j)

    def checkNopesInRow(self, row):
        pass

    def checkNopesInCol(self, col):
        pass

    def checkNopes(self):
        pass
        
    
    def __str__(self):
        res = []
        for row in self.items:
            r = []
            for col in row:
                r.append(str(col))
            res.append('\n'.join(r))
            res.append(' ')
        
        return '\n'.join(res)

    def __getitem__(self, coords):
        return self.items[coords[0]][coords[1]]

    def __setitem__(self, coords, val):
        row = coords[0]
        col = coords[1]
        self.items[row][col].content = val

        for i in range(self.size):
            self.items[row][i].nopes.add(val)
            self.items[i][col].nopes.add(val)


clues = [
    0,0,1,2,
    0,2,0,0,
    0,3,0,0,
    0,1,0,0
]

w = World(4, clues)
print(w, '\n')