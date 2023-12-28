from flask import Flask
from .config import Config
from mongoengine import connect


app = Flask(__name__)
app.config.from_object(Config)

connect("gpt_songs")
from api import routes  