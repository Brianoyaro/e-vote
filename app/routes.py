from flask import render_template, redirect, url_for, flash, abort, session
from app.forms import LoginForm, SubmitForm, ChoiceForm, ChangePlaceForm
from app import app, redisClient, voters_collection as voters, candidates_collection, geo
import uuid


@app.errorhandler(404)
def Not_found_error(error):
    return render_template('404.html')


@app.route('/', methods=['GET', 'POST'])
def home():
    '''index page of application
    '''
    form = LoginForm()
    if form.validate_on_submit():
        idNumber = int(form.idNumber.data)
        serialNumber = int(form.serialNumber.data)
        user = voters.find_one({'idNumber': idNumber, 'serialNumber': serialNumber}, {'_id': 0})
        if not user:
            flash('Credentials do not match. Try again')
            return redirect(url_for('home'))
        status = user.get('status')
        if status == 'voted':
            flash('You have already voted')
            return redirect(url_for('home'))
        if user and not status:
            flash('Logged in successfully. You can now vote!')
            token = str(uuid.uuid4())
            redisClient.hset(token, mapping=user)
            # expire the key after 10 minutes
            redisClient.expire(token, 600)
            # to delete the  key
            # redisClient.delete(token)
            return redirect(url_for('register', token=token))
    return render_template('index.html', form=form)


@app.route('/register/<token>', methods=['GET', 'POST'])
def register(token):
    '''allows a user to change their voting location
    '''
    session['visited'] = True
    session['token'] = token
    current_user = redisClient.hgetall(token)
    if not current_user:
        abort(404)
    voter = voters.find_one({'idNumber': int(current_user.get('idNumber'))})
    user_county = voter.get('votingCounty')
    if not user_county:
        user_county = voter.get('county')
    user_constituency = voter.get('votingConstituency')
    if not user_constituency:
        user_constituency = voter.get('constituency')
    mapping = {
            'name': current_user.get('name'),
            'county': user_county,
            'constituency': user_constituency
            }
    return render_template('new_county_or_constituency.html', mapping=mapping, token=token)


@app.route('/president/<token>', methods=['GET', 'POST'])
def president(token):
    '''Presidential voting
    '''
    session['visited'] = True
    session['token'] = token
    current_user = redisClient.hgetall(token)
    if not current_user:
        abort(404)
    voter = voters.find_one({'idNumber': int(current_user.get('idNumber'))})
    candidates = list(candidates_collection.find({'position': 'president'}, {'_id': 0}))
    form = ChoiceForm()
    form.choice.choices = [(c['name'], "{} ({})".format(c['name'], c['party'])) for c in candidates]
    # the following lines tackle misusing of a token to vote unlimited times
    my_president = voter.get('president')
    if my_president:
        redisClient.incr(my_president, -1)
        voters.update_one({'idNumber': int(current_user.get('idNumber'))}, {'$set': {'president': ''}})
        # reduce count of this particular candidate in mongo
        candidates_collection.update_one({'name': my_president}, {'$inc': {'count': -1}})
    # checking ends here
    if form.validate_on_submit():
        president = form.choice.data
        # store that this voter selected this candidate
        voters.update_one({'idNumber': int(current_user.get('idNumber'))}, {'$set': {'president': president}})
        redisClient.incr(president, 1)
        # increase in mongo too
        candidates_collection.update_one({'name': president}, {'$inc': {'count': 1}})
        return redirect(url_for('governor', token=token))
    candidates = candidates_collection.find({'position': 'president'}, {'_id': 0, 'name': 1, 'party': 1})
    return render_template('voting.html', candidates=candidates, form=form, voter=voter, logo='Presidential Candidates')


@app.route('/governor/<token>', methods=['GET', 'POST'])
def governor(token):
    '''governor voting
    '''
    session['visited'] = True
    session['token'] = token
    current_user = redisClient.hgetall(token)
    if not current_user:
        abort(404)
    voter = voters.find_one({'idNumber': int(current_user.get('idNumber'))}, {'_id': 0})
    # the following lines tackle misusing of a token to vote unlimited times
    my_governor = voter.get('governor')
    if my_governor:
        redisClient.incr(my_governor, -1)
        # reduce count of this particular candidate in mongo
        candidates_collection.update_one({'name': my_governor}, {'$inc': {'count': -1}})
        voters.update_one({'idNumber': int(current_user.get('idNumber'))}, {'$set': {'governor': ''}})
    # checking ends here
    voter_county = voter.get('votingCounty')
    if not voter_county:
        voter_county = voter.get('county')
    candidates = candidates_collection.find({'position': 'governor', 'county': voter_county}, {'_id': 0})
    form = ChoiceForm()
    form.choice.choices = [(c['name'], "{} ({})".format(c['name'], c['party'])) for c in candidates]
    if form.validate_on_submit():
        governor = form.choice.data
        # store that this voter selected this candidate
        voters.update_one({'idNumber': int(current_user.get('idNumber'))}, {'$set': {'governor': governor}})
        redisClient.incr(governor, 1)
        # increase in mongo too
        candidates_collection.update_one({'name': governor}, {'$inc': {'count': 1}})
        return redirect(url_for('mp', token=token))
    return render_template('voting.html', form=form, candidates=candidates, voter=voter, logo='{} Governor Candidates'.format(voter_county))


@app.route('/mp/<token>', methods=['GET', 'POST'])
def mp(token):
    '''mp voting
    '''
    session['visited'] = True
    session['token'] = token
    current_user = redisClient.hgetall(token)
    if not current_user:
        abort(404)
    voter = voters.find_one({'idNumber': int(current_user.get('idNumber'))}, {'_id': 0})
    # the following lines tackle misusing of a token to vote unlimited times
    my_mp = voter.get('mp')
    if my_mp:
        redisClient.incr(my_mp, -1)
        # reduce count of this particular candidate in mongo
        candidates_collection.update_one({'name': my_mp}, {'$inc': {'count': -1}})
        voters.update_one({'idNumber': int(current_user.get('idNumber'))}, {'$set': {'mp': ''}})
    # checking ends here
    voter_constituency = voter.get('votingConstituency')
    if not voter_constituency:
        voter_constituency = voter.get('constituency')
    candidates = candidates_collection.find({'position': 'MP', 'constituency': voter_constituency}, {'_id': 0})
    form = ChoiceForm()
    form.choice.choices = [(c['name'], "{} ({})".format(c['name'], c['party'])) for c in candidates]
    if form.validate_on_submit():
        mp = form.choice.data
        # store that this voter selected this candidate
        voters.update_one({'idNumber': int(current_user.get('idNumber'))}, {'$set': {'mp': mp}})
        redisClient.incr(mp, 1)
        # increase in mongo too
        candidates_collection.update_one({'name': mp}, {'$inc': {'count': 1}})
        return redirect(url_for('view', token=token))
    return render_template('voting.html', form=form, candidates=candidates, voter=voter, logo='{} MP Candidates'.format(voter_constituency))


@app.route('/view/<token>', methods=['GET', 'POST'])
def view(token):
    '''allows a voter to see their selected candidates
    '''
    # session['visited'] = True
    # session['token'] = token
    current_user = redisClient.hgetall(token)
    if not current_user:
        abort(404)
    voter = voters.find_one({'idNumber': int(current_user.get('idNumber'))}, {'id': 0})
    mapping = {
            'president': voter.get('president'),
            'governor': voter.get('governor'),
            'mp': voter.get('mp')
            }
    form = SubmitForm()
    if form.validate_on_submit():
        session['visited'] = False
        session['token'] = None
        voters.update_one({'idNumber': int(current_user.get('idNumber'))},{'$set': {'status': 'voted'}})
        # delete token current_user from redis to save up space and prevent misuse of token
        redisClient.delete(token)
        flash('You have finished voting')
        return redirect(url_for('home'))
    return render_template('view.html', mapping=mapping, form=form, token=token)


@app.route('/change_county/<token>', methods=['GET', 'POST'])
def change_county(token):
    '''allows one to change their default voting county
    '''
    current_user = redisClient.hgetall(token)
    if not current_user:
        abort(404)
    voter = voters.find_one({'idNumber': int(current_user.get('idNumber'))}, {'id': 0})
    all_counties = list(geo.find({}, {'_id': 0, 'constituency': 0}))
    form = ChangePlaceForm()
    form.place.choices = [(c['county'], c['county']) for c in all_counties]
    if form.validate_on_submit():
        # county = form.county.data
        county = form.place.data
        voters.update_one({'idNumber': int(current_user.get('idNumber'))},{'$set': {'votingCounty': county}})
        return redirect(url_for('register', token=token))
    return render_template('change_place.html', form=form, logo='All Counties')


@app.route('/change_constituency/<token>', methods=['GET', 'POST'])
def change_constituency(token):
    '''allows one to change their default voting constituency
    '''
    current_user = redisClient.hgetall(token)
    if not current_user:
        abort(404)
    voter = voters.find_one({'idNumber': int(current_user.get('idNumber'))}, {'id': 0})
    user_county = voter.get('votingCounty')
    if not user_county:
        user_county = voter.get('county')
    constituencies = list(geo.find({'county': user_county}, {'_id': 0, 'county': 0}))
    # to handle out of range error
    if len(constituencies) == 0:
        constituencies = [{'constituencies': []}]
    form = ChangePlaceForm()
    form.place.choices = [(c, c) for c in constituencies[0].get('constituencies')]
    if form.validate_on_submit():
        constituency = form.place.data
        voters.update_one({'idNumber': int(current_user.get('idNumber'))},{'$set': {'votingConstituency': constituency}})
        return redirect(url_for('register', token=token))
    return render_template('change_place.html', form=form, logo='{} constituencies'.format(user_county))


@app.context_processor
def is_navbar_valid():
    '''habdles logic for showing nav bar only when a user is validated
    '''
    return {'valid_navbar': session.get('visited', False), 'my_token': session.get('token')}
