from flask_mail import Mail, Message
from flask import Flask, render_template , request,redirect,session
from flask_mysqldb import MySQL
from flask_mysql_connector import MySQL
import mysql.connector

confi = {
    'host': 'carrentals.mysql.database.azure.com',
    'user': 'kreation@carrentals',
    'password': 'Wethepeople@3',
    'database': 'universalRentals',
    'port' : '3306'
}


conn = mysql.connector.connect(**confi)
cursor = conn.cursor()
#cursor.execute("Insert Into users(username,password,colour,email_address,fullName) VALUES ('John ','adsfdfsfsd ', ' green ', ' email ','fullname')")
#conn.commit()

#cursor.execute("Select * from users")
#rentalhistory = cursor.fetchall()

#print(rentalhistory)

def getuserinfocb(username):
    conn = mysql.connector.connect(**confi)
    cursor = conn.cursor()
    cursor.execute("select * from users where username='"+username+"'")
    records = cursor.fetchall()
    print(records[0][2])
    return records

def getuserpointscb(username):
    conn = mysql.connector.connect(**confi)
    cursor = conn.cursor()
    cursor.execute("select points from users where username='"+username+"'")
    points = cursor.fetchall()
    return points[0][0]

def updatepointscb(totalpoints,username):
    conn = mysql.connector.connect(**confi)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET points = '"+str(totalpoints)+"' WHERE username = '"+username+"'")
    conn.commit()


