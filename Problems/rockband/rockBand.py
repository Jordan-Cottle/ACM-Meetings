from itertools import cycle


class BandMember:
    def __init__(self, songs):
        self.setLength = 0
        self.trackIndex = -1
        
        self.songList = [int(song) for song in songs]
        self.songPreferences = {int(song): index+1 for index, song in enumerate(songs)}

    def playSong(self, song):
        pos = self.songPreferences[song]
        if pos > self.setLength:
            self.setLength = pos

    def getSong(self):
        if self.trackIndex == self.setLength-1:
            self.setLength += 1
            self.trackIndex += 1
            return self.songList[self.trackIndex]
        else:
            self.trackIndex += 1
            return self.songList[self.trackIndex]
    
    def getSet(self):
        return sorted(self.songList[:self.setLength])
    
    def __str__(self):
        return f'{str(self.songPreferences)}: {self.setLength}'

def validSet(bandMembers):
    return bandMembers[0].setLength == bandMembers[-1].setLength != 0
        

members, song = (int(num) for num in input().split())
bandMembers = []

for i in range(int(members)):
    bandMembers.append(BandMember(input().split()))

for bandMember in cycle(bandMembers):
    song = bandMember.getSong()
    for bandMember in bandMembers:
        bandMember.playSong(song)
    
    if validSet(bandMembers):
        break

trackSet = bandMembers[0].getSet()
print(len(trackSet))
print(*trackSet, sep=' ')