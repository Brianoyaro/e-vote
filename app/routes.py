from flask import render_template, request, redirect, url_for, flash
from app.forms import LoginForm, NewConstituencyForm
from app import app, redisClient
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
        found = False
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
            flash('Credentials do not match. Try again')
    return render_template('index.html', form=form)

@app.route('/register/<token>', methods=['GET', 'POST'])
def register(token):
    form = NewConstituencyForm()
    voter = redisClient.hgetall(token)
    if form.validate_on_submit():
        county = form.county.data
        constituency = form.constituency.data
        if county != '':
            voter['county'] = county
        if constituency != '':
            voter['constituency'] = constituency
        if county != '' or constituency != '':
            # delete user from redis
            redisClient.delete(token)
            # insert a new user in redis with updated information
            token = str(uuid.uuid4())
            redisClient.hset(token, mapping=voter)
        return redirect(url_for('president', token=token))
    return render_template('new_constituency.html', form=form, voter=voter, token=token)

@app.route('/president/<token>', methods=['GET', 'POST'])
def president(token):
    voter = redisClient.hgetall(token)
    return '<p>This is for presidential voting</p>'
