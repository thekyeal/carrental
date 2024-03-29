from flask import Flask, render_template , request,redirect,session
from flask_mysqldb import MySQL
from flask_sqlalchemy  import SQLAlchemy
from flask_mail import Mail, Message
from PIL import Image

import random
 ## modules 
import hashing 
import database
import chatbot


app = Flask(__name__,
            static_folder='static',
            template_folder='templates')


app.secret_key = 'any random string'


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'urentalstt@gmail.com'
app.config['MAIL_PASSWORD'] = 'jwwwmimewqfwhqku'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


mysql = MySQL(app)
mail = Mail(app)


app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'M7faRQD6wL'
app.config['MYSQL_PASSWORD'] = 'Yg0gCXFrly'
app.config['MYSQL_DB'] = 'M7faRQD6wL'

@app.route("/sendemail")
def index():
   msg = Message('show me boobs', sender = 'urentalstt@gmail.com', recipients = ['koolkat90210@gmail.com'])
   msg.body = "Hello Flask message sent from Flask-Mail"
   mail.send(msg)
   return "Sent"

@app.route('/')
def home():
	session.pop('username', None)
	packages = database.loadpackages()	
	return render_template('index.html',packages=packages)
	
@app.route('/home')
def homepage():
	username = session['username']
	packages = database.loadpackages()	
	return render_template('index.html',packages=packages)


@app.route("/test")
def work():
	return render_template('index.html')

@app.route('/login')
def loginform():
	if 'username' in session:
		username = session['username']
		records = database.getuserinfo(username)
		totalpoints= database.getuserpoints(username)
		profileinfo = {
			'username':records[0][1],
			'fullname':records[0][5],
			'email':records[0][4],
			'totalpoints':totalpoints,
			}
		rentalhistory = database.getrentalhistory(username)
		carinfo = database.availablecars()
		return render_template('profile.html',user = profileinfo, history = rentalhistory , car = carinfo)
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
		msg.body = "Your userID is: "+username+" \n\n Feel free to login to you account at https://universalrentals.herokuapp.com/login \n\n Thank you for registering"
		mail.send(msg)
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
				username = session['username']
				rentalhistory = database.getrentalhistory(username)
				carinfo = database.availablecars()
				return render_template('profile.html',user = profileinfo, history = rentalhistory , car = carinfo, username=username)
		message = "Password Incorrect"
		return render_template('login.html',message = message)
	message = "Feel free to login"
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
		packages = database.loadpackages()

		return render_template('index.html',carrent=notice,packages=packages,user=username)
		

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
		if(len(record)==0):
			message = "Username not found"
			return render_template('adminlogin.html',message = message)
		passwordinput = record[0][0]
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



@app.route("/removevehicle", methods=['GET','POST'])
def removalofcar():
	if request.method == 'POST':
		car =str(request.form['carid'])
		database.removecar(car)
		prompt = "Car deleted"
		records = database.getcars()
	return render_template('removecar.html',message=prompt,car=records)



@app.route("/removecustomer")
def removecustomer():
	username = session['username']
	users = database.getusers()
	return render_template('removeperson.html',userdata=users)

@app.route("/removeperson", methods=['GET','POST'])
def removalofperson():
	if request.method == 'POST':
		cusid =str(request.form['personid'])
		database.removepersonel(cusid)
		message = "User deleted"
		users = database.getusers()
	return render_template('removeperson.html',message=message,userdata=users)



@app.route("/addpackage",methods=['GET','POST'])
def addpackage():
	if request.method == 'POST':
		username = session['username']
		packagename =str(request.form['packageID'])
		carid = str(request.form['carID'])
		carname = str(request.form['carname'])
		modelnumber = str(request.form['modelnumber'])
		duration = str(request.form['duration'])
		category = str(request.form['category'])
		points = str(request.form['points'])
		totalcost = str(request.form['cost'])
		database.insertpackage(packagename,carid,carname,modelnumber,duration,category,totalcost,points)
		message = "Package added!"
		return render_template('addpackage.html',message=message)
	if request.method == 'GET':
		return render_template('addpackage.html')


@app.route("/rentpackage", methods=['GET','POST'])
def rentpackage():
	if request.method == 'POST':
		username = session['username']
		carrented = str(request.form['carrented'])
		modelnumber = str(request.form['modelno'])
		duration = str(request.form['duration'])
		category = str(request.form['category'])
		points = str(request.form['points'])
		totalcost = str(request.form['cost'])	
		database.insertrental(username,carrented,modelnumber,duration,category,points,totalcost)	
		packages = database.loadpackages()	
		rented = 'Package Rented'
		return render_template('index.html',packages=packages,message=rented,user=username)

@app.route("/loginuser", methods=['GET','POST'])
def login():
	if request.method == 'POST':
		session['username'] = str(request.form['username'])
		password = str(request.form['password'])
		username = session['username']
		record = database.getuserinfo(username)
		if(len(record)==0):
			message = "Username not found"
			packages = database.loadpackages()	
			return render_template('index.html',message = message,packages=packages)
		
		passwordinput = record[0][1]			
		if(hashing.verify_password(passwordinput, password)):
			session['username'] = username
			user = session['username']
			packages = database.loadpackages()			
			return render_template('index.html',user = user,packages=packages)
	message = "Password Incorrect"
	packages = database.loadpackages()	
	return render_template('index.html',message = message,packages=packages)
		
@app.route("/signout")
def singout():
	session.pop('username', None)
	packages = database.loadpackages()	
	return render_template('index.html',packages=packages)



@app.route("/addcar")
def showcar():
	return render_template('addcar.html')
	




@app.route("/insertcar",methods=['GET','POST'])
def addcar():
	if request.method == 'POST':
		username = session['username']
		carID =str(request.form['carID'])
		carname =str(request.form['carname'])
		modelnumber = str(request.form['modelnumber'])
		category = str(request.form['category'])
		cost = str(request.form['cost'])
		carstatus = "Available"
		database.addnewcar(carID,carname,modelnumber,category,cost,carstatus)
		message = "Car added!"
		return render_template('addcar.html',message=message)
	if request.method == 'GET':
		return render_template('addcar.html')


		
@app.route("/pickup",methods=['GET','POST'])
def pickup():
	if request.method == 'POST':
		adminemail="koolkat90210@gmail.com"
		email =str(request.form['email'])
		frompoint =str(request.form['frompoint'])
		to = str(request.form['to'])
		leaving = str(request.form['leaving'])
		returning = str(request.form['returning'])
		msg = Message(' New Pick up / Drop Off Reuest', sender = 'urentalsttgmail.com', recipients = [adminemail])
		msg.body = "New Request see details below \n "+email+" would like to be picked up from "+frompoint+" at "+leaving+" \nAnd is going to "+to+" and would like to be collected at "+returning+""
		mail.send(msg)
		packages = database.loadpackages()	
		requesting = "Request sent"
	return render_template('index.html',packages=packages,requested=requesting)

if __name__ == '__main__':
    app.run(debug=True)