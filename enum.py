class Enum(object):
    def __init__(self, tupleList):
        self.tupleList = tupleList

    def __getattr__(self, name):
        return self.tupleList.index(name)