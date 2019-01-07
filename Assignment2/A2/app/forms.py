from flask_wtf import Form
from wtforms import StringField, TextField, IntegerField, TextAreaField, SubmitField, RadioField,SelectField

from wtforms import validators, ValidationError
from wtforms.validators import DataRequired

class ContactForm(Form):
   study = SelectField('How many hours do you spend during the day studying or in class on average?', choices = [('zero', '0'),
      ('one', '1'), ('two', '2'), ('three', '3'), ('four', '4'), ('five', '5'), ('six', '6'), ('seven', '7'), ('eight', '8'), ('more', '8+')])

   sport = RadioField('How many minutes did you engage in light physical activity today? Ex. gardening, walking, etc.', choices = [('zero','0'),
      ('oneToThirty','1-30'), ('ThirtyToSixty','30-60'), ('PlusSixty','60+')])

   food = RadioField('How do you feel about what you had ate today?', choices = [('Satisfied','Satisfied'),
      ('justOk','Just ok'), ('notHappy','Not happy'), ('help','Help!')])

   social = RadioField('How many hours did you communicate or talk with people (Ex. Skype, in person, call etc.)?', choices = [('zero','0'),
      ('one','1'), ('two','2'), ('more','2+')])

   sleep = SelectField('How many hours do you think you slept last night?', choices = [('zero', '0'),
      ('one', '1'), ('two', '2'), ('three', '3'), ('four', '4'), ('five', '5'), ('six', '6'), ('seven', '7'), ('eight', '8'),('more', '9+')])

   submit = SubmitField("Send")

class StudyForm(Form):

   study_1 = RadioField('Are you happy with the amount that you are studying?', choices = [('Yes','Yes'), ('No','No')])

   study_2 = RadioField('Are you satisfied with your study habits/quality?', choices = [('Yes','Yes'), ('No','No')])

   study_3 = RadioField('Are you satisfied with your results/grades in school?', choices = [('Yes','Yes'), ('No','No')])

   submit = SubmitField("Send")

class PhysicalForm(Form):

   physical_1 = RadioField('How many minutes were you engaged in moderate or vigorous physical activity?(Ex. Brisk walking, jogging, running, soccer, cycling etc.?)',
                        choices = [('zero','0-15'),('fifteenToThirty','15-30'), ('ThirtyToSixty','30-60'), ('PlusSixty','60+')])

   physical_2 = RadioField('How many hours did you spend inactive?(Ex. Watching t.v., studying, spent on the computer)?',
                        choices = [('zero','0-15'),('onetoTwo','1-2'), ('twoToFour','2-4'), ('PlusFour','4+')])

   physical_3 = RadioField('How satisfied are you with your exercise level today? ?',
                        choices = [('Satisfied','Satisfied'),('justOk','Just ok'), ('notHappy','Not happy'), ('help','Help!')])
   submit = SubmitField("Send")

class FoodForm(Form):
   food_1 = RadioField('What are your barriers to achieving a satisfying diet',
                        choices = [('noTime','No time'),('cook','Can not cook'), ('money','Not enough money'), ('healthy','I am not sure how to eat healthy!')])
   submit = SubmitField("Send")

class NetworkForm(Form):
   network_1 = RadioField('how satisfied are you with your use of a social network?',
                        choices = [('Satisfied','Satisfied'),('justOk','Just ok'), ('notHappy','Not happy'), ('help','Help!')])
   submit = SubmitField("Send")

class SleepForm(Form):
   sleep_1 = RadioField('What do you think are the reasons that you need more sleep? Click on the best option below.',
                        choices =[('anxious','I have trouble falling asleep because I am anxious'),
                                   ('interrupt','I wake up in the middle of the night and can not fall back asleep'),
                                   ('busy','I am too busy with school'),
                                   ('general', 'I have trouble falling asleep in general'),
                                   ('roommate', 'My roommate keeps me up')])
   submit = SubmitField("Send")


class AddressForm(Form):
  address = StringField('Address', validators=[DataRequired("Please enter an address.")])
  submit = SubmitField("Search")