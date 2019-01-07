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
        
        
        

@webapp.route('/gridview',methods=['GET'])
#display all images in the bucket
def gridview():
    
    s3_client = boto3.client('s3')
    s3 = boto3.resource('s3')
    s3.Bucket(s3_config['bucketid'])
    
    #get keys in user
    cnx = get_db()
    cursor = cnx.cursor()
    username = session['auth']
    #print(username)
    query = '''SELECT key1,key2,key3,key4 FROM project1.images Join users on userId = users.id where users.login = %s '''
    cursor.execute(query,(username, ))
    thum_urls = []
    
    row = cursor.fetchone()
    while row is not None:
        
        key = row[0]
        fname_new = os.path.join('app\static',key)   
    #if os.stat(fname_new).st_size == 0:
        s3_client.download_file(s3_config['bucketid'],key,fname_new)
        thum_urls.append(['static/'+key,key,row[1],row[2],row[3]])
        
        row = cursor.fetchone()
    
    
    #for keys with userid x:
    #fname_new = os.path.join('app\static','aaa_kEa5E.jpg')    
    ##print(fname_new)
    
    #s3_client.download_file(s3_config['bucketid'],'aaa_kEa5E.jpg',fname_new)
    #thum_urls= ['static/aaa_kEa5E.jpg','static/flip_test.jpg']
    
    
    
    return render_template("gridview.html", imageurls = thum_urls)

#s3=boto3.resource('s3')

#buckets = s3.buckets.all()



        
        
        
@webapp.route('/choose',methods=['get'])
def choose():
    
    return redirect(url_for('detail_view'))