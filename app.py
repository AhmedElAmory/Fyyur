#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import date,datetime
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# connect to a local postgresql database

migrate=Migrate(app,db)

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
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    genres = db.Column(db.String)
    website = db.Column(db.String)
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    shows=db.relationship('Show', backref='venue', lazy=True)

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String)
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String)
    shows=db.relationship('Show', backref='artist', lazy=True)


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    starttime = db.Column(db.DateTime)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'))
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'))
    venue_name = db.Column(db.String)
    artist_name = db.Column(db.String)
    artist_image_link = db.Column(db.String(500))
    venue_image_link = db.Column(db.String(500))

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
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

# Called to retrieve the available Venues
@app.route('/venues')
def venues():
  venuedata=db.session.query(Venue)
  data=[]
  for i in venuedata:
    flag=False
    for j in data:
      if j['city']==i.city and j['state']==i.state:
        index = data.index(j)
        data[index]['venues'].append({"id":i.id,"name":i.name,"num_upcoming_shows":0})
        flag=True
        break

    if flag==False:
      data.append({"city":i.city,"state":i.state,"venues":[{"id":i.id,"name":i.name,"num_upcoming_shows":0}]})


  return render_template('pages/venues.html', areas=data)

# Searching for Venues
@app.route('/venues/search', methods=['POST'])
def search_venues():
  search_term=request.form.get('search_term')
  venues=db.session.query(Venue).filter(Venue.name.ilike("%"+search_term+"%")).all()
  response={
    "count": len(venues),
    "data": []
  }

  for i in venues:
    response['data'].append({
      "id": i.id,
      "name": i.name,
      "num_upcoming_shows": 0,
    })
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

# Show a specific venue details
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  
  venuedata=Venue.query.filter_by(id=venue_id).first()
  data={
    "id": venuedata.id,
    "name": venuedata.name,
    "genres": venuedata.genres[1:len(venuedata.genres)-1].split(","),
    "address": venuedata.address,
    "city": venuedata.city,
    "state": venuedata.state,
    "phone": venuedata.phone,
    "website": venuedata.website,
    "facebook_link": venuedata.facebook_link,
    "seeking_talent": venuedata.seeking_talent,
    "seeking_description": venuedata.seeking_description,
    "image_link": venuedata.image_link,
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }

  showsdata=db.session.query(Venue,Show).filter_by(id=venue_id).join(Show).all()

  for i in showsdata:
    if i.Show.starttime<= datetime.now():
      data['past_shows'].append({
        "artist_id": i.Show.artist_id,
        "artist_name": i.Show.artist_name,
        "artist_image_link": i.Show.artist_image_link,
        "start_time": i.Show.starttime.strftime("%Y-%m-%d %H:%M:%S")
      })
    else:
      data['upcoming_shows'].append({
        "artist_id": i.Show.artist_id,
        "artist_name": i.Show.artist_name,
        "artist_image_link": i.Show.artist_image_link,
        "start_time": i.Show.starttime.strftime("%Y-%m-%d %H:%M:%S")
      })

  data['past_shows_count']=len(data['past_shows'])
  data['upcoming_shows_count']=len(data['upcoming_shows'])

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

# Loads forms
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)
# Creates a venue
@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    address = request.form.get('address')
    phone = request.form.get('phone')
    genres = request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link')
    venue=Venue(
      name=name,
      city=city,
      state=state,
      address=address,
      phone=phone,
      genres=genres,
      facebook_link=facebook_link
    )
    db.session.add(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  except:
    #on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Venue ' + request.form.get('name') + ' could not be listed.')
    db.session.rollback()
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  return None

#  Artists
#  ----------------------------------------------------------------

# Called to retrieve available artists
@app.route('/artists')
def artists():
  artistdata=db.session.query(Artist)
  data=[]
  for i in artistdata:
      data.append({"id":i.id,"name":i.name})
      
  return render_template('pages/artists.html', artists=data)

# Search for Artists
@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term=request.form.get('search_term')
  artists=db.session.query(Artist).filter(Artist.name.ilike("%"+search_term+"%")).all()
  response={
    "count": len(artists),
    "data": []
  }

  for i in artists:
    response['data'].append({
      "id": i.id,
      "name": i.name,
      "num_upcoming_shows": 0,
    })

  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

# Show a specific artist details
@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artistdata=db.session.query(Artist).filter_by(id=artist_id).first()
  data={
    "id": artistdata.id,
    "name": artistdata.name,
    "genres": artistdata.genres[1:len(artistdata.genres)-1].split(","),
    "city": artistdata.city,
    "state": artistdata.state,
    "phone": artistdata.phone,
    "website": artistdata.website,
    "facebook_link": artistdata.facebook_link,
    "seeking_venue": artistdata.seeking_venue,
    "seeking_description": artistdata.seeking_description,
    "image_link": artistdata.image_link,
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }

  showsdata=db.session.query(Artist,Show).filter_by(id=artist_id).join(Show).all()
  for i in showsdata:
    if i.Show.starttime<= datetime.now():
      data['past_shows'].append({
        "venue_id": i.Show.venue_id,
        "venue_name": i.Show.venue_name,
        "venue_image_link": i.Show.venue_image_link,
        "start_time": i.Show.starttime.strftime("%Y-%m-%d %H:%M:%S")
      })
    else:
      data['upcoming_shows'].append({
        "venue_id": i.Show.venue_id,
        "venue_name": i.Show.venue_name,
        "venue_image_link": i.Show.venue_image_link,
        "start_time": i.Show.starttime.strftime("%Y-%m-%d %H:%M:%S")
      })
      print(data['upcoming_shows'][0]['venue_name'])

  data['past_shows_count']=len(data['past_shows'])
  data['upcoming_shows_count']=len(data['upcoming_shows'])

  return render_template('pages/show_artist.html', artist=data)

# Not Completed TODO
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # TODO
  # form = ArtistForm()
  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

# Not Completed TODO
@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  #TODO
  
  # form = VenueForm()
  # venue={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  # }
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

# Loads forms
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

# Creates an artist
@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  try:
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone')
    genres = request.form.getlist('genres')
    facebook_link = request.form.get('facebook_link')
    artist=Artist(
      name=name,
      city=city,
      state=state,
      phone=phone,
      genres=genres,
      facebook_link=facebook_link
    )
    db.session.add(artist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
    #on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Artist ' + request.form.get('name') + ' could not be listed.')
    db.session.rollback()
  finally:
    db.session.close()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

# Called to retrieve the available Shows
@app.route('/shows')
def shows():
  showdata=db.session.query(Show)
  data=[]
  for i in showdata:
    data.append({
    "venue_id":i.venue_id,
    "venue_name":i.venue_name,
    "artist_id": i.artist_id,
    "artist_name": i.artist_name,
    "artist_image_link": i.artist_image_link,
    "start_time": i.starttime.strftime("%Y-%m-%d %H:%M:%S")
    })
  
  return render_template('pages/shows.html', shows=data)

# Loads forms
@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

# Creates a Show
@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  try:
    starttime = request.form.get('start_time')
    artist_id = request.form.get('artist_id')
    venue_id = request.form.get('venue_id')
    venue=db.session.query(Venue).filter_by(id=venue_id).first()
    artist=db.session.query(Artist).filter_by(id=artist_id).first()
    
    show = Show(
      starttime=starttime,
      artist_id=artist_id,
      venue_id=venue_id,
      venue_name=venue.name,
      artist_name=artist.name,
      artist_image_link=artist.image_link,
      venue_image_link=venue.image_link
    )
    db.session.add(show)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')
  except:
    #on unsuccessful db insert, flash an error instead.
    flash('An error occurred. Show could not be listed.')
    db.session.rollback()
  finally:
    db.session.close()
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
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
