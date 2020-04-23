import json
import os

from unittest.mock import patch
from requests import HTTPError, Response

from tests.unit.tests_client import HTTPPrettyTestMixin


class ModelTestMixin(HTTPPrettyTestMixin):
    MODEL_KLASS = None

    def sample_list(self):
        return self._read_sample(action='list')

    def sample_detail(self):
        return self._read_sample(action='detail')

    def _read_sample(self, action):
        path = os.path.dirname(__file__)
        filename = f'{self.MODEL_KLASS._RESOURCE_NAME}.{action}.json'
        with open(os.path.join(path, 'samples', filename), 'r') as f:
            return json.loads(f.read())

    def patch_get(self, data):
        return patch('tsuru.client.TsuruClient.get', return_value=data)

    def patch_get_error(self, content=None, status_code=404):
        response = Response()
        response.status_code = status_code
        response._content = content
        error = HTTPError(response=response)
        return patch('tsuru.client.TsuruClient.get', side_effect=error)

    def test_fields(self):
        raise NotImplementedError()

    def test_invalid_field(self):
        raise NotImplementedError()

    def test_list(self):
        raise NotImplementedError()

    def test_detail(self):
        raise NotImplementedError()

    def test_not_found(self):
        raise NotImplementedError()
