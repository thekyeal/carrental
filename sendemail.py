from flask import Flask, render_template , request,redirect,session
from flask_mysqldb import MySQL
from flask_mail import Mail, Message

app = Flask(__name__,
            static_folder='static',
            template_folder='templates')




mail = Mail(app)

def sendcredentials(email,username):
    msg = Message('Account Credentials', sender = 'urentalsttgmail.com', recipients = [email])
    msg.body = "Your userID is: "+username+" \n Feel free to login to you account at https://universalrentals.herokuapp.com/login \n Thank you for registring"
    mail.send(msg)


