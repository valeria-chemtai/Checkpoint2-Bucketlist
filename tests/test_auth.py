import unittest
import json
from app import create_app, db


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.user_details = {
            "username": "newuser",
            "email": "newuser@app.com",
            "password": "new_password1"
        }
        self.bucketlist = {"name": "participate in heart marathon race"}

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_register_new_user(self):
        """Test that user registration works"""
        resp = self.client.post("/auth/register/", data=self.user_details)
        result = json.loads(resp.data.decode())
        self.assertEqual(result["message"], "Successfully Registered")
        self.assertEqual(resp.status_code, 201)

    def test_register_new_user_with_blank_data(self):
        """Test error/message displayed with invalid data for registration"""
        resp = self.client.post("/auth/register/",
                                data={"username": "newuser",
                                      "email": "newuser@app.com"})
        result = json.loads(resp.data.decode())
        self.assertEqual(result["message"], "Password must be non-empty.")
        self.assertEqual(resp.status_code, 500)

    def test_register_already_registered_user(self):
        """Test user can only register once"""
        resp = self.client.post("/auth/register/", data=self.user_details)
        self.assertEqual(resp.status_code, 201)
        resp = self.client.post("/auth/register/", data=self.user_details)
        result = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 409)
        self.assertEqual(
            result["message"], "Already Resgistered. Login Please")

    def test_login_registered_user(self):
        """Test registered user successful login"""
        resp = self.client.post("/auth/register/", data=self.user_details)
        self.assertEqual(resp.status_code, 201)
        resp = self.client.post("/auth/login/", data=self.user_details)
        result = json.loads(resp.data.decode())
        self.assertTrue(result['access_token'])
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(result["message"], "Login Successful")

    def test_login_registered_user_invalid_password(self):
        """Test registered user with invalid password login response"""
        resp = self.client.post("/auth/register/", data=self.user_details)
        self.assertEqual(resp.status_code, 201)
        resp = self.client.post("/auth/login/",
                                data={"username": "newuser@app.com",
                                      "password": "password1"})
        result = json.loads(resp.data.decode())
        self.assertEqual(resp.status_code, 409)
        self.assertEqual(result["message"],
                         "email/password Combination Invalid")

    def test_login_unregistered_user(self):
        """Test unregistered user can not login"""
        resp = self.client.post("/auth/login/", data=self.user_details)
        result = json.loads(resp.data.decode())
        self.assertEqual(result["message"],
                         "login details Unknown. Register First")
        self.assertEqual(resp.status_code, 401)


if __name__ == "__main__":
    unittest.main()
