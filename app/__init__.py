from flask import Flask
from redis import Redis
from app.config import Config
import pymongo
import uuid

app = Flask(__name__)
app.config.from_object(Config)
redisClient = Redis()
# I want to try the navbar
app.secret_key = str(uuid.uuid4())
# trying navbar ends here

# create a mongo client
client = pymongo.MongoClient()
# create a database called e_vote
db = client['e_vote']
# create a voters collection and candidates collection
voters_collection = db['voters']
candidates_collection = db['candidates']
geo = db['geo']


from api import bp
app.register_blueprint(bp)

from app import routes
