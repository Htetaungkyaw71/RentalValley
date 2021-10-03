from flask_wtf import FlaskForm
from wtforms import StringField,FileField,SubmitField,TextAreaField,SelectField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField
from datetime import datetime


class CreateForm(FlaskForm):
    title = StringField('title',validators=[DataRequired()])
    owner = StringField('Owner name', validators=[DataRequired()])
    description = StringField('eg 1 bed 1 bedroom 1 bathroom',validators=[DataRequired()])
    price = StringField('Price for 1 month/ks', validators=[DataRequired()])
    map = StringField('enter google map src link', validators=[DataRequired()])
    exterior = FileField('Exterior photo of house', validators=[DataRequired()])
    living_room = FileField('Living_room photo of house', validators=[DataRequired()])
    bedroom = FileField('Bedroom photo of house', validators=[DataRequired()])
    bathroom = FileField('Bathroom photo of house', validators=[DataRequired()])
    kitchen = FileField('Kitchen photo of house', validators=[DataRequired()])
    backyard = FileField('Backyard photo of house', validators=[DataRequired()])
    about = TextAreaField('About the space',validators=[DataRequired()])
    rule = TextAreaField('House rules', validators=[DataRequired()])
    category = SelectField('Category', coerce=int)
    submit = SubmitField('submit',validators=[DataRequired()])



g = [
    ('male','male'),
    ('female','female'),
    ('other','other')

]

e = [
    ('Full-time-professional','Full-time-professional'),
    ('Part-time-professional','Part-time-professional'),
    ('Student','Student'),
    ('Not Employed','Not Employed')

]

class Createprofile(FlaskForm):
    birth = DateField('Birth date', format='%Y-%m-%d',)
    about = TextAreaField(
                          'Add some details about your interests and hobbies to let potential housemates and hosts get to know you.', validators=[DataRequired()])
    gender = SelectField('Select gender',choices=g)
    social = StringField('Your social media accounts link',validators=[DataRequired()])
    employment = SelectField('Employment status',choices=e)
    submit = SubmitField('submit', validators=[DataRequired()])


class Createrequest(FlaskForm):
    move_in = DateField('Move_in', format='%Y-%m-%d',)
    move_out = DateField('Move-out', format='%Y-%m-%d', )
    about = TextAreaField('Introduce yourself to the host', validators=[DataRequired()])
    phnumber = StringField('Your phone number', validators=[DataRequired()])
    submit = SubmitField('Request booking', validators=[DataRequired()])