import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


from models import setup_db, Movie, Actor, db
from auth.auth import AuthError, requires_auth

migrate = Migrate()



def create_app(test_config=None):
    # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  migrate.init_app(app, db)
  CORS(app)
  @app.after_request
  def after_request(response):
      response.headers.add(
          "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
      )
      response.headers.add(
          "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
      )
      return response

  @app.route('/movies', methods=['GET'])
  @requires_auth(permission='get:movies')
  def get_movies(payload):
    try:
      movies = Movie.query.all()

      if len(movies) == 0:
        abort(404)

      return jsonify({'success': True, 'movies': [movie.format() for movie in movies]})
    
    except Exception as e:
      print(e)
      abort(422)
    


  @app.route('/movies', methods=['POST'])
  @requires_auth(permission='post:movies')
  def create_movie(payload):
    body = request.get_json()

    new_title = body.get('title', None)
    new_release_date = body.get('release_date', None)

    if (new_title is None) or (new_release_date is None):
      abort(422)

    try:
      movie = Movie(title=new_title, release_date=new_release_date)
      movie.insert()

      return jsonify({'success': True, 'movie': movie.format()})
    
    except Exception as e:
      print(e)
      abort(422)

  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth(permission='delete:movies')
  def delete_movie(payload, movie_id):
    try:
      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
      
      if movie is None:
        abort(404)
      
      movie.delete()
      return jsonify({'success': True, 'deleted': movie.id})

    except Exception as e:
      print(e)
      abort(422)

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth(permission='patch:movies')
  def update_movie(payload, movie_id):
    body = request.get_json()

    new_title = body.get('title', None)
    new_release_date = body.get('release_date', None)

    try:
      if (new_title is None) and (new_release_date is None):
        abort(422)

      movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

      if not movie:
        abort(404)
    
      if new_title is not None:
        movie.title = new_title
      if new_release_date is not None:
        movie.release_date = new_release_date

      movie.update()

      return jsonify({'success': True, 'movie': movie.format()})

    except Exception as e:
      print(e)
      abort(422)


  @app.route('/actors', methods=['GET'])
  @requires_auth(permission='get:actors')
  def get_actors(payload):
    try:
      actors = Actor.query.all()
      
      if not actors:
        print(f'actors: {actors}')
        abort(404)

      return jsonify({'success': True, 'actors': [actor.format() for actor in actors]})

    except Exception as e:
      print(e)
      abort(404)

  @app.route('/actors', methods=['POST'])
  @requires_auth(permission='post:actors')
  def create_actor(payload):
    body = request.get_json()

    new_name = body.get('name', None)
    new_age = body.get('age', None)
    new_gender = body.get('gender', None)

    if (new_name is None) or (new_age is None) or (new_gender is None):
      abort(422)

    try:
      actor = Actor(name=new_name, age=new_age, gender=new_gender)
      actor.insert()

      return jsonify({'success': True, 'actor': actor.format()})
    
    except Exception as e:
      print(e)
      abort(422)



  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth(permission='delete:actors')
  def delete_actor(payload, actor_id):
    try:
      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
      
      if actor is None:
        abort(404)
      
      actor.delete()
      return jsonify({'success': True, 'deleted': actor.id})

    except Exception as e:
      print(e)
      abort(422)

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth(permission='patch:actors')
  def update_actor(payload, actor_id):
    body = request.get_json()

    new_name = body.get('name', None)
    new_age = body.get('age', None)
    new_gender = body.get('gender', None)

    

    try:
      if (new_name is None) or (new_age is None) or (new_gender is None):
        abort(422)

      actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

      if not actor:
        abort(404)
    
      if new_name is not None:
        actor.title = new_name
      if new_age is not None:
        actor.age = new_age
      if new_gender is not None:
        actor.gender = new_gender

      actor.update()

      return jsonify({'success': True, 'actor': actor.format()})

    except Exception as e:
      print(e)
      abort(422)


  # Error Handling

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({"success": False, "error": 422, "message": "Unprocessable"}), 422


  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({"success": False, "error": 400, "message": "Bad Request"}), 400


  @app.errorhandler(401)
  def unauthorized(error):
      print(error)
      return jsonify({"success": False, "error": 401, "message": "Unathorized"}), 401


  @app.errorhandler(405)
  def method_not_allowed(error):
      print(error)
      return (
          jsonify({"success": False, "error": 405, "message": "Method Not Allowed"}),
          405,
      )


  @app.errorhandler(500)
  def internal_server_error(error):
      print(error)
      return (
          jsonify({"success": False, "error": 500, "message": "Internal Server Error"}),
          500,
      )


  @app.errorhandler(404)
  def not_found(error):
      return (
          jsonify({"success": False, "error": 404, "message": "Resource Not Found"}),
          404,
      )


  @app.errorhandler(AuthError)
  def auth_error(error):
      print(error)
      return (
          jsonify(
              {
                  "success": False,
                  "error": error.status_code,
                  "message": error.error["description"],
              }
          ),
          error.status_code,
      )


  return app


app = create_app()

if __name__ == "__main__":
    app.run()