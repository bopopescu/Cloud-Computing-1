from flask import render_template, redirect, url_for, request, g
from app import webapp

import boto3
import json
import decimal

import tempfile
import os



@webapp.teardown_appcontext
def teardown_db(exception):

    return

@webapp.route('/signup',methods=['GET'])
#Return file upload form
def signup():
    return render_template("signup.html")


@webapp.route('/signup_submit',methods=['POST'])
#Signup a new Account
def signup_submit():

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')

    username = request.form.get("n1")
    password = request.form.get("n2")

    error = False

    if username == "" or password== "":
        error=True
        error_msg="Error: All fields are required!"

    response = table.get_item(
        Key={
            'username': username
        }
    )

    #TODO: get the row from

    if 'Item' in response:
        error = "Error! Username is already exist!"
        return render_template("signup.html",  error_msg  =error,)

    if error:
        return render_template("signup.html", error_msg  =error_msg,)

    response = table.put_item(
    Item = {
        'username' : username,
        'password' : password
    }

)


    return redirect(url_for('login'))