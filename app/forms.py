from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    idNumber = StringField('ID Number', validators=[DataRequired()])
    serialNumber = StringField('serial Number', validators=[DataRequired()])
    submit = SubmitField('submit')


class ChoiceForm(FlaskForm):
    choice = RadioField('Candidate', choices=[], validators=[DataRequired()])
    submit = SubmitField('submit')


class SubmitForm(FlaskForm):
    submit = SubmitField('submit')


class ChangePlaceForm(FlaskForm):
    place = RadioField('Constituency', choices=[], validators=[DataRequired()])
    submit = SubmitField('submit')
