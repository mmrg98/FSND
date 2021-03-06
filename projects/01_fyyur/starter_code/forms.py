from datetime import datetime
from flask_wtf import Form, FlaskForm
from enum import Enum
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL


class Genres(Enum):
    Alternative='Alternative'
    Blues= 'Blues'
    Classical= 'Classical'
    Country='Country'
    Electronic= 'Electronic'
    Folk='Folk'
    Funk= 'Funk'
    HipHop= 'HipHop'
    HeavyMetal= 'HeavyMetal'
    Instrumental= 'Instrumental'
    Jazz= 'Jazz'
    MusicalTheatre= 'MusicalTheatre'
    Pop= 'Pop'
    Punk= 'Punk'
    RB= 'RB'
    Reggae= 'Reggae'
    RocknRoll ='RocknRoll'
    Soul='Soul'
    Other= 'Other'
state_choices = [
    ('AL', 'AL'),
    ('AK', 'AK'),
    ('AZ', 'AZ'),
    ('AR', 'AR'),
    ('CA', 'CA'),
    ('CO', 'CO'),
    ('CT', 'CT'),
    ('DE', 'DE'),
    ('DC', 'DC'),
    ('FL', 'FL'),
    ('GA', 'GA'),
    ('HI', 'HI'),
    ('ID', 'ID'),
    ('IL', 'IL'),
    ('IN', 'IN'),
    ('IA', 'IA'),
    ('KS', 'KS'),
    ('KY', 'KY'),
    ('LA', 'LA'),
    ('ME', 'ME'),
    ('MT', 'MT'),
    ('NE', 'NE'),
    ('NV', 'NV'),
    ('NH', 'NH'),
    ('NJ', 'NJ'),
    ('NM', 'NM'),
    ('NY', 'NY'),
    ('NC', 'NC'),
    ('ND', 'ND'),
    ('OH', 'OH'),
    ('OK', 'OK'),
    ('OR', 'OR'),
    ('MD', 'MD'),
    ('MA', 'MA'),
    ('MI', 'MI'),
    ('MN', 'MN'),
    ('MS', 'MS'),
    ('MO', 'MO'),
    ('PA', 'PA'),
    ('RI', 'RI'),
    ('SC', 'SC'),
    ('SD', 'SD'),
    ('TN', 'TN'),
    ('TX', 'TX'),
    ('UT', 'UT'),
    ('VT', 'VT'),
    ('VA', 'VA'),
    ('WA', 'WA'),
    ('WV', 'WV'),
    ('WI', 'WI'),
    ('WY', 'WY'),
]

class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()], choices=state_choices
    )
    
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone'
    )

    website = StringField(
        'website', validators=[URL()]
    )
    image_link = StringField(

        'image_link', validators=[URL()]
    )

    genres = SelectMultipleField('genres', validators=[DataRequired(), AnyOf(values=[genres.value for genres in Genres])],
    choices=[(genres.value, genres.value) for genres in Genres])

    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    seeking_talent = SelectField(
        'genres', validators=[DataRequired()],
        choices=[(True,True), (False,False)]
        )
    seeking_description = StringField(
        'seeking_description'
    )


class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()], choices=state_choices
    )
    phone = StringField(
        'phone'
    )

    website = StringField('website', validators=[URL()])

    genres = SelectMultipleField('genres', validators=[DataRequired(), AnyOf(values=[genres.value for genres in Genres])],
    choices=[(genres.value, genres.value) for genres in Genres])


    facebook_link = StringField(

        'facebook_link', validators=[URL()]
    )
    image_link = StringField(

        'image_link', validators=[URL()]
    )
    seeking_venue = SelectField(

        'seeking_venue', validators=[DataRequired()],
        choices=[(True,True), (False,False)])
    seeking_description = StringField(

        'seeking_description', validators=[DataRequired()]
    )
