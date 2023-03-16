# import re
# import string
# def pythonBasics():
#     allChar = 0
#     allNum = 0
#     allSpaces = 0
#     allPunctuations = 0

#     # print("#####")
#     print("From PY")
#     varX = 'tgyhjGGHGH 456 $%^&*+ . '
#     totalLen = len(varX)
#     allSpaces = len(re.findall('\s', varX))
#     allChar = len(re.findall('[a-zA-Z]',varX))
#     allNum = len(re.findall('[0-9]', varX))
#     # allPunctuations = len(re.findall("[!'#$%&\()*+, -./:;<=>?@[\]^_`{|}~]", varX))
    
#     print("Total Length: {}, Characters: {}, Digits: {}, Spaces: {}, Punctuations: {}".format(totalLen, allChar,allNum,allSpaces,allPunctuations))
    
#     # ##Test Regex
#     # textA = "The rain in Spain"
#     # textB = re.search("The rain in Spain", textA)
#     # # print(type(textB))
#     # if textB:
#     #     print("TextB PRESENT in TextA")
#     # else:
#     #     print("TextB is NOT present in TextA")

def pythonBasics():
    g_question = 'cat dog 42 compu5 1huh 0 apple'
    updatedList = []
    spacedList = g_question.split()

    for i in spacedList:
        if i.isdigit():
            i = '#{0}'.format(i)
            updatedList.append(i)
        elif i.isalpha():
            i = '${0}'.format(i)
            updatedList.append(i)
        else:
            updatedList.append(i)

    updatedString = ' '.join(updatedList)
    print(updatedString)

    return True


pythonBasics()
