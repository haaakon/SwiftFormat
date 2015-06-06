import format
from sourcecodepart import *
import word
import re

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

class Enum(object):
    def __init__(self, tupleList):
        self.tupleList = tupleList

    def __getattr__(self, name):
        return self.tupleList.index(name)

LineType = Enum(('comment','closureToVariable','closure','endOfClosure','unknown'))


KeyWord = Enum(('string','func'))

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
        if self.lineType == LineType.unknown:
            strippedOfWhitespace = self.content.lstrip()

            if strippedOfWhitespace.startswith("//"):
                self.lineType = LineType.comment
                return

            ###### CLOSURES
            p = re.compile(r'\bin(\b|$)')
            result = p.search(strippedOfWhitespace)
            if result:
                self.lineType = LineType.closureToVariable
                #else:
                #    self.lineType = LineType.closure
            elif "}" in strippedOfWhitespace:
                self.lineType = LineType.endOfClosure

    def numberOfLeftBraces(self):
        if self.lineType != LineType.comment:
            return self.formattedContent.count('}')
        return 0

    def numberOfRightBraces(self):
        if self.lineType != LineType.comment:
            return self.formattedContent.count('{')
        return 0

    def newLinesForBraces(self):
        newLines = ""
        for i in range(0, self.containsStartCurly):
            newLines += "\n"
        self.containsStartCurly = 0
        return newLines

#cleans up spacing between keywords in a line based on a set of given rules
#URLForResource("AstronomyPicture" , withExtension:"momd")   -> URLForResource("AstronomyPicture", withExtension: "momd")

    def fixSpacingBetweenKeywords(self):
        constructedWord = ""
        index = 0
        formattedLine = ""
        skipCharacters = 0
        for character in self.formattedContent:
            if skipCharacters > 0:
                index = index + 1
                skipCharacters = skipCharacters - 1
                continue
            if word.KeyWord.isKeyWordSeparator(character) and len(self.formattedContent) > index + 1:
                currentKeyWord = word.KeyWord(constructedWord,character)
                nextCharacter = self.formattedContent[index + 1]
                nextAfterNextCharacter = ""
                if len(self.formattedContent) < index + 3:
                    nextAfterNextCharacter = ""
                else:
                    nextAfterNextCharacter = self.formattedContent[index + 2]
                sourceCodePart = SourceCodePart(character,nextCharacter,nextAfterNextCharacter,2)
                sourceCodePart.lastReadKeyWord = constructedWord
                formattedPartOfSource = currentKeyWord.addOrRemoveSpaces(sourceCodePart)
                formattedLine = formattedLine + formattedPartOfSource.characterAtIndex0 + formattedPartOfSource.characterAtIndex1 + formattedPartOfSource.characterAtIndex2
                skipCharacters = formattedPartOfSource.numberOfCharactersParserShouldSkip
                constructedWord = ""
            else:
                constructedWord = constructedWord + character
                formattedLine = formattedLine + character
            index = index + 1
        self.formattedContent = formattedLine

    def parseContent(self):
        self.splitToMultipleLines()
        self.removeDoubleWhitespace()

    def removeDoubleWhitespace(self):
        previousCharacter = ""
        parsedCodeLine = ""
        for c in self.formattedContent:
            if c == " ":
                parsedCodeLine = self.removeUnecessaryWhiteSpaceFromLine(parsedCodeLine,c,previousCharacter)
            else:
                parsedCodeLine = parsedCodeLine + c
            previousCharacter = c
        self.formattedContent = parsedCodeLine

    def removeUnecessaryWhiteSpaceFromLine(self,currentParsedLine,currentCharacter,previousCharacter):
        noUnecessaryWhiteSpace = ""
        if previousCharacter == " " and currentCharacter == " ":
            noUnecessaryWhiteSpace = currentParsedLine
        else:
            noUnecessaryWhiteSpace = currentParsedLine + currentCharacter
        return noUnecessaryWhiteSpace

    def splitToMultipleLines(self):
        brackets = 0
        newLine = ""
        endCurlyNumber = 0
        startCurlyNumber = 0
        # go through characters in the line
        for c in self.formattedContent:
            if c == "}":
                #first bracket on a line should not be set to next line
                if brackets == 0:
                    newLine = newLine + c
                else:
                    newLine = newLine + '\n' + c
                brackets += 1
                endCurlyNumber += 1
            elif c == "{":
                if brackets == 0:
                    newLine = newLine + c
                else:
                    newLine = newLine + '\n' + c
                    startCurlyNumber -= 1
                brackets += 1
                startCurlyNumber += 1
            else:
                if c == " ":
                    pass
                else:
                    if startCurlyNumber > 0:
                        newLine = newLine + '\n'
                        startCurlyNumber -= 1
                newLine = newLine + c
        self.formattedContent = newLine

