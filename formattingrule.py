from sourcecodepart import *
import word
class FormattingRule:
    ###
    ### formats to this format: ["string", "string2", "string3"]
    ###
    @classmethod
    def formatStringInList(cls,sourceCodePart):
        if sourceCodePart.characterAtIndex2 != " ":
            if sourceCodePart.characterAtIndex2 == ",":
                return SourceCodePart(sourceCodePart.characterAtIndex0,",","",2)
            else:
                return SourceCodePart(sourceCodePart.characterAtIndex0,","," ",1)
        return SourceCodePart(sourceCodePart.characterAtIndex0,",",sourceCodePart.characterAtIndex2,2)
    @classmethod
    def formatMethodArgument(cls,sourceCodePart):
        if sourceCodePart.characterAtIndex1 == " ":
            return SourceCodePart(sourceCodePart.characterAtIndex0,sourceCodePart.characterAtIndex1,sourceCodePart.characterAtIndex2,2)
        else:
            return SourceCodePart(sourceCodePart.characterAtIndex0," ",sourceCodePart.characterAtIndex1,1)
    @classmethod
    def formatMethod(cls,sourceCodePart):
        if sourceCodePart.characterAtIndex1 == " ":
            if word.KeyWord.isKeyWordSeparator(sourceCodePart.characterAtIndex2):
                return SourceCodePart(sourceCodePart.characterAtIndex0,"",sourceCodePart.characterAtIndex2,2)
            else:
                return SourceCodePart(sourceCodePart.characterAtIndex0," ",sourceCodePart.characterAtIndex2,2)
        else:
            return SourceCodePart(sourceCodePart.characterAtIndex0,"",sourceCodePart.characterAtIndex1,1)
    #generic case for setting spaces
    @classmethod
    def formatGeneric(cls,sourceCodePart):
        if sourceCodePart.characterAtIndex1 == ")":
            if sourceCodePart.lastReadKeyWord:
                return SourceCodePart("",sourceCodePart.characterAtIndex1,sourceCodePart.characterAtIndex2,2)
        return SourceCodePart(sourceCodePart.characterAtIndex0,sourceCodePart.characterAtIndex1,sourceCodePart.characterAtIndex2,2)

