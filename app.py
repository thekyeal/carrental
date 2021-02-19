from flask import Flask, render_template , request,redirect
from flask_mysqldb import MySQL
from flask_mail import Mail, Message

import random

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

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
		username = request.form['username']
		userID = random.randint(0,100)
		x = username.split()
		fname = x[0]
		lname = x[1]
		username = fname[0:3] + lname[0:3] + str(userID)
		password = request.form['confirmpassword']
		colour = request.form['colour']
		email = request.form['email']

		conn = mysql.connect
		cursor = conn.cursor()
		try:
			cursor.execute("Insert Into users(username,password,colour,email_address) VALUES ('"+ username +"','"+ password + "', '"+ colour + "', '"+ email +"')")
			conn.commit()
			msg = Message("Your userID is: "+username+" and password is: "+password+" Feel free to login to you account at https://universalrentals.herokuapp.com/login", sender="urentalstt@gmail.com", recipients=[email])
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
		if(len(record)==0):
			message = "Username not found"
			return render_template('login.html',message = message)
		for word in record:
			if password in word:
				return redirect("/profile")
			message = "Password Incorrect"
			return render_template('login.html',message = message)

@app.route("/profile")
def showpage():
	return render_template('profile.html')


if __name__ == '__main__':
    app.run(debug=True)