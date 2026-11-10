import unittest
from flask_app import app


class FlaskTests(unittest.TestCase):
    def test_get(self):
        response = app.test_client().get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Герман".encode(), response.data)

    def test_post(self):
        response = app.test_client().post("/", data={"name": "Олег"})
        self.assertIn("Олег".encode(), response.data)


if __name__ == "__main__":
    unittest.main()
