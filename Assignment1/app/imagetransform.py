from flask import render_template, redirect, url_for, request, session, g
from app import webapp

import tempfile
import os

import mysql.connector
from app.config import db_config
from app.config import s3_config

from wand.image import Image
import boto3

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

@webapp.route('/imagetransform/form',methods=['GET'])
#Return file upload form
def image_form():
    return render_template("imagetransform/form.html")


@webapp.route('/imagetransform',methods=['POST'])
#Upload a new image and tranform it
def image_transform():

    # check if the post request has the file part
    if 'image_file' not in request.files:
        return "Missing uploaded file"

    new_file = request.files['image_file']

    # if user does not select file, browser also
    # submit a empty part without filename
    if new_file.filename == '':
        return 'Missing file name'

    # s3.Object('farshadsafavi-1',new_file.filename).put(Body=new_file)

    tempdir = tempfile.gettempdir()
    fname = os.path.join('app/static/',new_file.filename)
    new_file.save(fname)

    s3_client = boto3.client('s3')
    # Upload the file to S3
    name_file = session['auth'] + '_' + new_file.filename
    s3_client.upload_file(fname, s3_config['bucketid'], name_file)


    #Transform the image
    img = Image(filename=fname)
    i = img.clone()
    i.rotate(90)
    fname_rotated = os.path.join('app/static','rotated_' + new_file.filename)
    i.save(filename=fname_rotated)
    # Upload the file to S3
    s3_client = boto3.client('s3')
    name_file_rotated = session['auth'] + '_rotated_' + new_file.filename
    s3_client.upload_file(fname_rotated, s3_config['bucketid'], name_file_rotated)


    img = Image(filename=fname)
    i = img.clone()
    i.flip()
    fname_flipped = os.path.join('app/static','flip_' + new_file.filename)
    i.save(filename=fname_flipped)
    # Upload the file to S3
    s3_client = boto3.client('s3')
    name_file_flipped = session['auth'] + '_flipped_' + new_file.filename
    s3_client.upload_file(fname_flipped, s3_config['bucketid'], name_file_flipped)


    img = Image(filename=fname)
    i = img.clone()
    i.flop()
    fname_flopped = os.path.join('app/static','flop_' + new_file.filename)
    i.save(filename=fname_flopped)
     # Upload the file to S3
    s3_client = boto3.client('s3')
    name_file_flopped = session['auth'] + '_flopped_' + new_file.filename
    s3_client.upload_file(fname_flopped, s3_config['bucketid'], name_file_flopped)

    cnx = get_db()
    cursor = cnx.cursor()
    userId = session['id']
    key1   = name_file
    key2   = name_file_rotated
    key3   = name_file_flipped
    key4   = name_file_flopped

    query = ''' INSERT INTO images(userId, key1, key2, key3, key4 ) VALUES (%s, %s, %s, %s, %s)
            '''
    cursor.execute(query,(userId, key1, key2, key3, key4 ))
    cnx.commit()



    print(fname[4:])

    return render_template("imagetransform/view.html",
                           f1=fname[4:],
                           f2=fname_rotated[4:],
                           f3=fname_flipped[4:],
                           f4=fname_flopped[4:])


