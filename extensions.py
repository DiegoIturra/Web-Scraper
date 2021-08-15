from flask_apscheduler import APScheduler
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
scheduler = APScheduler()
marshmallow = Marshmallow()
