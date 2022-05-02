import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from redis import Redis

from producer import Producer

load_dotenv()

from celery_work.tasks import login_app_email

login_app_email.apply_async(())

prod = Producer("mystream", host=REDIS_HOST, port=6379, db=0)
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
CORS(app)

from views.auth import my_view

app.register_blueprint(my_view)
from views.doctor import doctor_view

app.register_blueprint(doctor_view)
from views.patient import patient_view

app.register_blueprint(patient_view)

from views.booking.booking import booking_view

app.register_blueprint(booking_view)
