from flask import render_template, request, redirect, url_for, flash
from app.forms import LoginForm, NewConstituencyForm, ChoiceForm, SubmitForm
from app import app, redisClient, voters_collection as voters, candidates_collection
import uuid


data = [
        {'idNumber': 1, 'serialNumber': 1, 'name': 'Brian Mokua', 'county': 'Mombasa', 'constituency': 'Kiasuni'},
        {'idNumber': 2, 'serialNumber': 2, 'name': 'Johnstone Kahindi', 'county': 'Kilifi', 'constituency': 'Kilifi-poly'},
        {'idNumber': 3, 'serialNumber': 3, 'name': 'Sylvetser Onyango', 'county': 'Kajiado', 'constituency': 'Kiserian'}
        ]

@app.route('/', methods=['GET', 'POST'])
def home():
    form = LoginForm()
    if form.validate_on_submit():
        idNumber = int(form.idNumber.data)
        serialNumber = int(form.serialNumber.data)
        '''found = False
        for user in data:
            if user['idNumber'] == idNumber and user['serialNumber'] == serialNumber:
                found = True
                token = str(uuid.uuid4())
                redisClient.hset(token, mapping=user)
                # expire the key after 1.5 days
                redisClient.expire(token, 129600)
                # to delete the  key
                # redisClient.delete(token)
        if found:
            return redirect(url_for('register', token=token))
        if not found:
            flash('Credentials do not match. Try again')'''
        
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
            # expire the key after 1.5 days
            redisClient.expire(token, 129600)
            # to delete the  key
            # redisClient.delete(token)
            return redirect(url_for('register', token=token))
    return render_template('index.html', form=form)

@app.route('/register/<token>', methods=['GET', 'POST'])
def register(token):
    form = NewConstituencyForm()
    voter = redisClient.hgetall(token)
    voterId = voter.get('idNumber')
    voterId = int(voterId)
    if form.validate_on_submit():
        county = form.county.data
        constituency = form.constituency.data
        if county != '':
            # voter['county'] = county
            voters.update_one({'idNumber': voterId},{'$set': {'votingCounty': county}})
        if constituency != '':
            # voter['constituency'] = constituency
            voters.update_one({'idNumber': voterId}, {'$set': {'votingConstituency': constituency}})
        if county != '' or constituency != '':
            # delete user from redis
            redisClient.delete(token)
            voter = voters.find_one({'idNumber': voterId}, {'_id': 0})
            # insert a new user in redis with updated information
            token = str(uuid.uuid4())
            redisClient.hset(token, mapping=voter)
        return redirect(url_for('president', token=token))
    return render_template('new_constituency.html', form=form, voter=voter, token=token)

@app.route('/president/<token>', methods=['GET', 'POST'])
def president(token):
    current_user = redisClient.hgetall(token)
    voter = voters.find_one({'idNumber': int(current_user.get('idNumber'))})
    candidates = candidates_collection.find({'position': 'president'}, {'_id': 0})
    '''if request.method == 'POST':
        post_data = request.data
        return post_data'''
    form = ChoiceForm()
    if form.validate_on_submit():
        president = form.choice.data
        voters.update_one({'idNumber': int(current_user.get('idNumber'))}, {'$set': {'president': president}})
        # in redis, incr the presidential candidate
        redisClient.incr(president, 1)
        # find a way to backup storage in a different place apart from redis e.g in mongo
        return redirect(url_for('governor', token=token))
    return render_template('voting.html', candidates=candidates, form=form, voter=voter, logo='Presidential Candidates')

@app.route('/governor/<token>', methods=['GET', 'POST'])
def governor(token):
    current_user = redisClient.hgetall(token)
    voter = voters.find_one({'idNumber': int(current_user.get('idNumber'))}, {'_id': 0})
    voter_county = voter.get('votingCounty')
    if not voter_county:
        voter_county = voter.get('county')
    candidates = candidates_collection.find({'position': 'governor', 'county': voter_county}, {'_id': 0})
    form = ChoiceForm()
    if form.validate_on_submit():
        governor = form.choice.data
        voters.update_one({'idNumber': int(current_user.get('idNumber'))}, {'$set': {'governor': governor}})
        redisClient.incr(governor, 1)
        return redirect(url_for('mp', token=token))
    return render_template('voting.html', form=form, candidates=candidates, voter=voter, logo='{} Governor Candidates'.format(voter_county))

@app.route('/mp/<token>', methods=['GET', 'POST'])
def mp(token):
    current_user = redisClient.hgetall(token)
    voter = voters.find_one({'idNumber': int(current_user.get('idNumber'))}, {'_id': 0})
    voter_constituency = voter.get('votingConstituency')
    if not voter_constituency:
        voter_constituency = voter.get('constituency')
    candidates = candidates_collection.find({'position': 'MP', 'constituency': voter_constituency}, {'_id': 0})
    form = ChoiceForm()
    if form.validate_on_submit():
        mp = form.choice.data
        voters.update_one({'idNumber': int(current_user.get('idNumber'))}, {'$set': {'mp': mp}})
        redisClient.incr(mp, 1)
        # return render_template('view.html')
        return redirect(url_for('view', token=token))
    return render_template('voting.html', form=form, candidates=candidates, voter=voter, logo='{} MP Candidates'.format(voter_constituency))


@app.route('/view/<token>', methods=['GET', 'POST'])
def view(token):
    current_user = redisClient.hgetall(token)
    voter = voters.find_one({'idNumber': int(current_user.get('idNumber'))}, {'id': 0})
    mapping = {
            'president': voter.get('president'),
            'governor': voter.get('governor'),
            'mp': voter.get('mp')
            }
    form = SubmitForm()
    if form.validate_on_submit():
        voters.update_one({'idNumber': int(current_user.get('idNumber'))},{'$set': {'status': 'voted'}})
        flash('You have finished voting')
        return redirect(url_for('home'))
    return render_template('view.html', mapping=mapping, form=form)
