__author__ = 'hakonbogen'
## model for a part of formatted source code
## used when telling formatter what characters to write next

class SourceCodePart:
    lastReadKeyWord = None
    characterAtIndex0 = None
    characterAtIndex1 = None
    characterAtIndex2 = None
    numberOfCharactersParserShouldSkip = -1

    def __init__(self,characterAtIndex0,characterAtIndex1,characterAtIndex2,numberOfCharctersParserShouldSkip):
        self.characterAtIndex0 = characterAtIndex0
        self.characterAtIndex1 = characterAtIndex1
        self.characterAtIndex2 = characterAtIndex2
        self.numberOfCharactersParserShouldSkip = numberOfCharctersParserShouldSkip


