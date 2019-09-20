from heapq import heappush, heappop

class Node:
    def __init__(self, id):
        self.id = id
        self.neighbors = set()

    def addNeighbor(self, neighbor):
        self.neighbors.add(neighbor)
        neighbor.neighbors.add(self)

    def __hash__(self):
        return self.id
    
    def __eq__(self, other):
        return self.id == other.id
    
    def __repr__(self):
        return f'{self.id}: {len(self.neighbors)}'


for line in iter(input, '0'):
    numIntersections, numPaths = (int(num) for num in line.split())

    start = Node(1)
    end = Node(2)
    graph = {start: start, end: end}
    for i in range(numPaths):
        a, b, cost = (int(num) for num in input().split())

        nodeA = Node(a)
        nodeB = Node(b)

        if nodeA not in graph:
            graph[nodeA] = nodeA
            print("Didn't find node")
        
        if nodeB not in graph:
            graph[nodeB] = nodeB
        
        node = graph[nodeA]
        node.addNeighbor(nodeB)

        print(f'{a} -> {b}: {cost}')
        print(graph)
