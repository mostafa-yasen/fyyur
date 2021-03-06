from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
import datetime
import json


db = SQLAlchemy()

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    website = db.Column(db.String(120))

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.update(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Venue {self.id}>'

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'genres': json.loads(self.genres),
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'phone': self.phone,
            'image_link': self.image_link,
            'website': self.website,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
            'facebook_link': self.facebook_link
        }

    @property
    def serialize_with_upcoming_shows_count(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'facebook_link': self.facebook_link,
            'address': self.address,
            'image_link': self.image_link,
            'website': self.website,
            'seeking_description': self.seeking_description,
            'seeking_talent': self.seeking_talent,
            'num_shows': Show.query.filter(
                Show.start_time > datetime.datetime.now(),
                Show.venue_id == self.id
            )
        }

    @property
    def serialize_with_shows_details(self):
        return {
            'id': self.id,
            'name': self.name,
            'state': self.state,
            'city': self.city,
            'address': self.address,
            'phone': self.phone,
            'facebook_link': self.facebook_link,
            'image_link': self.image_link,
            'seeking_description': self.seeking_description,
            'seeking_talent': self.seeking_talent,
            'genres': json.loads(self.genres),
            'website': self.website,
            'upcoming_shows': [
                show.serialize_with_artist_venue for show in Show.query.filter(
                    Show.start_time > datetime.datetime.now(),
                    Show.venue_id == self.id
                ).all()
            ],
            'past_shows': [
                show.serialize_with_artist_venue for show in Show.query.filter(
                    Show.start_time < datetime.datetime.now(),
                    Show.venue_id == self.id
                ).all()
            ],
            'upcoming_shows_count': len(
                Show.query.filter(
                    Show.start_time > datetime.datetime.now(),
                    Show.venue_id == self.id
                ).all()
            ),
            'past_shows_count': len(
                Show.query.filter(
                    Show.start_time < datetime.datetime.now(),
                    Show.venue_id == self.id
                ).all()
            )
        }

    @property
    def filter_on_city_state(self):
        return {
            'city': self.city,
            'state': self.state,
            'venues': [
                v.serialize_with_upcoming_shows_count
                for v in Venue.query.filter(
                    Venue.city == self.city, Venue.state == self.state
                ).all()
            ]
        }


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    facebook_link = db.Column(db.String(120))
    seeking_description = db.Column(db.String(500))


    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.update(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Artist {self.id}>'

    @property
    def serialize_with_shows_details(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'genres': json.loads(self.genres),
            'phone': self.phone,
            'facebook_link': self.facebook_link,
            'image_link': self.image_link,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'website': self.website,
            'upcoming_shows': [
                show.serialize_with_artist_venue for show in Show.query.filter(
                    Show.start_time > datetime.datetime.now(),
                    Show.artist_id == self.id
                ).all()
            ],
            'past_shows': [
                show.serialize_with_artist_venue for show in Show.query.filter(
                    Show.start_time < datetime.datetime.now(),
                    Show.artist_id == self.id
                ).all()
            ],
            'upcoming_shows_count': len(
                Show.query.filter(
                    Show.start_time > datetime.datetime.now(),
                    Show.artist_id == self.id
                ).all()
            ),
            'past_shows_count': len(
                Show.query.filter(
                    Show.start_time < datetime.datetime.now(),
                    Show.artist_id == self.id
                ).all()
            )
        }

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'image_link': self.image_link,
            'genres': json.loads(self.genres),
            'seeking_venue': self.seeking_venue,
            'facebook_link': self.facebook_link,
        }


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime())
    venue_id = db.Column(
        db.Integer, db.ForeignKey('Venue.id'),
        nullable=False
    )
    venue = db.relationship(
        'Venue', backref=db.backref('shows', cascade='all, delete')
    )
    artist_id = db.Column(
        db.Integer,
        db.ForeignKey('Artist.id'),
        nullable=False
    )
    artist = db.relationship(
        'Artist', backref=db.backref('shows', cascade='all, delete')
    )

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.update(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Show {self.id}>'

    @property
    def serialize(self):
        return {
            'id': self.id,
            'start_time': self.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
            'artist_id': self.artist_id,
            'venue_id': self.venue_id
        }

    @property
    def serialize_with_artist_venue(self):
        return {
            'id': self.id,
            'venue': [v.serialize for v in Venue.query.filter(Venue.id == self.venue_id).all()][0],
            'artist': [a.serialize for a in Artist.query.filter(Artist.id == self.artist_id).all()][0],
            'start_time': self.start_time.strftime("%m/%d/%Y, %H:%M:%S")
        }