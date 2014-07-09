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
            fileString = "%s%s\n" % (fileString, parsedLine)
        fileString = fileString[:-1]
        return fileString

    def identifyLine(self,sourceCodeLine):
        lineArray = line.split(" ")
        firstWord = lineArray[0]
        #print(firstWord)
        if firstWord == "#import":
            self.currentStatement = Statement.IMPORT
        if firstWord.isspace():
            noWhiteSpace = line.lstrip()
            if len(noWhiteSpace) == 0:
                self.currentStatement = Statement.EMPTYLINE
            else:
                self.identifyLine(noWhiteSpace)
        else:
            self.currentStatement = Statement.UNKNOWN


    #def updateIndentationLevel(self,line):
        #self.currentIndentationLevel +=indentationLevelIncrease



    def addOrRemoveWhiteSpace(self,originalLine):
        # se if line needs to be further split up
        originalLine = originalLine.lstrip()
        originalLine = originalLine.rstrip()
        isComment = False
        lines = originalLine.split("\n")
        newConstructedLine = ""
        for line in lines:
            # just strip away all unecessary whitespace
            line = line.rstrip()
            line = line.lstrip()

            if line.startswith("//"):
                newConstructedLine = newConstructedLine + originalLine + '\n'
                continue

            indentationLeveDecrease = line.count('}')
            if indentationLeveDecrease > 0:
                self.currentIndentationLevel -= 1
            numberOfWhiteSpaceNeeded =  (self.numberOfSpacesPerIndentationLevel * self.currentIndentationLevel)
            line = self.addLeadingSpacesToString(numberOfWhiteSpaceNeeded,line)
            newConstructedLine = newConstructedLine + line + '\n'
            indentationLevelIncrease = line.count('{')
            if indentationLevelIncrease > 0 and len(lines) == 1:
                self.currentIndentationLevel +=1
                newConstructedLine = newConstructedLine + ""
            elif line.count('{') > 0:
                self.currentIndentationLevel += 1
        #remove last newline when more strings were connected
        newConstructedLine = newConstructedLine[:-1]
        return newConstructedLine
# when there are multiple brackets on a line, or brackets together with words on a line,adds a new line between them
    # { var str = ""
    def addNewLineBeforeBraces(self,line):
        brackets = 0
        newLine = ""
        parsedLine = SourceLine.Line()

        # go through characters in the line
        for c in line:
            if c == "}":
                #first bracket on a line should not be set to next line
                if brackets == 0:
                    newLine = newLine + c
                else:
                    newLine = newLine + '\n' + c
                brackets += 1
                parsedLine.containsEndCurly += 1
            elif c == "{":
                if brackets == 0:
                    newLine = newLine + c
                else:
                    newLine = newLine + '\n' + c
                    parsedLine.containsStartCurly -= 1
                brackets += 1
                parsedLine.containsStartCurly += 1
            else:
                if c == " ":
                    parsedLine.identifyKeyWord()
                    # do something with keyword ?
                    parsedLine.keyWord = ""
                else:
                    if parsedLine.containsStartCurly > 0:
                        newLine = newLine + '\n'
                        parsedLine.containsStartCurly -= 1
                newLine = newLine + c
        return newLine

    def parseKeyWordsInLine(self,parsingLine):
        previousCharacter = ""
        parsedCodeLine = ""
        parsedLine = SourceLine.Line()
        for c in parsingLine:
            if c == " ":
                parsedLine.identifyKeyWord()
                # do something with keyword ?
                parsedLine.keyWord = ""
                parsedCodeLine = self.removeUnecessaryWhiteSpaceFromLine(parsedCodeLine,c,previousCharacter)
            else:
                parsedCodeLine = parsedCodeLine + c
            previousCharacter = c
        return parsedCodeLine

    def removeUnecessaryWhiteSpaceFromLine(self,currentParsedLine,currentCharacter,previousCharacter):
        noUnecessaryWhiteSpace = ""
        if previousCharacter == " " and currentCharacter == " ":
            noUnecessaryWhiteSpace = currentParsedLine
        else:
            noUnecessaryWhiteSpace = currentParsedLine + currentCharacter
        return noUnecessaryWhiteSpace

    def addLeadingSpacesToString(self,numberOfLeadingSpaces,string):
        newString = string
        for i in range(0,numberOfLeadingSpaces):
            newString = " %s" % newString
        return newString

  def indentLine(self,sourceCodeLine):
        newLine = sourceCodeLine.content
        indentationLevelDecreaseOrIncrease = sourceCodeLine.numberOfLeftBraces() + sourceCodeLine.numberOfRightBraces()
        newLine = self.parseKeyWordsInLine(newLine)
        if indentationLevelDecreaseOrIncrease > 1:
            newLine = self.addNewLineBeforeBraces(line)
            #line = "%s - %i - LSPACE: %i whspcaneeded: %i" % (line,self.currentIndentationLevel, leading_spaces,numberOfWhiteSpaceNeeded)
        #self.currentIndentationLevel += indentationLevelIncrease
        newLine = self.addOrRemoveWhiteSpace(newLine)
        return newLine

    def alterAndWriteLine(self,sourceCodeLine):

        # first check if line should be saved anyway
        alteredLine = ""
        if self.currentStatement == Statement.EMPTYLINE and self.lastReadStatement == Statement.EMPTYLINE:
            ks = ""
        elif self.currentStatement == Statement.EMPTYLINE:
            ks = ''
        else:
            self.indentLine(sourceCodeLine)
        return sourceCodeLine

    def parseLine(self,rawLine):
        sourceCodeLine = SourceLine.Line(rawLine)
        parsedLine = self.alterAndWriteLine(sourceCodeLine)
        self.lineNumber +=1
        self.lastReadStatement = self.currentStatement
        return parsedLine

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



if __name__ == "__main__":
   main(sys.argv[1:])