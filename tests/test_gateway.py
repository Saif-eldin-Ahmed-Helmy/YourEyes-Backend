"""Gateway contract checks without model downloads or provider requests."""
import importlib.util
import os
from pathlib import Path
import unittest
from unittest.mock import Mock, patch

from flask import Flask


class GatewayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('gateway', Path(__file__).parents[1] / 'app/routes/gemini.py')
        cls.gateway = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.gateway)
        cls.app = Flask(__name__)
        cls.app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
        cls.app.register_blueprint(cls.gateway.bp)

    def setUp(self):
        self.client = self.app.test_client()
        self.payload = {'contents': [{'parts': [{'text': 'Describe this image'}]}]}

    def test_missing_configuration_and_invalid_payload(self):
        with patch.dict(os.environ, {'GOOGLE_GEMINI_API_KEY': ''}):
            self.assertEqual(self.client.post('/gemini/generate', json=self.payload).status_code, 503)
        with patch.dict(os.environ, {'GOOGLE_GEMINI_API_KEY': 'test-only'}):
            self.assertEqual(self.client.post('/gemini/generate', json={}).status_code, 400)

    def test_only_local_native_clients_are_accepted(self):
        self.assertEqual(self.client.post('/gemini/generate', json=self.payload, environ_overrides={'REMOTE_ADDR': '192.0.2.1'}).status_code, 403)
        self.assertEqual(self.client.post('/gemini/generate', json=self.payload, headers={'Origin': 'https://example.com'}).status_code, 403)

    def test_provider_key_stays_on_server_and_contract_is_preserved(self):
        result = {'candidates': [{'content': {'parts': [{'text': 'Result'}]}}]}
        provider = Mock(status_code=200)
        provider.json.return_value = result
        with patch.dict(os.environ, {'GOOGLE_GEMINI_API_KEY': 'test-only', 'GEMINI_MODEL': 'gemini-2.5-flash'}), patch.object(self.gateway.requests, 'post', return_value=provider) as post:
            response = self.client.post('/gemini/generate', json=self.payload)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, result)
            self.assertNotIn('test-only', response.get_data(as_text=True))
            self.assertNotIn('key=', post.call_args.args[0])
            self.assertEqual(post.call_args.kwargs['headers']['x-goog-api-key'], 'test-only')
            self.assertEqual(post.call_args.kwargs['timeout'], 30)

    def test_provider_failure_is_not_forwarded(self):
        provider = Mock(status_code=403, text='private provider details')
        with patch.dict(os.environ, {'GOOGLE_GEMINI_API_KEY': 'test-only'}), patch.object(self.gateway.requests, 'post', return_value=provider):
            response = self.client.post('/gemini/generate', json=self.payload)
            self.assertEqual(response.status_code, 502)
            self.assertNotIn('private', response.get_data(as_text=True))


if __name__ == '__main__':
    unittest.main()
