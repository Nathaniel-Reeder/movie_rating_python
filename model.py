"""Models for movie ratings app."""

from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()


class User(db.Model):
    '''A user'''
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String)
    
    #ratings = a list of Rating objects
    
    def __repr__(self):
        return f'<User user_id={self.id} email={self.email}>'
    
class Movie(db.Model):
    '''A movie'''
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String)
    overview = db.Column(db.Text)
    release_date = db.Column(db.DateTime)
    poster_path = db.Column(db.String)
    
    #ratings = a list of Rating objects
    
    def __repr__(self):
        return f'<Movie movie_id={self.id} title={self.title}>'

class Rating(db.Model):
    '''A rating'''
    __tablename__ = 'ratings'
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    score = db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    movie = db.relationship("Movie", backref='ratings')
    user = db.relationship("User", backref='ratings')
    
    def __repr__(self):
        return f"<Rating rating_id={self.id} score={self.score}>"

def connect_to_db(flask_app, echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['POSTGRES_URI']
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
