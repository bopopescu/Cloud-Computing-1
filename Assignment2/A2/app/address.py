from app import webapp
from flask import Flask, render_template, session, request, redirect, url_for, g
import boto3
from boto3.dynamodb.conditions import Key, Attr
import geocoder
import urllib2
import json

webapp.secret_key = 'development key'
dynamodb = boto3.resource('dynamodb')

@webapp.route('/address', methods = ['GET', 'POST'])
def address():
   if 'auth' not in session:
       return redirect(url_for('login'))

   places = []
   network =[]
   physical = []
   food = []
   sleep = []
   my_coordinates = (43.6629, -79.3957)
   address = "University Of Toronto"

   places = read_links_from_academics_db()
   network =  read_links_from_network_db()
   physical = read_links_from_physical_db()
   food = read_links_from_food_db()
   sleep = read_links_from_sleep_db()

   return render_template('address.html', my_coordinates=my_coordinates, places=places,
                           network=network, physical = physical, food = food, sleep = sleep)


def read_links_from_academics_db():
   # If students answer no to the last two questions automatically,
   # prompt all tips, otherwise it will say Keep up the great work!

   table = dynamodb.Table('academics')
   responses = []
   for i in [1,2,3]:
      response = table.scan(
         FilterExpression = Attr('number').eq(i)
         )
      d ={
         'name': response['Items'][0]['title'],
         'url': response['Items'][0]['link'],
      }
      responses.append (d)
   return responses


def read_links_from_network_db():
   # If students answer no to the last two questions automatically,
   # prompt all tips, otherwise it will say Keep up the great work!

   table = dynamodb.Table('network')
   responses = []
   for i in [1,2]:
      response = table.scan(
         FilterExpression = Attr('number').eq(i)
         )
      d ={
         'name': response['Items'][0]['title'],
         'url': response['Items'][0]['link'],
      }
      responses.append (d)
   return responses

def read_links_from_physical_db():
   # If students answer no to the last two questions automatically,
   # prompt all tips, otherwise it will say Keep up the great work!

   table = dynamodb.Table('physical')
   responses = []
   for i in [4,5, 6, 9]:
      response = table.scan(
         FilterExpression = Attr('number').eq(i)
         )
      d ={
         'name': response['Items'][0]['title'],
         'url': response['Items'][0]['link'],
      }
      responses.append (d)
   return responses

def read_links_from_food_db():
   # If students answer no to the last two questions automatically,
   # prompt all tips, otherwise it will say Keep up the great work!

   table = dynamodb.Table('food')
   responses = []
   for i in [14,15,16]:
      response = table.scan(
         FilterExpression = Attr('number').eq(i)
         )
      d ={
         'name': response['Items'][0]['title'],
         'url': response['Items'][0]['link'],
      }
      responses.append (d)
   return responses

def read_links_from_sleep_db():
   # If students answer no to the last two questions automatically,
   # prompt all tips, otherwise it will say Keep up the great work!

   table = dynamodb.Table('sleep')
   responses = []
   for i in [15]:
      response = table.scan(
         FilterExpression = Attr('number').eq(i)
         )
      d ={
         'name': response['Items'][0]['title'],
         'url': response['Items'][0]['link'],
      }
      responses.append (d)
   return responses