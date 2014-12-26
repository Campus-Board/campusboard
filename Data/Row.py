__author__ = 'jzelar'

class Row(object):
    tiles = []
    numTiles = 0

    def addTile(self, tile):
        #if (self.numTiles > 2):
        #    return False
        self.tiles.append(tile)
        #self.numTiles += 1