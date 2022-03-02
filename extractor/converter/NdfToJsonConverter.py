
from enum import Enum
from pprint import pprint
from sre_parse import State
import string

# Helper class for NdfToJsonConverter that holds the possible states of it's statemachine
class States(Enum):
    IN_BETWEEN_USEFUL_DATA = 1
    ON_EXPORT_KEYWORD = 2 # "export"
    ON_OBJECT_NAME = 3 # "Descriptor_Unit_Truck_WC52_US"
    ON_BASE_TYPE_EQUALS_KEYWORD = 4 # "=" or "is"
    ON_OBJECT_BASE_TYPE_NAME = 5 # "TEntityDescriptor"

    ON_OBJECT_OPENING_BRACKET = 6 # "("
    ON_OBJECT_CLOSING_BRACKET = 7 # ")"

    ON_ARRAY_OPENING_BRACKET = 8 # "[", ","
    ON_ARRAY_CLOSING_BRACKET = 9 # "]"

    ON_ARRAY_FIELD_NAME = 13 # "NilDescriptorIfCadavre,"
    
    ON_OBJECT_FIELD_NAME = 10 # "DescriptorId"
    ON_VALUE_EQUALS_KEYWORD = 11 # "="
    ON_FIELD_VALUE_STRING = 12 # "GUID:{85c06d35-a1ee-49ae-9b80-7356bdbdc5fd}" or "'foo bar'"

    ON_MAP_OPENING = 14 # "MAP ["
    ON_MAP_ITEM = 15 # "( Foo, Bar ),"
    ON_MAP_CLOSING_BRACKET = 16 # "]"

    ON_EOF = 1000

# An internal object representing a partially filled json object
class DataObject:
    def __init__(self):
        self.parent = None
        self.type = "object"
        self.fields = {}
        self.currentField = None

# An internal object representing a partially filled json array
class DataArray:
    def __init__(self):
        self.type = "array"
        self.parent = None
        self.items = []

# An internal object representing the statemachine's current state
class CurrentData:
    def __init__(self):
        # The index of the current character in the file/text that we are parsing
        self.currentPosition = 0
        # Holds certain strings temporarily while we parse them
        # Mostly used to workaround inconsistent formatting in the raw file/text and
        # allow it to be parsed as if it wasn't inconsistent.
        self.remappedRawString = None
        # What the state machine thinks the currently processed bit of data/text is
        self.state = States.IN_BETWEEN_USEFUL_DATA
        # Holds everything that we parsed since the parsing began. We assume that the whole file is actually supposed to be a list.
        self.currentPartialData = DataArray()
        # We start at nest level 1
        self.currentNestLevel = 1
        # We are currently editing this DataArray or DataObject
        self.currentlyEditedItem = None
        # We are currently editing/parsing this field
        self.fieldNameCandidate = None
        # We are currently editing/parsing this string value
        self.fieldValueCandidate = None

class ValueFormatters:
    # The keys of the dict that are created from "MAP []"s
    def formatMapKey(rawValue):
        return rawValue.strip("(, \n")
    # The values of the dict that are created from "MAP []"s
    def formatMapValue(rawValue):
        return rawValue.strip("), \n")
    def formatStringFieldValue(rawValue):
        return rawValue.strip("'").strip(',')

# Convert and NDF formatted file/text into a json-like data structure for easier parsing
class NdfToJsonConverter:
    def __init__(self):
        self.collectDebugMessages = True

    def convert_file(self, file):
        if not file:
            raise FileNotFoundError

        with open(file, 'r') as file:
            return self.convert_ndf_text(file.read())

    def convert_ndf_text(self, text: string):
        if not text:
            raise Exception

        # https://stackoverflow.com/a/1884277
        def find_nth(haystack, needle, n, offset = 0):
            start = haystack.find(needle, offset)
            while start >= 0 and n > 1:
                start = haystack.find(needle, start+len(needle))
                n -= 1
            return start

        # Returns true if there are no spaces in `str` around the `position`
        # Used for telling apart "Foo,Bar" and "Foo, Bar"
        def noSpacesAround(str, position):
            if not str:
                return True
            if position < 0:
                return True
            firstPos = position - 1
            secondPos = position + 1

            ret = True

            if 0 <= firstPos <= len(str):
                if str[firstPos] == ' ':
                    ret = False
            if 0 <= secondPos <= len(str):
                if str[secondPos] == ' ':
                    ret = False
            return ret

        currentData = CurrentData()
        textLength = len(text)
        # Collected in unittests only (controlled by `self.collectDebugMessages`).
        # Declared here so that it can be used in the `debugMessage()` helper function properly
        debugMessagesThisLoop = []

        def debugMessage(message):
            if self.collectDebugMessages:
                debugMessagesThisLoop.append(message)

        # Parses the next term/word/token from the file/text
        # Returns non-empty string(!) when we are not at EOF
        # Returns False when we are at EOF
        def getNextWord():
            while currentData.currentPosition < textLength - 1:
                if not currentData.remappedRawString:
                    # Find the next whitespace or eol character
                    whitespacePosition = text.find(' ', currentData.currentPosition + 1)
                    if (whitespacePosition >= 0):
                        # When we have a bunch of whitespaces then we can skip ahead for a significant performance boost
                        # This however will mean that our "word" will have a bunch of whitespaces at it's end that will need to be stripped
                        while whitespacePosition < textLength and text[whitespacePosition] == ' ':
                            whitespacePosition += 1
                    newlinePosition = text.find('\n', currentData.currentPosition + 1)

                    # If one of them is not found then use the position of the file's end 
                    # (so we don't skip the very last word of the file)
                    if newlinePosition == -1:
                        newlinePosition = textLength -1
                    if whitespacePosition == -1:
                        whitespacePosition == textLength -1
                    if newlinePosition >= whitespacePosition:
                        wordEndPosition = whitespacePosition
                    else:
                        wordEndPosition = newlinePosition
                    if wordEndPosition == -1:
                        wordEndPosition = textLength - 1

                    # Find the next potential word
                    # Edge cases:
                    # - might contain a single whitespace or a single eol character
                    # - might contain "//" which is the start of a commented line
                    # - might contain syntax like "Foo=~/Bar" which is supposed to be mapped as if it were properly spaced like "Foo = ~/Bar"
                    # - might contain a partial "((0)" which is actually supposed to be mapped into a single string like "((0) * Foo)"
                    # - might contain a partial "(0" which is actually supposed to be mapped into a single string like "(0 * Foo)"
                    # - might contain a partial "Foo(Bar=~/Baz" which is supposed to be mapped like "Foo ( Bar = ~/Baz  Bar2 = ~/Baz2 )"
                    word = text[currentData.currentPosition:wordEndPosition].strip()
                
                    # If we find "//" or a word starting with "//" then skip to the next line
                    if word and len(word) >= 2 and word[0:2] == "//":
                        newlinePosition = text.find('\n', currentData.currentPosition + 1)
                        if newlinePosition == -1:
                            newlinePosition = textLength -1
                        wordEndPosition = newlinePosition
                        word = None        

                    
                    if word:
                        # The `Foo(Foo2=~/Bar2  Foo3=~/Bar3)` syntax
                        if word.find("(") > 0 and word.count("(") > word.count(")") and noSpacesAround(word, word.find("(")):
                            end = find_nth(text, ")", word.count("("), currentData.currentPosition)
                            if end >= 0:
                                wordEndPosition = end+1
                                currentData.remappedRawString = text[currentData.currentPosition:wordEndPosition].replace('=', ' = ').replace('(', ' ( ').replace(')', ' ) ')
                                word = None
                            else:
                                # idk
                                pass
                        # The "Foo=~/Bar" syntax
                        else:
                            if word.find('=') > 0:
                                currentData.remappedRawString = word.replace('=', ' = ')    
                                word = None                  
                        
                        
                    if word and len(word) >= 2 and word[0] == "(":
                        # The `((80) * Metre) )` but split into `"((80)", "*", "Metre)" and ")"` syntax
                        # Also the `(0 * Seconde)` but split into `"(0", "*", and "Seconde)"` syntax
                        if word[1] == "(" or word[1].isdigit():
                            end = find_nth(text, ")", word.count("("), currentData.currentPosition)
                            if end >= 0:
                                wordEndPosition = end+1
                                word = text[currentData.currentPosition:wordEndPosition].strip()
                            else:
                                # idk
                                pass
                        

                    # Make sure to remember where we are at
                    currentData.currentPosition = wordEndPosition
                else:
                    # We are taking a break from parsing the original raw text because we have a string that was remapped from it to
                    # allow for better parsing. e.g. "Foo=~Bar" -> "Foo = ~Bar"
                    # In this case we are removing the start of this remapped text until it fully disappears

                    whitespacePosition = currentData.remappedRawString.find(' ')
                    if whitespacePosition == -1:
                        whitespacePosition = len(currentData.remappedRawString)
                    word = currentData.remappedRawString[0:whitespacePosition]
                    # Remove the part of the remappedRawString that we just consumed
                    currentData.remappedRawString = currentData.remappedRawString[whitespacePosition:].strip()
                    word = word.strip()

                # If we still have a valid word after handling all the edge cases, then we are going to use that. 
                # Otherwise we keep on looping until we find a valid non-empty word or EOF
                if word:
                    return word

            return False

        # Helper function for getting a reference to the DataObject/DataArray that we are currently filling
        def getCurrentlyEditedItem():
            return currentData.currentlyEditedItem
        
        # Helper function for setting the DataObject/DataArray that we are currently filling
        def setCurrentlyEditedItem(item):
            debugMessage('Setting currently edited item to an '+item.type)
            currentData.currentlyEditedItem = item
        
        # Helper function for creating DataObject/DataArray instances under the currently edited one and setting it's `parent` field correctly
        # @param type "object"|"array"
        # @param nameInParentObjectFieldList 
        #       - if the currentlyEditedItem is an object, then the newly created item will be stored in it's field list under this key
        #       - if the currentlyEditedItem is an array, then the newly created item will be added to it, and the new item's `_type_name` will be set to this value
        # @param optionalItemBaseTypeName when provided, it will set the newly created item's `_base_type_name` field to this value
        def createAndStoreNestedItem(type, nameInParentObjectFieldList = None, optionalItemBaseTypeName = None):
            if type == "object":
                newItem = DataObject()
            else:
                newItem = DataArray()

            currentlyEditedItem = getCurrentlyEditedItem()


            newItem.parent = currentlyEditedItem

            if newItem.type == "object":
                if currentlyEditedItem.type == "object":
                    debugMessage("Creating new nested object and storing it under '"+nameInParentObjectFieldList+"'")
                else:
                    newItem.fields['_type_name'] = nameInParentObjectFieldList
                    debugMessage("Creating new nested object and setting it's '_type_name' field to '"+nameInParentObjectFieldList+"'")
                
                if optionalItemBaseTypeName:
                    newItem.fields['_base_type_name'] = optionalItemBaseTypeName
                    debugMessage("Setting '_base_type_name' to '"+optionalItemBaseTypeName+"'")
            else:
                debugMessage("Creating new nested array and storing it under '"+nameInParentObjectFieldList+"'")

            if currentlyEditedItem.type == 'object':
                currentlyEditedItem.fields[nameInParentObjectFieldList] = newItem
            else:    
                currentlyEditedItem.items.append(newItem)

                
            
            return newItem

        # Used for creating the output data structure. 
        # Creates native dicts/lists from our internal DataObject/DataArray types
        def formatPartialData(partialData):
            if not partialData:
                return None

            def formatDataIfNeeded(childObject):
                if isinstance(childObject, DataObject) or isinstance(childObject, DataArray):
                    return formatPartialData(childObject)
                else:
                    return childObject


            if partialData.type == "object":
                if partialData.fields:
                    val = dict(map(lambda kv: (kv[0], formatDataIfNeeded(kv[1])), partialData.fields.items()))
                else:
                    val = {}
            else:
                if partialData.items:
                    val = list(map(formatDataIfNeeded, partialData.items))
                else:
                    val = []
            return val

        # Initially we want to edit this empty DataArray object that was initialized in `currentData.currentPartialData`
        if not currentData.currentlyEditedItem and currentData.currentPartialData:
            currentData.currentlyEditedItem = currentData.currentPartialData


        nextWord = getNextWord()
        while nextWord != False:

            debugMessagesThisLoop = []
           
            if currentData.state == States.IN_BETWEEN_USEFUL_DATA:
                if nextWord == "export":
                    currentData.state = States.ON_EXPORT_KEYWORD
            elif currentData.state == States.ON_EXPORT_KEYWORD:
                if nextWord == "is" or nextWord == "=":
                    currentData.state = States.ON_BASE_TYPE_EQUALS_KEYWORD
                elif nextWord == "(":
                    currentData.state = States.ON_OBJECT_OPENING_BRACKET
                else:
                    currentData.fieldNameCandidate = nextWord
                    currentData.fieldValueCandidate = None
            elif currentData.state == States.ON_BASE_TYPE_EQUALS_KEYWORD:
                if nextWord == "(":
                    currentData.state = States.ON_OBJECT_OPENING_BRACKET
                else:
                    currentData.fieldValueCandidate = nextWord
            elif currentData.state == States.ON_OBJECT_OPENING_BRACKET:
                item = createAndStoreNestedItem('object', currentData.fieldNameCandidate, currentData.fieldValueCandidate)
                currentData.fieldNameCandidate = None
                currentData.fieldValueCandidate = None
                setCurrentlyEditedItem(item)
                
                currentData.currentNestLevel += 1
                if nextWord == ')' or nextWord == '),':
                    currentData.state = States.ON_OBJECT_CLOSING_BRACKET
                else:
                    item.currentField = nextWord
                    currentData.fieldNameCandidate = nextWord
                    currentData.state = States.ON_OBJECT_FIELD_NAME
            elif currentData.state == States.ON_ARRAY_OPENING_BRACKET:
                item = createAndStoreNestedItem('array', getCurrentlyEditedItem().currentField)
                setCurrentlyEditedItem(item)

                

                currentData.currentNestLevel += 1

                if nextWord == ']' or nextWord == '],':
                    currentData.state = States.ON_ARRAY_CLOSING_BRACKET
                else:
                    currentData.fieldNameCandidate = nextWord
                    currentData.fieldValueCandidate = None

                    currentData.state = States.ON_ARRAY_FIELD_NAME
            elif currentData.state == States.ON_ARRAY_FIELD_NAME:
                item = getCurrentlyEditedItem()

                if nextWord != '(':
                    if currentData.fieldNameCandidate:
                        item.items.append(ValueFormatters.formatStringFieldValue(currentData.fieldNameCandidate))
                        currentData.fieldNameCandidate = None
                        currentData.fieldValueCandidate = None

                if nextWord == '(':
                    currentData.state = States.ON_OBJECT_OPENING_BRACKET
                elif nextWord == ']' or nextWord == '],':
                    currentData.state = States.ON_ARRAY_CLOSING_BRACKET
                else:
                    currentData.fieldNameCandidate = nextWord
                    currentData.fieldValueCandidate = None

                    # currentData.state = States.ON_ARRAY_FIELD_NAME
            elif currentData.state == States.ON_OBJECT_FIELD_NAME:
                if nextWord == '=':
                    currentData.state = States.ON_VALUE_EQUALS_KEYWORD
                # elif nextWord == "(":
                #     currentData.state = States.ON_OBJECT_OPENING_BRACKET
                # elif nextWord == "[":
                #     currentData.state = States.ON_ARRAY_OPENING_BRACKET
                # else:
                #     if currentData.fieldNameCandidate:
                #         item = getCurrentlyEditedItem()
            elif currentData.state == States.ON_VALUE_EQUALS_KEYWORD:
                # if ( elseif [
                item = getCurrentlyEditedItem()
                if nextWord == '[':
                    currentData.state = States.ON_ARRAY_OPENING_BRACKET
                elif nextWord == "MAP":
                    currentData.state = States.ON_MAP_OPENING
                elif item.type == 'object':
                    currentData.fieldValueCandidate = nextWord
                    currentData.state = States.ON_FIELD_VALUE_STRING
            elif currentData.state == States.ON_MAP_OPENING:
                if nextWord == "[":
                    # Ignore the "[" character of "MAP [ "
                    pass
                elif nextWord == "[]" or nextWord == "[]," or nextWord == "]" or nextWord == "],":
                    item = createAndStoreNestedItem('object', getCurrentlyEditedItem().currentField)
                    currentData.state = States.ON_MAP_CLOSING_BRACKET
                else:
                    item = createAndStoreNestedItem('object', getCurrentlyEditedItem().currentField)
                    setCurrentlyEditedItem(item)
                    currentData.state = States.ON_MAP_ITEM

                    currentData.fieldNameCandidate = ValueFormatters.formatMapKey(nextWord)
                    currentData.fieldValueCandidate = None
            elif currentData.state == States.ON_MAP_ITEM:
                if nextWord == "(":
                    # Ignore the "(" of "( foo, bar ),"
                    pass
                elif nextWord == ")" or nextWord == "),":
                    # Ignore the ")" or ")," of "( foo, bar ),"

                    item = getCurrentlyEditedItem()
                    item.fields[currentData.fieldNameCandidate] = currentData.fieldValueCandidate
                    currentData.fieldNameCandidate = None
                    currentData.fieldValueCandidate = None
                elif nextWord == "]" or nextWord == "],":
                    currentData.state = States.ON_MAP_CLOSING_BRACKET
                else:
                    if not currentData.fieldNameCandidate:
                        currentData.fieldNameCandidate = ValueFormatters.formatMapKey(nextWord)
                    else:
                        if not currentData.fieldValueCandidate:
                            currentData.fieldValueCandidate = ValueFormatters.formatMapValue(nextWord)
                        else:
                            currentData.fieldValueCandidate += " " + ValueFormatters.formatMapValue(nextWord)
                    if nextWord[-1:] == ")" or nextWord[-2:] == "),":
                        item = getCurrentlyEditedItem()
                        item.fields[currentData.fieldNameCandidate] = currentData.fieldValueCandidate
                        currentData.fieldNameCandidate = None
                        currentData.fieldValueCandidate = None
            elif currentData.state == States.ON_MAP_CLOSING_BRACKET:
                currentData.fieldNameCandidate = None
                currentData.fieldValueCandidate = None
                if nextWord == ')' or nextWord == '),':
                        currentData.state = States.ON_OBJECT_CLOSING_BRACKET
                elif nextWord == ']' or nextWord == '],':
                        currentData.state = States.ON_ARRAY_CLOSING_BRACKET
                else: 
                    item = getCurrentlyEditedItem().parent
                    setCurrentlyEditedItem(item)
                    item.currentField = nextWord
                    currentData.fieldNameCandidate = nextWord
                    if item.type == "array":
                        currentData.state = States.ON_ARRAY_FIELD_NAME
                    else:
                        currentData.state = States.ON_OBJECT_FIELD_NAME
            elif currentData.state == States.ON_FIELD_VALUE_STRING:
                if nextWord == '(':
                    currentData.state = States.ON_OBJECT_OPENING_BRACKET
                else:
                    item = getCurrentlyEditedItem()
                    if currentData.fieldNameCandidate and currentData.fieldValueCandidate:
                        if item.type == 'object':
                            stringValue = currentData.fieldValueCandidate.strip("'")
                            item.fields[currentData.fieldNameCandidate] = stringValue
                            debugMessage("Setting '"+currentData.fieldNameCandidate+"' to '"+stringValue+"'")
                            currentData.fieldNameCandidate = None
                            currentData.fieldValueCandidate = None
                            
                    if nextWord == ')' or nextWord == '),':
                        currentData.state = States.ON_OBJECT_CLOSING_BRACKET
                    else: 
                        item.currentField = nextWord
                        currentData.fieldNameCandidate = nextWord
                        if item.type == "array":
                            currentData.state = States.ON_ARRAY_FIELD_NAME
                        else:
                            currentData.state = States.ON_OBJECT_FIELD_NAME
            elif currentData.state == States.ON_OBJECT_CLOSING_BRACKET:
                currentData.currentNestLevel -= 1
                item = getCurrentlyEditedItem()
                if item and item.parent:
                    setCurrentlyEditedItem(item.parent)
                if nextWord == '':
                    currentData.state = States.ON_EOF
                    # The loop will exit after this point
                elif nextWord == ')' or nextWord == '),':
                    pass
                elif nextWord == ']' or nextWord == '],':
                    currentData.state = States.ON_ARRAY_CLOSING_BRACKET
                elif nextWord == 'export':
                    currentData.state = States.ON_EXPORT_KEYWORD
                else:
                    item = getCurrentlyEditedItem()
                    item.currentField = nextWord
                    currentData.fieldNameCandidate = nextWord
                    if item.type == "array":
                        currentData.state = States.ON_ARRAY_FIELD_NAME
                    else:
                        currentData.state = States.ON_OBJECT_FIELD_NAME
            elif currentData.state == States.ON_ARRAY_CLOSING_BRACKET:
                currentData.currentNestLevel -= 1
                item = getCurrentlyEditedItem()
                if item and item.parent:
                    setCurrentlyEditedItem(item.parent)
                if nextWord == '(':
                    currentData.state = States.ON_OBJECT_OPENING_BRACKET
                elif nextWord == ')' or nextWord == '),':
                    currentData.state = States.ON_OBJECT_CLOSING_BRACKET
                else:
                    item = getCurrentlyEditedItem()
                    item.currentField = nextWord
                    currentData.fieldNameCandidate = nextWord
                    if item.type == "array":
                        currentData.state = States.ON_ARRAY_FIELD_NAME
                    else:
                        currentData.state = States.ON_OBJECT_FIELD_NAME

            elif currentData.state == States.ON_EOF:
                print('This will never actually run, because we exit the loop when we see that the next word is EOF.')


            debugWord = nextWord
            
            if nextWord == '':
                nextWord = False
            else:
                nextWord = getNextWord()
                if not nextWord: # run it one more time to make sure we can also react to the state set by the very last word
                    nextWord = ''

            
            if self.collectDebugMessages:
                for message in debugMessagesThisLoop:
                    print('    ' + message, sep='')
                print('[' + str(currentData.currentNestLevel) + '] ', '"'+debugWord+'"', ' ('+str(currentData.state)+')', sep = '')
            

        ret = formatPartialData(currentData.currentPartialData)

        if self.collectDebugMessages:
            print('\n-----RET-----\n')
            pprint(ret, indent=4)
            print('\n-----/RET-----\n')
        return ret
        


