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

class PostPlanTestCase(TestCase):
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
        self.token = api_resp["data"]["token"]


    def test_post(self):
        resp = self.client.post(
            "/api/plan/",
            data = json.dumps({
                "name" : "test",
	        "desc" : "Son 4 clases por mes",
	        "number_of_classes" : 4,
	        "price" : 2000.0,
	        "method" : 1
            }),
            headers = {
                "x-access-tokens" : self.token
            },
            content_type = "application/json"
        )

        self.assertEqual(resp.status_code, 201)
        api_resp = json.loads(resp.data.decode())
        self.assertTrue(api_resp["success"])

        resp = self.client.get(
            "/api/plan/test",
            headers = {
                "x-access-tokens" : self.token
            }
        )
        self.assertEqual(resp.status_code, 200)
        api_resp = json.loads(resp.data.decode())
        self.assertTrue(api_resp["success"])
        

    # Remove all the users
    def tearDown(self):
        db.drop_all()


class GetAllPlans(TestCase):
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
        self.token = api_resp["data"]["token"]

        # Post 10 plans
        for i in range(1, 11):
            resp = self.client.post(
                "/api/plan/",
                data = json.dumps({
                    "name" : f"test{i}",
	            "desc" : "Son 4 clases por mes",
	            "number_of_classes" : 4,
	            "price" : 2000.0,
	            "method" : 1
                }),
                headers = {
                    "x-access-tokens" : self.token
                },
                content_type = "application/json"
            )
        

    def test_get_all(self):
        resp = self.client.get(
            "/api/plan/all",
            headers = {
                "x-access-tokens" : self.token
            }
        )
        
        self.assertEqual(resp.status_code, 200)
        api_resp = json.loads(resp.data.decode())
        self.assertTrue(api_resp["success"])
        self.assertEqual(len(api_resp["data"]["plans_of_payment"]), 10)

    # Remove all the users
    def tearDown(self):
        db.drop_all()


class DeletePlanTestCase(TestCase):
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
        self.token = api_resp["data"]["token"]

        # Post 10 plans
        for i in range(1, 11):
            resp = self.client.post(
                "/api/plan/",
                data = json.dumps({
                    "name" : f"test{i}",
	            "desc" : "Son 4 clases por mes",
	            "number_of_classes" : 4,
	            "price" : 2000.0,
	            "method" : 1
                }),
                headers = {
                    "x-access-tokens" : self.token
                },
                content_type = "application/json"
            )
            
    def test_delete_afew(self):
        for i in range(1, 6):
            resp = self.client.delete(
                f"/api/plan/test{i}",
                headers = {
                    "x-access-tokens" : self.token
                }
            )
            
            self.assertEqual(resp.status_code, 200)
            api_resp = json.loads(resp.data.decode())
            self.assertTrue(api_resp["success"])
            

            resp = self.client.get(
                f"/api/plan/test{i}",
                headers = {
                    "x-access-tokens" : self.token
                }
            )

            self.assertEqual(resp.status_code, 422)
            api_resp = json.loads(resp.data.decode())
            self.assertTrue(not api_resp["success"])

            

    # Remove all the users
    def tearDown(self):
        db.drop_all()



class UpdatePlanTestCase(TestCase):
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
        self.token = api_resp["data"]["token"]

        # Post 10 plans
        for i in range(1, 11):
            resp = self.client.post(
                "/api/plan/",
                data = json.dumps({
                    "name" : f"test{i}",
	            "desc" : "Son 4 clases por mes",
	            "number_of_classes" : 4,
	            "price" : 2000.0,
	            "method" : 1
                }),
                headers = {
                    "x-access-tokens" : self.token
                },
                content_type = "application/json"
            )
            
    def test_update(self):
        resp = self.client.put(
            "/api/plan/test1",
            data = json.dumps({
                "name" : "test11"
            }),
            headers = {
                "x-access-tokens" : self.token
            },
            content_type = "application/json"
        )
        
        resp = self.client.get(
            "/api/plan/test11",
            headers = {
                "x-access-tokens" : self.token
            }
        )
            
        self.assertEqual(resp.status_code, 200)
        api_resp = json.loads(resp.data.decode())
        self.assertTrue(api_resp["success"])
        

            

    # Remove all the users
    def tearDown(self):
        db.drop_all()
