from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime
from flask_migrate import Migrate

app = Flask(__name__)
db = SQLAlchemy()
migrate = Migrate(app, db)


class Venue(db.Model):
	__tablename__ = 'Venue'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	city = db.Column(db.String(120))
	state = db.Column(db.String(120))
	address = db.Column(db.String(120))
	phone = db.Column(db.String(120))
	website = db.Column(db.String(120))
	genres = db.Column(db.String(120))
	image_link = db.Column(db.String(500))
	facebook_link = db.Column(db.String(120))
	seeking_talent = db.Column(db.Boolean(), unique=False, default=True)
	seeking_description = db.Column(db.String(500))
	shows = db.relationship('Show', backref='show_v', cascade="all,delete")


	def __init__(self, name, city, state, address, phone, website, genres, image_link,
	 			facebook_link, seeking_talent, seeking_description):
		self.name = name
		self.city = city
		self.phone = phone
		self.state = state
		self.address = address
		self.image_link = image_link
		self.facebook_link = facebook_link
		self.website = website
		self.genres = genres
		self.seeking_talent = seeking_talent
		self.seeking_description = seeking_description



	def __repr__(self):
		return f"<Venue {self.name}>"

	# TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
	__tablename__ = 'Artist'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String)
	city = db.Column(db.String(120))
	state = db.Column(db.String(120))
	phone = db.Column(db.String(120))
	website = db.Column(db.String(120))
	genres = db.Column(db.String(120))
	image_link = db.Column(db.String(500))
	facebook_link = db.Column(db.String(120))
	seeking_venue = db.Column(db.Boolean(), unique=False, default=True)
	seeking_description = db.Column(db.String(500))
	shows = db.relationship('Show', backref='show_a', cascade="all,delete")


	def __init__(self, name, city, state, phone, genres, website, image_link,
				facebook_link, seeking_venue, seeking_description):
		self.name = name
		self.city = city
		self.phone = phone
		self.state= state
		self.genres= genres
		self.image_link= image_link
		self.facebook_link= facebook_link
		self.website = website
		self.seeking_venue = seeking_venue
		self.seeking_description = seeking_description

	def __repr__(self):
		return f"<Artist {self.name}>"


class Show(db.Model):
	__tablename__ = 'Show'

	id = db.Column(db.Integer, primary_key=True)
	start_time = db.Column(db.DateTime)
	venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
	artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)


	def __init__(self, start_time, venue_id, artist_id):
		self.start_time = start_time
		self.venue_id = venue_id
		self.artist_id = artist_id

	def __repr__(self):
		return f"<Show: {self.start_time}>"
