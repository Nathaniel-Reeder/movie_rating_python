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
    
    @classmethod
    def create(cls, email, password):
        '''Create and return a new user'''
        return cls(email=email, password=password)
    
    @classmethod
    def get_all(cls):
        '''Return all users in the database.'''
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, user_id):
        '''Return a user object with the ID given in the parmeter'''
        return cls.query.get(user_id)
    
    @classmethod
    def get_by_email(cls, email):
        '''Return a user object with the email given in the parameter'''
        return cls.query.filter(cls.email == email).first()
        
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
    
    @classmethod
    def create(cls, title, overview, release_date, poster_path):
        '''Create and return a new movie.'''
        return cls(title=title, overview=overview, release_date=release_date, poster_path=poster_path)
    
    @classmethod
    def get_all(cls):
        '''Return all movies in the database.'''
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, movie_id):
        '''Return a movie with a matching ID'''
        return cls.query.get(movie_id)

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
    
    @classmethod
    def create(cls, user, movie, score):
        return cls(user=user, movie=movie, score=score)
    
    @classmethod
    def get_all(cls):
        '''Return all ratings in the database.'''
        return cls.query.all()

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
