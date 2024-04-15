from flask_pymongo import PyMongo
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
mongo = PyMongo()
