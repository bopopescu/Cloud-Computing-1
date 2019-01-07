from flask import render_template, session, request, redirect, url_for, g
from app import webapp
from app.config import s3_config

import mysql.connector
from app.config import db_config

import os
import boto3
from botocore.client import Config



@webapp.route('/detail_view',methods=['GET'])
#display all images in the bucket
def detail_view():

#get the 4 keys for this image and display them.

    s3_client = boto3.client('s3')
    s3 = boto3.resource('s3')
    s3.Bucket(s3_config['bucketid'])



    if 'im1' or 'im2' or 'im3' or 'im4' in request.args:
        ig1 = request.args['im1']
        ig2 = request.args['im2']
        ig3 = request.args['im3']
        ig4 = request.args['im4']



        fname_new1 = os.path.join('app\static',ig1)
        s3_client.download_file(s3_config['bucketid'],ig1,fname_new1)
        fname_new2 = os.path.join('app\static',ig2)
        s3_client.download_file(s3_config['bucketid'],ig2,fname_new2)
        fname_new3 = os.path.join('app\static',ig3)
        s3_client.download_file(s3_config['bucketid'],ig3,fname_new3)
        fname_new4 = os.path.join('app\static',ig4)
        s3_client.download_file(s3_config['bucketid'],ig4,fname_new4)




    return render_template("detail_view.html",
                           im1='static/'+ig1,
                           im2='static/'+ig2,
                           im3='static/'+ig3,
                           im4='static/'+ig4)