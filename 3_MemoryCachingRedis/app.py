from itertools import count
from time import time
from flask import Flask, render_template, request
from colorama import Cursor
import csv
import pyodbc
import redis

app = Flask(__name__)
##REFERENCES
#https://www.tutorialspoint.com/what-is-python-commit-method-in-mysql
#https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver16
#https://www.geeksforgeeks.org/querying-data-from-a-database-using-fetchone-and-fetchall/
##REDIS
#https://www.youtube.com/watch?v=jgpVdJB2sKQ&t=788s
#https://www.youtube.com/watch?v=_8lJ5lp8P0U
#https://realpython.com/python-redis/
#https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/cache-python-get-started

#Connect to DB
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

# Connect REDIS
redis_hostname = 'firstredis.redis.cache.windows.net'
redis_password = 'gSUQ2Krcv7OoCz95NhqMjH8342VMxvOaOAzCaKodcKo='
redis_client = redis.StrictRedis(host=redis_hostname, port=6380, db=0, password= redis_password, ssl=True)
# redis_client = redis.Redis(host= "localhost", port= 6379, db=0)
print("RED redis")
redis_client.set("myname","Saba Ruhee")
redisvariable = redis_client.get("myname")
print(redisvariable)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/otherIndex', methods = ['GET', 'POST'])
def otherIndex():
    return render_template('otherIndex.html')

########################################Query0########################################
@app.route('/displayAllRecords', methods = ['GET', 'POST'])
def displayAllRecords():
    # if request.method == 'GET':
    allRecords = []
    # searchName = request.form['name']
    conn = connection()
    cursor0 = conn.cursor()
    query0 = "SELECT * FROM dbo.a3_earthQuakeData"
    # print("Query-0", query0)
    cursor0.execute(query0)
    for row in cursor0.fetchall():
        allRecords.append(row)
    conn.close()
    # print("List of All Records", allRecords)
    recordCount = len(allRecords)
    if len(allRecords) < 1:
        return render_template('displayAllRecords.html', onFailure = "Records not found")
    else:
        return render_template('displayAllRecords.html', onSuccess = recordCount , allRecords = allRecords )
########################################Query00########################################
@app.route('/displayAllRecords2', methods = ['GET', 'POST'])
def displayAllRecords2():
    # if request.method == 'GET':
    allRecords = []
    # searchName = request.form['name']
    conn = connection()
    cursor0 = conn.cursor()
    query0 = "SELECT * FROM dbo.a3_mockQuiz"
    # print("Query-0", query0)
    cursor0.execute(query0)
    for row in cursor0.fetchall():
        allRecords.append(row)
    conn.close()
    # print("List of All Records", allRecords)
    recordCount = len(allRecords)
    if len(allRecords) < 1:
        return render_template('displayAllRecords2.html', onFailure = "Records not found")
    else:
        return render_template('displayAllRecords2.html', onSuccess = recordCount , allRecords = allRecords )
            
########################################Query1########################################
@app.route('/q1_withoutRedisRandomQuery', methods = ['GET', 'POST'])
def q1_withoutRedisRandomQuery():
    return render_template('q1_withoutRedisRandomQuery.html')

@app.route('/on_q1_withoutRedisRandomQuery', methods = ['GET', 'POST'])
def on_q1_withoutRedisRandomQuery():
    if request.method == 'POST':
        outputQ1 = []
        timeOfExecution = 0
        formCount = int(request.form['count'])
        connectDB_1 = connection()
        cursor1 = connectDB_1.cursor()
        query1 = "SELECT TOP (500) * FROM dbo.a3_earthQuakeData"

        timeBeforeQuery = time()

        for perQuery in range(formCount):
            print(perQuery)
            cursor1.execute(query1)
            outputQ1 = cursor1.fetchall()
        
        timeAfterQuery = time()        
        connectDB_1.close()

        timeOfExecution = timeAfterQuery - timeBeforeQuery
        # print("--outputQ1--", outputQ1)
        recordCount = len(outputQ1)
        if len(outputQ1) < 1:
            return render_template('q1_withoutRedisRandomQuery.html', onFailure = "Records not found")
        else:
            return render_template('q1_withoutRedisRandomQuery.html', onSuccess = recordCount , outputQ1 = outputQ1, timeOfExecution = timeOfExecution )

########################################Query2########################################
@app.route('/q2_withoutRedisRestrictedQueries', methods = ['GET', 'POST'])
def q2_withoutRedisRestrictedQueries():
    return render_template('q2_withoutRedisRestrictedQueries.html')

@app.route('/on_q2_withoutRedisRestrictedQueries', methods = ['GET', 'POST'])
def on_q2_withoutRedisRestrictedQueries():
    if request.method == 'POST':
        outputQ2 = []
        formRestrictedCount = int(request.form['restrictedCount'])
        connectDB_2 = connection()
        cursor2 = connectDB_2.cursor()
        query2 = "SELECT * FROM dbo.a3_earthQuakeData WHERE mag=2"
        # print("Query-0", query02)

        timeBeforeExecution = time()

        for perQuery in range(formRestrictedCount):
            print(perQuery)
            outputQ2 = cursor2.execute(query2)
            outputQ2 = cursor2.fetchall()

        timeAfterExecution = time()
        
        connectDB_2.close()

        timeOfExecution = timeAfterExecution - timeBeforeExecution 
        # print("List of All Records", outputQ2)
        recordCount = len(outputQ2)
        if len(outputQ2) < 1:
            return render_template('q2_withoutRedisRestrictedQueries.html', onFailure = "Records not found")
        else:
            return render_template('q2_withoutRedisRestrictedQueries.html', onSuccess = recordCount , outputQ2 = outputQ2, timeOfExecution = timeOfExecution)

########################################Query3########################################
@app.route('/q3_withRedisMultipleQueries', methods = ['GET', 'POST'])
def q3_withRedisMultipleQueries():
    return render_template('q3_withRedisMultipleQueries.html')

@app.route('/on_q3_withRedisMultipleQueries', methods = ['GET', 'POST'])
def on_q3_withRedisMultipleQueries():
    if request.method == 'POST':
        outputQ3 = []
        timeOfExecution = 0
        formCount = int(request.form['redisCount'])
        connectDB_3 = connection()
        cursor3 = connectDB_3.cursor()
        query3 = "SELECT TOP (500) * FROM dbo.a3_earthQuakeData"
        timeBeforeQuery = time()
        lenOutputQ3 = 0

        for perQuery in range(formCount):
            if lenOutputQ3 == 0:
                cursor3.execute(query3)
                outputQ3 = cursor3.fetchall()
                lenOutputQ3 = len(outputQ3)
                redis_client.set("lenOutputQ3",(lenOutputQ3))
                # print("PQ if-",perQuery)
            elif lenOutputQ3 != 0:
                # print("PQ else-",perQuery)
                # redisGet = redis_client.get("lenOutputQ3")
                # lenOutputQ3 = int(redisGet)
                continue
        
        timeAfterQuery = time() 
        connectDB_3.close()

        redisGet = redis_client.get("lenOutputQ3")
        lenOutputQ3 = int(redisGet)  
        
        timeOfExecution = timeAfterQuery - timeBeforeQuery
        # print("--outputQ3--", outputQ3)
        recordCount = len(outputQ3)
        if len(outputQ3) < 1:
            return render_template('q3_withRedisMultipleQueries.html', onFailure = "Records not found")
        else:
            return render_template('q3_withRedisMultipleQueries.html', onSuccess = recordCount , outputQ3 = outputQ3, timeOfExecution = timeOfExecution, countFromRedis = lenOutputQ3 )

#######################################Query04########################################
@app.route('/q4_withRedisRedisRestrictedQueries', methods = ['GET', 'POST'])
def q4_withRedisRedisRestrictedQueries():
    return render_template('q4_withRedisRedisRestrictedQueries.html')

@app.route('/on_q4_withRedisRedisRestrictedQueries', methods = ['GET', 'POST'])
def on_q4_withRedisRedisRestrictedQueries():
    if request.method == 'POST':
        outputQ4 = []
        timeOfExecution = 0
        formCount = int(request.form['redisCount'])
        connectDB_4 = connection()
        cursor4 = connectDB_4.cursor()
        query4 = "SELECT * FROM dbo.a3_earthQuakeData WHERE mag=2"
        timeBeforeQuery = time()
        lenOutputQ4 = 0

        for perQuery in range(formCount):
            if lenOutputQ4 == 0:
                cursor4.execute(query4)
                outputQ4 = cursor4.fetchall()
                lenOutputQ4 = len(outputQ4)
                redis_client.set("lenOutputQ4",(lenOutputQ4))
                # print("PQ if-",perQuery)
            elif lenOutputQ4 != 0:
                # print("PQ elif-",perQuery)
                # redisGet = redis_client.get("lenOutputQ4")
                # lenOutputQ4 = int(redisGet)
                continue

        timeAfterQuery = time()        
        connectDB_4.close()

        redisGet = redis_client.get("lenOutputQ4")
        lenOutputQ4 = int(redisGet)

        timeOfExecution = timeAfterQuery - timeBeforeQuery
        # print("--outputQ4--", outputQ4)
        recordCount = len(outputQ4)
        if len(outputQ4) < 1:
            return render_template('q4_withRedisRedisRestrictedQueries.html', onFailure = "Records not found")
        else:
            return render_template('q4_withRedisRedisRestrictedQueries.html', onSuccess = recordCount , outputQ4 = outputQ4, timeOfExecution = timeOfExecution, countFromRedis = lenOutputQ4 )


########################################MOCK-QUIZ2########################################
########################################Query01########################################

@app.route('/q01_withoutRedisEachQuery', methods = ['GET', 'POST'])
def q01_withoutRedisEachQuery():
    return render_template('q01_withoutRedisEachQuery.html')

@app.route('/on_q01_withoutRedisEachQuery', methods = ['GET', 'POST'])
def on_q01_withoutRedisEachQuery():
    if request.method == 'POST':
        outputQ01 = []
        timeOfExecution = []
        startRange = int(request.form['startRange'])
        endRange = int(request.form['endRange'])
        valueN = int(request.form['valueN'])
        connectDB_01 = connection()
        cursor01 = connectDB_01.cursor()
        # query01 = "SELECT TOP({0}) * FROM dbo.a3_mockQuiz WHERE D BETWEEN {1} AND {2};".format(valueN, startRange, endRange)

        for perQuery in range(5):
            print(perQuery)
            query01 = "SELECT TOP({0}) * FROM dbo.a3_mockQuiz WHERE D BETWEEN {1} AND {2};".format(valueN, startRange, endRange)
            timeBeforeQuery = time()
            cursor01.execute(query01)
            outputQ01 = cursor01.fetchall()
            timeAfterQuery = time()
            temp = timeAfterQuery - timeBeforeQuery
            timeOfExecution.append(temp)
            print("--",timeOfExecution)
                
        connectDB_01.close()
        totalTimeOfExecution = sum(timeOfExecution)
        
        # print("--outputQ1--", outputQ1)
        recordCount = len(outputQ01)
        if len(outputQ01) < 1:
            return render_template('q01_withoutRedisEachQuery.html', onFailure = "Records not found")
        else:
            return render_template('q01_withoutRedisEachQuery.html', onSuccess = recordCount , outputQ01 = outputQ01, timeOfExecution = timeOfExecution, totalTimeOfExecution = totalTimeOfExecution )

########################################Query02########################################

@app.route('/q02_withRedisEachQuery', methods = ['GET', 'POST'])
def q02_withRedisEachQuery():
    return render_template('q02_withRedisEachQuery.html')

@app.route('/on_q02_withRedisEachQuery', methods = ['GET', 'POST'])
def on_q02_withRedisEachQuery():
    if request.method == 'POST':
        outputQ02 = []
        timeOfExecution = []
        startRange = int(request.form['startRange'])
        endRange = int(request.form['endRange'])
        valueN = int(request.form['valueN'])
        connectDB_02 = connection()
        cursor02 = connectDB_02.cursor()
        lenOutputQ02 = 0
        
        # query01 = "SELECT TOP({0}) * FROM dbo.a3_mockQuiz WHERE D BETWEEN {1} AND {2};".format(valueN, startRange, endRange)
        query02 = "SELECT TOP({0}) * FROM dbo.a3_mockQuiz WHERE D BETWEEN {1} AND {2};".format(valueN, startRange, endRange)

        for perQuery in range(5):
            timeBeforeQuery = time()
            if lenOutputQ02 == 0:
                cursor02.execute(query02)
                outputQ02 = cursor02.fetchall()
                lenOutputQ02 = len(outputQ02)
                redis_client.set("lenOutputQ02",(lenOutputQ02))
            elif lenOutputQ02 != 0:
                print(lenOutputQ02)
                lenOutputQ02 = redis_client.get("lenOutputQ4")
                
            timeAfterQuery = time()
            temp = timeAfterQuery - timeBeforeQuery
            timeOfExecution.append(temp)
            print("--", timeOfExecution)
                
        connectDB_02.close()
        redisGet = redis_client.get("lenOutputQ4")
        lenOutputQ02 = int(redisGet)
        totalTimeOfExecution = sum(timeOfExecution)
        
        # print("--outputQ1--", outputQ1)
        recordCount = len(outputQ02)
        if len(outputQ02) < 1:
            return render_template('q02_withRedisEachQuery.html', onFailure = "Records not found")
        else:
            return render_template('q02_withRedisEachQuery.html', onSuccess = recordCount , outputQ02 = outputQ02, timeOfExecution = timeOfExecution, totalTimeOfExecution = totalTimeOfExecution, countFromRedis = lenOutputQ02 )

########################################FINISH########################################

if __name__ == '__main__':
    # app.run(debug=True, port=8093)
    app.run()   

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
    return render_template('thisWillRouteToTheApp_pyFile.html')

@app.route('/onSubmission', methods = ['GET', 'POST'])
def onSubmission():
    if request.method == 'POST':
        return render_template('thisWillRouteToTheApp_pyFile.html')
"""

########################################ENDS########################################


 





