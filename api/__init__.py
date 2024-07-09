from flask import Blueprint

bp = Blueprint('e-vote-api', __name__, url_prefix='/api/')

import api.routes