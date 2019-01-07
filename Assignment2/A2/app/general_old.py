from flask import Flask, render_template, request, flash, session, g, redirect, url_for
from forms import StudyForm, PhysicalForm, FoodForm, NetworkForm, SleepForm
from app import webapp
import boto3
from boto3.dynamodb.conditions import Key, Attr
import re

webapp.secret_key = 'development key'
dynamodb = boto3.resource('dynamodb')

@webapp.route('/academics', methods = ['GET', 'POST'])
def academics():
   form = StudyForm()
   keys= []
   if 'auth' not in session:
      return redirect(url_for('login'))
   if request.method == 'POST':
      if form.validate() == False:
         flash('All fields are required.')
         return render_template('academics.html', form = form,)
      else:
         academics_q1 = request.form.get('study_1')
         academics_q2 = request.form.get('study_2')
         academics_q3 = request.form.get('study_3')
         keys = read_from_academics_db(academics_q1, academics_q2, academics_q3)
         # links = read_links_from_academics_db(academics_q1, academics_q2, academics_q3)

         #keys.append(request.form.get('study_1'))
         #keys.append(request.form.get('study_2'))
         #keys.append(request.form.get('study_3'))

         return render_template('success.html', keys= keys, catagory = 'Academics ')
   elif request.method == 'GET':
      return render_template('academics.html', form = form)

@webapp.route('/physicals', methods = ['GET', 'POST'])
def physicals():
   form = PhysicalForm()
   keys= []
   if 'auth' not in session:
      return redirect(url_for('login'))
   if request.method == 'POST':
      if form.validate() == False:
         flash('All fields are required.')
         return render_template('physicals.html', form = form)
      else:
         physical_q1 = request.form.get('physical_1')
         physical_q2 = request.form.get('physical_2')
         physical_q3 = request.form.get('physical_3')
         keys = read_from_physical_db(physical_q1, physical_q2, physical_q3)

         #keys.append(request.form.get('physical_1'))
         #keys.append(request.form.get('physical_2'))
         #keys.append(request.form.get('physical_3'))

         return render_template('success.html', keys= keys, catagory = 'Physical Activity ')
   elif request.method == 'GET':
      return render_template('physicals.html', form = form)

@webapp.route('/food', methods = ['GET', 'POST'])
def food():
   form = FoodForm()
   keys= []
   if 'auth' not in session:
      return redirect(url_for('login'))
   if request.method == 'POST':
      if form.validate() == False:
         flash('All fields are required.')
         return render_template('food.html', form = form)
      else:
         food_q1 = request.form.get('food_1')
         keys = read_from_food_db(food_q1)

         #keys.append(request.form.get('food_1'))
         return render_template('success.html', keys= keys, catagory = 'Food ')
   elif request.method == 'GET':
      return render_template('food.html', form = form)

@webapp.route('/network', methods = ['GET', 'POST'])
def network():
   form = NetworkForm()
   keys= []
   if 'auth' not in session:
      return redirect(url_for('login'))
   if request.method == 'POST':
      if form.validate() == False:
         flash('All fields are required.')
         return render_template('network.html', form = form)
      else:
         network_q1 = request.form.get('network_1')
         keys = read_from_network_db(network_q1)
         # keys.append("My network: these may be friends, family, mentors, faith leaders, health care providers. What is most important is the relationship. When we need support, we turn to those who we trust and who we know will listen compassionately and without judgment. We know who those people are because we always feel better after talking and spending time with them. Reflect on the people who you you included in your support network, who would you feel most comfortable talking to if you needed emotional support? Recognize that in addition to the people in your life, there are also resources available that you can access if you are ever in need of someone to talk (Click on the tab below for details). Perhaps take a look at the resources now, figure out which ones you would feel most comfortable access.  Often, when we are in need of help, we are not feeling our best, and navigating a complex system of support can be that much more challenging. Becoming familiar with the resources available in advance can make reaching out for support, when we need it, much easier.")
         #keys.append(request.form.get('network_1'))
         return render_template('success.html', keys= keys, catagory = 'Network ')
   elif request.method == 'GET':
      return render_template('network.html', form = form)

@webapp.route('/sleep', methods = ['GET', 'POST'])
def sleep():
   form = SleepForm()
   keys= []
   if 'auth' not in session:
      return redirect(url_for('login'))
   if request.method == 'POST':
      if form.validate() == False:
         flash('All fields are required.')
         return render_template('sleep.html', form = form)
      else:
         sleep_q1 = request.form.get('sleep_1')
         # keys.append(read_from_sleep_db(sleep_q1))
         keys = read_from_sleep_db(sleep_q1)
         return render_template('success.html', keys= keys, catagory = 'Sleep ')
   elif request.method == 'GET':
      return render_template('sleep.html', form = form)


# All tips are stored in academics table
# Returns all tips based on answers that user inserted
def read_from_academics_db(academics_q1, academics_q2, academics_q3):
   # If students answer no to the last two questions automatically,
   # prompt all tips, otherwise it will say Keep up the great work!
   if (academics_q2 != 'Yes'and academics_q3 != 'Yes'):
      table = dynamodb.Table('academics')
      responses = []
      for i in [1,2,3]:
         response = table.scan(
            FilterExpression = Attr('number').eq(i)
            )
         responses.append (response['Items'][0]['content'])
      return responses
   else:
      return ['Keep up the great work!']

def read_links_from_academics_db(academics_q1, academics_q2, academics_q3):
   # If students answer no to the last two questions automatically,
   # prompt all tips, otherwise it will say Keep up the great work!
   if (academics_q2 != 'Yes'and academics_q3 != 'Yes'):
      table = dynamodb.Table('academics')
      responses = []
      for i in [1,2,3]:
         response = table.scan(
            FilterExpression = Attr('number').eq(i)
            )
         responses.append (response['Items'][0]['link'])
      return responses


# All tips are stored in physical activity table
# Returns all tips based on answers that user inserted
def read_from_physical_db(physical_q1, physical_q2, physical_q3):
   # *All tips will be prompted, Additional words prompted for those who exceed
   # 30+ moderate to vigorous/day
   table = dynamodb.Table('physical')
   responses = []
   if physical_q1 == 'zero':
      responses.append('you need more exercise!')
   if physical_q1 == 'ThirtyToSixty' or physical_q1 == 'PlusSixty':
      responses.append('Keep up the great work!')
   for i in [1,2,3,4,5,6,7,8,9]:
      response = table.scan(
         FilterExpression = Attr('number').eq(i)
         )
      responses.append (response['Items'][0]['content'])
   return responses

# All tips are stored in food table
# Returns all tips based on answers that user inserted
def read_from_food_db(food_q1):
   responses=[]
   table = dynamodb.Table('food')
   if food_q1 == 'noTime':
      for i in [1, 6, 7, 9, 14, 15]:
         response = table.scan(
            FilterExpression = Attr('number').eq(i)
            )
         responses.append (response['Items'][0]['content'])
      return responses
   if food_q1 == 'cook':
      for i in [ 6, 7]:
         response = table.scan(
            FilterExpression = Attr('number').eq(i)
            )
         responses.append (response['Items'][0]['content'])
      return responses
   if food_q1 == 'money':
      for i in [ 1, 14, 15, 16]:
         response = table.scan(
            FilterExpression = Attr('number').eq(i)
            )
         responses.append (response['Items'][0]['content'])
      return responses
   if food_q1 == 'healthy':
      for i in [2, 3, 4, 5, 8, 10, 11, 12, 13]:
         response = table.scan(
            FilterExpression = Attr('number').eq(i)
            )
         responses.append (response['Items'][0]['content'])
      return responses

# All tips are stored in network table
# Returns all tips based on answers that user inserted
def read_from_network_db(network_q1):
   # If students answer not happy or help! to the last two questions,
   # automatically prompt all tips, otherwise it will show Resources Available: On Campus:
   table = dynamodb.Table('network')
   responses = []
   if network_q1 == 'notHappy' or network_q1 == 'help':
      response = table.scan(
         FilterExpression = Attr('number').eq(3)
         )
      responses.append (response['Items'][0]['content'])
      return responses
   else:
      for i in [1, 2]:
         response = table.scan(
            FilterExpression = Attr('number').eq(i)
            )
         responses.append (response['Items'][0]['content'])
      return responses


# All tips are stored in sleep table
def read_from_sleep_db(sleep_q1):
   responses=[]
   table = dynamodb.Table('sleep')

   if sleep_q1 == 'anxious':
      for i in [1, 3, 5, 8, 9, 10, 11, 14]:
         response = table.scan(
            FilterExpression = Attr('number').eq(i)
            )
         responses.append (response['Items'][0]['content'])
      return responses

   if sleep_q1 == 'interrupt':
      for i in [4, 5, 6, 7, 8, 9, 10, 11, 12, 14]:
         response = table.scan(
            FilterExpression = Attr('number').eq(i)
            )
         responses.append (response['Items'][0]['content'])
      return responses

   if sleep_q1 == 'busy':
      for i in [2, 5, 9, 10, 11, 14]:
         response = table.scan(
            FilterExpression = Attr('number').eq(i)
            )
         responses.append (response['Items'][0]['content'])
      return responses

   if sleep_q1 == 'general':
      for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14]:
         response = table.scan(
            FilterExpression = Attr('number').eq(i)
            )
         responses.append (response['Items'][0]['content'])
      return responses

   if sleep_q1 == 'roommate':
      for i in [12, 13, 14]:
         response = table.scan(
            FilterExpression = Attr('number').eq(i)
            )
         responses.append (response['Items'][0]['content'])
      return responses


