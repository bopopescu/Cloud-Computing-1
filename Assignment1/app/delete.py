from flask import render_template, session, request, redirect, url_for, g
from app import webapp

from app.config import s3_config
import mysql.connector
from app.config import db_config
import os
import boto3
from botocore.client import Config



s3=boto3.client('s3','us-east-1',config=Config(s3={'addressing_style': 'path'}))


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



@webapp.route('/delete',methods=['get'])
def delete():
    query = '''
    TRUNCATE TABLE project1.images
    SET FOREIGN_KEY_CHECKS = 0;
    TRUNCATE TABLE project1.users;
    SET FOREIGN_KEY_CHECKS = 1;

    '''

    cnx = get_db()
    cursor = cnx.cursor()
    cursor.execute(query,multi=True)
    session.clear()
    ss3 = boto3.resource('s3')
    buc = ss3.Bucket(s3_config['bucketid'])

    for key in buc.objects.all():
        key.delete()


    return redirect(url_for('main'))



