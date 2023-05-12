'''CRUD operations'''
from model import db, User, Movie, Rating, connect_to_db

# User functions

def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def get_all_users():
    '''Return all users in the database.'''
    return User.query.all()

def get_user_by_id(user_id):
    '''Return the user with the id given in the parameter'''
    return User.query.get(user_id)

def get_user_by_email(email):
    '''Return the user with the email given in the parameter'''
    return User.query.filter(User.email == email).first()


# Movie functions
def create_movie(title, overview, release_date, poster_path):
    '''Create and return a new movie.'''
    
    movie = Movie(title=title, overview=overview, release_date=release_date, poster_path=poster_path)
    
    return movie

def get_all_movies():
    '''Return all movies in the database'''
    return Movie.query.all()

def get_movie_by_id(movie_id):
    '''Return a movie with the id given in the parameter'''
    return Movie.query.get(movie_id)


# Rating functions
def create_rating(user, movie, score):
    '''Create and return a new rating'''
    rating = Rating(user=user, movie=movie, score=score)
    return rating



if __name__ == '__main__':
    from server import app
    connect_to_db(app)