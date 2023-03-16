from flask import Flask, render_template, request
from colorama import Cursor
import csv
import pyodbc


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
    return render_template('otherIndex.html')

#ASSIGNMENT-04

########################################Query00########################################
@app.route('/displayAllRecords2', methods = ['GET', 'POST'])
def displayAllRecords2():
    # if request.method == 'GET':
    allRecords = []
    # searchName = request.form['name']
    conn = connection()
    cursor0 = conn.cursor()
    query0 = "SELECT * FROM dbo.earthquakedata;"
    # print("Query-0", query0)
    cursor0.execute(query0)
    allRecords = cursor0.fetchall()
    conn.close()
    # print("List of All Records", allRecords)
    recordCount = len(allRecords)
    if len(allRecords) < 1:
        return render_template('displayAllRecords2.html', onFailure = "Records not found")
    else:
        return render_template('displayAllRecords2.html', onSuccess = recordCount , allRecords = allRecords )
        
########################################Query01########################################
# @app.route('/q01_A4_magPie', methods = ['GET', 'POST'])
# def q01_A4_magPie():
#     return render_template('q01_A4_magPie.html')

@app.route('/q01_A4_magPie', methods = ['GET', 'POST'])
def q01_A4_magPie():
    # if request.method == 'GET':
    output011 = []
    output012 = []
    output013 = []
    output014 = []
    # searchName = request.form['name']
    connectDB_01 = connection()
    cursor01 = connectDB_01.cursor()

    query011 = "SELECT * FROM dbo.earthquakedata WHERE mag < 1.0 ORDER BY mag DESC"
    cursor01.execute(query011)
    output011 = cursor01.fetchall()

    query012 = "SELECT * FROM dbo.earthquakedata WHERE mag BETWEEN 1.0 AND 2.0 ORDER BY mag DESC"
    cursor01.execute(query012)
    output012 = cursor01.fetchall()

    query013 = "SELECT * FROM dbo.earthquakedata WHERE mag BETWEEN 2.0 AND 3.0 ORDER BY mag DESC"
    cursor01.execute(query013)
    output013 = cursor01.fetchall()

    query014 = "SELECT * FROM dbo.earthquakedata WHERE mag > 3.0 ORDER BY mag DESC"
    cursor01.execute(query014)
    output014 = cursor01.fetchall()

    connectDB_01.close()
    if len(output011) == 0 and len(output012) == 0 and len(output013) == 0 and len(output014) == 0:
        return render_template('q01_A4_magPie.html', onFailure = "Records not found")
    else:
        return render_template('q01_A4_magPie.html',onSuccess = "Clusters Found", a1 = len(output011), a2 = len(output012), a3 = len(output013), a4 = len(output014))

########################################Query02########################################
@app.route('/q02_A4_magBar', methods = ['GET', 'POST'])
def q02_A4_magBar():
    # if request.method == 'GET':
    output021 = []
    output022 = []
    output023 = []
    output024 = []
    # searchName = request.form['name']
    connectDB_02 = connection()
    cursor02 = connectDB_02.cursor()

    query021 = "SELECT * FROM dbo.earthquakedata WHERE mag < 1.0 ORDER BY mag DESC"
    cursor02.execute(query021)
    output021 = cursor02.fetchall()

    query022 = "SELECT * FROM dbo.earthquakedata WHERE mag BETWEEN 1.0 AND 2.0 ORDER BY mag DESC"
    cursor02.execute(query022)
    output022 = cursor02.fetchall()

    query023 = "SELECT * FROM dbo.earthquakedata WHERE mag BETWEEN 2.0 AND 3.0 ORDER BY mag DESC"
    cursor02.execute(query023)
    output023 = cursor02.fetchall()

    query024 = "SELECT * FROM dbo.earthquakedata WHERE mag > 3.0 ORDER BY mag DESC"
    cursor02.execute(query024)
    output024 = cursor02.fetchall()
    
    connectDB_02.close()
    if len(output021) == 0 and len(output022) == 0 and len(output023) == 0 and len(output024) == 0:
        return render_template('q02_A4_magBar.html', onFailure = "Records not found")
    else:
        return render_template('q02_A4_magBar.html',onSuccess = "Clusters Found", a1 = len(output021), a2 = len(output022), a3 = len(output023), a4 = len(output024))

    if request.method == 'GET':
        return render_template('q02_A4_magBar.html')
    else:
        return render_template('/')

########################################Query03########################################
@app.route('/q03_A4_scatterMagDepth', methods = ['GET', 'POST'])
def q03_A4_scatterMagDepth():
    # if request.method == 'GET':
    output03 = []
    # searchName = request.form['name']
    connectDB_03 = connection()
    cursor03 = connectDB_03.cursor()

    query03 = "SELECT TOP (2000) mag, depth FROM [dbo].[earthquakedata] ORDER BY [time] DESC;"
    cursor03.execute(query03)
    output03 = cursor03.fetchall()


    print("---",output03)

    connectDB_03.close()
    if len(output03) == 0:
        return render_template('q03_A4_scatterMagDepth.html', onFailure = "Records not found")
    else:
        return render_template('q03_A4_scatterMagDepth.html',onSuccess = "Clusters Found", a1 = output03)

########################################Query04########################################
@app.route('/q04_A4_pie', methods = ['GET', 'POST'])
def q04_A4_pie():
    return render_template('q04_A4_pie.html')

@app.route('/on_q04_A4_pie', methods = ['GET', 'POST'])
def on_q04_A4_pie():
    if request.method == 'POST':
        output04 = []

        startRange = int(request.form['startRange'])
        endRange = int(request.form['endRange'])
        connectDB_04 = connection()
        cursor04 = connectDB_04.cursor()

        query04 = "SELECT COUNT(food) as foodCount, food FROM dbo.fQuiz4Data WHERE store Between {0} And {1} GROUP BY food ORDER BY food DESC".format(startRange, endRange)
        cursor04.execute(query04)
        output04 = cursor04.fetchall()

        print("print",output04)
        connectDB_04.commit()
        connectDB_04.close()
        
        
        print("---", output04)
        if len(output04) == 0:
            return render_template('q04_A4_pie.html', onFailure = "Records not found")
        else:
            return render_template('q04_A4_pie.html',onSuccess = "Records", a1 = output04 )

########################################Query05########################################
@app.route('/q05_A4_pie', methods = ['GET', 'POST'])
def q05_A4_pie():
    return render_template('q05_A4_pie.html')

@app.route('/on_q05_A4_pie', methods = ['GET', 'POST'])
def on_q05_A4_pie():
    if request.method == 'POST':
        output05 = []
        outputList = []
        startRange = int(request.form['startRange'])
        endRange = int(request.form['endRange'])
        connectDB_05 = connection()
        cursor05 = connectDB_05.cursor()
        count = startRange
        finalDict = {}

        query05 = "SELECT COUNT(food) as foodCount, food FROM dbo.fQuiz4Data WHERE store Between {0} And {1} GROUP BY food ORDER BY food DESC ;".format(startRange, endRange)
        cursor05.execute(query05)
        output05 = cursor05.fetchall()
        print("--",output05[0][0])
        temp = output05[0][0]
        outputList.append(temp)
        finalDict["Magnitude Range between {0} - {1}".format(count, count+1)] = temp
        count = count + 1

        print("print",finalDict)
        connectDB_05.commit()
        connectDB_05.close()
        
        
        print("---", output05)
        if len(output05) == 0:
            return render_template('q05_A4_pie.html', onFailure = "Records not found")
        else:
            return render_template('q05_A4_pie.html',onSuccess = "Records", a1 = finalDict )
#######################################################################################
#https://www.geeksforgeeks.org/python-frequency-of-each-character-in-string/
#https://roytuts.com/google-pie-chart-using-python-flask/
@app.route('/q11_mockQuiz', methods = ['GET', 'POST'])
def q11_mockQuiz():
    return render_template('q11_mockQuiz.html')

@app.route('/on_q11_mockQuiz', methods = ['GET', 'POST'])
def on_q11_mockQuiz():
    if request.method == 'POST':
        output011 = []
        name = request.form['name']
        connectDB_01 = connection()
        all_freq = {}


        for i in name:
            if i in all_freq:
                all_freq[i] += 1
            else:
                all_freq[i] = 1
        
        output011 = all_freq
        # print("---",output011)

        connectDB_01.close()
        return render_template('q11_mockQuiz.html',onSuccess = "Clusters Found", a1 = output011)

########################################Query06########################################
@app.route('/q06_A4_bar', methods = ['GET', 'POST'])
def q06_A4_bar():
    return render_template('q06_A4_bar.html')

@app.route('/on_q06_A4_bar', methods = ['GET', 'POST'])
def on_q06_A4_bar():
    if request.method == 'POST':
        output06 = []

        startRange = int(request.form['startRange'])
        endRange = int(request.form['endRange'])
        connectDB_06 = connection()
        cursor06 = connectDB_06.cursor()

        query06 = "SELECT nst, COUNT(nst)  FROM dbo.a3_earthQuakeData as nstCount WHERE nst BETWEEN {0} and {1} GROUP By nst ".format(startRange, endRange)
        cursor06.execute(query06)
        output06 = cursor06.fetchall()

        print("print",output06)
        connectDB_06.commit()
        connectDB_06.close()
        
        
        print("---", output06)
        if len(output06) == 0:
            return render_template('q06_A4_bar.html', onFailure = "Records not found")
        else:
            return render_template('q06_A4_bar.html',onSuccess = "Records", a1 = output06 )

########################################Query07########################################
@app.route('/q07_A4_pie', methods = ['GET', 'POST'])
def q07_A4_pie():
    return render_template('q07_A4_pie.html')

@app.route('/on_q07_A4_pie', methods = ['GET', 'POST'])
def on_q07_A4_pie():
    if request.method == 'POST':
        output07 = []

        nSlices = int(request.form['nSlices'])
        minValue = 20
        maxValue = 560
        #max value - minvalue/interval
        interval = int((maxValue-minValue) / nSlices)
        connectDB_07 = connection()
        cursor07 = connectDB_07.cursor()
        startRange = minValue
        outputList = []
        finalDict = {}

        for i in range(nSlices):
            endRange = startRange + interval
            query07 = "SELECT COUNT(*) FROM dbo.a3_mockQuiz WHERE D BETWEEN {0} and {1}".format(startRange, endRange)
            cursor07.execute(query07)
            output07 = cursor07.fetchall()
            # print("--",output07[0][0])
            temp = output07[0][0]
            outputList.append(temp)
            finalDict["D Range between {0} - {1}".format(startRange, endRange)] = temp
            startRange = endRange
            print("i",i)
        

        print("print",finalDict)
        connectDB_07.commit()
        connectDB_07.close()
        
        if len(output07) == 0:
            return render_template('q07_A4_pie.html', onFailure = "Records not found")
        else:
            return render_template('q07_A4_pie.html',onSuccess = "Records", a1 = finalDict )

########################################Query08########################################
@app.route('/q08_fruitsPie', methods = ['GET', 'POST'])
def q08_fruitsPie():
    return render_template('q08_fruitsPie.html')

@app.route('/on_q08_fruitsPie', methods = ['GET', 'POST'])
def on_q08_A4_pie():
    if request.method == 'POST':
        output08 = []

        nSlices = int(request.form['nSlices'])
        nFruits = request.form['nFruits']
        fruitSplit = nFruits.split(",")


        #max value - minvalue/interval
        interval = int(1/ nSlices)
        connectDB_08 = connection()
        cursor08 = connectDB_08.cursor()
        startRange = 0
        outputList = []
        finalDict = {}

        for i in range(len(fruitSplit)):
            fruitName = fruitSplit[i-1]
            endRange = startRange + interval
            query08 = "SELECT COUNT(*), column4  FROM [dbo].[fruitsData] WHERE column4 = '{0}' GROUP BY column4 ORDER BY column4;".format(fruitName)
            cursor08.execute(query08)
            output08 = cursor08.fetchall()
            # print("--",output08[0][0])
            temp = output08[0][0]
            outputList.append(temp)
            finalDict["{0}".format(fruitName)] = temp
            startRange = endRange
            print("i",i)
        

        print("print",finalDict)
        connectDB_08.commit()
        connectDB_08.close()
        
        if len(output08) == 0:
            return render_template('q08_fruitsPie.html', onFailure = "Records not found")
        else:
            return render_template('q08_fruitsPie.html',onSuccess = "Records", a1 = finalDict )

########################################Query09########################################
@app.route('/q09_fruitsColumn', methods = ['GET', 'POST'])
def q09_fruitsColumn():
    return render_template('q09_fruitsColumn.html')

@app.route('/on_q09_fruitsColumn', methods = ['GET', 'POST'])
def on_q09_fruitsColumn():
    if request.method == 'POST':
        output09 = []

        nSlices = int(request.form['nSlices'])
        nFruits = request.form['nFruits']
        fruitSplit = nFruits.split(",")


        #max value - minvalue/interval
        interval = int(1/ nSlices)
        connectDB_09 = connection()
        cursor09 = connectDB_09.cursor()
        startRange = 0
        outputList = []
        finalDict = {}

        for i in range(len(fruitSplit)):
            fruitName = fruitSplit[i-1]
            endRange = startRange + interval
            query09 = "SELECT COUNT(*), column4  FROM [dbo].[fruitsData] WHERE column4 = '{0}' GROUP BY column4 ORDER BY column4;".format(fruitName)
            cursor09.execute(query09)
            output09 = cursor09.fetchall()
            # print("--",output09[0][0])
            temp = output09[0][0]
            outputList.append(temp)
            finalDict["{0}".format(fruitName)] = temp
            startRange = endRange
            print("i",i)
        

        print("print",finalDict)
        connectDB_09.commit()
        connectDB_09.close()
        
        if len(output09) == 0:
            return render_template('q09_fruitsColumn.html', onFailure = "Records not found")
        else:
            return render_template('q09_fruitsColumn.html',onSuccess = "Records", a1 = finalDict )

######################################QUERY-21#################################################
#https://www.geeksforgeeks.org/python-frequency-of-each-character-in-string/
#https://roytuts.com/google-pie-chart-using-python-flask/
@app.route('/q21_mockQuiz', methods = ['GET', 'POST'])
def q21_mockQuiz():
    return render_template('q21_mockQuiz.html')

@app.route('/on_q21_mockQuiz', methods = ['GET', 'POST'])
def on_q21_mockQuiz():
    if request.method == 'POST':
        textEntered = request.form['textEntered']
        totalwords = len(textEntered)
        print("TotalWords", totalwords)
        connectDB_21 = connection()
        letter_freq = {}
        finalDict = {}
        totalChar = 0
        totalDig = 0
        totalSpaces = 0
        totalLength = len(textEntered)
        print("Total Length-", totalLength)


        # for i in textEntered:
        #     if i in letter_freq:
        #         letter_freq[i] += 1
        #     else:
        #         letter_freq[i] = 1

        for i in textEntered:
            if(i.isalpha()):
                totalChar = totalChar + 1
        print("Total Char",totalChar)

        for i in textEntered:
            if(i.isdigit()):
                totalDig = totalDig + 1
        print("totalDig",totalDig)

        for i in textEntered:
            if(i.isspace()):
                totalSpaces = totalSpaces + 1
        print("totalSpaces",totalSpaces)

        totalPunctuation = totalLength - (totalChar + totalDig + totalSpaces)

        letter_freq['totalChar'] = totalChar
        letter_freq['totalDig'] = totalDig
        letter_freq['totalSpaces'] = totalSpaces
        letter_freq['totalPunctuation'] = totalPunctuation
        
        print("---",letter_freq)

        connectDB_21.close()
        return render_template('q21_mockQuiz.html',onSuccess = "Found", a1 = letter_freq, totalwords= totalwords, totalChar = totalChar, totalDig = totalDig, totalSpaces = totalSpaces, totalPunctuation = totalPunctuation)
########################################Query21########################################
@app.route('/q22_scatter', methods = ['GET', 'POST'])
def q22_scatter():
    # if request.method == 'GET':
    output21 = []
    # searchName = request.form['name']
    connectDB_21 = connection()
    cursor21 = connectDB_21.cursor()

    query21 = "SELECT x, y  FROM [dbo].[pQuiz4Data]"
    cursor21.execute(query21)
    output21 = cursor21.fetchall()


    print("---",output21)

    connectDB_21.close()
    if len(output21) == 0:
        return render_template('q22_scatter.html', onFailure = "Records not found")
    else:
        return render_template('q22_scatter.html',onSuccess = "Clusters Found", a1 = output21)

########################################Query23########################################
@app.route('/q23_vertical', methods = ['GET', 'POST'])
def q23_vertical():
    return render_template('q23_vertical.html')

@app.route('/on_q23_A4_pie', methods = ['GET', 'POST'])
def on_q23_A4_pie():
    if request.method == 'POST':
        output23 = []

        startRange = int(request.form['startRange'])
        endRange = int(request.form['endRange'])
        connectDB_23 = connection()
        cursor23 = connectDB_23.cursor()

        query23 = "SELECT COUNT(food) as foodCount, food FROM dbo.fQuiz4Data WHERE store Between {0} And {1} GROUP BY food ORDER BY food DESC ;".format(startRange, endRange)
        cursor23.execute(query23)
        output23 = cursor23.fetchall()

        print("print",output23)
        connectDB_23.commit()
        connectDB_23.close()
        
        
        print("---", output23)
        if len(output23) == 0:
            return render_template('q23_vertical.html', onFailure = "Records not found")
        else:
            return render_template('q23_vertical.html',onSuccess = "Records", a1 = output23 )
########################################Query10########################################
########################################FINISH########################################

if __name__ == '__main__':
    app.run(debug=True, port=8084)
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


 





