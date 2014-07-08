class Line:
    containsStartCurly = 0
    containsEndCurly = 0
    keyWord = ""

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

