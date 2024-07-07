from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    idNumber = StringField('ID Number', validators=[DataRequired()])
    serialNumber = StringField('serial Number', validators=[DataRequired()])
    submit = SubmitField('submit')


class NewConstituencyForm(FlaskForm):
    constituency = StringField('New constituency', validators=[])
    county = StringField('New county', validators=[])
    submit = SubmitField('submit')

class ChoiceForm(FlaskForm):
    choice = StringField('Enter candidate')
    submit = SubmitField('submit')

class SubmitForm(FlaskForm):
    submit = SubmitField('submit')
