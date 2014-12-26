__author__ = 'jzelar'

class Tile(object):
    entries = []
    type = -1
    typeMap = {'important': 'bg-yellow', 'information': 'bg-red', 'event': 'bg-lightBlue', 'other': 'bg-green'}

    def addEntry(self, entry):
        self.entries.append(entry)

    def setType(self, type):
        self.type = type

    def addEntries(self, entries):
        self.entries = entries