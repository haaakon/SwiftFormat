# repse
import enum
from sourcecodepart import *
from formattingrule import *
keyWordType = enum.Enum(('while','for',
                 'string',
                 'method',
                 "methodArgument",
                 "class",
                 "macro",
                 'IMPORT',
                 "EMPTYLINE",
                 "anyone",
                 "unknown"))
keywordSeparators = ['"',"'",")",":",".",","," "]

class KeyWord:
    type = keyWordType.unknown
    keywordSeparator = ""
    text = ""

    @classmethod
    def isKeyWordSeparator(cls,character):
        if character in keywordSeparators:
            return True
        else:
            return False
        #URLForResource("AstronomyPicture" , withExtension:"momd")   -> URLForResource("AstronomyPicture", withExtension: "momd")

    def addOrRemoveSpaces(self,sourceCodePart):
        if self.type == keyWordType.string:
            return self.formattingForString(sourceCodePart)
        if self.type == keyWordType.methodArgument:
            return FormattingRule.formatMethodArgument(sourceCodePart)
        if self.type == keyWordType.method:
            return FormattingRule.formatMethod(sourceCodePart)
        if self.type == keyWordType.anyone:
            return FormattingRule.formatGeneric(sourceCodePart)
        return SourceCodePart(sourceCodePart.characterAtIndex0,sourceCodePart.characterAtIndex1,sourceCodePart.characterAtIndex2,2)

    def formattingForString(self,sourceCodePart):
        # we are dealing with a list or argument:
        if self.anyIsComma(sourceCodePart.characterAtIndex1,sourceCodePart.characterAtIndex2):
            return FormattingRule.formatStringInList(sourceCodePart)
        else:
            return FormattingRule.formatMethod(sourceCodePart)
    def formattingForAnyone(self,currentcharacter,nextCharacter,nextAfterNextCharacter):
        pass
    def anyIsComma(self,character,character2):
        if character == ",":
            return True
        if character2 == ",":
            return True
        return False

    def identifyKeyWord(self):
        if self.keywordSeparator == '"':
            self.type = keyWordType.string
        elif self.keywordSeparator == ':':
            self.type = keyWordType.methodArgument
        elif self.keywordSeparator == ")":
            self.type = keyWordType.method
        elif self.keywordSeparator == " ":
            self.type = keyWordType.anyone
        else:
            self.type = keyWordType.unknown
        #if self.keywordSeparator == ":":
        #    self.type = keyWordType.methodArgument
        pass

    def __init__(self, keyWord,keywordSeparator):
        self.keyWord = keyWord
        self.keywordSeparator = keywordSeparator
        self.identifyKeyWord()
