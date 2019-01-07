from app import webapp
from forms import ContactForm
from flask import Flask, render_template, request, flash, session, g, redirect, url_for
from boto3.dynamodb.conditions import Key, Attr
import json, time, boto3, re, datetime

webapp.secret_key = 'development key'
dynamodb = boto3.resource('dynamodb')
table_datasets = dynamodb.Table('questionaire')
dict_1 = {'zero': 0, 'one': 1, 'two': 2, 'three':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'more':9}
dict_2 = {'zero': 0, 'oneToThirty': 1,'ThirtyToSixty': 2,'PlusSixty' : 3}
dict_3 = {'Satisfied':3,'justOk': 2,'notHappy': 1, 'help': 0}
dict_4 = {'zero': 0, 'one': 1, 'two': 2, 'more': 3}


@webapp.route('/form', methods = ['GET', 'POST'])
def contact():
   if 'auth' not in session:
      return redirect(url_for('login'))
   form = ContactForm()
   keys= []
   if (user_has_data_today()):
      # keys.append(get_today_answers_from_db('q1')[0])
      # keys.append(get_today_answers_from_db('q2')[0])
      # keys.append(get_today_answers_from_db('q3')[0])
      # keys.append(get_today_answers_from_db('q4')[0])
      # keys.append(get_today_answers_from_db('q5')[0])
      return render_template('successq.html', keys= keys, catagory = 'Questionnaire')
   else:
      if request.method == 'POST':
         if form.validate() == False:
            flash('All fields are required.')
            return render_template('form.html', form = form)
         else:
            general_q1 = dict_1[str(request.form.get('study'))]
            general_q2 = dict_2[str(request.form.get('sport'))]
            general_q3 = dict_3[str(request.form.get('food'))]
            general_q4 = dict_4[str(request.form.get('social'))]
            general_q5 = dict_1[str(request.form.get('sleep'))]
            write_to_users_db(general_q1, general_q2, general_q3, general_q4, general_q5)

            keys.append(request.form.get('study'))
            keys.append(request.form.get('sport'))
            keys.append(request.form.get('food'))
            keys.append(request.form.get('social'))
            keys.append(request.form.get('sleep'))
            return render_template('successq.html', keys= keys, catagory = 'General ')
      elif request.method == 'GET':
         return render_template('form.html', form = form)

@webapp.route('/update', methods = ['GET', 'POST'])
def update():
   if 'auth' not in session:
      return redirect(url_for('login'))
   delete_today_entry();
   return redirect(url_for('contact'))

# def get_today_answers_from_db(question_number):
#    all_general =[]
#    response = table_datasets.scan(
#       FilterExpression = Attr('user-date').begins_with(get_user_date())
#    )
#    if 'Items' not in response or not response['Items']:
#       return (all_general)
#    for item in response['Items']:
#       all_general.append(json.dumps(item[question_number]))
#    return all_general

def delete_today_entry():
   table_datasets.delete_item(
    Key={
        'user-date': get_user_date()
    }
)
# save data in users db, These five questions are later used to tracking the progress
# for graphs and prediction. No return value is needed
def write_to_users_db(general_q1, general_q2, general_q3, general_q4, general_q5):
   if(not user_has_data_today()):
      response = table_datasets.put_item(
         Item = {
            'user-date' : get_user_date(),
            'q1' : general_q1,
            'q2' : general_q2,
            'q3' : general_q3,
            'q4' : general_q4,
            'q5' : general_q5,
            'date': time.strftime("%Y/%m/%d"),
            'day' : datetime.datetime.now().timetuple().tm_yday
         }
      )
      return True
   return False

def write_to_users_db_fake(i, p):
   j = i%2 + 5
   k = i%3
   l = i%4
   m = i%3
   o = i + 59
   date_s = p + str(i)
   response = table_datasets.put_item(
      Item = {
         'user-date' : get_user_date_fake(str(i)),
         'q1' : j,
         'q2' : k,
         'q3' : l,
         'q4' : m,
         'q5' : j,
         'date':date_s,
         'day' : o
      }
   )
   return True


#Reads all of the requested question from the database. The username needs to match the
  #sesseion login
def read_question_from_db(question_number):
   all_general =[]
   response = table_datasets.scan(
      FilterExpression = Attr('user-date').begins_with(session['auth'])
   )

   if 'Items' not in response or not response['Items']:
      return (all_general)
   i = 0
   for item in response['Items']:
      all_general.append((response['Items'][i][question_number]))
      i = i + 1
   return (all_general)


def read_dates_from_db():
   all_general =[]
   response = table_datasets.scan(
      FilterExpression = Attr('user-date').begins_with(session['auth'])
   )
   if 'Items' not in response or not response['Items']:
      return (all_general)
   i = 0
   for item in response['Items']:
      all_general.append((response['Items'][i]['date']))
      i = i + 1
   return (all_general)

def get_user_date_fake(i):
   res = session['auth'] + "-" + time.strftime("%Y/03/") + i
   return res

def get_user_date():
   res = session['auth'] + "-" + time.strftime("%Y/%m/%d")
   return res

def user_has_data_today():
   response = table_datasets.scan(
      FilterExpression = Attr('user-date').eq(get_user_date())
      )
   if 'Items' not in response or not response['Items']:
      return False
   else:
      return True


