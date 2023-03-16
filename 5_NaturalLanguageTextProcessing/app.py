from asyncore import write
import imp
from importlib.resources import path
from itertools import count
from flask import Flask, render_template, request
from colorama import Cursor
import csv
import os
import pyodbc
from nltk import word_tokenize, PorterStemmer, RegexpTokenizer, sent_tokenize
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import string
import re
from nltk import ngrams

nltk.download('punkt')
nltk.download('stopwords')

app = Flask(__name__)
##REFERENCES
#https://www.tutorialspoint.com/what-is-python-commit-method-in-mysql
#https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver16
#https://www.geeksforgeeks.org/querying-data-from-a-database-using-fetchone-and-fetchall/

def connection():
    s = 'kickstartingdb.database.windows.net' #Your server name 
    d = 'kickstart' 
    u = 'saba' #Your login
    p = 'kickstart@123' #Your login password
    cstr = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER='+s+';DATABASE='+d+';UID='+u+';PWD='+ p
    print("cstr", cstr)
    conn = pyodbc.connect(cstr)
    print("conn", conn)
    return conn


@app.route('/')
def index():
    return render_template('index.html')

########################################REFERENCES########################################
#https://web.stanford.edu/class/archive/cs/cs106a/cs106a.1204/handouts/py-file.html
#https://stackoverflow.com/questions/19591458/python-reading-from-a-file-and-saving-to-utf-8
##https://stackoverflow.com/questions/42954872/what-does-w-for-w-in-word-tokens-if-mean-in-python
##https://stackoverflow.com/questions/3182268/nltk-and-language-detection
#https://people.revoledu.com/kardi/tutorial/Python/NLP1.html
#https://sites.pitt.edu/~naraehan/python3/reading_writing_methods.html
#https://stackoverflow.com/questions/28392860/print-10-most-frequently-occurring-words-of-a-text-that-including-and-excluding
#https://stackoverflow.com/questions/56837218/how-to-remove-n-from-output-screen-while-using-sent-tokenize-using-nltk
########################################Query00########################################
##
### CLEAN DATA
###1.Change to Lower Case #2.Remove Punctuation #3.Remove common words #4.Additionally word stemming
            
def Clean():
    ##\w+ matches any word character (equal to [a-zA-Z0-9_])
    token = RegexpTokenizer(r'\w+')
    staticPath = "static_files/"
    filtered_sentence = []
    directorypath = os.listdir(staticPath)
    for files in directorypath:
        allFiles = open("static_files/"+files, encoding="utf8")
        fliesAfterClean = 'cleaned/{0}'.format(files)
        for perFile in allFiles:
            #Change to Lower Case
            perFile = perFile.lower()
            #Remove Punctuation - Tokenize
            tokenizedFiles = token.tokenize(perFile)

            #Remove the common words
            #https://stackoverflow.com/questions/42954872/what-does-w-for-w-in-word-tokens-if-mean-in-python
            filtered_words = [w for w in tokenizedFiles if not w in stopwords.words('english')]
            finalList = " ".join(filtered_words)

            writeOnFile = open(fliesAfterClean, 'a', encoding='utf-8')
            writeOnFile.write(finalList+ "\n")
            writeOnFile.close()
    allFiles.close()

####Learn NLP
def learnNLP():

    nlpSampleText = """
    This eBook is for the use of anyone anywhere in the United States and
most other parts of the world at no cost and with almost no restrictions
whatsoever. You may copy it, give it away or re-use it under the terms
of the Project Gutenberg License included with this eBook or online at
www.gutenberg.org. If you are not located in the United States, you
will have to check the laws of the country where you are located before
using this eBook.
        Release Date: January, 1991 [eBook #11]
    [Most recently updated: October 12, 2020]
    """
    # print(nlpSampleText)
    #tokenization or listing based on words
    # print("Word Tokenize",word_tokenize(nlpSampleText))####
    #tokenization or listing based on sentences
    # print("Sentence Tokenize: ",sent_tokenize(nlpSampleText))####
    #Counts the frequency
    
    tokenizedWords = word_tokenize(nlpSampleText)
    # print("Frequency Dist",FreqDist(tokenizedWords))####
    # fd = FreqDist(tokenizedWords)
    # print(fd[0][0])
    # print(fd.most_common(20))
    stop_words = set(stopwords.words('english'))
    # print(len(stop_words))
    # print("Stoopp",stop_words)
    str1 = 'abcdef'
    str2 = 'abcdf'
    com_str = ''.join(set(str1).intersection(str2))
    print("com",com_str)
    word_data = "The best performance can bring in sky high success."
    nltk_tokens = nltk.tokenize.word_tokenize(word_data)  	

    # print(list(nltk.bigrams(nltk_tokens)))
    sentence = 'some big sentence'
    # list(ngrams(word_tokenize(sentence), 2))
    twoLetter = list(ngrams(sentence, 2))
    print("sentence", twoLetter)

#######
def pythonBasics():
    allChar = 0
    allNum = 0
    allSpaces = 0
    allPunctuations = 0

    print("##############################################################################")
    print("From PY")
    varX = 'tgyhj 456 $%^&* . '
    totalLen = len(varX)
    for i in varX:
        if i.isdigit():
            allNum += 1
        elif i.isalpha():
            allChar += 1
        elif i.isspace():
            allSpaces += 1
        elif i in string.punctuation:
            allPunctuations += 1
    # print("Total Length: {}, Characters: {}, Digits: {}, Spaces: {}, Punctuations: {}".format(totalLen, allChar,allNum,allSpaces,allPunctuations))
    
    ##Test Regex
    textA = "The rain in Spain"
    textB = re.search("^The.*Spain$", textA)
    # print(type(textB))
    if textB:
        print("TextB PRESENT in TextA")
    else:
        print("TextB is NOT present in TextA")

    

    
    print("##############################################################################")

    return True

########################################Query01########################################
#https://stackoverflow.com/questions/28392860/print-10-most-frequently-occurring-words-of-a-text-that-including-and-excluding
@app.route('/q1_FrequentWords', methods = ['GET', 'POST'])
def q1_FrequentWords():
    return render_template('q1_FrequentWords.html')

@app.route('/on_q1_FrequentWords', methods = ['GET', 'POST'])
def on_q1_FrequentWords():
    if request.method == 'POST':
        finalDict = {}
        frequentNum = int(request.form['frequentNum'])
        fileName = 'static_files/Alamo.txt'
        fileOpen = open(fileName, 'rt', encoding= 'utf-8')
        fileText = fileOpen.read()
        fileOpen.close()
        token = RegexpTokenizer(r'\w+')
        totalwords = fileText.count(" ")+1
        
        # fileText = "Burro hablando de orejas, que burro."
        allWords = token.tokenize(fileText)
        # print("Allwords",len(allWords))
        # allWords = nltk.tokenize.word_tokenize(tokenizedText)
        allWordDist = nltk.FreqDist(w.lower() for w in allWords)
        print(allWordDist)
        stopwords = nltk.corpus.stopwords.words('spanish')
        allWordExceptStopDist = nltk.FreqDist(w.lower() for w in allWords if w not in stopwords)

        mostCommon= allWordExceptStopDist.most_common(frequentNum)
        # print("Most Common", mostCommon)
        # [('de', 145), ('la', 89), ('en', 65), ('los', 65), ('el', 55)]
        finalDict = dict(mostCommon)

        print("TotalWords", totalwords)

        # print("Final", finalDict)
        
    return render_template('q1_FrequentWords.html', onSuccess = "Record Found", totalwords = totalwords, finalDict = finalDict)

########################################Query02########################################
@app.route('/q2_stopWordsMatch', methods = ['GET', 'POST'])
def q2_stopWordsMatch():
    # if request.method == 'POST':
    finalDict = {}
    fileName = 'static_files/Alamo.txt'
    fileOpen = open(fileName, 'rt', encoding= 'utf-8')
    fileText = fileOpen.read()
    fileOpen.close()
    token = RegexpTokenizer(r'\w+')
    totalwords = fileText.count(" ")+1
    
    # fileText = "Burro hablando de orejas, que burro."
    allWords = token.tokenize(fileText)
    # print("Allwords",len(allWords))
    # allWords = nltk.tokenize.word_tokenize(tokenizedText)
    allWordDist = nltk.FreqDist(w.lower() for w in allWords)
    # print(allWordDist)
    stopwords = nltk.corpus.stopwords.words('spanish')
    # print("STop",stopwords)
    allWordWithStopDist = nltk.FreqDist(w.lower() for w in allWords if w in stopwords)
    # print("Words that are stop words", allWordWithStopDist)

    mostCommon= allWordWithStopDist.most_common()
    print("Most Common", mostCommon)
    # [('de', 145), ('la', 89), ('en', 65), ('los', 65), ('el', 55)]
    finalDict = dict(mostCommon)

    # print("Final", finalDict)
        
    return render_template('q2_stopWordsMatch.html', onSuccess = "Record Found", finalDict = finalDict)
########################################Query11########################################
#https://www.geeksforgeeks.org/python-how-to-search-for-a-string-in-text-files/
#https://www.tutorialspoint.com/python/os_listdir.htm

@app.route('/q11_singleWordSearch', methods = ['GET', 'POST'])
def q11_singleWordSearch():
    return render_template('q11_singleWordSearch.html')

@app.route('/on_q11_singleWordSearch', methods = ['GET', 'POST'])
def on_q11_singleWordSearch():
    if request.method == 'POST':
        flag = 0
        lineNumber = []
        lineCount = 0
        wordFoundCount = 0
        finalDict = {}
        enteredText = request.form['enteredText']
        staticPath = "static_files/"
        directorypath = os.listdir(staticPath)
        # print("--",directorypath)
        for perFile in directorypath:
            fileOpen = open("cleaned/{0}".format(perFile), encoding="utf8")
            lineCount = 0
            lineNumber = []

            for perLine in fileOpen:
                lineCount += 1
                # print("---",line)
                if enteredText in perLine:
                    wordFoundCount += 1
                    lineNumber.append(lineCount)
                    flag = 1
                finalDict[perFile] = [lineNumber, len(lineNumber)]
            fileOpen.close()
        print("wordFoundCount", wordFoundCount)
        # print("Line number:", lineNumber)
        # print("finalDict:", finalDict)
        
        if flag == 0:
            return render_template('q11_singleWordSearch.html', onFailure = "String not Found")
        elif flag == 1:
            return render_template('q11_singleWordSearch.html', onSuccess = finalDict)
            # for x in finalDict:
            #     print("String found in File: {0} - Line No: {1} ".format(x,finalDict[x]))

########################################Query11########################################
#https://www.geeksforgeeks.org/python-program-convert-string-list/
#https://stackoverflow.com/questions/50004602/how-to-find-character-bigrams-and-trigrams
#https://stackoverflow.com/questions/29216889/slicing-a-dictionary
#https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value

@app.route('/q3_twoLetterBigrams', methods = ['GET', 'POST'])
def q3_twoLetterBigrams():
    return render_template('q3_twoLetterBigrams.html')

@app.route('/on_q3_twoLetterBigrams', methods = ['GET', 'POST'])
def on_q3_twoLetterBigrams():
    if request.method == 'POST':
        nCount = int(request.form['nCount'])
        finalDict = {}
        fileOpen = open("cleaned/Alamo.txt", encoding="utf8")

        for perLine in fileOpen:
            perTwoLetterBigrams = list(ngrams(perLine, 2))
            # print("sentence", perTwoLetterBigrams)
            for i in perTwoLetterBigrams:
                if i[1] == " ":
                    continue

                if i in finalDict:
                    finalDict[i] += 1
                else:
                    finalDict[i] = 1
        finalDict = dict(sorted(finalDict.items(), key=lambda item: item[1], reverse= True))
        # print("finalDict", finalDict)
        # nSlicedDict = dict(list(finalDict.items())[:2])
        nSlicedDict = dict(list(finalDict.items())[:nCount])
        print("nSlicedDict", nSlicedDict)
            
        fileOpen.close()
        
        if nCount is None:
            return render_template('q3_twoLetterBigrams.html', onFailure = "Please enter Count")
        else:
            return render_template('q3_twoLetterBigrams.html', onSuccess = "Records found", a1 = nSlicedDict)

########################################Query4########################################
#https://stackoverflow.com/questions/17140886/how-to-search-and-replace-text-in-a-file
@app.route('/q4_replaceCharSeq', methods = ['GET', 'POST'])
def q4_replaceCharSeq():
    return render_template('q4_replaceCharSeq.html')

@app.route('/on_q4_replaceCharSeq', methods = ['GET', 'POST'])
def on_q4_replaceCharSeq():
    if request.method == 'POST':
        replaceChar = request.form['replaceChar']
        withChar = request.form['withChar']
        finalDict = {}
        allLines = []
        perLineCount = 0
        totalReplaced = 0
        print("##################")

        #Read file
        with open('cleaned/AliceInWonderland.txt', 'r',encoding="utf8") as fileOpen :
            dataInFIle = fileOpen.read()
        
        #replace string
        afterReplace = dataInFIle.replace(replaceChar, withChar)
        # print("afterReplace",afterReplace)

        #place the replaced data into file
        with open('cleaned/AliceInWonderland.txt', 'w',encoding="utf8") as fileOpen:
            fileOpen.write(afterReplace)
        
        with open('cleaned/AliceInWonderland.txt', 'r',encoding="utf8") as fileOpen:
            for perLine in fileOpen:
                perLineCount += 1
                if withChar in perLine:
                    # allLines.append(perLine)
                    finalDict[perLineCount] = perLine

        print("finalDict",finalDict)
        fileOpen.close()

        totalReplaced = len(finalDict)
                    
        if totalReplaced == 0:
            return render_template('q4_replaceCharSeq.html', onFailure = "Records not found")
        else:
            return render_template('q4_replaceCharSeq.html', onSuccess = "Records found", a1 = finalDict, totalReplaced = totalReplaced)
########################################Query05########################################
#https://stackoverflow.com/questions/28392860/print-10-most-frequently-occurring-words-of-a-text-that-including-and-excluding
@app.route('/q5_5wordTotalOccurences_remove', methods = ['GET', 'POST'])
def q5_5wordTotalOccurences_remove():
    return render_template('q5_5wordTotalOccurences_remove.html')

@app.route('/on_q5_5wordTotalOccurences_remove', methods = ['GET', 'POST'])
def on_q5_5wordTotalOccurences_remove():
    if request.method == 'POST':
        finalDict = {}
        word1 = request.form['word1']
        word2 = request.form['word2']
        word3 = request.form['word3']
        word4 = request.form['word4']
        word5 = request.form['word5']
        print("ll",word5)
        wordList = [word1, word2, word3,word4,word5]
        wordCount1 = 0
        wordCount2 = 0
        wordCount3 = 0
        wordCount4 = 0
        wordCount5 = 0
        fileOpen = open("cleaned/Prac.txt", encoding="utf8")

        for perLine in fileOpen:
            print("---",perLine)

            perLineList = perLine.split()
            # print("perWord", perLineList)

            for perWord in perLineList:
                print("Per",perWord) 
                if perWord == word1:
                    wordCount1 += 1
                elif perWord == word3:
                    wordCount2 += 1
                elif perWord == word3:
                    wordCount3 += 1
                elif perWord == word4:
                    wordCount4 += 1
                elif perWord == word5:
                    wordCount5 += 1

            finalDict[word1] = wordCount1
            finalDict[word2] = wordCount2
            finalDict[word3] = wordCount3
            finalDict[word4] = wordCount4
            finalDict[word5] = wordCount5

            # for word in bannedWord:
            #     toPrint = toPrint.replace(word, "")
            
        print("--",finalDict)
    return render_template('q5_5wordTotalOccurences_remove.html', onSuccess = "Record Found", finalDict = finalDict)


########################################Query00########################################
########################################FINISH########################################

if __name__ == '__main__':
    # Clean()
    # pythonBasics()
    # learnNLP()
    app.run(debug=True, port=8095)
    # app.run()

########################################CLONE########################################
"""

@app.route('/displayAllRecords', methods = ['GET', 'POST'])
def displayAllRecords():
    # if request.method == 'GET':
    allRecords = []
    # searchName = request.form['name']
    conn = connection()
    cursor0 = conn.cursor()
    query0 = "SELECT * FROM dbo.people"
    print("Query-1", query0)
    cursor0.execute(query0)
    # print("All Records: ",cursor.fetchall())
    for row in cursor0.fetchall():
        print("row[6]]",row[6])
        if row[6] == "" or row[6]== " " or row[6]==None:
            row[6] = "defaultUser.jpg"
        picturPath = "static/"+row[6]
        allRecords.append({"name": row[0], "state": row[1], "salary": row[2], "grade": row[3], "room": row[4], "telnum": row[5], "picture": picturPath, "keywords": row[7]})
    conn.close()
    # print("List of Rec-", allRecords)
    if len(allRecords) < 1:
        return render_template('displayAllRecords.html', onFailure = "Records not found")
    else:
        return render_template('displayAllRecords.html', onSuccess = "Record Found", allRecords = allRecords )




FOR UPDATE OR DELETE RECORDS

@app.route('/recordUpdated', methods = ['GET', 'POST'])
def recordUpdated():
    if request.method == 'POST':
        name = request.form['name']
        recordClass = request.form['class']
        comments = request.form['comments']
        connectDB_12 = connection()
        cursor12 = connectDB_12.cursor()
        query12 = "UPDATE dbo.quiz1_data SET class = {0}, comments = '{1}' WHERE name='{2}'".format(recordClass, comments, name)
        cursor12.execute(query12)
        recordCount = cursor12.rowcount
        connectDB_12.commit()
        # print("Count- {0}".format(recordCount))
        connectDB_12.close()
        if recordCount <= 0:
            return render_template('updateRecord.html', onFailure = "Records not found")
        else:
            return render_template('updateRecord.html', onSuccess = "Record Updated")



        


@app.route('/thisWillRouteToTheApp_pyFile', methods = ['GET', 'POST'])
def thisWillRouteToTheApp_pyFile():
    # completeCSV = csv.DictReader(open("data.csv"))
    return render_template('thisWillRouteToTheApp_pyFile.html')

@app.route('/onSubmission', methods = ['GET', 'POST'])
def onSubmission():
    if request.method == 'POST':
        return render_template('thisWillRouteToTheApp_pyFile.html')
"""

########################################ENDS########################################


 





