import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor


class CapstoneTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variable and initialize app"""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ.get('TEST_DATABASE_URI')
        setup_db(self.app, self.database_path)

        self.new_movie = {
        "title": "movie_test",
        "release_date": "1/21/1999"
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

    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()