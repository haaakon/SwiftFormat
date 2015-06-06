import SourceLine
import sys
import copy
import os
import argparse

class Enum(object):
    def __init__(self, tupleList):
        self.tupleList = tupleList

    def __getattr__(self, name):
        return self.tupleList.index(name)


Statement = Enum(('while','for',
                 'dictionary',
                 "comment",
                 "implementation",
                 "END",
                 'IMPORT',
                 "EMPTYLINE",
                 "UNKNOWN"))

Character = Enum(("SPACE"
                            ,"UNKNOWN"))

class FileReader:
    """A simple example class"""
    lastReadCharacter = ""
    lastReadLine = ""
    currentStatement = Statement.UNKNOWN
    lastReadStatement = Statement.UNKNOWN

    currentCharacter = Character.UNKNOWN
    lastReadCharacter = Character.UNKNOWN

    currentIndentationLevel = 0
    numberOfSpacesPerIndentationLevel = 4
    lineNumber = 1

    isInsideClosureVariable = False
    isInsideMultilineComment = False
    sourceCodeLineObjects = []
    rawDataFromFile = ""

    def reset(self):
        self.lineNumber = 1
        self.currentIndentationLevel = 0
        self.numberOfSpacesPerIndentationLevel = 4
        self.lastReadCharacter = Character.UNKNOWN
        self.currentStatement = Statement.UNKNOWN
        self.lastReadStatement = Statement.UNKNOWN

    def __init__(self,file):
        self.rawDataFromFile = file.read()
        file.close()

    def formattedSource(self):
        return self.parseSourceFromString(self.rawDataFromFile)

    def compareTestCasesInReadFile(self):
        unFormattedSource = ""
        formattedSource = ""
        readingFirstPart = True
        for line in self.rawDataFromFile.split("\n"):
            if "@@@" in line:
                readingFirstPart = False
            else:
                if readingFirstPart:
                    unFormattedSource = unFormattedSource + line + "\n"
                else:
                    formattedSource = formattedSource + line + "\n"
        parsedSource = self.parseSourceFromString(unFormattedSource)
        return parsedSource,formattedSource

    def readToString(self):
        fileString = ""
        for line in file:
            parsedLine = self.parseLine(line)
            fileString = "%s%s" % (fileString, parsedLine)

    def parseSourceFromString(self,sourceCode):
        sourceLines = sourceCode.split("\n")
        fileString = ""
        for line in sourceLines:
            parsedLine = self.parseLine(line)
            fileString = "%s%s\n" % (fileString, parsedLine.formattedContent)
        fileString = fileString[:-1]
        return fileString

    def addLeadingSpacesToString(self,numberOfLeadingSpaces,string):
        newString = string
        for i in range(0,numberOfLeadingSpaces):
            newString = " %s" % newString
        return newString

    def addOrRemoveWhiteSpace(self,sourceCodeLine):
        # se if line needs to be further split up
        unalteredline = copy.copy(sourceCodeLine.formattedContent)

        originalLine = sourceCodeLine.formattedContent.lstrip()
        originalLine = sourceCodeLine.formattedContent.rstrip()
        isComment = False
        lines = originalLine.split("\n")
        newConstructedLine = ""
        for line in lines:
            # just strip away all unecessary whitespace
            line = line.rstrip()
            line = line.lstrip()

            if sourceCodeLine.lineType == SourceLine.LineType.comment:
                sourceCodeLine.formattedContent = originalLine
                newConstructedLine = newConstructedLine + originalLine + '\n'
                self.sourceCodeLineObjects.append(sourceCodeLine)
                continue
            if not line:
                sourceCodeLine.formattedContent = originalLine
                self.sourceCodeLineObjects.append(sourceCodeLine)
                newConstructedLine = newConstructedLine + originalLine + '\n'
                continue
            if "*/" in line:
                self.isInsideMultilineComment = False
            if "/*" in line or self.isInsideMultilineComment:
                sourceCodeLine.formattedContent = originalLine
                self.isInsideMultilineComment = True
                newConstructedLine = newConstructedLine + unalteredline + '\n'
                sourceCodeLine.lineType = SourceLine.LineType.comment
                numberOfWhiteSpaceNeeded =  (self.numberOfSpacesPerIndentationLevel * self.currentIndentationLevel)
                line = self.addLeadingSpacesToString(numberOfWhiteSpaceNeeded,line)
                sourceCodeLine.formattedContent = line
                self.sourceCodeLineObjects.append(sourceCodeLine)

                continue

            indentationLeveDecrease = line.count('}')
            if indentationLeveDecrease > 0:
                self.currentIndentationLevel -= 1
            numberOfWhiteSpaceNeeded =  (self.numberOfSpacesPerIndentationLevel * self.currentIndentationLevel)
            if sourceCodeLine.lineType == SourceLine.LineType.closureToVariable:
                self.isInsideClosureVariable = True
            if sourceCodeLine.lineType == SourceLine.LineType.endOfClosure and self.isInsideClosureVariable:
                numberOfWhiteSpaceNeeded =+ self.numberOfSpacesPerIndentationLevel
                self.isInsideClosureVariable = False

            line = self.addLeadingSpacesToString(numberOfWhiteSpaceNeeded,line)
            sourceCodeLine.formattedContent = line
            newConstructedLine = newConstructedLine + line + '\n'
            indentationLevelIncrease = line.count('{')
            if indentationLevelIncrease > 0 and len(lines) == 1:
                self.currentIndentationLevel +=1
                newConstructedLine = newConstructedLine + ""
            elif line.count('{') > 0:
                self.currentIndentationLevel += 1
            self.sourceCodeLineObjects.append(sourceCodeLine)
        #remove last newline when more strings were connected
        newConstructedLine = newConstructedLine[:-1]
        sourceCodeLine.formattedContent = newConstructedLine
        return sourceCodeLine

# when there are multiple brackets on a line, or brackets together with words on a line,adds a new line between them
    # { var str = ""


    def indentLine(self,sourceCodeLine):
        indentationLevelDecreaseOrIncrease = sourceCodeLine.numberOfLeftBraces() + sourceCodeLine.numberOfRightBraces()

        if sourceCodeLine.lineType != SourceLine.LineType.comment:
            sourceCodeLine.removeDoubleWhitespace()
        newLine = ""
        if indentationLevelDecreaseOrIncrease > 1:
            sourceCodeLine.splitToMultipleLines()
        if sourceCodeLine.lineType != SourceLine.LineType.comment:
            sourceCodeLine = self.addOrRemoveWhiteSpace(sourceCodeLine)
        else:
            newLine =  sourceCodeLine.formattedContent
        return sourceCodeLine

    def parseLine(self,rawLine):
        sourceCodeLine = SourceLine.Line(rawLine)
        sourceCodeLine = self.indentLine(sourceCodeLine)
        if sourceCodeLine.lineType != SourceLine.LineType.comment:
            sourceCodeLine.fixSpacingBetweenKeywords()
        self.lineNumber +=1
        self.lastReadStatement = self.currentStatement
        return sourceCodeLine

def main(argv):
    parser = argparse.ArgumentParser()
    defineArguments(parser)
    args = parser.parse_args()
    if args.file:
        parsedText = openFile(args.file)
        if args.output:
            writeToFile = open(args.output,'w')
            writeToFile.write(parsedText)
            writeToFile.close()


def defineArguments(parser):
    parser.add_argument('--file', help='the file to auto format')
    parser.add_argument('--output', help='name of file to output formatted source code to')


def openFile(fileName):
    with open(fileName, 'r') as fin:
        fileReader = FileReader(fin)
        formattedSourceCode = fileReader.formattedSource()
        return formattedSourceCode

if __name__ == '__main__':
    main(sys.argv[1:])

