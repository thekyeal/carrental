from flask_mail import Mail, Message
from flask import Flask, render_template , request,redirect,session
from flask_mysqldb import MySQL

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

mysql = MySQL(app)

app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'M7faRQD6wL'
app.config['MYSQL_PASSWORD'] = 'Yg0gCXFrly'
app.config['MYSQL_DB'] = 'M7faRQD6wL'


def addnewuser(username,hashedpassword,colour,email,fullname):
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("Insert Into users(username,password,colour,email_address,fullname) VALUES ('"+ username +"','"+ hashedpassword + "', '"+ colour + "', '"+ email +"','"+fullname+"')")
    conn.commit()


def getuserinfo(username):
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("select * from users where username='"+username+"'")
    records = cursor.fetchall()
    return records

def getadminlogin(username):
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("select * from admin where adminID='"+username+"'")
    records = cursor.fetchall()
    return records

def passwordselectoradmin(username):
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM admin WHERE adminID='"+username+"'")
    password = cursor.fetchall()
    return password

def passwordselector(username):
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username='"+username+"'")
    password = cursor.fetchall()
    return password



def getuserpoints(username):
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("select points from users where username='"+username+"'")
    points = cursor.fetchall()
    return points[0][0]

def getrentalhistory(username):
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("select carRented,modelNo,duration,category,pointsEarned,totalCost from RentalHistory where username='"+username+"'")
    rentalhistory = cursor.fetchall()
    return rentalhistory

def availablecars():
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("Select * from cars WHERE carStatus='Available' LIMIT 3")
    cars = cursor.fetchall()
    return cars

def updatepoints(totalpoints,username):
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET points = '"+str(totalpoints)+"' WHERE username = '"+username+"'")
    conn.commit()

def insertrental(username,carrented,modelnumber,duration,category,pointsearned,totalcost):
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("insert into RentalHistory(username,carRented,modelNo,duration,category,pointsEarned,totalcost) Values ('"+username+"','"+carrented+"','"+modelnumber+"','"+duration+"','"+category+"','"+str(pointsearned)+"','"+str(totalcost)+"') ")
    conn.commit()

def updatecarstatus(carid):
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("UPDATE cars SET carStatus = 'Unavailable' WHERE carid = '"+carid+"'")
    conn.commit()

def getadminrentalhistory():
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("select username,carRented,duration,totalCost from RentalHistory ")
    adminrentalhistory = cursor.fetchall()
    return adminrentalhistory

def numberofrents():
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM RentalHistory")
    rents = cursor.fetchall()
    return rents

def totalcostofrents():
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("select totalCost from RentalHistory")
    costtotal = cursor.fetchall()
    totalcost=sum(t[0] for t in costtotal)
    return totalcost

def numberofusers():
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    countuser = cursor.fetchall()
    return countuser

def getcostbyuser():
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("select username, SUM(totalCost) from RentalHistory group by username ")
    usertotals = cursor.fetchall()
    return usertotals

def getcars():
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("select * from cars ")
    cardata = cursor.fetchall()
    return cardata

def removecar(carid):
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("SET foreign_key_checks = 0")
    cursor.execute("delete from cars where carID ='"+carid+"'")
    conn.commit()
    cursor.execute("SET foreign_key_checks = 1")

def getusers():
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("select * from users ")
    userdata = cursor.fetchall()
    return userdata


def removepersonel(cusid):
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("SET foreign_key_checks = 0")
    cursor.execute("delete from users where username ='"+cusid+"'")
    conn.commit()
    cursor.execute("SET foreign_key_checks = 1")

def insertpackage(packageid,carID,carrented,modelnumber,duration,category,totalcost,points):
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("insert into packages(packageID,carID,rentedCar,modelnumber,rentDuration,Category,totalCost,rewardedPoints) Values ('"+packageid+"','"+carID+"','"+carrented+"','"+modelnumber+"','"+duration+"','"+category+"','"+str(totalcost)+"','"+str(points)+"') ")
    conn.commit()

def loadpackages():
    conn = mysql.connect
    cursor = conn.cursor()
    cursor.execute("select * from packages ")
    packages = cursor.fetchall()
    return packages
