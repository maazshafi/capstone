import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

# JWT Tokens for each role
ASSISTANT_TOKEN = os.getenv('ASSISTANT_TOKEN')
DIRECTOR_TOKEN = os.getenv('DIRECTOR_TOKEN')
PRODUCER_TOKEN = os.getenv('PRODUCER_TOKEN')


class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variable and initialize app"""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ.get('TEST_DATABASE_URI')
        setup_db(self.app, self.database_path)

        self.casting_assistant = ASSISTANT_TOKEN
        self.casting_director = DIRECTOR_TOKEN
        self.executive_producer = PRODUCER_TOKEN

        self.new_movie = {
        "title": "movie_unit_test",
        "release_date": "1/22/1990"
        }

        self.invalid_new_movie = {
        "title": "movie_unit_test_fail"
        }

        self.invalid_movie = {
            "title": "movie_test"
        }

        self.new_actor = {
        "name": "actor_test",
        "age": "25",
        "gender": "F"
        }

        # bindss the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass


    """
    Tests
    """

    # GET /movies endpoint
    # testing casting assistant test 1
    def test_get_movies(self):
        res = self.client().get('/movies', headers={"Authorization": f"Bearer {self.casting_assistant}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # no bearer
    def test_401_get_movies_fail(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unathorized')

    # POST /movies
    def test_post_movies(self):
        res = self.client().post('/movies', headers={"Authorization": f"Bearer {self.executive_producer}"}, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_403_post_movies_fail(self):
        res = self.client().post('/movies', headers={"Authorization": f"Bearer {self.casting_assistant}"}, json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    
    def test_422_post_movies_fail(self):
        res = self.client().post('/movies', headers={"Authorization": f"Bearer {self.executive_producer}"}, json=self.invalid_new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    # DELETE /movies
    def test_delete_movies(self):
        # inject new test movie value to db
        test_movie = Movie(title='Test_for_delete', release_date='2/22/1990')
        test_movie.insert()

        movie_id = test_movie.id

        res = self.client().delete(f'/movies/{movie_id}', headers={"Authorization": f"Bearer {self.executive_producer}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], movie_id)

    def test_422_delete_movies_fail(self):
        movie_id = 99999999

        res = self.client().delete(f'/movies/{movie_id}', headers={"Authorization": f"Bearer {self.executive_producer}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    # PATCH /movies
    def test_patch_movies(self):
        # inject new test movie value to db
        test_movie = Movie(title='Test_for_patch', release_date='3/22/1990')
        test_movie.insert()

        movie_id = test_movie.id

        modified_test_movie = {
        "title": "Test_for_patch_updated",
        "release_date": "4/22/1990"
        }

        res = self.client().patch(f'/movies/{movie_id}', headers={"Authorization": f"Bearer {self.executive_producer}"}, json=modified_test_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    
    def test_422_patch_movies_fail(self):
        movie_id = 9999999

        modified_test_movie = {
        "title": "Test_for_patch_fail_updated",
        "release_date": "5/22/1990"
        }

        res = self.client().patch(f'/movies/{movie_id}', headers={"Authorization": f"Bearer {self.casting_director}"}, json=modified_test_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')


    # GET /actors endpoint
    def test_get_actors(self):
        res = self.client().get('/actors', headers={"Authorization": f"Bearer {self.casting_director}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_401_get_actors_fail(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unathorized')

    # POST /actors
    def test_post_actors(self):
        res = self.client().post('/actors', headers={"Authorization": f"Bearer {self.executive_producer}"}, json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_422_post_actors_fail(self):
        res = self.client().post('/actors', headers={"Authorization": f"Bearer {self.executive_producer}"}, json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    # DELETE /actors
    def test_delete_actor(self):
        # inject new test actor value to db
        test_actor = Actor(name='Test_delete_actor', age=21, gender='M')
        test_actor.insert()

        actor_id = test_actor.id

        res = self.client().delete(f'/actors/{actor_id}', headers={"Authorization": f"Bearer {self.executive_producer}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], actor_id)

    def test_422_delete_actor(self):
        actor_id = 999999

        res = self.client().delete(f'/actors/{actor_id}', headers={"Authorization": f"Bearer {self.executive_producer}"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    # PATCH /actors
    def test_patch_actors(self):
        # inject new test actor value to db
        test_actor = Actor(name='Test_patch_actor', age=21, gender='M')
        test_actor.insert()

        actor_id = test_actor.id

        modified_test_actor = {
        "name": "Test_patch_actor_updated",
        "age": "26",
        "gender": "F"
        }

        res = self.client().patch(f'/actors/{actor_id}', headers={"Authorization": f"Bearer {self.executive_producer}"}, json=modified_test_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_422_patch_actors_fail(self):
        actor_id = 99999

        modified_test_actor = {
        "name": "Test_patch_actor_updated",
        "age": "26",
        "gender": "F"
        }

        res = self.client().patch(f'/actors/{actor_id}', headers={"Authorization": f"Bearer {self.executive_producer}"}, json=modified_test_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Resource Not Found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()