from flask import render_template, redirect, url_for, request, g
from app import webapp

import mysql.connector
from app.config import db_config

import random
import tempfile
import os


def connect_to_database():
    return mysql.connector.connect(user=db_config['user'],
                                   password=db_config['password'],
                                   host=db_config['host'],
                                   database=db_config['database'])

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

@webapp.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@webapp.route('/signup',methods=['GET'])
#Return file upload form
def signup():
    return render_template("signup.html")


@webapp.route('/signup_submit',methods=['POST'])
#Signup a new Account
def signup_submit():
    cnx = get_db()
    cursor = cnx.cursor()

    userid = request.form.get("n1")
    password = request.form.get("n2")


    error = False

    if userid == "" or password== "":
        error=True
        error_msg="Error: All fields are required!"

    query = '''SELECT * FROM users WHERE login = %s '''
    cursor.execute(query,(userid, ))

    row = cursor.fetchone()
    if row:
        error = "Error! Username is already exist!"
        return render_template("signup.html",  error_msg  =error,)

    if error:
        return render_template("signup.html", error_msg  =error_msg,)


    query = ''' INSERT INTO users( login, password) VALUES (%s, %s)
            '''

    useridnum = random.randint(1,100)

    cursor.execute(query,(userid, password))
    cnx.commit()

    return redirect(url_for('store'))