from flask_testing import TestCase
from flask import current_app

# To connect with the database
from app.extensions import db

# The models
from app.models import User, BlackListToken

# The config
from app.config import Config
from app import create_app

# Fetch the base dir
import os
basedir = os.path.abspath(os.path.dirname(__file__))

import json

# For debugin
import pdb

# To have time
import time

class SigUpTestCase(TestCase):
    def create_app(self):
        # Re configurate
        Config.SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
        Config.TESTING = True
        Config.WTF_CSRF_ENABLED = False
        return create_app()  # Create the app with the configuration
    
    # Simulates that a user exist
    def setUp(self):
        self.test_user = {
            "name" : "pedrito",
            "passwd" : "pedrito",
            "email" : "pedrito@gmail.com",
            "schoolname" : "chupi"
        }
        
        db.create_all()


    def test_signup_post(self):
        resp = self.client.post(
            "/api/auth/signup",
            data = json.dumps(self.test_user),
            content_type = "application/json"
        )

        self.assertEqual(resp.status_code, 201)
        
        api_resp = json.loads(resp.data.decode())
        
        self.assertTrue(api_resp["success"])
        self.assertTrue("token" in api_resp["data"].keys())
        self.assertTrue(isinstance(api_resp["data"]["token"], str))

        user_model = User.query.filter_by(email = self.test_user["email"]).first()
        self.assertIsNotNone(user_model)

    def test_get_user(self):
        resp = self.client.post(
            "/api/auth/signup",
            data = json.dumps(self.test_user),
            content_type = "application/json"
        )

        self.assertEqual(resp.status_code, 201)
        api_resp = json.loads(resp.data.decode())
        
        resp = self.client.get(
            "/api/auth/settings",
            headers = {
                "x-access-tokens" : api_resp["data"]["token"]
            }
        )
        
        self.assertEqual(resp.status_code, 200)
        api_resp = json.loads(resp.data.decode())

        self.assertTrue(api_resp["success"])
        self.assertTrue("user" in api_resp["data"].keys())
        self.assertEqual(api_resp["data"]["user"]["name"], self.test_user["name"])
        

    # Remove all the users
    def tearDown(self):
        db.drop_all()


class LoginTestCase(TestCase):
    def create_app(self):
        # Re configurate
        Config.SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
        Config.TESTING = True
        Config.WTF_CSRF_ENABLED = False
        return create_app()  # Create the app with the configuration
    
    # Simulates that a user exist
    def setUp(self):
        self.test_user = {
            "name" : "pedrito",
            "passwd" : "pedrito",
            "email" : "pedrito@gmail.com",
            "schoolname" : "chupi"
        }
        
        db.create_all()

        resp = self.client.post(
            "/api/auth/signup",
            data = json.dumps(self.test_user),
            content_type = "application/json"
        )

        api_resp = json.loads(resp.data.decode())
        self.signup_token = api_resp["data"]["token"]

        
    def test_login(self):
        # Take time to generate a unique tokens
        time.sleep(1)
        
        resp = self.client.post(
            "/api/auth/login",
            data = json.dumps({
                "email" : self.test_user["email"],
                "passwd" : self.test_user["passwd"]
            }),
            content_type = "application/json"
        )
        
        self.assertEqual(resp.status_code, 200)
        api_resp = json.loads(resp.data.decode())
        
        self.assertTrue(api_resp["success"])
        self.assertTrue("token" in api_resp["data"].keys())
        
        self.assertNotEqual(api_resp["data"]["token"], self.signup_token)
        

    # Remove all the users
    def tearDown(self):
        db.drop_all()



class UpdateUserTestCase(TestCase):
    def create_app(self):
        # Re configurate
        Config.SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
        Config.TESTING = True
        Config.WTF_CSRF_ENABLED = False
        return create_app()  # Create the app with the configuration
    
    # Simulates that a user exist
    def setUp(self):
        self.test_user = {
            "name" : "pedrito",
            "passwd" : "pedrito",
            "email" : "pedrito@gmail.com",
            "schoolname" : "chupi"
        }
        
        db.create_all()

        resp = self.client.post(
            "/api/auth/signup",
            data = json.dumps(self.test_user),
            content_type = "application/json"
        )

        api_resp = json.loads(resp.data.decode())
        self.signup_token = api_resp["data"]["token"]


    def test_update(self):
        resp = self.client.put(
            "/api/auth/settings",
            data = json.dumps({
                "name" : "filemon"
            }),
            headers = {
                "x-access-tokens" : self.signup_token
            },
            content_type = "application/json"
        )

        self.assertEqual(resp.status_code, 200)
        api_resp = json.loads(resp.data.decode())
        self.assertTrue(api_resp["success"])

        resp = self.client.get(
            "/api/auth/settings",
            headers = {
                "x-access-tokens" : self.signup_token
            }
        )
        
        self.assertEqual(resp.status_code, 200)
        api_resp = json.loads(resp.data.decode())

        self.assertTrue(api_resp["success"])
        self.assertTrue("user" in api_resp["data"].keys())
        self.assertEqual(api_resp["data"]["user"]["name"], "filemon")
        
    
    # Remove all the users
    def tearDown(self):
        db.drop_all()

class LogOutTestCase(TestCase):
    def create_app(self):
        # Re configurate
        Config.SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
        Config.TESTING = True
        Config.WTF_CSRF_ENABLED = False
        return create_app()  # Create the app with the configuration


    # Simulates that a user exist
    def setUp(self):
        self.test_user = {
            "name" : "pedrito",
            "passwd" : "pedrito",
            "email" : "pedrito@gmail.com",
            "schoolname" : "chupi"
        }
        
        db.create_all()

        resp = self.client.post(
            "/api/auth/signup",
            data = json.dumps(self.test_user),
            content_type = "application/json"
        )

        api_resp = json.loads(resp.data.decode())
        self.signup_token = api_resp["data"]["token"]


    def test_logout(self):
        resp = self.client.post(
            "/api/auth/logout",
            headers = {
                "x-access-tokens" : self.signup_token
            }
        )

        self.assertEqual(resp.status_code, 200)
        api_resp = json.loads(resp.data.decode())
        self.assertTrue(api_resp["success"])

        resp = self.client.get(
            "/api/auth/settings",
            headers = {
                "x-access-tokens" : self.signup_token
            }
        )
        
        self.assertEqual(resp.status_code, 401)
        api_resp = json.loads(resp.data.decode())
        self.assertFalse(api_resp["success"])
    
    # Remove all the users
    def tearDown(self):
        db.drop_all()



    
class DeleteUserTestCase(TestCase):
    def create_app(self):
        # Re configurate
        Config.SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
        Config.TESTING = True
        Config.WTF_CSRF_ENABLED = False
        return create_app()  # Create the app with the configuration


    # Simulates that a user exist
    def setUp(self):
        self.test_user = {
            "name" : "pedrito",
            "passwd" : "pedrito",
            "email" : "pedrito@gmail.com",
            "schoolname" : "chupi"
        }
        
        db.create_all()

        resp = self.client.post(
            "/api/auth/signup",
            data = json.dumps(self.test_user),
            content_type = "application/json"
        )

        api_resp = json.loads(resp.data.decode())
        self.signup_token = api_resp["data"]["token"]


    def test_delete(self):
        resp = self.client.delete(
            "/api/auth/delete",
            headers = {
                "x-access-tokens" : self.signup_token
            }
        )

        self.assertEqual(resp.status_code, 200)
        api_resp = json.loads(resp.data.decode())
        self.assertTrue(api_resp["success"])

        resp = self.client.get(
            "/api/auth/settings",
            headers = {
                "x-access-tokens" : self.signup_token
            }
        )
        
        self.assertEqual(resp.status_code, 401)
        api_resp = json.loads(resp.data.decode())
        self.assertFalse(api_resp["success"])

    def test_delete_cascade_tokens(self):
        resp = self.client.post(
            "/api/auth/logout",
            headers = {
                "x-access-tokens" : self.signup_token
            }
        )

        self.assertEqual(resp.status_code, 200)
        api_resp = json.loads(resp.data.decode())
        self.assertTrue(api_resp["success"])

        time.sleep(1)
        
        resp = self.client.post(
            "/api/auth/login",
            data = json.dumps({
                "email" : self.test_user["email"],
                "passwd" : self.test_user["passwd"]
            }),
            content_type = "application/json"
        )

        self.assertEqual(resp.status_code, 200)
        api_resp = json.loads(resp.data.decode())
        self.assertTrue(api_resp["success"])
        
        self.signup_token = api_resp["data"]["token"]
        
        resp = self.client.post(
            "/api/auth/logout",
            headers = {
                "x-access-tokens" : self.signup_token
            }
        )

        self.assertEqual(resp.status_code, 200)
        api_resp = json.loads(resp.data.decode())
        self.assertTrue(api_resp["success"])


        time.sleep(1)

        resp = self.client.post(
            "/api/auth/login",
            data = json.dumps({
                "email" : self.test_user["email"],
                "passwd" : self.test_user["passwd"]
            }),
            content_type = "application/json"
        )

        self.assertEqual(resp.status_code, 200)
        api_resp = json.loads(resp.data.decode())
        self.assertTrue(api_resp["success"])
        self.signup_token = api_resp["data"]["token"]
        
        self.assertTrue(len(BlackListToken.query.all()) > 0)

        resp = self.client.delete(
            "/api/auth/delete",
            headers = {
                "x-access-tokens" : self.signup_token
            }
        )

        self.assertEqual(resp.status_code, 200)
        api_resp = json.loads(resp.data.decode())
        self.assertTrue(api_resp["success"])

        self.assertTrue(len(BlackListToken.query.all()) == 0)
        
        
    # Remove all the users
    def tearDown(self):
        db.drop_all()
