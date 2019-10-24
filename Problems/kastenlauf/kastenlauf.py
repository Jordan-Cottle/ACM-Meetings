class Location:
    destination = None
    def __init__(self, pos):
        self.x, self.y = (int(n) for n in pos.split())
    
    def distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    def near(self, other):
        return self.distance(other) <= 1000

    def __eq__(self, value):
        return self.x == value.x and self.y == value.y

    def __lt__(self, value):
        return self.distance(Location.destination) < value.distance(Location.destination)
    
    def __hash__(self):
        return self.x << 16 | self.y


numCases = int(input())

for _ in range(numCases):
    numStores = int(input())

    home = Location(input())

    stores = []

    for __ in range(numStores):
        stores.append(Location(input()))

    destination = Location(input())

    Location.destination = destination

    openList = []
    closedList = set()

    curr = home
    while curr != destination:
        if curr.near(destination):
            print('happy')
            break

        neighbors = []
        for store in stores:
            if (curr.near(store) and store not in closedList):
                neighbors.append(store)
        
        openList.extend((neighbor for neighbor in neighbors if neighbor not in openList))
        closedList.add(curr)

        if(len(openList) == 0):
            print('sad')
            break
        curr = min(openList)
        openList.remove(curr)
