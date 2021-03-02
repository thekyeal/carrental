from flask import Flask, render_template , request,redirect
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from PIL import Image

import random
import hashlib
import os
import binascii
 
def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',provided_password.encode('utf-8'),salt.encode('ascii'),100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password



app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] ='koolkat90210@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] ='koolkat90210@gmail.com'
app.config['MAIL_PASSWORD'] ='bananapie1'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mysql = MySQL(app)
mail = Mail(app)

app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'M7faRQD6wL'
app.config['MYSQL_PASSWORD'] = 'Yg0gCXFrly'
app.config['MYSQL_DB'] = 'M7faRQD6wL'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route("/createaccount", methods=['POST'])
def createaccount():
	if request.method == 'POST':
		message = "Account Created! Please check your email for your login credentials"
		fail = "Error in creating account, please try again"
		name = request.form['username']
		userID = random.randint(0,100)
		x = name.split()
		fname = x[0]
		lname = x[1]
		username = fname[0:3] + lname[0:3] + str(userID)
		password = request.form['confirmpassword']
		hashedpassword = hash_password(password)

		colour = request.form['colour']
		email = request.form['email']

		conn = mysql.connect
		cursor = conn.cursor()
		try:
			cursor.execute("Insert Into users(username,password,colour,email_address,fullname) VALUES ('"+ username +"','"+ hashedpassword + "', '"+ colour + "', '"+ email +"','"+name+"')")
			conn.commit()
			msg = Message('Account Credentials', sender = 'urentalsttgmail.com', recipients = [email])
			msg.body = "Your userID is: "+username+" and password is: "+password+" Feel free to login to you account at https://universalrentals.herokuapp.com/login"
			mail.send(msg)
			return render_template('index.html')
		except Exception as e:
				print(e)
	return render_template('index.html')

@app.route("/signin", methods=['GET','POST'])
def signing():
	if request.method == 'POST':
		username = str(request.form['username'])
		password = str(request.form['password'])
		conn = mysql.connect
		cursor = conn.cursor()
		cursor.execute("SELECT password FROM users WHERE username='"+username+"'")
		record = cursor.fetchall()
		passwordinput = record[0][0]
		if(len(record)==0):
			message = "Username not found"
			return render_template('login.html',message = message)
		if(verify_password(passwordinput, password)):
				cursor1 = mysql.connection.cursor()
				cursor1.execute("select * from users where username='"+username+"'")
				records = cursor1.fetchall()	
				pointsq = "select pointsEarned from RentalHistory where username='"+username+"'"
				cursor3 = mysql.connection.cursor()
				cursor3.execute(pointsq)
				pointsq = cursor3.fetchall()
				totalpoints=sum(t[0] for t in pointsq)		
				profileinfo = {
					'username':records[0][0],
					'fullname':records[0][4],
					'email':records[0][3],
					'totalpoints':totalpoints,
					}
				rentalhistory = "select carRented,modelNo,duration,category,pointsEarned,totalCost from RentalHistory where username='"+username+"'"
				cursor2 = mysql.connection.cursor()
				cursor2.execute(rentalhistory)
				rentalhistory = cursor2.fetchall()
				return render_template('profile.html',user = profileinfo, history = rentalhistory)
		message = "Password Incorrect"
		return render_template('login.html',message = message)

@app.route("/profile")
def showpage():
	return render_template('profile.html')

@app.route("/profilepic", methods=['GET','POST'])
def savepic():
    if request.method == 'POST':
        username = str(request.form['username'])
        pict = str(request.form['myImage'])
    return render_template('profile.html')



if __name__ == '__main__':
    app.run(debug=True)