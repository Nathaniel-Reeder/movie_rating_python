"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key ='dev'
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def home():
    '''View homepage'''
    
    return render_template('homepage.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = crud.get_user_by_email(email)
    
    if user.password == password:
        session['user_id'] = user.id
        flash('Logged in!')
        return redirect('/')
    else:
        flash('Sorry, there was a problem logging you in.')
        return redirect('/')

@app.route('/movies')
def all_movies():
    '''View all movies.'''
    movies = crud.get_all_movies()
    
    return render_template('all_movies.html', movies=movies)

@app.route('/movies/<movie_id>')
def show_movie(movie_id):
    '''Show a specific movie's details'''
    movie = crud.get_movie_by_id(movie_id)
    
    return render_template('movie_details.html', movie=movie)

@app.route('/users')
def all_users():
    '''View all users.'''
    users = crud.get_all_users()
    
    return render_template('all_users.html', users=users)

@app.route('/users', methods=['POST'])
def register_user():
    '''Create a new user'''
    
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = crud.get_user_by_email(email)
    
    if user:
        flash('Cannot create an account with that email. Please try again.')
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash('Account Created! Please log in.')
    
    return redirect('/')

@app.route('/users/<user_id>')
def show_user(user_id):
    '''Show a user profile'''
    user = crud.get_user_by_id(user_id)
    
    return render_template('user_profile.html', user=user)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
