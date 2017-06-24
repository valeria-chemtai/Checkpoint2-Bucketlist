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

    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    def test_bucketlist_item_creation(self):
        """Test bucketlist item creation"""
        resp = self.client.post("/auth/register/", data=self.user_details)
        self.assertEqual(resp.status_code, 201)
        result = self.client.post("/auth/login/", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]

        self.client.post(
            "/bucketlists/",
            headers=dict(Authorization=access_token),
            data=self.bucketlist)
        # result = json.loads(bucketlist.data.decode())

        resp = self.client.post("/bucketlists/1/items/", headers=dict(
            Authorization=access_token), data=self.item)
        self.assertEqual(resp.status_code, 201)
        self.assertIn("Standard chartered marathon", str(resp.data))

    def test_bucketlist_item_creation_with_Existing_name(self):
        """Test bucketlist item creation with existing name"""
        resp = self.client.post("/auth/register/", data=self.user_details)
        self.assertEqual(resp.status_code, 201)
        result = self.client.post("/auth/login/", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]

        self.client.post(
            "/bucketlists/",
            headers=dict(Authorization=access_token),
            data=self.bucketlist)
        # result = json.loads(bucketlist.data.decode())
        self.client.post("/bucketlists/1/items/", headers=dict(
            Authorization=access_token), data=self.item)

        resp = self.client.post("/bucketlists/1/items/", headers=dict(
            Authorization=access_token), data=self.item)
        self.assertEqual(resp.status_code, 205)
        self.assertIn("Item exists", str(resp.data))

    def test_bucketlist_item_creation_without_bucketlist(self):
        """Test bucketlist item creation with no bucketlist"""
        resp = self.client.post("/auth/register/", data=self.user_details)
        self.assertEqual(resp.status_code, 201)
        result = self.client.post("/auth/login/", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]
        resp = self.client.post("/bucketlists/1/items/", headers=dict(
            Authorization=access_token), data=self.item)
        self.assertEqual(resp.status_code, 404)

    def test_bucketlist_item_edit(self):
        """Test edit bucketlist item by id"""
        resp = self.client.post("/auth/register/", data=self.user_details)
        self.assertEqual(resp.status_code, 201)
        # login user
        result = self.client.post("/auth/login/", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]
        # create bucketlist
        self.client.post('/bucketlists/', headers=dict(
            Authorization=access_token),
            data=self.bucketlist)
        # create bucketlist item
        bucketlist_item = self.client.post(
            "/bucketlists/1/items/", headers=dict(Authorization=access_token),
            data=self.item)
        result = json.loads(bucketlist_item.data.decode())
        resp = self.client.put(
            "/bucketlists/1/items/1/",
            headers=dict(Authorization=access_token),
            data={"name": "Stan Chart Marathon"})
        result = self.client.get(
            "/bucketlists/1/items/1/",
            headers=dict(Authorization=access_token))
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Stan Chart", str(result.data))

    def test_nonexistence_bucketlist_item_edit(self):
        """Test edit non existence bucketlist item by id"""
        resp = self.client.post("/auth/register/", data=self.user_details)
        self.assertEqual(resp.status_code, 201)
        # login user
        result = self.client.post("/auth/login/", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]

        resp = self.client.put(
            "/bucketlists/1/items/1/",
            headers=dict(Authorization=access_token),
            data={"name": "Stan Chart Marathon"})
        self.assertEqual(resp.status_code, 404)

    def test_bucketlist_item_edit_with_existing_name(self):
        """Test edit bucketlist item with existing name"""
        resp = self.client.post("/auth/register/", data=self.user_details)
        self.assertEqual(resp.status_code, 201)
        # login user
        result = self.client.post("/auth/login/", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]
        # create bucketlist
        self.client.post('/bucketlists/', headers=dict(
            Authorization=access_token),
            data=self.bucketlist)
        # create bucketlist item
        bucketlist_item = self.client.post(
            "/bucketlists/1/items/", headers=dict(Authorization=access_token),
            data=self.item)
        self.client.post(
            "/bucketlists/1/items/", headers=dict(Authorization=access_token),
            data={"name": "Stan Chart Marathon"})
        result = json.loads(bucketlist_item.data.decode())
        resp = self.client.put(
            "/bucketlists/1/items/1/",
            headers=dict(Authorization=access_token),
            data={"name": "Stan Chart Marathon"})
        self.assertEqual(resp.status_code, 409)
        self.assertIn("Name exists, enter another", str(resp.data))

    def test_bucketlist_item_edit_blank_name(self):
        """Test edit bucketlist item by with blank name"""
        resp = self.client.post("/auth/register/", data=self.user_details)
        self.assertEqual(resp.status_code, 201)
        # login user
        result = self.client.post("/auth/login/", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]
        # create bucketlist
        self.client.post('/bucketlists/', headers=dict(
            Authorization=access_token),
            data=self.bucketlist)
        # create bucketlist item
        bucketlist_item = self.client.post(
            "/bucketlists/1/items/", headers=dict(Authorization=access_token),
            data=self.item)
        result = json.loads(bucketlist_item.data.decode())
        resp = self.client.put(
            "/bucketlists/1/items/1/",
            headers=dict(Authorization=access_token))
        result = self.client.get(
            "/bucketlists/1/items/1/",
            headers=dict(Authorization=access_token))
        self.assertEqual(resp.status_code, 400)
        self.assertIn("Enter a Valid Name", str(resp.data))

    def test_bucketlist_item_deletion(self):
        """Test bucketlist item can be deleted"""
        resp = self.client.post("/auth/register/", data=self.user_details)
        self.assertEqual(resp.status_code, 201)
        result = self.client.post("/auth/login/", data=self.user_details)

        access_token = json.loads(result.data.decode())["access_token"]
        # create bucketlist
        self.client.post('/bucketlists/', headers=dict(
            Authorization=access_token),
            data=self.bucketlist)
        # create bucketlist item
        bucketlist_item = self.client.post(
            "/bucketlists/1/items/", headers=dict(Authorization=access_token),
            data=self.item)
        result = json.loads(bucketlist_item.data.decode())
        # delete created bucketlist item
        resp = self.client.delete("/bucketlists/1/items/1/",
                                  headers=dict(
                                      Authorization=access_token))
        self.assertEqual(resp.status_code, 200)
        # confirm item has been deleted by accessing it
        resp = self.client.get(
            "/bucketlists/1/items/1/", headers=dict(
                Authorization=access_token))
        self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
