import unittest
import app
import os 
from app import app
import hashing 
import database
from flask import url_for
from flask import Flask, render_template , request,redirect,session
import requests
import database


class BasicTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()



    def test_signin(self):
        url = 'http://127.0.0.1:5000/signin'
        response = requests.post(url, data=dict(username='ThoShe89', password='Housebunnys12'))
        data = str(response.text)
        self.assertIn("Account Details",data)

    def test_fail_signin(self):
        url = 'http://127.0.0.1:5000/signin'
        response = requests.post(url, data=dict(username='ThoShe89', password='Houbunnys12'))
        data = str(response.text)
        self.assertNotIn("Account Details",data)

    def test_logout(self):        
        url = 'http://127.0.0.1:5000/signin'
        response = requests.post(url, data=dict(username='ThoShe89', password='Houbunnys12'))
        url = 'http://127.0.0.1:5000/signout'       
        response = requests.get(url)
        data = str(response.text)
        self.assertNotIn('Thoshe89', data)


    def test_rentacar(self):
        url = 'http://127.0.0.1:5000/signin'
        response = requests.post(url, data=dict(username='ThoShe89', password='Houbunnys12'))
        url = 'http://127.0.0.1:5000/rent' 
        response = requests.post(url,data=dict(username = 'ThoShe89',points = '67',carrented = 'Land Rover',modelnumber = 'Defender',duration = '5',category = 'offroad',carprice = '100',carid = '02'))
        data = str(response.text)
        print(data)





        


 
       


    


if __name__ == '__main__':
    unittest.main()