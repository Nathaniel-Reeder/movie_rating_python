'''Script to seed the database.'''

import os 
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system('dropdb ratings')
os.system('createdb ratings')

model.connect_to_db(server.app)
model.db.create_all()

with open('data/movies.json') as f:
    movie_data = json.loads(f.read())
    # Create movies, store them in list so we can use them
    # to create fake ratings later
    
    movies_in_db = []
    
    for movie in movie_data:
        title_to_add = movie['title']
        overview_to_add = movie['overview']
        poster_to_add = movie['poster_path']
        # get the release date as a string
        release_date_str = movie['release_date']
        # convert release date to datetime object
        release_date_to_add = datetime.strptime(release_date_str, '%Y-%m-%d')
        
        new_movie = crud.create_movie(title_to_add, overview_to_add, release_date_to_add, poster_to_add)
        movies_in_db.append(new_movie)

model.db.session.add_all(movies_in_db)
model.db.session.commit()

for n in range(10):
    email = f'user{n}@test.com'
    password = 'test'
    # Create a user with the generated info
    user = crud.create_user(email, password)
    model.db.session.add(user)
    
    # Create 10 random ratings for the test user
    for i in range(10):
        #Get a random movie using choice on the list saved when we seed the movie table
        random_movie = choice(movies_in_db)
        #Get a random score between 1 and 5
        score = randint(1, 5)
        
        #Create the rating with the generated info
        rating = crud.create_rating(user, random_movie, score)
        model.db.session.add(rating)
        
model.db.session.commit()