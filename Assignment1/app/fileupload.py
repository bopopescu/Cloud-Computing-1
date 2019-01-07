from flask import render_template, redirect, url_for, request, g
from app import webapp

import mysql.connector
from app.config import db_config


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

@webapp.route('/test/FileUpload/form',methods=['GET'])
#Return file upload form
def upload_form():
    return render_template("fileupload/form.html")


@webapp.route('/test/FileUpload',methods=['POST'])
#Upload a new file and store in the systems temp directory
def file_upload():
    cnx = get_db()
    cursor = cnx.cursor()

    userid = request.form.get("userID")
    password = request.form.get("password")

    query = '''SELECT  *
               FROM  users as u
               WHERE u.userid== %s AND u.password = %s'''

    error = False
    if query:
        error=True
        error_msg="The username or password you entered is already used. Please try different user or password."

    if userid == "" or password== "":
        error=True
        error_msg="Error: All fields are required!"

    if error:
        return render_template("fileupload/form.html", error_msg  =error_msg,)

    # check if the post request has the file part
    if 'uploadedfile' not in request.files:
        return "Missing uploaded file"

    query = ''' INSERT INTO users(login, password) VALUES (%s, %s)
            '''

    cursor.execute(query,(userid, password))
    cnx.commit()

    new_file = request.files['uploadedfile']

    # if user does not select file, browser also
    # submit a empty part without filename
    if new_file.filename == '':
        return 'Missing file name'

    tempdir = tempfile.gettempdir()

    new_file.save(os.path.join(tempdir,new_file.filename))

    return "Success"
