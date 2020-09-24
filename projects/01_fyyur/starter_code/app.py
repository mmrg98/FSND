#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
from datetime import datetime
from models import app, db, Venue, Artist, Show
import datetime
import json
import dateutil.parser
import babel
from flask import (
	Flask,
	render_template,
	request, Response,
	flash,
	redirect,
	url_for,
	abort
)
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

moment = Moment(app)
app.config.from_object('config')
db.init_app(app)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


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

@app.route('/venues')
def venues():
	""" This method list all exist venues in database """

	locals = []
	venues = Venue.query.all()
	for place in Venue.query.distinct(Venue.city, Venue.state).all():
		locals.append({
        'city': place.city,
        'state': place.state,
        'venues': [{
            'id': venue.id,
            'name': venue.name,
        } for venue in venues if
            venue.city == place.city and venue.state == place.state]
    })

	return render_template('pages/venues.html', areas=locals);


@app.route('/venues/search', methods=['GET', 'POST'])
def search_venues():
	""" Search Method: takes the search term from search label (POST)
	and returns every venue that it's name contains the search term (GET) """

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

	"""This method takes venue's id and redirects to this
	venue's page that contains all the details about this venue"""

	venue = Venue.query.get(venue_id)
	shows=Show.query.filter(venue_id==venue.id)
	past_shows = db.session.query(Artist, Show).join(Show).join(Venue).\
    filter(
        Show.venue_id == venue_id,
        Show.artist_id == Artist.id,
        Show.start_time < datetime.now()
    ).\
    all()

	upcoming_shows = db.session.query(Artist, Show).join(Show).join(Venue).\
    filter(
        Show.venue_id == venue_id,
        Show.artist_id == Artist.id,
        Show.start_time > datetime.now()
    ).\
    all()

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
    "image_link": venue.image_link,
    'past_shows': [{
            'artist_id': artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for artist, show in past_shows],
        'upcoming_shows': [{
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for artist, show in upcoming_shows],
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
    }


	return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():

  """ This function to invoke venue's form so the user can fill it """

  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

	"""This method create venues by taking venues details from venue's
	 form that user should fill and create the venue using these details"""


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

	"""This method takes venue's ID and delete the venue that has given ID from database"""


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
@app.route('/artists')
def artists():
	"""This method list all exist artists in database """

	artists = Artist.query.all()
	data=[{
	"id": artist.id,
	"name": artist.name,
	} for artist in artists]


	return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():

	""" Search Method: takes the search term from search label (POST)
	and returns every artist that it's name contains the search term (GET) """

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

	"""This method takes artist's id and redirects to this
	artist's page that contains all the details about this artist"""

	artist = Artist.query.get(artist_id)
	shows=Show.query.filter(artist_id==artist.id)

	past_shows = db.session.query(Venue, Show).join(Show).join(Artist).\
    filter(
        Show.artist_id == artist_id,
        Show.venue_id == Venue.id,
        Show.start_time < datetime.now()
    ).\
    all()

	upcoming_shows = db.session.query(Venue, Show).join(Show).join(Artist).\
    filter(
        Show.venue_id == Venue.id,
        Show.artist_id == artist_id,
        Show.start_time > datetime.now()
    ).\
    all()


	data={
    "id": artist.id ,
    "name": artist.name,
    "genres": artist.genres,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    'past_shows': [{
            'venue_id': venue.id,
            "venue_name": venue.name,
            "venue_image_link": venue.image_link,
            "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for venue, show in past_shows],
        'upcoming_shows': [{
            'venue_id': venue.id,
            'venue_name': venue.name,
            'venue_image_link': venue.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for venue, show in upcoming_shows],
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
    }

	return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

	""" This method takes artist's ID and fill artist form
	with artist's details to edit this details"""

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

	""" Here the method takes the given artist's ID and takes the details of
	this artist from artist form and submit the changes of these details"""

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

	""" This method takes venue's ID and fill venue form
	with venue's details to edit this details"""

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

	""" Here the method takes the given venue's ID and takes the details of
	this venue from venue form and save the changes of these details"""

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

  """ This function to invoke artist's form so the user can fill it """

  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

		"""This method create venues by taking venues details from venue's
		 form that user should fill and create the venue using these details"""

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

		"""returns list of all shows """

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

  """ invoke show form to create new show """
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():

		"""This method create show by taking show details from show's
		 form that user should fill and create the show using these details"""

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
