from colorama import Cursor
from flask import Flask, render_template, request, redirect
import csv
import pyodbc

app = Flask(__name__)

##REFERENCES
#https://www.tutorialspoint.com/what-is-python-commit-method-in-mysql

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
# POST corresponds to adding an element
# GET corresponds to fetch data
# @app.route('/searchByName', methods=['GET','POST'])

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

########################################Query01########################################
@app.route('/searchName', methods = ['GET', 'POST'])
def searchName():
    # completeCSV = csv.DictReader(open("data.csv"))
    return render_template('searchName.html')

@app.route('/resultImage', methods = ['GET', 'POST'])
def resultImage():
    if request.method == 'POST':
        searchName = request.form['searchName']
        allRecords = []
        connectDB = connection()
        con_cursor = connectDB.cursor()
        # con_cursor.execute("SELECT Picture FROM dbo.people WHERE Name = 'Dhruvi'")
        query1 = "SELECT * FROM dbo.people WHERE Name = '{0}'".format(searchName)
        print("Query-1", query1)
        con_cursor.execute(query1)
        
        for perRecord in con_cursor.fetchall():
            if perRecord[6] == "" or perRecord[6] == " " or perRecord is None:
                perRecord[6] = 'xyz.jpg'
            picturePath = "static/{0}".format(perRecord[6])
            allRecords.append({'name': perRecord[0], 'state': perRecord[1],'salary': perRecord[2],'grade': perRecord[3],'room': perRecord[4],'telnum': perRecord[5],'picture': picturePath,'keyword': perRecord[7] })
        
        connectDB.close()
        if len(allRecords) < 1:
            return render_template('searchName.html', onFailure = "Records not found")
        else:
            return render_template('searchName.html', onSuccess = "Record Found", allRecords = allRecords )

########################################Query02########################################
@app.route('/salaryLessPic', methods = ['GET', 'POST'])
def salaryLessPic():
    # completeCSV = csv.DictReader(open("data.csv"))
    allRecords = []
    connectDB = connection()
    cursor2 = connectDB.cursor()
    query02 = "SELECT * FROM dbo.people WHERE Salary < 99000"
    print("Query-1", query02)
    cursor2.execute(query02)
    for row in cursor2.fetchall():
        print("row[6]]",row[6])
        if row[6] == "" or row[6]== " " or row[6]==None:
            row[6] = "defaultUser.jpg"
        picturPath = "static/"+row[6]
        allRecords.append({"name": row[0], "state": row[1], "salary": row[2], "grade": row[3], "room": row[4], "telnum": row[5], "picture": picturPath, "keywords": row[7]})
    connectDB.close()
    print("List of Rec-", allRecords)
    return render_template("salaryLessPic.html", allRecords = allRecords)

########################################Query03########################################
# @app.route('/addPic', methods = ['GET', 'POST'])
# def addPic():
#     # completeCSV = csv.DictReader(open("data.csv"))
#     return render_template('addPic.html')
########################################Query04########################################
@app.route('/removeRec', methods = ['GET', 'POST'])
def removeRec():
    # completeCSV = csv.DictReader(open("data.csv"))
    return render_template('removeRec.html')

@app.route('/recordRemoved', methods = ['GET', 'POST'])
def recordRemoved():
    if request.method == 'POST':
        searchName = request.form['name']
        connectDB_04 = connection()
        cursor04 = connectDB_04.cursor()
        query04 = "DELETE FROM dbo.people WHERE Name='{0}'".format(searchName)
        cursor04.execute(query04)
        # print(cursor04.execute(query04))
        # print(cursor04.rowcount)
        connectDB_04.commit()
        connectDB_04.close()
        return redirect('/')
        
########################################Query05########################################
@app.route('/updateKeyword', methods = ['GET', 'POST'])
def updateKeyword():
    # completeCSV = csv.DictReader(open("data.csv"))
    return render_template('updateKeyword.html')

@app.route('/keywordUpdated', methods = ['GET', 'POST'])
def keywordUpdated():
    if request.method == 'POST':
        name = request.form['name']
        keyword = request.form['keyword']
        connectDB5 = connection()
        cursor05 = connectDB5.cursor()
        query05 = "UPDATE dbo.people SET Keywords = '{0}' WHERE Name='{1}';".format(keyword,name)
        cursor05.execute(query05)
        # For update and delete the cursor execute will have no records
        # print(cursor.execute(query05))
        connectDB5.commit()
        recordCount = cursor05.rowcount
        connectDB5.close()
        if recordCount <= 0:
            return render_template('updateKeyword.html', onFailure = "Records not found")
        else:
            return render_template('updateKeyword.html', onSuccess = "Record Found", recordCount = recordCount )


########################################Query06########################################
@app.route('/updateSalary', methods = ['GET', 'POST'])
def updateSalary():
    # completeCSV = csv.DictReader(open("data.csv"))
    return render_template('updateSalary.html')

@app.route('/salaryChanged', methods = ['GET', 'POST'])
def salaryChanged():
    if request.method == 'POST':
        name = request.form['name']
        salary = request.form['salary']
        connectDB_06 = connection()
        cursor06 = connectDB_06.cursor()
        query06 = "UPDATE dbo.people SET Salary = '{0}' WHERE Name='{1}'".format(salary, name)
        print("Query-1", query06)
        cursor06.execute(query06)
        # print("All Records: ",cursor.fetchall())
        cursor06.commit()
        recordCount = cursor06.rowcount
        connectDB_06.close()
        # print("List of Rec-", allRecords)
        if recordCount <= 0:
            return render_template('updateSalary.html', onFailure = "Records not found")
        else:
            return render_template('updateSalary.html', onSuccess = "Record Salary Updated", recordCount = recordCount )

########################################Query03########################################

########################################FINISH########################################

if __name__ == '__main__':
    app.run(debug=True, port=8091)
    # app.run()

########################################CLONE########################################
"""
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


 





