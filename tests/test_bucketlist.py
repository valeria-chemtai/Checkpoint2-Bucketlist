import unittest
import json
from app.views import create_app, db


class BucketlistTestCase(unittest.TestCase):
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

    def test_bucketlist_create(self):
        """Test api can create bucketlist"""
        self.client.post("/auth/register", data=self.user_details)
        result = self.client.post("/auth/login", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]
        resp = self.client.post('/bucketlists/', headers=dict(
            Authorization=access_token),
            data=self.bucketlist)
        self.assertEqual(resp.status_code, 201)
        self.assertIn("heart marathon", str(resp.data))

    def test_bucketlist_create_without_auth(self):
        """Test api can not create bucketlist without authentication"""
        resp = self.client.post('/bucketlists/', headers=dict(
            Authorization="1234"),
            data=self.bucketlist)
        self.assertEqual(resp.status_code, 401)
        self.assertIn("Invalid token. Please register or login",
                      str(resp.data))

    def test_bucketlist_get(self):
        """Test api can get  bucketlists"""
        self.client.post("/auth/register", data=self.user_details)
        result = self.client.post("/auth/login", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]
        self.client.post("/bucketlists/", headers=dict(
            Authorization=access_token),
            data=self.bucketlist)
        resp = self.client.get("/bucketlists/",
                               headers=dict(
                                   Authorization=access_token),
                               )
        self.assertEqual(resp.status_code, 200)
        self.assertIn("heart marathon", str(resp.data))

    def test_bucketlist_get_by_id(self):
        """Test api can get bucketlist by id"""
        self.client.post("/auth/register", data=self.user_details)
        result = self.client.post("/auth/login", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]

        bucketlist = self.client.post(
            "/bucketlists/",
            headers=dict(Authorization=access_token),
            data=self.bucketlist)

        result = json.loads(bucketlist.data.decode())

        resp = self.client.get(
            "/bucketlists/{}".format(result["id"]),
            headers=dict(Authorization=access_token))
        # assert that the bucketlist is actually returned given its ID
        self.assertEqual(resp.status_code, 200)
        self.assertIn("heart marathon race", str(resp.data))

    def test_bucketlist_edit(self):
        """Test bucketlist can be edited"""
        self.client.post("/auth/register", data=self.user_details)
        result = self.client.post("/auth/login", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]

        bucketlist = self.client.post(
            "/bucketlists/",
            headers=dict(Authorization=access_token),
            data=self.bucketlist)
        result = json.loads(bucketlist.data.decode())

        # Edit created bucketlist
        resp = self.client.put(
            "/bucketlists/{}".format(result["id"]),
            headers=dict(Authorization=access_token),
            data={
                "name": "participate in 10,000km heart marathon race"
            })
        # Get details of edited bucketlist for confirmation
        result = self.client.get(
            "/bucketlists/{}".format(result["id"]),
            headers=dict(Authorization=access_token))
        self.assertIn("10,000km heart marathon race", str(result.data))
        self.assertEqual(resp.status_code, 200)

    def test_bucketlist_edit_without_auth(self):
        """Test bucketlist can not  be edited without authentication"""
        self.client.post("/auth/register", data=self.user_details)
        result = self.client.post("/auth/login", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]

        bucketlist = self.client.post(
            "/bucketlists/",
            headers=dict(Authorization=access_token),
            data=self.bucketlist)
        result = json.loads(bucketlist.data.decode())

        # Edit created bucketlist
        resp = self.client.put(
            "/bucketlists/{}".format(result["id"]),
            headers=dict(Authorization="123"),
            data={
                "name": "participate in 10,000km heart marathon race"
            })
        # Get details of edited bucketlist for confirmation
        result = self.client.get(
            "/bucketlists/{}".format(result["id"]),
            headers=dict(Authorization=access_token))
        self.assertIn("Invalid token. Please register or login", str(resp.data))
        self.assertEqual(resp.status_code, 401)

    def test_bucketlist_deletion(self):
        """Test API can delete an existing bucketlist"""
        self.client.post("/auth/register", data=self.user_details)
        result = self.client.post("/auth/login", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]

        # create bucketlist
        bucketlist = self.client.post(
            "/bucketlists/",
            headers=dict(Authorization=access_token),
            data=self.bucketlist)
        result = json.loads(bucketlist.data.decode())

        # delete created bucketlist
        resp = self.client.delete(
            "/bucketlists/{}".format(result["id"]),
            headers=dict(Authorization=access_token),)
        self.assertEqual(resp.status_code, 200)

        # confirm truly bucketlist has been deleted by accessing it
        resp = self.client.get(
            "/bucketlists/1",
            headers=dict(Authorization=access_token))
        self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
