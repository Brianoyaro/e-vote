from flask import Flask
from redis import Redis
from app.config import Config
import pymongo

app = Flask(__name__)
app.config.from_object(Config)
redisClient = Redis()

# create a mongo client
client =pymongo.MongoClient()
# create a database called e_vote
db =  client['e_vote']
# create a voters collection and candidates collection
voters_collection = db['voters']
candidates_collection = db['candidates']

from app import routes
