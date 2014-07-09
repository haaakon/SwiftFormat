import format
class Enum(object):
    def __init__(self, tupleList):
        self.tupleList = tupleList

    def __getattr__(self, name):
        return self.tupleList.index(name)

LineType = Enum(('comment','unknown'))


class Line:
    containsStartCurly = 0
    containsEndCurly = 0
    lineType = LineType.unknown
    content = ""
    formattedContent = ""
    keyWord = ""
    def __init__(self, content):
        self.content = content
        self.formattedContent = content
        self.identifyLineType()

    def identifyLineType(self):
        if self.lineType() == LineType.unknown:
            strippedOfWhitespace = self.content.lstrip()
            if strippedOfWhitespace.startswith("//"):
                self.lineType = LineType.comment

    def numberOfLeftBraces(self):
        if self.lineType != LineType.comment:
            return self.formattedContent.count('}')
        return 0
    def numberOfRightBraces(self):
        if self.lineType != LineType.comment:
            return self.formattedContent.count('{')
        return 0
    def identifyKeyWord(self):
        if self.keyWord == "for":
            kd = ""
        elif self.keyWord == "if":
            ak = ""

    def newLinesForBraces(self):
        newLines = ""
        for i in range(0, self.containsStartCurly):
            newLines += "\n"
        self.containsStartCurly = 0
        return newLines

