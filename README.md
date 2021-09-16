
# Casting Agency API Backend


## Casting Agency Specifications

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Motivation for project
 Udacity capstone project to demonstrate skills learned within the course on fullstack development. Mainly over using Flask, Auth0, SQLAlchemy, Databases, unit testing, REST, and deploying application to heroku,

## Getting Started

  

### Installing Dependencies for the Backend

  

1.  **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

  

2.  **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

  

3.  **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

  

```bash

pip install -r requirements.txt

```

  

This will install all of the required packages we selected within the `requirements.txt` file.

  

4.  **Key Dependencies**

  

-  [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

  

-  [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

  

-  [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

  

### Database Setup

  

With Postgres running, restore a database using the capstone_test.psql file provided. From the backend folder in terminal run:

  

```bash

psql capstone_test<capstone_test.psql

```

[How to backup psql database in Windows 10](https://sqlbackupandftp.com/blog/how-to-backup-and-restore-postgresql-database)

  

### Running the server

  

From within the root directory first ensure you are working using your created virtual environment.

  

To run the server, execute:

  

```bash
. ./setup.sh
flask run

```

  

## Testing

  

To run the tests, run the below within the root directory

  

```

dropdb capstone_test

createdb capstone_test

psql capstone_test< capstone_test.psql

python test_app.py

```

If 401 Token expired error encountered, then user should try requesting a new JWT token using the auth0 login endpoint below and update the JWT's within the setup.sh and re-run that file. You will need to grab the JWT from the URL where you see `access_token=` after logging in with one of the account credentials below .

 ### Credentials & RBAC access rules
 - Casting Assistant
    -   Can view actors and movies
-   Casting Director
    -   All permissions a Casting Assistant has and…
    -   Add or delete an actor from the database
    -   Modify actors or movies
-   Executive Producer
    -   All permissions a Casting Director has and…
    -   Add or delete a movie from the database
  
 
- assistant@test.com - auth0password!
- director@test.com - auth0password!
- producer@test.com - auth0password!

[auth0 Login endpoint](https://fsndms.us.auth0.com/authorize?audience=capstone&response_type=token&client_id=6XMKvEw7sGBtved4afQaEXZUJ0M9WvtG&redirect_uri=http://localhost:8080/login-results)

## Project hosted at
  https://mscapstone.herokuapp.com/

You can use the provided postman collection to test the API routes and update the bearer token there for each endpoint depending on what the user wants to accomplish.

## API Reference

  

### Getting Started


### Error Handling

  

Errors are returned as JSON objects in the following format:

  

```

{

"success": False,

"error": 400,

"message": "bad request"

}

```
  

### Endpoints

  

#### GET /movies

  

- General:

	- Returns a list of  movies

- Sample: `curl http://127.0.0.1:5000/movies`

  

```

{

"movies": [

	{

		"id": 3,

		"release_date": "Thu, 21 Jan 2100 00:00:00 GMT",

		"title": "movie_producer_1"

	},

	{

		"id": 1,

		"release_date": "Mon, 25 Jan 1999 00:00:00 GMT",

		"title": "movie_1_patched_local"

	}

	],

		"success": true

	}

```

 
  

### DELETE /movies/{movie_id}

  

- General:

	- Deletes the movie of the given ID if it exists.

	- Returns the id of the deleted movie and success value

- Sample: `curl http://127.0.0.1:5000/movies/2 -X DELETE`

  

```

{

	"deleted": 2,

	"success": true

}

```

  

### POST /movies

  

- General:

	- Creates a new movie using the submitted title and release date

	- Returns success value and newly inserted movie

- Sample (If on windows): `curl http://127.0.0.1:5000/movies-X POST -H "Content-Type: application/json" -d "{ \"title\": \"test_movie\", \"release_date\": \"1/21/2100\"}"`

  

- Sample: `curl http://127.0.0.1:5000/movies-X POST -H "Content-Type: application/json" -d '{ "title": "test_movie", "release_date": "1/21/2100"}"'`

  

```

{

	"movie": {

		"id": 3,

		"release_date": "Thu, 21 Jan 2100 00:00:00 GMT",

		"title": "test_movie"

		},

	"success": true

}

```

### PATCH /movies/{movie_id}

  

- General:

	- Modify's the movie of the given ID if it exists.

	- Returns the modified movie and success value

- Sample (If on windows): `curl http://127.0.0.1:5000/movies/1 -X PATCH -H "Content-Type: application/json" -d "{ \"title\": \"movie_1_patched_local\", \"release_date\": \"1/25/1999\"}"`

  

- Sample: `curl http://127.0.0.1:5000/movies/1 -X PATCH -H "Content-Type: application/json" -d '{ "title": "movie_1_patched_local", "release_date": "1/25/1999"}"'`

```

{

	"movie": {

		"id": 1,

		"release_date": "Mon, 25 Jan 1999 00:00:00 GMT",

		"title": "movie_1_patched_local"

	},

	"success": true

}

```


### GET /actors

  

- General:
	
	- Returns a list of questions and list of actors

- Sample: `curl http://127.0.0.1:5000/actors`

  

```

{

"actors": [

	{

		"age": 27,

		"gender": "F",

		"id": 1,

		"name": "actor_producer_2"

	},

	{

		"age": 28,

		"gender": "F",

		"id": 3,

		"name": "patched_@"

	},

	{

		"age": 28,

		"gender": "M",

		"id": 4,

		"name": "actor_producer"

	}

	],

		"success": true

	}

```

### DELETE /actors/{actor_id}

  

- General:

	- Deletes the actor of the given ID if it exists.

	- Returns the id of the deleted actor and success value

- Sample: `curl http://127.0.0.1:5000/actor/2 -X DELETE`

  

```

{

	"deleted": 2,

	"success": true

}

```

  

### POST /actors

  

- General:

	- Creates a new actor using the submitted name, age, and gender

	- Returns success value and newly inserted actor

- Sample (If on windows): `curl http://127.0.0.1:5000/actors-X POST -H "Content-Type: application/json" -d "{ \"name\": \"actor_producer\", \"age\": \"28\", \"gender\": \"M\"}"`

  

- Sample: `curl http://127.0.0.1:5000/actors-X POST -H "Content-Type: application/json" -d '{ "name": "actor_producer", "age":"28", "gender": "M" }"'`

  

```

{

	"actor": {

		"age": 28,

		"gender": "M",

		"id": 4,

		"name": "actor_producer"

	},

	"success": true

}

```

### PATCH /actors/{actor_id}

  

- General:

	- Modify's the actor of the given ID if it exists.

	- Returns the modified actor and success value

- Sample (If on windows): `curl http://127.0.0.1:5000/actors/3 -X POST -H "Content-Type: application/json" -d "{ \"name\": \"patched_actor\", \"age\": \"28\", \"gender\": \"F\"}"`

  

- Sample: `curl http://127.0.0.1:5000/actors/3 -X POST -H "Content-Type: application/json" -d '{ "name": "patched_actor", "age":"28", "gender": "F" }"'`

```

{

	"actor": {

		"age": 28,

		"gender": "F",

		"id": 3,

		"name": "patched_actor"

	},

	"success": true

}

```
