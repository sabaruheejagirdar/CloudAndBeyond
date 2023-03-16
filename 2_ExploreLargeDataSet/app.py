from flask import Flask, render_template, request
from colorama import Cursor
import csv
import pyodbc
import geopy.distance
from datetime import datetime

app = Flask(__name__)
##REFERENCES
#https://www.tutorialspoint.com/what-is-python-commit-method-in-mysql
#https://docs.microsoft.com/en-us/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-ver16
#https://www.geeksforgeeks.org/querying-data-from-a-database-using-fetchone-and-fetchall/
#https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude


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

########################################Query00########################################
@app.route('/displayAllRecords', methods = ['GET', 'POST'])
def displayAllRecords():
    # if request.method == 'GET':
    allRecords = []
    # searchName = request.form['name']
    conn = connection()
    cursor0 = conn.cursor()
    query0 = "SELECT TOP (100) [time],[latitude],[longitude],[depth],[mag],[magType],[nst],[gap],[dmin],[rms],[net],[id],[updated],[place],[type],[horizontalError],[depthError],[magError],[magNst],[status],[locationSource],[magSource] FROM dbo.earthquakedata"
    # print("Query-0", query0)
    cursor0.execute(query0)
    # print("All Records: ",cursor.fetchall())
    for row in cursor0.fetchall():
        # print("row[3]]",row[3])
        # if row[3] == "" or row[3]== " " or row[3]==None:
        #     row[3] = "defaultUser.jpg"
        # picturPath = "static/"+row[3]
        allRecords.append({"time": row[0], "latitude": row[1], "longitude": row[2], "mag": row[4], "place": row[13], "id": row[11]})
    conn.close()
    # print("List of Rec-", allRecords)
    if len(allRecords) < 1:
        return render_template('displayAllRecords.html', onFailure = "Records not found")
    else:
        return render_template('displayAllRecords.html', onSuccess = "Record Found", allRecords = allRecords )

########################################Query01########################################
#Largest 5 quakes
@app.route('/largestQuakes', methods = ['GET', 'POST'])
def largestQuakes():
    allRecords = []
    # searchName = request.form['name']
    connect_DB01 = connection()
    cursor01 = connect_DB01.cursor()
    query01 = "SELECT TOP (5) [mag],[place] FROM dbo.earthquakedata ORDER BY [mag] DESC;"
    # print("Query-0", query0)
    cursor01.execute(query01)
    # print("All Records: ",cursor.fetchall())
    for row in cursor01.fetchall():
        allRecords.append({"mag": row[0], "place": row[1]})
    connect_DB01.close()
    # print("List of Rec-", allRecords)
    if len(allRecords) < 1:
        return render_template('largestQuakes.html', onFailure = "Records not found")
    else:
        return render_template('largestQuakes.html', onSuccess = "Record Found", allRecords = allRecords )

########################################Query00########################################
# Earthquakes within 500KM of Arlington
@app.route('/withinArlington', methods = ['GET', 'POST'])
def withinArlington():
    return render_template('withinArlington.html')

@app.route('/arlingtonEarthquakes', methods = ['GET', 'POST'])
def arlingtonEarthquakes():
    if request.method == 'POST':
        allRecords = []
        formLatitude = float(request.form['latitude'])
        formLongitude = float(request.form['longitude'])
        formRadius = float(request.form['radius'])
        connectDB_02 = connection()
        cursor02 = connectDB_02.cursor()
        query02 = "SELECT TOP 100 latitude ,longitude,type FROM dbo.earthquakedata WHERE type='earthquake'"
        # print("Query-0", query0)
        cursor02.execute(query02)
        # print("All Records: ",cursor.fetchall())
        #https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
        for row in cursor02.fetchall():
            # allRecords.append({"latitude": row[0], "longitude": row[1], "type": row[2]})
            # arlington_coordinates = (32.7324106535524, -97.11266783050309)
            arlington_coordinates = (formLatitude, formLongitude)
            earthquakes_coordinates = (row[0], row[1])
            distance = geopy.distance.distance(arlington_coordinates, earthquakes_coordinates).kilometers
            print("-----")
            print(arlington_coordinates)
            print(earthquakes_coordinates)
            print(distance)
            if distance < formRadius:
            # if distance < 1000:
                allRecords.append({"latitude": row[0], "longitude": row[1], "type": row[2], "distance": distance})
        connectDB_02.close()
        # print("List of Rec-", allRecords)
        if len(allRecords) < 1:
            return render_template('withinArlington.html', onFailure = "Records not found")
        else:
            return render_template('withinArlington.html', onSuccess = "Record Found", allRecords = allRecords )

########################################Query05########################################
@app.route('/dallasLargest', methods = ['GET', 'POST'])
def dallasLargest():
    return render_template('dallasLargest.html')

@app.route('/largestQuakeDallas', methods = ['GET', 'POST'])
def largestQuakeDallas():
    if request.method == 'POST':
        allRecords = []
        formLatitude = float(request.form['latitude'])
        formLongitude = float(request.form['longitude'])
        formRadius = float(request.form['radius'])
        connectDB_05 = connection()
        cursor02 = connectDB_05.cursor()
        query05 = "SELECT TOP 100 latitude ,longitude,type, place, id FROM dbo.earthquakedata WHERE type='earthquake'"
        # print("Query-0", query0)
        cursor02.execute(query05)
        largestDallasQuake = []
        distance = 0
        prevDistance = 0
        #https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
        for row in cursor02.fetchall():
            dallas_coordinates = (formLatitude, formLongitude)
            earthquakes_coordinates = (row[0], row[1])
            distance = geopy.distance.distance(dallas_coordinates, earthquakes_coordinates).kilometers
            # if distance < 1000:
            if distance < formRadius:
                allRecords.append({"latitude": row[0], "longitude": row[1], "type": row[2], "place": row[3], "id":row[4], "distance": distance})
                if distance > prevDistance:
                    largestDallasQuake = [row[0], row[1], row[2],row[3],row[4], distance]
            prevDistance = distance

        connectDB_05.close()
        # print("List of Rec-", allRecords)
        if len(allRecords) < 1:
            return render_template('dallasLargest.html', onFailure = "Records not found")
        else:
            return render_template('dallasLargest.html', onSuccess = "Record Found", allRecords = allRecords, largestDallasQuake = largestDallasQuake )

########################################Query03########################################
@app.route('/greaterThanRicherScale', methods = ['GET', 'POST'])
def greaterThanRicherScale():
    return render_template('greaterThanRicherScale.html')

@app.route('/resultGreaterRitcher', methods = ['GET', 'POST'])
def resultGreaterRitcher():
    if request.method == 'POST':
        allRecords = []
        countOfRecords =0
        formStartDate = request.form['startDateRitcher']
        formEndDate = request.form['endDateRichter']
        formMagnitude = float(request.form['magnitude'])
        connectDB_03 = connection()
        cursor03 = connectDB_03.cursor()
        query03 = "SELECT * FROM dbo.earthquakedata WHERE time BETWEEN '{0}' and '{1}' and mag > {2}".format(formStartDate, formEndDate, formMagnitude)
        # print("Query-0", query03)
        cursor03.execute(query03)
        # print("All Records: ",cursor.fetchall())
        for row in cursor03.fetchall():
            allRecords.append({"time": row[0], "magnitude": row[4], "place": row[13], "id": row[11]})
        connectDB_03.close()
        # print("List of Rec-", allRecords)
        totalRecords = len(allRecords)
        if len(allRecords) < 1:
            return render_template('greaterThanRicherScale.html', onFailure = "Records not found")
        else:
            return render_template('greaterThanRicherScale.html', onSuccess = totalRecords , allRecords = allRecords )

########################################Query04########################################
@app.route('/recentQuakes', methods = ['GET', 'POST'])
def recentQuakes():
    # if request.method == 'GET':
    # allRecords = []
    # searchName = request.form['name']
    connectDB_04 = connection()
    cursor04 = connectDB_04.cursor()
    query041 = "SELECT COUNT(*) FROM dbo.earthquakedata WHERE (time BETWEEN '2022-02-02' and '2022-02-10') and (mag BETWEEN 1.00 and 2.00)"
    cursor04.execute(query041)
    output041 = cursor04.fetchall()
    # print(output041[0][0])

    query042 = "SELECT COUNT(*) FROM dbo.earthquakedata WHERE (time BETWEEN '2022-02-02' and '2022-02-10') and (mag BETWEEN 1.00 and 2.00)"
    cursor04.execute(query042)
    output042 = cursor04.fetchall()
    # print(output042[0][0])

    query043 = "SELECT COUNT(*) FROM dbo.earthquakedata WHERE (time BETWEEN '2022-02-02' and '2022-02-10') and (mag BETWEEN 2.00 and 3.00)"
    cursor04.execute(query043)
    output043 = cursor04.fetchall()
    # print(output043[0][0])

    query044 = "SELECT COUNT(*) FROM dbo.earthquakedata WHERE (time BETWEEN '2022-02-02' and '2022-02-10') and (mag BETWEEN 3.00 and 4.00)"
    cursor04.execute(query044)
    output044 = cursor04.fetchall()
    # print(output044[0][0])
    connectDB_04.close()
    return render_template('recentQuakes.html', onSuccess = "Record Found", mag1 = output041[0][0], mag2 = output042[0][0], mag3 = output043[0][0], mag4 = output044[0][0])
########################################Query06########################################
##Are quakes more common within 1000 km of Anchorage (61 N, 150 W) than Dallas (32.8 N, 96.8 W)
@app.route('/commonQuakes', methods = ['GET', 'POST'])
def commonQuakes():
    return render_template('commonQuakes.html')

@app.route('/resultCommonQuakes', methods = ['GET', 'POST'])
def resultCommonQuakes():
    if request.method == 'POST':
        allRecordsAnchorage = []
        allRecordsDallas = []

        formLatitude1 = float(request.form['latitude1'])
        formLongitude1 = float(request.form['longitude1'])
        formRadius1 = float(request.form['radius1'])

        formLatitude2 = float(request.form['latitude2'])
        formLongitude2 = float(request.form['longitude2'])
        formRadius2 = float(request.form['radius2'])

        distance = 0
        distance1 = 0

        connectDB_06 = connection()
        cursor06 = connectDB_06.cursor()
        query06 = "SELECT TOP 50 latitude ,longitude,type FROM dbo.earthquakedata WHERE type='earthquake'"
        query06B = "SELECT TOP 50 latitude ,longitude,type FROM dbo.earthquakedata WHERE type='earthquake'"
        # print("Query-0", query0)
        cursor06.execute(query06)
        output06 = cursor06.fetchall()

        cursor06.execute(query06B)
        output06B = cursor06.fetchall()
        # print("All Records: ",cursor06.fetchall())
        #https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
        for row in output06:
            print("ROW11")
            # allRecords.append({"latitude": row[0], "longitude": row[1], "type": row[2]})
            # arlington_coordinates = (32.7324106535524, -97.11266783050309)
            anchorage_coordinates = (formLatitude1, formLongitude1)
            earthquakes_coordinates = (row[0], row[1])
            distance = geopy.distance.distance(anchorage_coordinates, earthquakes_coordinates).kilometers
            print("-----")
            print(anchorage_coordinates)
            print(earthquakes_coordinates)
            print(distance)
            if distance < formRadius1:
            # if distance < 1000:
                allRecordsAnchorage.append({"latitude": row[0], "longitude": row[1], "type": row[2], "distance": distance})
        print(allRecordsAnchorage)
        # print("All Records: ",cursor06.fetchall())
        for rowDallas in output06B:
            print("ROW 2")
            # allRecords.append({"latitude": row[0], "longitude": row[1], "type": row[2]})
            # arlington_coordinates = (32.7324106535524, -97.11266783050309)
            dallas_coordinates = (formLatitude2, formLongitude2)
            earthquakes_coordinates = (rowDallas[0], rowDallas[1])
            distance1 = geopy.distance.distance(dallas_coordinates, earthquakes_coordinates).kilometers
            print("-----")
            print(dallas_coordinates)
            print(earthquakes_coordinates)
            print(distance1)
            if distance1 < formRadius2:
            # if distance < 1000:
                allRecordsDallas.append({"latitude": rowDallas[0], "longitude": rowDallas[1], "type": rowDallas[2], "distance1": distance1})
        
        quakesAtAnchorage = len(allRecordsAnchorage)
        quakesAtDallas = len(allRecordsDallas)

        print(quakesAtAnchorage)
        print(quakesAtDallas)

        if quakesAtAnchorage > quakesAtDallas:
            onSuccess = "Anchrorage has: {0} earthqauakes and Dallas has {1} within given range.\n Earthquakes at Anchorage are more common than Dallas".format(quakesAtAnchorage, quakesAtDallas)
        else:
            onSuccess = "Anchrorage has: {0} earthqauakes and Dallas has {1} within given range.\n Earthquakes at Dallas are more common than Anchorage".format(quakesAtAnchorage, quakesAtDallas)

        connectDB_06.close()

        if quakesAtAnchorage == 0 and quakesAtDallas == 0:
            return render_template('commonQuakes.html', onFailure = "Records Not found")
        else:
            return render_template('commonQuakes.html', onSuccess = onSuccess)

########################################Query07########################################
## Night quakes
@app.route('/nightQuakes', methods = ['GET', 'POST'])
def nightQuakes():
    # if request.method == 'GET':
    allRecords = []
    # searchName = request.form['name']
    connectDB_07 = connection()
    cursor07 = connectDB_07.cursor()
    query07 = "SELECT * FROM dbo.earthquakedata WHERE mag > 4.0 AND (DATEPART(hour,time) >= 18 OR DATEPART(hour,time) <= 06)"
    # print("Query-0", query0)
    cursor07.execute(query07)
    # print("All Records: ",cursor.fetchall())
    for row in cursor07.fetchall():
        # print("row[3]]",row[3])
        # if row[3] == "" or row[3]== " " or row[3]==None:
        #     row[3] = "defaultUser.jpg"
        # picturPath = "static/"+row[3]
        allRecords.append({"time": row[0], "place": row[13], "mag": row[4], "id": row[11]})
    connectDB_07.close()
    countAllRec = len(allRecords)
    # print("List of Rec-", allRecords)
    if len(allRecords) < 1:
        return render_template('nightQuakes.html', onFailure = "Records not found")
    else:
        return render_template('nightQuakes.html', onSuccess = "Record Found", allRecords = allRecords, countAllRec = countAllRec )


########################################Query08########################################
@app.route('/clusterQuakes', methods = ['GET', 'POST'])
def clusterQuakes():
    # if request.method == 'GET':
    allRecords81 = []
    allRecords82 = []
    allRecords83 = []
    # searchName = request.form['name']
    connectDB_08 = connection()
    cursor08 = connectDB_08.cursor()

    query081 = "SELECT TOP 10 * FROM dbo.earthquakedata WHERE mag BETWEEN 1.0 AND 2.0 ORDER BY mag DESC"
    cursor08.execute(query081)
    output081 = cursor08.fetchall()
    for row in output081:
        allRecords81.append({"time": row[0], "mag": row[4], "place": row[13], "id": row[11]})
    
    query082 = "SELECT TOP 10 * FROM dbo.earthquakedata WHERE mag BETWEEN 2.0 AND 3.0 ORDER BY mag DESC"
    cursor08.execute(query082)
    output082 = cursor08.fetchall()
    for row in output082:
        allRecords82.append({"time": row[0], "mag": row[4], "place": row[13], "id": row[11]})

    query083 = "SELECT * FROM dbo.earthquakedata WHERE mag BETWEEN 2.0 AND 3.0 ORDER BY mag DESC"
    cursor08.execute(query083)
    output083 = cursor08.fetchall()
    for row in output083:
        allRecords83.append({"time": row[0], "mag": row[4], "place": row[13], "id": row[11]})

    print("---")
    print(allRecords81)
    print(allRecords82)
    print(allRecords83)
    connectDB_08.close()
    # print("List of Rec-", allRecords)
    if len(allRecords81) == 0 and len(allRecords82) == 0 and len(allRecords83) == 0:
        return render_template('clusterQuakes.html', onFailure = "Records not found")
    else:
        return render_template('clusterQuakes.html',onSuccess = "Clusters Found", cluster1 = allRecords81, cluster2 =allRecords82, cluster3 = allRecords83)

########################################FINISH########################################
########################################FINISH########################################
########################################FINISH########################################
########################################FINISH########################################

if __name__ == '__main__':
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


 





