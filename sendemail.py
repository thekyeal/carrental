from flask import Flask, render_template , request,redirect,session
from flask_mysqldb import MySQL
from flask_mail import Mail, Message

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'urentalstt@gmail.com'
app.config['MAIL_PASSWORD'] = 'jwwwmimewqfwhqku'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True



mail = Mail(app)

def sendemail(email,username):
    msg = Message('Account Credentials', sender = 'urentalsttgmail.com', recipients = [email])
    msg.body = "Your userID is: "+username+" \n Feel free to login to you account at https://universalrentals.herokuapp.com/login \n Thank you for registring"
    mail.send(msg)


