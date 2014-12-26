__author__ = 'jzelar'

class Entry(object):
    title = ""
    content = ""
    id = ""

    def __init__(self, title, content, id):
        self.title = title
        self.content = content
        self.id = id