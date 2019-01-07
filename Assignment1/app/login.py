from flask import render_template, session, request, redirect, url_for, g
from app import webapp


import mysql.connector
from app.config import db_config

# import random

webapp.secret_key = ''

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

@webapp.route('/login',methods=['GET','POST'])
def login():
    return render_template("login.html", error = "")

@webapp.route('/login_submit',methods=['POST'])
def login_submit():
    cnx = get_db()
    cursor = cnx.cursor()


    n1= request.form.get('n1','')
    n2= request.form.get('n2','')

    if n1 == '' or  n2=='':
        error = "Error! Username or password is required!"
        return render_template("login.html", error = error, n1=n1, n2=n2)

    query = '''SELECT * FROM users WHERE login = %s '''
    cursor.execute(query,(n1, ))

    row = cursor.fetchone()
    if not row:
        error = "Error! Username is not exist!"
        return render_template("login.html", error = error)

    row0 = row[0]
    row1 = row[1]
    row2 = row[2]

    if n1 == row1 and \
       n2 == row2:
        session['id']   = row0
        session['auth'] = request.form.get('n1')
        # session['usrename'] = 'spy'
        return redirect(url_for('welcome'))
        return redirect(url_for('store'))
    else:
        error = "Error! Incorrect username or password!"
        return render_template("login.html", error = error)



@webapp.route('/login/store',methods=['GET','POST'])
def store():
  # if 'username' not in session:
    if 'auth' not in session:
        return redirect(url_for('login'))

    return redirect(url_for('image_form'))


# # @webapp.route('/secure/index',methods=['GET','POST'])
# # def another_secret():
# #     return render_template("example6_secret.html")

@webapp.route('/logout',methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('store'))



