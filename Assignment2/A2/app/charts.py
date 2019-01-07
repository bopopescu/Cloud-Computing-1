from flask import Flask, render_template, session, request, redirect, url_for, g
from flask import Markup
from app import webapp
from questionaire import read_question_from_db, write_to_users_db_fake, read_dates_from_db
from itertools import imap
import numpy
import boto3
from boto3.dynamodb.conditions import Key, Attr
webapp.secret_key = 'development key'
dynamodb = boto3.resource('dynamodb')

@webapp.route("/chart",methods=['GET','POST'])
def chart():
    if 'auth' not in session:
        return redirect(url_for('login'))
    # labels = read_dates_from_db()
    # values = read_question_from_db('q2')
    dates = read_question_from_db('date')
    dictionary  = dict(zip(dates, read_question_from_db('q1')))
    dictionary1 = dict(zip(dates, read_question_from_db('q2')))
    dictionary2 = dict(zip(dates, read_question_from_db('q3')))
    dictionary3 = dict(zip(dates, read_question_from_db('q4')))
    dictionary4 = dict(zip(dates, read_question_from_db('q5')))
    # all_general =[]
    # all_general= read_question_from_db('q1')
    # write_fake_data()
    # all_general=read_dates_from_db()
    # return str(values)

    labels=[]
    values=[]
    for key in sorted(dictionary.iterkeys()):
        labels.append(key)
        values.append(dictionary[key])

    labels1=[]
    values1=[]
    for key in sorted(dictionary1.iterkeys()):
        labels1.append(key)
        values1.append(dictionary1[key])

    labels2=[]
    values2=[]
    for key in sorted(dictionary2.iterkeys()):
        labels2.append(key)
        values2.append(dictionary2[key])

    labels3=[]
    values3=[]
    for key in sorted(dictionary3.iterkeys()):
        labels3.append(key)
        values3.append(dictionary3[key])

    labels4=[]
    values4=[]
    for key in sorted(dictionary4.iterkeys()):
        labels4.append(key)
        values4.append(dictionary4[key])

    return render_template('chart.html', values=values[-15:], labels=labels[-15:],
        values1=values1[-15:], labels1=labels1[-15:], values2=values2[-15:], labels2=labels2[-15:],
         values3=values3[-15:], labels3=labels3[-15:], values4=values4[-15:], labels4=labels4[-15:])


def write_fake_data():
    for i in range(11,32):
        j = '2017/03/'
        write_to_users_db_fake(i, j)

@webapp.route("/academics_detail",methods=['GET','POST'])
def academics_detail():
    if 'auth' not in session:
        return redirect(url_for('login'))

    dates = read_question_from_db('date')
    days = read_question_from_db('day')
    dictionary  = dict(zip(dates, read_question_from_db('q1')))
    dictionary2  = dict(zip(days, read_question_from_db('q1')))

    n_date = len(dates)
    last_submission= 0
    dates_sorted= sorted(dates)
    if n_date != 0:
        last_submission = dates_sorted[n_date-1]

    n = len(days)
    last_difference= 0
    days_sorted= sorted(days)
    if n != 0:
        last_difference = days_sorted[n-1] - days_sorted[n-2]
    # days[n] - days[n - 1]

    labels=[]
    values=[]
    for key in sorted(dictionary.iterkeys()):
        labels.append(key)
        values.append(dictionary[key])

    x=[]
    y=[]
    for key in sorted(dictionary2.iterkeys()):
        x.append(key)
        y.append(dictionary2[key])

    x_float = [float(i) for i in x]
    y_float = [float(i) for i in y]
    r = 0
    if n != 0:
        r = (pearsonr(x_float, y_float))

    # r = client.invoke(
    #     FunctionName='arn:aws:lambda:us-east-1:683550530607:function:calculate_pearson_coef',
    #     InvocationType='RequestResponse',
    # )

    pearson= "No study pattern."
    if r < -0.5 and r > -1:
        pearson= "The study pattern show large decrease."
        pattern = "large_decrease"
    if r < -0.3 and r > -0.50:
        pearson = "The study pattern show medium decrease."
        pattern = "medium_decrease"
    if r < -0.1 and r > -0.30:
        pearson = "The study pattern show small decrease."
        pattern = "small_decrease"
    if 0.5 < r  and r < 1:
        pearson = "The study pattern show large increase."
        pattern = "large_increase"
    if 0.3 < r  and r < 0.5:
        pearson = "The study pattern show medium increase."
        pattern = "medium_increase"
    if 0.1 < r  and r < 0.3:
        pearson = "The study pattern show small increase."
        pattern = "small_increase"

    if pearson== "No study pattern.":
        tips = ["Please click on academics Tap for further questions."]
    else:
        tips = read_from_academics_db_to_analysis(pattern)

    values1=[]
    b = [float(n) for n in values]
    average = round(numpy.mean(b), 0)
    std     = round(numpy.std(b), 0)
    count = 0
    for i in b:
        values1.append(average)
        count = count + 1

    dictionary1  = dict(zip(labels, b))
    outliers = []
    for label in labels:
        if dictionary1[label]< 1 :
            outliers.append(label)

    str_outliers =""
    for outlier in outliers:
        str_outliers =  str_outliers + str(outlier) + "***"

    outliers= str_outliers


    return render_template('academicsDetail.html', values=values, values1=values1,
        labels=labels, pearson=pearson, average= average, std= std, outliers=outliers,
        last_difference = last_difference,last_submission= last_submission, tips=tips)


@webapp.route("/physicals_detail",methods=['GET','POST'])
def physicals_detail():
    if 'auth' not in session:
        return redirect(url_for('login'))

    dict_1 = {0: 'zero', 1: '1-30 minutes',2: '30-60 minutes',3: 'Plus sixty minutes'}

    dates = read_question_from_db('date')
    days = read_question_from_db('day')
    dictionary  = dict(zip(dates, read_question_from_db('q2')))
    dictionary2  = dict(zip(days, read_question_from_db('q2')))

    n_date = len(dates)
    last_submission= 0
    dates_sorted= sorted(dates)
    if n_date != 0:
        last_submission = dates_sorted[n_date-1]

    n = len(days)
    last_difference= 0
    days_sorted= sorted(days)
    if n != 0:
        last_difference = days_sorted[n-1] - days_sorted[n-2]

    labels=[]
    values=[]
    for key in sorted(dictionary.iterkeys()):
        labels.append(key)
        values.append(dictionary[key])

    x=[]
    y=[]
    for key in sorted(dictionary2.iterkeys()):
        x.append(key)
        y.append(dictionary2[key])

    x_float = [float(i) for i in x]
    y_float = [float(i) for i in y]
    r = 0
    if n != 0:
        r = (pearsonr(x_float, y_float))

    # r = client.invoke(
    #     FunctionName='arn:aws:lambda:us-east-1:683550530607:function:calculate_pearson_coef',
    #     InvocationType='RequestResponse',
    # )

    pearson= "No physical activity pattern."

    if r < -0.5 and r > -1:
        pearson= "The physical activity pattern show large decrease."
        pattern = "large_decrease"
    if r < -0.3 and r > -0.50:
        pearson = "The physical activity pattern show medium decrease."
        pattern = "medium_decrease"
    if r < -0.1 and r > -0.30:
        pearson = "The physical activity pattern show small decrease."
        pattern = "small_decrease"
    if 0.5 < r  and r < 1:
        pearson = "The physical activity pattern show large increase."
        pattern = "large_increase"
    if 0.3 < r  and r < 0.5:
        pearson = "The physical activity pattern show medium increase."
        pattern = "medium_increase"
    if 0.1 < r  and r < 0.3:
        pearson = "The physical activity pattern show small increase."
        pattern = "small_increase"

    if pearson== "No physical activity pattern.":
        tips = ["Please click on physicals Tap for further questions."]
    else:
        tips = read_from_physical_db_analysis(pattern)
        tips.append("Please click on physical Tap for further tips.")

    values1=[]
    b = [float(n) for n in values]
    average_float = round(numpy.mean(b), 0)
    average = dict_1[int(average_float)]
    std     = round(numpy.std(b), 0)
    count = 0
    for i in b:
        values1.append(average_float)
        count = count + 1


    dictionary1  = dict(zip(labels, b))
    outliers = []
    for label in labels:
        if dictionary1[label]< 1 :
            outliers.append(label)

    str_outliers =""
    for outlier in outliers:
        str_outliers =  str_outliers + str(outlier) + "***"

    outliers= str_outliers


    return render_template('physicalsDetail.html', values=values, values1=values1,
        labels=labels, pearson=pearson, average= average, std= std, outliers=outliers,
        last_difference = last_difference,last_submission= last_submission, tips=tips)

@webapp.route("/nutrition_detail",methods=['GET','POST'])
def nutrition_detail():
    if 'auth' not in session:
        return redirect(url_for('login'))

    dict_1 = {0: 'helpless', 1: 'Not happy',2: 'just Ok',3: 'Satisfied'}

    dates = read_question_from_db('date')
    days = read_question_from_db('day')
    dictionary  = dict(zip(dates, read_question_from_db('q3')))
    dictionary2  = dict(zip(days, read_question_from_db('q3')))

    n_date = len(dates)
    last_submission= 0
    dates_sorted= sorted(dates)
    if n_date != 0:
        last_submission = dates_sorted[n_date-1]

    n = len(days)
    last_difference= 0
    days_sorted= sorted(days)
    if n != 0:
        last_difference = days_sorted[n-1] - days_sorted[n-2]

    labels=[]
    values=[]
    for key in sorted(dictionary.iterkeys()):
        labels.append(key)
        values.append(dictionary[key])

    x=[]
    y=[]
    for key in sorted(dictionary2.iterkeys()):
        x.append(key)
        y.append(dictionary2[key])

    x_float = [float(i) for i in x]
    y_float = [float(i) for i in y]
    r = 0
    if n != 0:
        r = (pearsonr(x_float, y_float))

    # r = client.invoke(
    #     FunctionName='arn:aws:lambda:us-east-1:683550530607:function:calculate_pearson_coef',
    #     InvocationType='RequestResponse',
    # )

    pearson= "No nutrition activity pattern."

    if r < -0.5 and r > -1:
        pearson= "The nutrition activity pattern show large decrease."
        pattern="large_decrease"
    if r < -0.3 and r > -0.50:
        pearson = "The nutrition activity pattern show medium decrease."
        pattern="medium_decrease"
    if r < -0.1 and r > -0.30:
        pearson = "The nutrition activity pattern show small decrease."
        pattern="small_decrease"
    if 0.5 < r  and r < 1:
        pearson = "The nutrition activity pattern show large increase."
        pattern="large_increase"
    if 0.3 < r  and r < 0.5:
        pearson = "The nutrition activity pattern show medium increase."
        pattern="medium_increase"
    if 0.1 < r  and r < 0.3:
        pearson = "The nutrition activity pattern show small increase."
        pattern="small_increase"

    if pearson== "No nutrition activity pattern.":
        tips = ["Please click on physicals Tap for further questions."]
    else:
        tips = read_from_food_db_analysis(pattern)
        tips.append("Please click on Food Tap for further tips.")


    values1=[]
    b = [float(n) for n in values]
    average_float = round(numpy.mean(b), 0)
    average = dict_1[int(average_float)]
    std     = round(numpy.std(b), 0)
    count = 0
    for i in b:
        values1.append(average_float)
        count = count + 1


    dictionary1  = dict(zip(labels, b))
    outliers = []
    for label in labels:
        if dictionary1[label]< 1 :
            outliers.append(label)

    str_outliers =""
    for outlier in outliers:
        str_outliers =  str_outliers + str(outlier) + "***"

    outliers= str_outliers


    return render_template('foodDetail.html', values=values, values1=values1,
        labels=labels, pearson=pearson, average= average, std= std, outliers=outliers,
        last_difference = last_difference,last_submission= last_submission, tips=tips)


@webapp.route("/network_detail",methods=['GET','POST'])
def network_detail():
    if 'auth' not in session:
        return redirect(url_for('login'))

    dict_1 = {0: 'Zero', 1: 'One hour',2: 'Two hours',3: 'Plus two hours'}

    dates = read_question_from_db('date')
    days = read_question_from_db('day')
    dictionary  = dict(zip(dates, read_question_from_db('q4')))
    dictionary2  = dict(zip(days, read_question_from_db('q4')))

    n_date = len(dates)
    last_submission= 0
    dates_sorted= sorted(dates)
    if n_date != 0:
        last_submission = dates_sorted[n_date-1]

    n = len(days)
    last_difference= 0
    days_sorted= sorted(days)
    if n != 0:
        last_difference = days_sorted[n-1] - days_sorted[n-2]

    labels=[]
    values=[]
    for key in sorted(dictionary.iterkeys()):
        labels.append(key)
        values.append(dictionary[key])

    n = len(values)
    latest_value = 0
    if n != 0:
        latest_value = values[n-1]

    tips = read_from_network_db_analysis(latest_value)


    x=[]
    y=[]
    for key in sorted(dictionary2.iterkeys()):
        x.append(key)
        y.append(dictionary2[key])

    x_float = [float(i) for i in x]
    y_float = [float(i) for i in y]
    r = 0
    if n != 0:
        r = (pearsonr(x_float, y_float))

    # r = client.invoke(
    #     FunctionName='arn:aws:lambda:us-east-1:683550530607:function:calculate_pearson_coef',
    #     InvocationType='RequestResponse',
    # )

    pearson= "No network activity pattern."
    if r < -0.5 and r > -1:
        pearson= "The network activity pattern show large decrease."
    if r < -0.3 and r > -0.50:
        pearson = "The network activity pattern show medium decrease."
    if r < -0.1 and r > -0.30:
        pearson = "The network activity pattern show small decrease."
    if 0.5 < r  and r < 1:
        pearson = "The network activity pattern show large increase."
    if 0.3 < r  and r < 0.5:
        pearson = "The network activity pattern show medium increase."
    if 0.1 < r  and r < 0.3:
        pearson = "The network activity pattern show small increase."

    values1=[]
    b = [float(n) for n in values]
    average_float = round(numpy.mean(b), 0)
    average = dict_1[int(average_float)]
    std     = round(numpy.std(b), 0)
    count = 0
    for i in b:
        values1.append(average_float)
        count = count + 1


    dictionary1  = dict(zip(labels, b))
    outliers = []
    for label in labels:
        if dictionary1[label]< 1 :
            outliers.append(label)

    str_outliers =""
    for outlier in outliers:
        str_outliers =  str_outliers + str(outlier) + "***"

    outliers= str_outliers
    return render_template('networkDetail.html', values=values, values1=values1,
        labels=labels, pearson=pearson, average= average, std= std, outliers=outliers,
        last_difference = last_difference,last_submission= last_submission, tips = tips)


@webapp.route("/sleep_detail",methods=['GET','POST'])
def sleep_detail():
    if 'auth' not in session:
        return redirect(url_for('login'))

    dates = read_question_from_db('date')
    days = read_question_from_db('day')
    dictionary  = dict(zip(dates, read_question_from_db('q5')))
    dictionary2  = dict(zip(days, read_question_from_db('q5')))

    n_date = len(dates)
    last_submission= 0
    dates_sorted= sorted(dates)
    if n_date != 0:
        last_submission = dates_sorted[n_date-1]

    n = len(days)
    last_difference= 0
    days_sorted= sorted(days)
    if n != 0:
        last_difference = days_sorted[n-1] - days_sorted[n-2]

    labels=[]
    values=[]
    for key in sorted(dictionary.iterkeys()):
        labels.append(key)
        values.append(dictionary[key])

    x=[]
    y=[]
    for key in sorted(dictionary2.iterkeys()):
        x.append(key)
        y.append(dictionary2[key])

    x_float = [float(i) for i in x]
    y_float = [float(i) for i in y]
    r = 0
    if n != 0:
        r = (pearsonr(x_float, y_float))

    # r = client.invoke(
    #     FunctionName='arn:aws:lambda:us-east-1:683550530607:function:calculate_pearson_coef',
    #     InvocationType='RequestResponse',
    # )

    pearson= "No sleep pattern."

    if r < -0.5 and r > -1:
        pearson= "The sleep pattern show large decrease."
        pattern = "decrease"
    if r < -0.3 and r > -0.50:
        pearson = "The sleep pattern show medium decrease."
        pattern = "decrease"
    if r < -0.1 and r > -0.30:
        pearson = "The sleep pattern show small decrease."
        pattern = "decrease"
    if 0.5 < r  and r < 1:
        pearson = "The sleep pattern show large increase."
        pattern = "increase"
    if 0.3 < r  and r < 0.5:
        pearson = "The sleep pattern show medium increase."
        pattern = "increase"
    if 0.1 < r  and r < 0.3:
        pearson = "The sleep pattern show small increase."
        pattern = "increase"

    if pearson== "No sleep pattern.":
        tips = ["Please click on sleep Tap for further questions."]
    else:
        tips = read_from_sleep_db_analysis(pattern)
        tips.append("Please click on sleep Tap for further tips.")

    values1=[]
    b = [float(n) for n in values]
    average = round(numpy.mean(b), 0)
    std     = round(numpy.std(b), 0)
    count = 0
    for i in b:
        values1.append(average)
        count = count + 1

    dictionary1  = dict(zip(labels, b))
    outliers = []
    for label in labels:
        if dictionary1[label]< (average - std) :
            outliers.append(label)

    str_outliers =""
    for outlier in outliers:
        str_outliers =  str_outliers + str(outlier) + "***"

    outliers= str_outliers

    return render_template('sleepDetail.html', values=values, values1=values1,
        labels=labels, pearson=pearson, average= average, std= std, outliers=outliers,
        last_difference = last_difference,last_submission= last_submission, tips= tips)

def pearsonr(x, y):
  # Assume len(x) == len(y)
  n = len(x)
  sum_x = float(sum(x))
  sum_y = float(sum(y))
  sum_x_sq = sum(map(lambda x: pow(x, 2), x))
  sum_y_sq = sum(map(lambda x: pow(x, 2), y))
  psum = sum(imap(lambda x, y: x * y, x, y))
  num = psum - (sum_x * sum_y/n)
  den = pow((sum_x_sq - pow(sum_x, 2) / n) * (sum_y_sq - pow(sum_y, 2) / n), 0.5)
  if den == 0: return 0
  return round ((num / den), 2)


# All tips are stored in academics table
# Returns all tips based on answers that user inserted
def read_from_academics_db_to_analysis(academics_pattern):
   # If students answer no to the last two questions automatically,
   # prompt all tips, otherwise it will say Keep up the great work!
   table = dynamodb.Table('academics')
   responses = []
   if (academics_pattern == 'small_decrease' or academics_pattern  == 'medium_decrease'):
      for i in [2]:
         response = table.scan(
            FilterExpression = Attr('number').eq(i)
            )
         responses.append (response['Items'][0]['content'])
      return responses
   if (academics_pattern == 'large_decrease'):
      for i in [1, 2, 3]:
         response = table.scan(
            FilterExpression = Attr('number').eq(i)
            )
         responses.append (response['Items'][0]['content'])
      return responses
   else:
      return ['Keep up the great work!']

# All tips are stored in physical activity table
# Returns all tips based on answers that user inserted
def read_from_physical_db_analysis(pattern):
   # *All tips will be prompted, Additional words prompted for those who exceed
   # 30+ moderate to vigorous/day
   table = dynamodb.Table('physical')
   responses = []
   if pattern == 'small_decrease' or pattern == 'medium_decrease':
      responses.append('you need more exercise!')
   elif pattern == 'large_decrease':
      responses.append('you need to start exercise!')
   else:
      responses.append('Keep up the great work!')
   for i in [1,2,3]:
      response = table.scan(
         FilterExpression = Attr('number').eq(i)
         )
      responses.append (response['Items'][0]['content'])
   if pattern == 'small_increase'or pattern == 'medium_increase' or pattern == 'large_increase':
      responses=['Keep up the great work!']

   return responses

# All tips are stored in food table
# Returns all tips based on answers that user inserted
def read_from_food_db_analysis(pattern):
   responses=[]
   table = dynamodb.Table('food')
   if pattern == 'small_decrease' or pattern == 'medium_decrease':
      responses.append('you need more healthy nutrition!')
   elif pattern == 'large_decrease':
      responses.append('you need to seriously consider healthy food habits!')
   else:
      responses.append('Keep up the great work!')
   for i in [2, 3, 4]:
      response = table.scan(
         FilterExpression = Attr('number').eq(i)
         )
      responses.append (response['Items'][0]['content'])
   if pattern == 'small_increase'or pattern == 'medium_increase' or pattern == 'large_increase':
      responses=['Keep up the great work!']

   return responses


# All tips are stored in network table
# Returns all tips based on answers that user inserted
def read_from_network_db_analysis(pattern):
   # If students answer not happy or help! to the last two questions,
   # automatically prompt all tips, otherwise it will show Resources Available: On Campus:
   table = dynamodb.Table('network')
   responses = []
   if pattern == 1 or pattern== 0:
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
def read_from_sleep_db_analysis(pattern):
   responses=[]
   table = dynamodb.Table('sleep')
   if pattern == 'decrease':
      for i in [1, 2, 3]:
        response = table.scan(
            FilterExpression = Attr('number').eq(i)
            )
        responses.append (response['Items'][0]['content'])
   else:
        responses=['Keep up the great work!']
   return responses