from flask import Flask, render_template , request,redirect,session
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
from PIL import Image

import random


 ## modules 
import hashing 
import database
 



app = Flask(__name__,
            static_folder='static',
            template_folder='templates')


app.config["SECRET_KEY"] = "OCML3BRawWEUeaxcuKHLpw"

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
		fname = request.form['fname']
		lname = request.form['lname']
		userID = random.randint(0,100)
		username = fname[0:3] + lname[0:3] + str(userID)
		password = request.form['confirmpassword']
		hashedpassword = hashing.hash_password(password)

		colour = request.form['colour']
		email = request.form['email']
		fullname = fname +" "+lname
		database.addnewuser(username,hashedpassword,colour,email,fullname)
		msg = Message('Account Credentials', sender = 'urentalsttgmail.com', recipients = [email])
		msg.body = "Your userID is: "+username+" and password is: "+password+" Feel free to login to you account at https://universalrentals.herokuapp.com/login"
	return render_template('index.html')


@app.route("/signin", methods=['GET','POST'])
def signing():
	if request.method == 'POST':
		session['username'] = str(request.form['username'])
		password = str(request.form['password'])
		username = session['username']
		record = database.getuserinfo(username)
		if(len(record)==0):
			message = "Username not found"
			return render_template('login.html',message = message)

		passwordinput = record[0][1]
			
		if(hashing.verify_password(passwordinput, password)):
				records = database.getuserinfo(username)
				totalpoints= database.getuserpoints(username)
				profileinfo = {
					'username':records[0][0],
					'fullname':records[0][4],
					'email':records[0][3],
					'totalpoints':totalpoints,
					}
				rentalhistory = database.getrentalhistory(username)
				carinfo = database.availablecars()
				return render_template('profile.html',user = profileinfo, history = rentalhistory , car = carinfo)
		message = "Password Incorrect"
		return render_template('login.html',message = message)



@app.route("/profilepic", methods=['GET','POST'])
def savepic():
    if request.method == 'POST':
        username = str(request.form['username'])
        pict = str(request.form['myImage'])
    return render_template('profile.html')

@app.route("/rent", methods=['GET','POST'])
def rent():
	if request.method == 'POST':
		username = session['username']
		points = int(database.getuserpoints(username))
		carrented = str(request.form['carrented'])
		modelnumber = str(request.form['modelnumber'])
		duration = str(request.form['duration'])
		category = str(request.form['category'])
		carprice = str(request.form['carprice'])
		carid = str(request.form['carid'])
		
		if (int(points)>50):
			pointsused = str(request.form['points'])
			if(pointsused==''):
				pointsused = 0
			totalcost = float(carprice) + (int(duration) * 100) - int(pointsused)
			pointsearned = int(pointsused)
			totalpoints = points - pointsearned
			database.updatepoints(totalpoints,username)
		else:
			pointsused = 0
			totalcost = float(carprice) + (int(duration) * 100) - pointsused
			pointsearned = int(duration) * 50
			database.updatepoints(pointsearned,username)	
		database.insertrental(username,carrented,modelnumber,duration,category,pointsearned,totalcost)
		database.updatecarstatus(carid)

		notice = "car succesfully rented using "+str(pointsused)+" points thank you for using Universal Rentals"	
		
		return render_template('index.html')
		

@app.route("/adminprofile")
def showpage():
	username = session['username']
	records = database.getadminlogin(username)	
	profileinfo = {
		'adminid':records[0][0],
		'fullname':records[0][1],
		'email':records[0][3],
		'phonenumber':records[0][4]
				}
	return render_template('admininfo.html',profileinfo=profileinfo)

@app.route("/adminlogin")
def admin():
	return render_template('adminlogin.html')

@app.route("/adminsignin", methods=['GET','POST'])
def adminsigning():
	if request.method == 'POST':
		session['username'] = str(request.form['username'])
		password = str(request.form['password'])
		username = session['username']
		record = database.passwordselectoradmin(username)
		passwordinput = record[0][0]
		if(len(record)==0):
			message = "Username not found"
			return render_template('adminlogin.html',message = message)
		if(password == passwordinput):
				records = database.getadminlogin(username)	
				profileinfo = {
					'adminid':records[0][0],
					'fullname':records[0][1],
					'email':records[0][2],
					'phonenumber':records[0][3]
					}
				rentalhistory = database.getadminrentalhistory()
				rentotal = database.numberofrents()
				totalcost=database.totalcostofrents()
				numberofusers = database.numberofusers()
				profileinfo = {
					'users':numberofusers[0][0],
					'rents':rentotal[0][0],
					'sales':totalcost,
							}
				usertotals = database.getcostbyuser()
				return render_template('dashboard.html',history=rentalhistory, admininfo=profileinfo, userandtotal=usertotals)
		message = "Password Incorrect"
		return render_template('adminlogin.html',message = message)
		
@app.route("/removecar")
def removecar():
	username = session['username']
	records = database.getcars()
	return render_template('removecar.html',car=records)


@app.route("/removecustomer")
def removecustomer():
	username = session['username']
	users = database.getusers()
	return render_template('removeperson.html',userdata=users)


if __name__ == '__main__':
    app.run(debug=True)