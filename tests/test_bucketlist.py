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

        with self.app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    def test_bucketlist_create(self):
        """Test api can create bucketlist"""
        resp = self.client.post("/auth/register/", data=self.user_details)
        self.assertEqual(resp.status_code, 201)
        result = self.client.post("/auth/login/", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]
        resp = self.client.post('/bucketlists/', headers=dict(
            Authorization=access_token),
            data=self.bucketlist)
        self.assertEqual(resp.status_code, 201)
        self.assertIn("heart marathon", str(resp.data))

    def test_bucketlist_create_with_blank_name(self):
        """Test api can not create blank bucketlist"""
        resp = self.client.post("/auth/register/", data=self.user_details)
        self.assertEqual(resp.status_code, 201)
        result = self.client.post("/auth/login/", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]
        resp = self.client.post('/bucketlists/', headers=dict(
            Authorization=access_token),
            data={"name": " "})
        self.assertEqual(resp.status_code, 400)
        self.assertIn("Bucketlist can not be blank name",
                      str(resp.data))

    def test_bucketlist_create_without_auth(self):
        """Test api can not create bucketlist without authentication"""
        resp = self.client.post('/bucketlists/', headers=dict(
            Authorization="1234"),
            data=self.bucketlist)
        self.assertEqual(resp.status_code, 401)
        self.assertIn("Invalid token. Please register or login",
                      str(resp.data))

    def test_bucketlist_create_with_existing_name(self):
        resp = self.client.post("/auth/register/", data=self.user_details)
        self.assertEqual(resp.status_code, 201)
        result = self.client.post("/auth/login/", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]
        resp = self.client.post('/bucketlists/', headers=dict(
            Authorization=access_token),
            data=self.bucketlist)
        self.assertEqual(resp.status_code, 201)

        resp = self.client.post('/bucketlists/', headers=dict(
            Authorization=access_token),
            data=self.bucketlist)
        self.assertEqual(resp.status_code, 409)

    def test_bucketlist_get(self):
        """Test api can get  bucketlists"""
        resp = self.client.post("/auth/register/", data=self.user_details)
        self.assertEqual(resp.status_code, 201)
        result = self.client.post("/auth/login/", data=self.user_details)
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

    def test_bucketlist_get_with_search_word(self):
        """Test api can get  bucketlists with search word"""
        resp = self.client.post("/auth/register/", data=self.user_details)
        self.assertEqual(resp.status_code, 201)
        result = self.client.post("/auth/login/", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]
        self.client.post("/bucketlists/", headers=dict(
            Authorization=access_token),
            data=self.bucketlist)
        resp = self.client.get("/bucketlists/?q=heart marathon",
                               headers=dict(
                                   Authorization=access_token),
                               )

        self.assertEqual(resp.status_code, 200)
        self.assertIn("heart marathon", str(resp.data))

    def test_bucketlist_get_by_id(self):
        """Test api can get bucketlist by id"""
        resp = self.client.post("/auth/register/", data=self.user_details)
        self.assertEqual(resp.status_code, 201)
        result = self.client.post("/auth/login/", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]

        bucketlist = self.client.post(
            "/bucketlists/",
            headers=dict(Authorization=access_token),
            data=self.bucketlist)

        result = json.loads(bucketlist.data.decode())

        resp = self.client.get(
            "/bucketlists/{}/".format(result["id"]),
            headers=dict(Authorization=access_token))
        # assert that the bucketlist is actually returned given its ID
        self.assertEqual(resp.status_code, 200)
        self.assertIn("heart marathon race", str(resp.data))

    def test_bucketlist_edit(self):
        """Test bucketlist can be edited"""
        resp = self.client.post("/auth/register/", data=self.user_details)
        self.assertEqual(resp.status_code, 201)
        result = self.client.post("/auth/login/", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]

        bucketlist = self.client.post(
            "/bucketlists/",
            headers=dict(Authorization=access_token),
            data=self.bucketlist)
        result = json.loads(bucketlist.data.decode())

        # Edit created bucketlist
        resp = self.client.put(
            "/bucketlists/{}/".format(result["id"]),
            headers=dict(Authorization=access_token),
            data={
                "name": "participate in 10,000km heart marathon race"
            })
        # Get details of edited bucketlist for confirmation
        result = self.client.get(
            "/bucketlists/{}/".format(result["id"]),
            headers=dict(Authorization=access_token))
        self.assertIn("10,000km heart marathon race", str(result.data))
        self.assertEqual(resp.status_code, 200)

    def test_bucketlist_edit_with_other_existing_name(self):
        """Test bucketlist cannot be edited with existing name"""
        resp = self.client.post("/auth/register/", data=self.user_details)
        self.assertEqual(resp.status_code, 201)
        result = self.client.post("/auth/login/", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]

        self.client.post(
            "/bucketlists/",
            headers=dict(Authorization=access_token),
            data={"name": "participate in 10,000km heart marathon race"})

        bucketlist = self.client.post(
            "/bucketlists/",
            headers=dict(Authorization=access_token),
            data=self.bucketlist)
        result = json.loads(bucketlist.data.decode())

        # Edit created bucketlist
        resp = self.client.put(
            "/bucketlists/{}/".format(result["id"]),
            headers=dict(Authorization=access_token),
            data={
                "name": "participate in 10,000km heart marathon race"
            })

        self.assertIn("Name exists, enter another", str(resp.data))
        self.assertEqual(resp.status_code, 409)

    def test_nonexistence_bucketlist_edit(self):
        """Test nonexistence bucketlist can not be edited"""
        resp = self.client.post("/auth/register/", data=self.user_details)
        self.assertEqual(resp.status_code, 201)
        result = self.client.post("/auth/login/", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]

        resp = self.client.put(
            "/bucketlists/1/",
            headers=dict(Authorization=access_token),
            data={
                "name": "participate in 10,000km heart marathon race"
            })
        # Get details of edited bucketlist for confirmation
        self.assertEqual(resp.status_code, 404)

    def test_bucketlist_edit_blank_name(self):
        """Test bucketlist edit with blank name"""
        resp = self.client.post("/auth/register/", data=self.user_details)
        self.assertEqual(resp.status_code, 201)
        result = self.client.post("/auth/login/", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]

        bucketlist = self.client.post(
            "/bucketlists/",
            headers=dict(Authorization=access_token),
            data=self.bucketlist)
        result = json.loads(bucketlist.data.decode())

        # Edit created bucketlist
        resp = self.client.put(
            "/bucketlists/{}/".format(result["id"]),
            headers=dict(Authorization=access_token),
            data={"name": ""})
        # Get details of edited bucketlist for confirmation
        result = self.client.get(
            "/bucketlists/{}/".format(result["id"]),
            headers=dict(Authorization=access_token))
        self.assertIn("Enter a Valid Name", str(resp.data))
        self.assertEqual(resp.status_code, 400)

    def test_bucketlist_edit_without_auth(self):
        """Test bucketlist can not  be edited without authentication"""
        resp = self.client.post("/auth/register/", data=self.user_details)
        self.assertEqual(resp.status_code, 201)
        result = self.client.post("/auth/login/", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]

        bucketlist = self.client.post(
            "/bucketlists/",
            headers=dict(Authorization=access_token),
            data=self.bucketlist)
        result = json.loads(bucketlist.data.decode())

        # Edit created bucketlist
        resp = self.client.put(
            "/bucketlists/{}/".format(result["id"]),
            headers=dict(Authorization="123"),
            data={
                "name": "participate in 10,000km heart marathon race"
            })
        # Get details of edited bucketlist for confirmation
        result = self.client.get(
            "/bucketlists/{}/".format(result["id"]),
            headers=dict(Authorization=access_token))
        self.assertIn("Invalid token. Please register or login",
                      str(resp.data))
        self.assertEqual(resp.status_code, 401)

    def test_bucketlist_deletion(self):
        """Test API can delete an existing bucketlist"""
        resp = self.client.post("/auth/register/", data=self.user_details)
        self.assertEqual(resp.status_code, 201)
        result = self.client.post("/auth/login/", data=self.user_details)
        access_token = json.loads(result.data.decode())["access_token"]

        # create bucketlist
        bucketlist = self.client.post(
            "/bucketlists/",
            headers=dict(Authorization=access_token),
            data=self.bucketlist)
        result = json.loads(bucketlist.data.decode())

        # delete created bucketlist
        resp = self.client.delete(
            "/bucketlists/{}/".format(result["id"]),
            headers=dict(Authorization=access_token),)
        self.assertEqual(resp.status_code, 200)

        # confirm truly bucketlist has been deleted by accessing it
        resp = self.client.get(
            "/bucketlists/1/",
            headers=dict(Authorization=access_token))
        self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
