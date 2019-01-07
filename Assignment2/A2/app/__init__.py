
from flask import Flask

webapp = Flask(__name__)

from app import main
from app import general
from app import login
from app import signup
from app import questionaire
from app import charts
from app import address