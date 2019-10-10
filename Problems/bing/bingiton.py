class Tree:
    def __init__(self):
        self.count = 0
        self.children = {}
    
    def __getitem__(self, item):
        if item not in self.children:
            self.children[item] = Tree()
        
        return self.children[item]


n = int(input())

root = Tree()

for i in range(n):
    word = input()

    curr = root
    for char in word:
        curr = curr[char]
        curr.count += 1
    
    print(curr.count - 1)