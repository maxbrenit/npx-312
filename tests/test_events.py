"""
File to handle testing of the created models
"""

import unittest
from flask import jsonify
import json

from app import create_app, db

class EventsTestCase(unittest.TestCase):
    """
    This class represents the events test case
    """

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client
        self.event = {'name': 'birthday', 'category': 'party', 'location': 'nairobi', 'date': '12/12/2018',\
        'description': 'Everyone is welcome'}
        self.user_data = {'username': "chrisevans", 'email': "test@example.com", 'password': "J@yd33n",
            'cpassword': "J@yd33n"}
        self.login_data = {'email': "test@example.com", 'password': "J@yd33n"}
        self.user_data2 = {'username': "brucebarner", 'email': "bruce@infinity.com",
            'password': "sTr0ng3st@venger", 'cpassword': "sTr0ng3st@venger"}
        self.login_data2 = {'email': "bruce@infinity.com", 'password': "sTr0ng3st@venger"
        }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def register_user(self, data):
        return self.client().post('api/v2/auth/register', data=json.dumps(data), content_type='application/json' )

    def login_user(self, data):
        return self.client().post('/api/v2/auth/login', data=json.dumps(data), content_type='application/json' )

    def get_token(self):
        """register and login a user to get an access token"""
        self.register_user(self.user_data)
        result = self.login_user(self.login_data)
        access_token = json.loads(result.data.decode())['access_token']
        return access_token

    def get_new_token(self):
        """register and login a user to get an access token"""
        self.register_user(self.user_data2)
        result = self.login_user(self.login_data2)
        access_token = json.loads(result.data.decode())['access_token']
        return access_token

    def test_event_creation(self):
        """
        Test if API can create an event (POST request)    
        """
        access_token = self.get_token()  

        result = self.client().post('/api/v2/events', headers=dict(Authorization=access_token),
        data=json.dumps(self.event), content_type='application/json' )
        self.assertEqual(result.status_code, 201)
        self.assertEqual(self.event['name'], 'birthday')

    def test_empty_event_fields(self):
        """
        Test empty event fields.
        """
        access_token = self.get_token()
        myevent = {'name': "", 'category': "", 'location': "", 'date': "",\
        'description': 'Everyone is welcome'}
        res = self.client().post('/api/v2/events', headers=dict(Authorization=access_token),
        data=json.dumps(myevent), content_type='application/json' )
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertIn('cannot be empty', result['message'])

    def test_special_characters_in_event_name(self):
        """
        Test special characters.
        """
        access_token = self.get_token()
        myevent = {'name': "@# ha&(", 'category': "Development", 'location': "Nairobi", 'date': "12/12/2018",\
        'description': 'Everyone is welcome'}
        res = self.client().post('/api/v2/events', headers=dict(Authorization=access_token),
        data=json.dumps(myevent), content_type='application/json' )
        self.assertEqual(res.status_code, 400)
        result = json.loads(res.data.decode())
        self.assertIn('Event name cannot have special', result['message'])

    def test_getting_user_events(self):
        """
        Test API can get Events belonging to a user (GET request).
        """
        access_token = self.get_token()
        # create an event by making a POST request
        self.client().post(
            '/api/v2/events',
            headers=dict(Authorization= access_token), 
            data=json.dumps(self.event), content_type='application/json')
        # get all the event that belong to the test user by making a GET request
        res = self.client().get(
            '/api/v2/events',
            headers=dict(Authorization= access_token))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.event['name'], 'birthday')

    def test_getting_all_events(self):
        """
        Test API can get all Events in the system (GET request).
        """
        access_token = self.get_token()
        # create an event by making a POST request
        self.client().post(
            '/api/v2/events',
            headers=dict(Authorization= access_token), 
            data=json.dumps(self.event), content_type='application/json')
        # get all the event that belong to the test user by making a GET request
        res = self.client().get(
            '/api/v2/events/all')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(self.event['name'], 'birthday')

    def test_get_event_by_id(self):
        """Test API can get a single event by using it's id."""
        access_token = self.get_token()
        # Create event
        req = self.client().post(
            '/api/v2/events',
            headers=dict(Authorization= access_token),
            data=json.dumps(self.event), content_type='application/json')
        # get the response data in json format
        results = json.loads(req.data.decode())

        result = self.client().get(
            '/api/v2/events/{}'.format(results['id']),
            headers=dict(Authorization= access_token))
        # assert that the event is actually returned given its ID
        self.assertEqual(result.status_code, 200)
        self.assertEqual(self.event['name'], 'birthday')

    def test_event_editing(self):
        """Test API can edit an existing event. (PUT request)"""
        access_token = self.get_token()
        # Create an event
        req = self.client().post(
            '/api/v2/events',
            headers=dict(Authorization= access_token),
            data=json.dumps(self.event), content_type='application/json')
        results = json.loads(req.data.decode())
        # Edit created event
        edit={"name": "Software", 'category' : 'Development', 'location' : 'Eldoret',
                'date' : '12/1/2019', 'description' : 'Prizes will be won'}
        req = self.client().put(
            '/api/v2/events/{}'.format(results['id']),
            headers=dict(Authorization= access_token),
            data=json.dumps(edit), content_type='application/json')
        self.assertEqual(req.status_code, 200)

        # Get the edited event
        results = self.client().get(
            '/api/v2/events/{}'.format(results['id']),
            headers=dict(Authorization= access_token))
        self.assertIn("Software", str(results.data))

    def test_deleting_of_existing_event(self):
        """Test User can only delete an existing event"""
        access_token = self.get_token()
        # Create event
        self.client().post(
            '/api/v2/events',
            headers=dict(Authorization= access_token),
            data=json.dumps(self.event), content_type='application/json')
        # Delete created event
        res = self.client().delete(
            '/api/v2/events/2',
            headers=dict(Authorization= access_token))
        self.assertEqual(res.status_code, 404)

    def test_deleting_of_event(self):
        """Test API can delete an existing Event. (DELETE request)."""
        access_token = self.get_token()
        # Create event
        req = self.client().post(
            '/api/v2/events',
            headers=dict(Authorization= access_token),
            data=json.dumps(self.event), content_type='application/json')
        results = json.loads(req.data.decode())
        # Delete created event
        res = self.client().delete(
            '/api/v2/events/{}'.format(results['id']),
            headers=dict(Authorization= access_token))
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get(
            '/api/v2/events/1',
            headers=dict(Authorization= access_token))
        self.assertEqual(result.status_code, 404)

    def test_deleting_of_own_event(self):
        """Test User can only delete their own events. (DELETE request)."""
        access_token = self.get_token()
        access_token2 = self.get_new_token()
        # Create event.
        req = self.client().post(
            '/api/v2/events',
            headers=dict(Authorization= access_token),
            data=json.dumps(self.event), content_type='application/json')
        results = json.loads(req.data.decode())
        # Delete created event
        res = self.client().delete(
            '/api/v2/events/{}'.format(results['id']),
            headers=dict(Authorization= access_token2))
        self.assertEqual(res.status_code, 401)
        # Test to see if it exists, should return a 200 (Event still exists)
        result = self.client().get(
            '/api/v2/events/1',
            headers=dict(Authorization= access_token2))
        self.assertEqual(result.status_code, 200)

    def tearDown(self):
        """teardown all initialized variables."""
        # drop all tables
        db.session.remove()
        db.drop_all()
    

if __name__ == "__main__":
    unittest.main()