from flask import render_template, redirect, url_for, request, session, g
from app import webapp

@webapp.route('/welcome',methods=['GET','POST'])
def welcome():
    return render_template('welcome.html')

