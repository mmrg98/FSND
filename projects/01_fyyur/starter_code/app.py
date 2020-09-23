#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from datetime import datetime
import datetime
import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime
from flask_migrate import Migrate
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# TODO: connect to a local postgresql database
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:191198@localhost/fyyur"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

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

	def upcoming_shows(self):
		return Show.query.filter(Show.start_time>= datetime.today(),Show.venue_id==self.id)

	def upcoming_shows_count(self):
		return Show.query.filter(Show.start_time>= datetime.today(),Show.venue_id==self.id).count()

	def past_shows(self):
		return Show.query.filter(Show.start_time < datetime.today(),Show.venue_id==self.id)

	def past_shows_count(self):
		return Show.query.filter(Show.start_time < datetime.today(),Show.venue_id==self.id).count()



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

	def upcoming_shows(self):
		return Show.query.filter(Show.start_time>= datetime.today(),Show.artist_id==self.id)

	def upcoming_shows_count(self):
		return Show.query.filter(Show.start_time>= datetime.today(),Show.artist_id==self.id).count()

	def past_shows(self):
		return Show.query.filter(Show.start_time < datetime.today(),Show.artist_id==self.id)

	def past_shows_count(self):
		return Show.query.filter(Show.start_time < datetime.today(),Show.artist_id==self.id).count()

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

	def venue_name(self):
		v = Venue.query.get(self.venue_id)
		return v.name

	def venue_image_link(self):
		v = Venue.query.get(self.venue_id)
		return v.image_link

	def artist_name(self):
		artist = Artist.query.get(self.artist_id)
		return artist.name

	def artist_image_link(self):
		artist = Artist.query.get(self.artist_id)
		return artist.image_link



	def __init__(self, start_time, venue_id, artist_id):
		self.start_time = start_time
		self.venue_id = venue_id
		self.artist_id = artist_id

	def __repr__(self):
		return f"<Show: {self.start_time}>"


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  value=str(value)
  date = dateutil.parser.parse(value)
  if format == 'full':
	  format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
	  format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues', methods=['POST', 'GET'])
def venues():

	if request.method == 'POST':
		new_venue = Venue(request.form['name'], request.form['city'], request.form['state'],
		request.form['address'],request.form['genres'], request.form['phone'], request.form['website'], request.form['image_link'],
		 request.form['facebook_link'], request.form['seeking_talent'], request.form['seeking_description'])


		db.session.add(new_venue)
		db.session.commit()
		return {"message": f"venue {new_venue.name} has been created"}


	elif request.method == 'GET':
		venues = Venue.query.all()

		results = [{
		"city": venue.city,
		"state": venue.state,
		"venues": [{
		"id": v.id,
		"name": v.name,
		"num_upcoming_shows": Show.query.filter_by(venue_id=v.id),
		} for v in Venue.query.filter_by(city=venue.city).all()]
		} for venue in venues]
		return render_template('pages/venues.html', areas=results);


@app.route('/venues/search', methods=['GET', 'POST'])
def search_venues():
	search_term=request.form['search_term']
	result= Venue.query.filter(Venue.name.like('%' + search_term + '%'))

	response={
	"count":result.count(),
	"data": [{
	"id": v.id,
	"name": v.name,
	"num_upcoming_shows": v.shows.count,
	}for v in result]
	}
	return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
	venue = Venue.query.get(venue_id)
	shows=Show.query.filter(venue_id==venue.id)
	data={
    "id": venue.id ,
    "name": venue.name,
    "genres": venue.genres,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.website,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "seeking_description": venue.seeking_description,
    "image_link": venue,
    "upcoming_shows": [{
      "artist_id": sh.artist_id,
      "artist_name": Artist.query.get(sh.artist_id).name,
      "artist_image_link": "",
      "start_time": sh.start_time
    } for sh in shows],}


	return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():


	name = request.form['name']
	city = request.form['city']
	state = request.form['state']
	phone = request.form['phone']
	website = request.form['website']
	genres = request.form['genres']
	address = request.form['address']
	image_link = request.form['image_link']
	facebook_link = request.form['facebook_link']
	seeking_talent = request.form['seeking_talent']
	seeking_description = request.form['seeking_description']


	body = {}
	error = False
	if (name is None or city is None or state is None or phone is None or address is None or image_link is None
	 or genres is None or facebook_link is None or website is None or seeking_description is None or seeking_talent is None):
		error = True
		abort(400)

	else:
		try:
			if seeking_talent=="False":
				seeking_talent=False
			else:
				seeking_talent=True
			new_venue = Venue(name=name, city=city, state=state, phone=phone, website=website,
			genres=genres, address=address, image_link=image_link, facebook_link=facebook_link,
			seeking_talent=seeking_talent, seeking_description=seeking_description)

			db.session.add(new_venue)
			db.session.commit()
			flash('Venue ' + request.form['name'] + ' was successfully listed!')
			created_venue_id = new_venue.id

		except:
			error = True
			db.session.rollback()

		finally:
			db.session.close()

	if error:
		flash('An error occurred. Venue ' +  ' could not be listed.')

	return render_template('pages/home.html')



@app.route('/venues/<venue_id>/delete/', methods=['GET'])
def delete_venue(venue_id):
	error = False
	body = {}
	try:
		Venue.query.filter_by(id=venue_id).delete()
		db.session.commit()
		flash('Venue was successfully Deleted!')
	except:
		db.session.rollback()
	finally:
		db.session.close()

	return render_template('pages/home.html')


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists', methods=['POST', 'GET'])
def artists():

		if request.method == 'POST':
			new_artist = Artist(request.form['name'], request.form['city'], request.form['state'],
			request.form['phone'], request.form['genres'], request.form['image_link'], request.form['facebook_link'],
			request.form['website'], request.form['seeking_venue'], request.form['seeking_description'])


			db.session.add(new_artist)
			db.session.commit()
			return {"message": f"artist {new_artist.name} has been created"}


		elif request.method == 'GET':
	  		artists = Artist.query.all()
	  		data=[{
		  	"id": artist.id,
		  	"name": artist.name,
		    } for artist in artists]


	  		return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
	search_term=request.form['search_term']
	result= Artist.query.filter(Artist.name.like('%' + search_term + '%'))

	response={
	"count":result.count(),
	"data": [{
	"id": artist.id,
	"name": artist.name,
	"num_upcoming_shows": 0,
	}for artist in result]
	}
	return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

	artist = Artist.query.get(artist_id)


	return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  result = Artist.query.get(artist_id)
  form = ArtistForm(obj=result)

  artist={
	"id": result.id,
	"name": result.name,
	"genres": result.genres,
	"city": result.city,
	"state": result.state,
	"phone": result.phone,
	"website":result.website,
	"facebook_link": result.facebook_link,
	"seeking_venue": result.seeking_venue,
	"seeking_description": result.seeking_description,
	"image_link":result.image_link,
  }

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
	  result = Artist.query.get(artist_id)
	  form = ArtistForm(formdata=request.form, obj=result)
	  name = request.form['name']
	  city = request.form['city']
	  state = request.form['state']
	  phone = request.form['phone']
	  genres = request.form['genres']
	  website = request.form['website']
	  image_link = request.form['image_link']
	  facebook_link = request.form['facebook_link']
	  seeking_venue = request.form['seeking_venue']
	  seeking_description = request.form['seeking_description']
	  if seeking_venue=="False":
		  seeking_venue=False
	  else:
		  seeking_venue=True
	  result.name=name
	  result.city = city
	  result.state = state
	  result.phone = phone
	  result.genres = genres
	  result.website = website
	  result.image_link = image_link
	  result.facebook_link = facebook_link
	  result.seeking_venue = seeking_venue
	  result.seeking_description = seeking_description


	  db.session.commit()


	  return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  result = Venue.query.get(venue_id)
  form = VenueForm(obj=result)

  venue={
	"id": result.id,
	"name": result.name,
	"address": result.address,
	"city": result.city,
	"state": result.state,
	"phone": result.phone,
	"website":result.website,
	"facebook_link": result.facebook_link,
	"seeking_talent": result.seeking_talent,
	"seeking_description": result.seeking_description,
	"image_link":result.image_link,
  }

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
	 result = Venue.query.get(venue_id)
	 form = VenueForm(formdata=request.form, obj=result)
	 name = request.form['name']
	 city = request.form['city']
	 state = request.form['state']
	 phone = request.form['phone']
	 address = request.form['address']
	 website = request.form['website']
	 image_link = request.form['image_link']
	 facebook_link = request.form['facebook_link']
	 seeking_talent = request.form['seeking_talent']
	 seeking_description = request.form['seeking_description']
	 if seeking_talent=="False":
		 seeking_talent=False
	 else:
		 seeking_talent=True
	 result.name=name
	 result.city = city
	 result.state = state
	 result.phone = phone
	 result.address = address
	 result.website = website
	 result.image_link = image_link
	 result.facebook_link = facebook_link
	 result.seeking_talent = seeking_talent
	 result.seeking_description = seeking_description

	 db.session.commit()
	 return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

		name = request.form['name']
		city = request.form['city']
		state = request.form['state']
		phone = request.form['phone']
		genres = request.form['genres']
		website = request.form['website']
		image_link = request.form['image_link']
		facebook_link = request.form['facebook_link']
		seeking_venue = request.form['seeking_venue']
		seeking_description = request.form['seeking_description']


		body = {}
		error = False
		if (name is None or city is None or state is None or website is None
		or phone is None or image_link is None
		 or facebook_link is None or seeking_description is None):
			error = True
			abort(400)

		else:
			try:
				if seeking_venue=="False":
					seeking_venue=False
				else:
					seeking_venue=True


				new_artist = Artist(name=name, city=city, state=state, phone=phone,genres=genres,website=website,
				   image_link=image_link, facebook_link=facebook_link, seeking_venue=seeking_venue, seeking_description=seeking_description)

				db.session.add(new_artist)
				db.session.commit()
				flash('Artist ' + request.form['name'] + ' was successfully listed!')


			except:
				error = True
				db.session.rollback()

			finally:
				db.session.close()

		if error:
			flash('An error occurred. Artist ' +  ' could not be listed.')

		return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
	if request.method == 'POST':
		new_show = Show(request.form['artist_id'], request.form['venue_id'], request.form['start_time'])

		db.session.add(new_show)
		db.session.commit()
		return {"message": f"show {new_show.name} has been created"}


	elif request.method == 'GET':
		shows = Show.query.all()

		results = [{
		"venue_id": show.venue_id,
		"venue_name": Venue.query.get(show.venue_id).name,
		"artist_id": show.artist_id,
		"artist_name": Artist.query.get(show.artist_id).name,
		"artist_image_link": Artist.query.get(show.artist_id).image_link,
		"start_time": show.start_time,
		} for show in shows]
		return render_template('pages/shows.html', shows=results)


@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
		artist_id = request.form['artist_id']
		venue_id = request.form['venue_id']
		start_time = request.form['start_time']

		body = {}
		error = False
		if (start_time is None or venue_id is None or artist_id is None):
			error = True
			abort(400)

		else:
			try:
				new_show = Show(venue_id=venue_id, artist_id=artist_id, start_time=start_time)
				db.session.add(new_show)
				db.session.commit()
				flash('show '+ ' was successfully listed!')
				created_show_id = new_show.id
			except:
				error = True
				db.session.rollback()
			finally:
				db.session.close()

		if error:
			flash('An error occurred. Show ' +  ' could not be listed.')

		return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
	return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
	return render_template('errors/500.html'), 500


if not app.debug:
	file_handler = FileHandler('error.log')
	file_handler.setFormatter(
		Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
	)
	app.logger.setLevel(logging.INFO)
	file_handler.setLevel(logging.INFO)
	app.logger.addHandler(file_handler)
	app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
	app.run(debug=True)

# Or specify port manually:
'''
if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)
'''
