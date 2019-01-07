from flask import render_template, session, request, redirect, url_for, g
from app import webapp

import boto3
from boto3.dynamodb.conditions import Key, Attr

webapp.secret_key = '\x80\xa9s*\x12\xc7x\xa9d\x1f(\x03\xbeHJ:\x9f\xf0!\xb1a\xaa\x0f\xee'


@webapp.teardown_appcontext
def teardown_db(exception):

    return

@webapp.route('/login_submit',methods=['POST'])
def login_submit():

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('users')

    username = request.form.get('n1','')
    password = request.form.get('n2','')

    if username == '' or  password =='':
        error = "Error! Username or password is required!"
        return render_template("login.html", error = error, n1=username, n2=password)

    response = table.scan(
        FilterExpression = Attr('username').eq(username) & Attr('password').eq(password)
    )

    if 'Items' not in response or not response['Items']:
        error = "Error! There's a problem with your username or password!"
        return render_template("login.html", error = error, n1=username, n2=password)

    else:
        session['auth'] = username
        return redirect(url_for('store'))



@webapp.route('/login/store',methods=['GET','POST'])
def store():
  # if 'username' not in session:
    if 'auth' not in session:
        return redirect(url_for('login'))

    return redirect(url_for('welcome'))


@webapp.route('/logout',methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('main'))

@webapp.route('/login',methods=['GET','POST'])
def login():
    return render_template("login.html", error = "")

@webapp.route('/welcome',methods=['GET','POST'])
def welcome():
    return render_template("welcome.html", user = session['auth'])