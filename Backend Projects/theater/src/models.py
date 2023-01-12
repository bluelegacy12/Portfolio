import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Performers(db.Model):
    __tablename__ = 'performers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    phone = db.Column(db.String(10), unique=True, nullable=False)

    def __init__(self, name: str, phone: str, email: str):
        self.name = name
        self.phone = phone
        self.email = email

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email
        }


class Shows(db.Model):
    __tablename__ = 'shows'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    rehearsal_start = db.Column(db.Date, unique=False, nullable=False)
    show_open = db.Column(db.Date, unique=False, nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey(
        'performers.id'), nullable=False)

    def __init__(self, title: str, rehearsal_start: datetime, show_open: datetime, director_id: int):
        self.title = title
        self.rehearsal_start = rehearsal_start
        self.show_open = show_open
        self.director_id = director_id

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'rehearsal_start': self.rehearsal_start,
            'show_open': self.show_open,
            'director_id': self.director_id
        }


class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=False, nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable=False)
    performer_id = db.Column(db.Integer, db.ForeignKey(
        'performers.id'), nullable=False)


class Scenes(db.Model):
    __tablename__ = 'scenes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    scene_name = db.Column(db.String(128), unique=True, nullable=False)
    show_id = db.Column(db.Integer, db.ForeignKey('shows.id'), nullable=False)


class RehearsalVenues(db.Model):
    __tablename__ = 'rehearsal_venues'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    location = db.Column(db.String(128), unique=True, nullable=False)


class Conflicts(db.Model):
    __tablename__ = 'conflicts'
    date_time = db.Column(db.DateTime, primary_key=True,
                          autoincrement=False, nullable=False, unique=True)


performers_conflicts = db.Table(
    'performers_conflicts',
    db.Column(
        'performer_id', db.Integer,
        db.ForeignKey('performers.id'),
        primary_key=True
    ),

    db.Column(
        'conflict_date', db.DateTime,
        db.ForeignKey('conflicts.date_time'),
        primary_key=True
    )
)

scenes_roles = db.Table(
    'scenes_roles',
    db.Column(
        'scene_id', db.Integer,
        db.ForeignKey('scenes.id'),
        primary_key=True
    ),

    db.Column(
        'role_id', db.Integer,
        db.ForeignKey('roles.id'),
        primary_key=True
    )
)

shows_venues = db.Table(
    'shows_venues',
    db.Column(
        'show_id', db.Integer,
        db.ForeignKey('shows.id'),
        primary_key=True
    ),

    db.Column(
        'venue_id', db.Integer,
        db.ForeignKey('rehearsal_venues.id'),
        primary_key=True
    )
)
