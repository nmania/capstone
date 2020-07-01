import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor

# Tokens are formatted as such to limit lenght on a line
CASTING_ASSISTANT = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJkbXpZbGMyWTJlbVFHellkVXdrOCJ9.eyJpc3MiOiJodHRwczovL3pydXhpLWNhcHN0b25lLWZpbmFsLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWY5NjZiNWExNWI3YjAwMTM2MWFlMTMiLCJhdWQiOlsiY2FzdGluZyIsImh0dHBzOi8venJ1eGktY2Fwc3RvbmUtZmluYWwudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5MzQwMzUwMiwiZXhwIjoxNTkzNDg5OTAyLCJhenAiOiJKUmljM05GQjY2RjFrdG42NHdQamVnNVRJMTFqZTJrVSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJyZWFkOmFjdG9ycyIsInJlYWQ6bW92aWVzIl19.mq55QS9sgRvmBRswP4MKXh1p85dHU-6GUtBIBUCbHEGM7gl-iGBbvVXVbs6-a_o0nsPvWhC0sFHpm6nL7GBC39f3Qxdc-o4xVhKjSDkqHTBYJp7t9q45kp1ZvVeCMGMbF4a7cDTNtZAOcipIWo5QbhbR8UGPoxhNUkHS1EaEcyWkRl-0D0YJ-fZnF-rVgwcImM0TsIXhGrdNnobhFdd6VLZfs_PABE0qXWkyz6CxcfHJjEY4aFSlO6Eh-mWFMKYO4EAby0xjQLapNTG4ng9dzQ_mzeVxTrOd9G8ySaC-IcefQ_D4Eb1kbkkolP8a3IVvQQ9sjlVXLyNA-Lrdcq0OIQ')
CASTING_DIRECTOR = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNva1hNOFJVX05xWExzUjRqNTlzUiJ9.eyJpc3MiOiJodHRwczovL3VkYWNpdHktc2hvcC5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWVjNGZkZmM0MWI0YWIwYzZjOTJjNGFhIiwiYXVkIjpbImFnZW5jeSIsImh0dHBzOi8vdWRhY2l0eS1zaG9wLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE1ODk5ODY1NzEsImV4cCI6MTU5MDA3Mjk3MSwiYXpwIjoiZUg5QXBvRVZsaVliZ3pOWlVWN2ZnNXNOc3dwZDdxcXMiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.Vs4Uu6ADbqWJawK-8gb--IbDFyWAiBaWPWcF4VDykgmW1bYgx5XcHgPcUqHNrpp5RS8O9aHXugRTWb9qT0jSsnES7yAHFZ-N0Jspgn9UTgdkiXeMA3M7aWfgxsNll_yTWwN980yqQ0SFFSwM3qRxmpWGRKLsAFpHHzc6ZxeSld9FA2vZz3q5b8ln3izm-y2zJeaJJhMY4xg8JN9YEd8TZmhhbwDe1UwjW0pF7l0NgzmIMvNxRUKwppqETwXm0grSwTo-lMyPU5iWoQxaSna_vxO_8NNC7H_sX0tWxisQLV3vQcAgMwwH6Amwcbp4IGPzsrcQpoaH1kx3EI7c3ikzqA')  # noqa
EXECUTIVE_PRODUCER = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjJkbXpZbGMyWTJlbVFHellkVXdrOCJ9.eyJpc3MiOiJodHRwczovL3pydXhpLWNhcHN0b25lLWZpbmFsLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWZhODQ0Y2ZkMzBlMjAwMTM2NjA1MGIiLCJhdWQiOlsiY2FzdGluZyIsImh0dHBzOi8venJ1eGktY2Fwc3RvbmUtZmluYWwudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTU5MzQ3NjM2MCwiZXhwIjoxNTkzNTYyNzYwLCJhenAiOiJKUmljM05GQjY2RjFrdG42NHdQamVnNVRJMTFqZTJrVSIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6W119.C4xf9IZyWu4_tIsKj9sFpDIWpbdXY7kqO9kV_1vP1mvBsKGc343qYGn1Fn2LMSpFxOjX3c-SJZCFwG36le5AOHRehrtefegNBo3LUu3lgoyBakPK9wdE-uYJ2nszoD5v20XKQXyT8NCTkvIhigfptqitc3CPxhe9s_h0UpdCQudoF_u0zp76-hbGFt7dFYcuiShLFKLeZy0z9hO0tViZKmL09mRwTwo9AxRiokrVX82wcN91FsGPsgXC8JYd1oCqsW1J_yeVdcpP4l_bRO2Ga4sIedNNkptChVrkuzxxNILJvCFOZeddJCQC6_QhMpY5Noo4-dDXxenlHlX91XESMg')

class CastingAgencyTest(unittest.TestCase):
    """Setup test suite for the routes"""

    def setUp(self):
        """Setup application """
        self.app = create_app()
        self.client = self.app.test_client
        self.test_movie = {
            'title': 'Kungfu Masters',
            'release_date': '2020-05-06',
        }
        self.database_path = os.environ['DATABASE_URL']

        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after each test"""
        pass

    #  Tests that you can get all movies
    def test_get_all_movies(self):
        response = self.client().get(
            '/movies',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # Test to get a specific movie
    def test_get_movie_by_id(self):
        response = self.client().get(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Terminator Dark Fate')

    # tests for an invalid id to get a specific movie
    def test_404_get_movie_by_id(self):
        response = self.client().get(
            '/movies/100',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Test to create a movie
    def test_post_movie(self):
        response = self.client().post(
            '/movies',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Kungfu Masters')
        self.assertEqual(
            data['movie']['release_date'],
            'Wed, 06 May 2020 00:00:00 GMT'
        )

    # Test to create a movie if no data is sent
    def test_400_post_movie(self):
        response = self.client().post(
            '/movies',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # tests RBAC for creating a movie
    def test_401_post_movie_unauthorized(self):
        response = self.client().post(
            '/movies',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # Test to Update a movie
    def test_patch_movie(self):
        response = self.client().patch(
            '/movies/1',
            json={'title': 'Revelations', 'release_date': "2019-11-12"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Revelations')
        self.assertEqual(
            data['movie']['release_date'],
            'Tue, 12 Nov 2019 00:00:00 GMT'
        )

    # Test that 400 is returned if no data is sent to update a movie
    def test_400_patch_movie(self):
        response = self.client().patch(
            '/movies/1',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # tests RBAC for updating a movie
    def test_401_patch_movie_unauthorized(self):
        response = self.client().patch(
            '/movies/1',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # tests that 404 is returned for an invalid id to get a specific movie
    def test_404_patch_movie(self):
        response = self.client().patch(
            '/movies/12323',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # tests to delete a movie
    def test_delete_movie(self):
        response = self.client().delete(
            '/movies/2',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    # tests RBAC for deleting a movie
    def test_401_delete_movie(self):
        response = self.client().delete(
            '/movies/2',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # tests for an invalid id to delete a specific movie
    def test_404_delete_movie(self):
        response = self.client().delete(
            '/movies/22321',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    #  Tests that you can get all actors
    def test_get_all_actors(self):
        response = self.client().get(
            '/actors',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # Test to get a specific actor
    def test_get_actor_by_id(self):
        response = self.client().get(
            '/actors/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], 'Will Smith')

    # tests for an invalid id to get a specific actor
    def test_404_get_actor_by_id(self):
        response = self.client().get(
            '/actors/100',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Test to create an actor
    def test_post_actor(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Karl', 'age': 20, "gender": "male"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'Karl')
        self.assertEqual(data['actor']['age'], 20)
        self.assertEqual(data['actor']['gender'], 'male')

    # Test to create an actor if no data is sent
    def test_400_post_actor(self):
        response = self.client().post(
            '/actors',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # tests RBAC for creating an actor
    def test_401_post_actor_unauthorized(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Mary', 'age': 22, "gender": "female"},
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # Test to Update an actor
    def test_patch_actor(self):
        response = self.client().patch(
            '/actors/1',
            json={'name': 'Mariam', 'age': 25, "gender": "female"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'Mariam')
        self.assertEqual(data['actor']['age'], 25)
        self.assertEqual(data['actor']['gender'], 'female')

    # Test that 400 is returned if no data is sent to update an actor
    def test_400_patch_actor(self):
        response = self.client().patch(
            '/actors/1',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # tests RBAC for updating an actor
    def test_401_patch_actor_unauthorized(self):
        response = self.client().patch(
            '/actors/1',
            json={'name': 'John', 'age': 25, "gender": "male"},
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # tests that 404 is returned for an invalid id to get a specific actor
    def test_404_patch_actor(self):
        response = self.client().patch(
            '/actor/12323',
            json={'name': 'Johnathan', 'age': 25, "gender": "male"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # tests to delete an actor
    def test_delete_actor(self):
        response = self.client().delete(
            '/actors/2',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    # tests RBAC for deleting an actor
    def test_401_delete_actor(self):
        response = self.client().delete(
            '/actors/2',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # tests for an invalid id to get a specific actor
    def test_404_delete_actor(self):
        response = self.client().delete(
            '/actors/22321',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')


# Make the tests executable
if __name__ == "__main__":
    unittest.main()
