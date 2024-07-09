from api import bp
from app import candidates_collection, geo
from flask import jsonify

@bp.route('/candidates')
def candidates():
    candidates = list(candidates_collection.find({}, {'_id': 0, 'count': 0}))
    return jsonify(candidates), 200

@bp.route('/presidents')
def presidents():
    presidents = list(candidates_collection.find({'position': 'president'}, {'_id': 0, 'count': 0, 'position': 0}))
    return jsonify(presidents)

@bp.route('/governors/<county>')
def governors(county):
    governors = list(candidates_collection.find({'position': 'governor', 'county': county}, {'_id': 0, 'count': 0, 'position': 0}))
    return jsonify(governors)

@bp.route('/mps/<constituency>')
def mp(constituency):
    mps = list(candidates_collection.find({'position': 'MP', 'constituency': constituency}, {'_id': 0, 'count': 0, 'position': 0}))
    return jsonify(mps)

@bp.route('/counties')
def counties():
    counties = list(geo.find({}, {'constituencies': 0, '_id': 0}))
    return jsonify(counties)

@bp.route('/<county>/constituencies')
def constituencies(county):
    constituencies = list(geo.find({'county': county}, {'_id': 0, 'county': 0}))
    return jsonify(constituencies)

@bp.route('/tally')
def tally():
    tally = list(candidates_collection.find({}, {'_id': 0}))
    return jsonify(tally)

@bp.route('/president/tally')
def president_tally():
    tally = list(candidates_collection.find({'position': 'president'}, {'_id': 0}))
    return jsonify(tally)

@bp.route('/governor/tally')
def governor_tally():
    tally = list(candidates_collection.find({'position': 'governor'}, {'_id': 0}))
    return jsonify(tally)

@bp.route('/mp/tally')
def mp_tally():
    tally = list(candidates_collection.find({'position': 'MP'}, {'_id': 0}))
    return jsonify(tally)

'''@bp.app_errorhandler(error)
def not_found(error):
    return jsonify({'error': 'Not Found'}), 404'''