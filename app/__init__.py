from flask import Flask
from redis import Redis
from app.config import Config


app = Flask(__name__)
app.config.from_object(Config)
redisClient = Redis()

from app import routes
