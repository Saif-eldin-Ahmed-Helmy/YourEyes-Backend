"""HTTP contract smoke tests that do not download AI models or call providers."""

import os
import io
import sys
import unittest
from unittest.mock import MagicMock, patch


class RouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Model loading currently happens at import time. Stub external packages
        # so a routing regression can be checked without several GB of downloads.
        modules = {
            name: MagicMock()
            for name in (
                "cv2", "numpy", "torch", "transformers", "pytesseract",
                "textract", "gtts", "miniaudio", "requests", "PIL", "PIL.Image",
            )
        }
        cls.module_patch = patch.dict(sys.modules, modules)
        cls.module_patch.start()
        cls.key_patch = patch.dict(os.environ, {"GOOGLE_GEMINI_API_KEY": ""})
        cls.key_patch.start()
        from app import create_app

        cls.app = create_app()
        cls.app.testing = True

    @classmethod
    def tearDownClass(cls):
        cls.key_patch.stop()
        cls.module_patch.stop()

    def setUp(self):
        self.client = self.app.test_client()

    def test_description_accepts_post_and_rejects_get(self):
        response = self.client.post("/describe")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(self.client.get("/describe").status_code, 405)

    def test_clothing_route_fails_closed_without_provider_key(self):
        response = self.client.post("/clothes")
        self.assertEqual(response.status_code, 503)

    def test_hardware_command_is_consumed_once(self):
        self.assertEqual(self.client.post("/command", json={"key": 1}).status_code, 200)
        response = self.client.get("/command")
        self.assertEqual(response.json["key"], 1)
        self.assertEqual(self.client.get("/command").status_code, 404)

    def test_clothing_errors_do_not_expose_provider_details(self):
        from app.routes import clothes
        with patch.object(clothes, 'API_KEY', 'test-only'), patch.object(clothes.cv2, 'imdecode', side_effect=ValueError('private provider details')):
            response = self.client.post('/clothes', data={'image': (io.BytesIO(b'image'), 'image.jpg')})
            self.assertEqual(response.status_code, 500)
            self.assertNotIn('private', response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
