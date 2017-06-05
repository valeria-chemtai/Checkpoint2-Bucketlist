import unittest
import json
from app import create_app, db


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
        self.item = {"name": "Standard chartered marathon"}

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_bucketlist_item_creation(self):
        """Test bucketlist item creation"""
        self.client.post("/auth/register", data=self.user_details)
        result = self.client.post("/auth/login", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]

        self.client.post(
            "/bucketlists/",
            headers=dict(Authorization="Bearer " + access_token),
            data=self.bucketlist)
        # result = json.loads(bucketlist.data.decode())

        resp = self.client.post("/bucketlists/1/items/", headers=dict(
            Authorization="Bearer" + access_token), data=self.item)
        self.assertEqual(resp.status_code, 201)
        self.assertIn("Standard chartered marathon", str(resp.data))

    def test_bucketlist_item_deletion(self):
        """Test bucketlist item can be deleted"""
        # register user
        self.client.post("/auth/register", data=self.user_details)
        # login user
        result = self.client.post("/auth/login", data=self.user_details)

        access_token = json.loads(result.data.decode())["access_token"]
        # create bucketlist
        self.client.post('/bucketlists/', headers=dict(
            Authorization="Bearer " + access_token),
            data=self.bucketlist)
        # create bucketlist item
        bucketlist_item = self.client.post("/bucketlists/1/items/", headers=dict(Authorization="Bearer" + access_token), data=self.item)
        result = json.loads(bucketlist_item.data.decode())
        # delete created bucketlist item
        resp = self.client.delete("/bucketlists/1/items/1",
                                  headers=dict(
                                      Authorization="Bearer " + access_token),)
        self.assertEqual(resp.status_code, 200)
        # confirm item has been deleted by accessing it
        resp = self.client.get(
            "/bucketlists/1/items/1", headers=dict(
                Authorization="Bearer " + access_token))
        self.assertEqual(resp.status_code, 404)

    def test_bucketlist_item_get_by_id(self):
        """Test get bucketlist item by id"""
        self.client.post("/auth/register", data=self.user_details)
        # login user
        result = self.client.post("/auth/login", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]
        # create bucketlist
        self.client.post('/bucketlists/', headers=dict(
            Authorization="Bearer " + access_token),
            data=self.bucketlist)
        # create bucketlist item
        bucketlist_item = self.client.post(
            "/bucketlists/1/items", headers=dict(Authorization="Bearer" + access_token), data=self.item)
        result = json.loads(bucketlist_item.data.decode())
        resp = self.client.get(
            "/bucketlists/1/items/1",
            headers=dict(Authorization="Bearer " + access_token))
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Standard chartered marathon", str(resp.data))


if __name__ == "__main__":
    unittest.main()
