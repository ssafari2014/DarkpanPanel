from fastapi import FastAPI
import mysql.connector
from fastapi.openapi.models import Response  # dict converted response:Response
from pydantic import BaseModel

mydb = mysql.connector.connect(host="localhost", user="root", password="", database="python")

my_cursor = mydb.cursor()
app = FastAPI()

# movies = [{'title': '', 'year': ''},
#           {'title': 'batman', 'year': 2021},
#           {'title': 'joker', 'year': 2022},
#           {'title': 'Jailbreak', 'year': 2023},
#           {'title': 'Vikings', 'year': 2008},
#           {'title': 'Game of Thrones', 'year': 2016},
#           {'title': 'test', 'year': 2000},
#           ]


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


# get all movies
@app.get("/movies")
def get_movies(response: Response):
    sql = "SELECT * FROM movies"
    my_cursor.execute(sql)
    movies = my_cursor.fetchall()
    # return movies
    return response.status_code


# get single movie

@app.get("/movie/{movie_id}")
def get_movie(movie_id: int):
    sql = "SELECT * FROM movies WHERE id = %s "
    val = (movie_id,)
    my_cursor.execute(sql, val)
    movie = my_cursor.fetchall()
    return movie[0]


@app.delete("/movie/{movie_id}")
def delete_movie(movie_id: int):
    sql = "DELETE FROM movies WHERE id = %s"
    val = (movie_id,)
    my_cursor.execute(sql, val)
    mydb.commit()
    # movies.pop(movie_id)
    return {'message': 'movie has been deleted successfully'}


# create movie
@app.post("/create_movie")
def create_movie(movie: dict):
    sql = "INSERT INTO movies(title, year, storyline) VALUES (%s, %s, %s)"
    val = (movie['title'], movie['year'], movie['storyline'])
    my_cursor.execute(sql, val)
    mydb.commit()
    # movies.append(movie)
    # return {'message': 'yes'}
    return movie


# update movie
# @app.post("/update_movie")
# def update_movie(movie_id: int, movie: dict):
#     sql = "UPDATE movies SET title = %s , year = %s, storyline = %s WHERE id = %s"
#     val = (movie['title'], movie['year'], movie['storyline'], movie_id)
#     my_cursor.execute(sql, val)
#     mydb.commit()
#     return movie
    # movie_to_be_updated = movies[movie_id]  # get movie to update
    # movie_to_be_updated['title'] = movie['title']  # update title
    # movie_to_be_updated['year'] = movie['year']  # update year
    # movies[movie_id] = movie_to_be_updated  # has been_updated successfully
    # return movie_to_be_updated
@app.post("/update_movie")
def update_movie(movie: dict):
    sql = "UPDATE movies SET title = %s , year = %s, storyline = %s WHERE id = %s"
    val = (movie['title'], movie['year'], movie['storyline'], movie['id'])
    my_cursor.execute(sql, val)
    mydb.commit()
    return movie