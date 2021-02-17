from flask import Flask, render_template , request
from flask_mysqldb import MySQL
import random

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')

mysql = MySQL(app)

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
			return render_template('index.html')
		except Exception as e:
				print(e)
	return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)