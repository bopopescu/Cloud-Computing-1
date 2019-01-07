
from flask import Flask

webapp = Flask(__name__)

from app import fileupload
from app import imagetransform
from app import login
from app import signup
from app import main
from app import welcome
from app import gridview
from app import detail_view
from app import delete
