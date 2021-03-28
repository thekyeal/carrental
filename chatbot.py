from flask_mail import Mail, Message
from flask import Flask, render_template , request,redirect,session
from flask_mysqldb import MySQL
from flask_mysql_connector import MySQL
import mysql.connector

confi = {
    'host': 'unirentals.mysql.database.azure.com',
    'user': 'Kreation@unirentals',
    'password': 'KyealAnnaKeidell@',
    'database': 'unirentals'
}

conn = mysql.connector.connect(**confi)
cursor = conn.cursor()
#cursor.execute("Insert Into users(username,password1,colour,email_address,fullname) VALUES ('John ','adsfdfsfsd ', ' green ', ' email ','fullname')")
conn.commit()

cursor.execute("Select * from users")






