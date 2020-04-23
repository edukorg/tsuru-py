import json
import unittest

import httpretty
from unittest.mock import patch

from tsuru import client


class HTTPPrettyTestMixin:
    API_URL = 'https://my-tsuru:8080'

    def setUp(self):
        self.patcher = patch('tsuru.client.TsuruClient._URL', self.API_URL)
        self.patcher.start()

    def tearDown(self):
        self.patcher.stop()

    def patch_token(self, token='42'):
        return patch('tsuru.client.TsuruClient._TOKEN', token)

    @property
    def request_count(self):
        return len(httpretty.httpretty.latest_requests)

    @property
    def latest_request_header(self):
        last_request = httpretty.httpretty.last_request
        return last_request.headers


class TestTsuruClient(HTTPPrettyTestMixin, unittest.TestCase):
    @httpretty.activate
    def test_request_error(self):
        httpretty.register_uri(
            httpretty.GET,
            f'{self.API_URL}/potato',
            body="Find the best daily deals",
            status=404,
        )

        with self.patch_token():
            with self.assertRaises(Exception):
                client.TsuruClient.get(
                    resource='potato',
                )

        self.assertEqual(1, self.request_count)
        self.assertEqual('42', self.latest_request_header['Authentication'])

    @httpretty.activate
    def test_list_resource(self):
        httpretty.register_uri(
            httpretty.GET,
            f'{self.API_URL}/potato',
            body=json.dumps([{'answer': 314}]),
        )

        with self.patch_token():
            data = client.TsuruClient.get(
                resource='potato',
            )

        self.assertEqual(1, self.request_count)
        self.assertEqual('42', self.latest_request_header['Authentication'])
        self.assertEqual([{'answer': 314}], data)

    @httpretty.activate
    def test_detail_resource(self):
        httpretty.register_uri(
            httpretty.GET,
            f'{self.API_URL}/potato/314',
            body=json.dumps({'answer': 314}),
        )

        with self.patch_token():
            data = client.TsuruClient.get(
                resource='potato',
                pk=314,
            )

        self.assertEqual(1, self.request_count)
        self.assertEqual('42', self.latest_request_header['Authentication'])
        self.assertEqual({'answer': 314}, data)

    @httpretty.activate
    def test_bound_list_from_resource(self):
        httpretty.register_uri(
            httpretty.GET,
            f'{self.API_URL}/potato/314/answers',
            body=json.dumps([{'answer': 666}]),
        )

        with self.patch_token():
            data = client.TsuruClient.get(
                from_resource='potato',
                from_pk=314,
                resource='answers',
            )

        self.assertEqual(1, self.request_count)
        self.assertEqual('42', self.latest_request_header['Authentication'])
        self.assertEqual([{'answer': 666}], data)

    @httpretty.activate
    def test_bound_list_from_resource_without_id(self):
        with self.patch_token():
            with self.assertRaises(UnboundLocalError):
                client.TsuruClient.get(
                    from_resource='potato',
                    resource='answers',
                )

        self.assertEqual(0, self.request_count)

    @httpretty.activate
    def test_bound_detail_from_resource(self):
        httpretty.register_uri(
            httpretty.GET,
            f'{self.API_URL}/potato/314/answers/666',
            body=json.dumps([{'answer': 666}]),
        )

        with self.patch_token():
            data = client.TsuruClient.get(
                from_resource='potato',
                from_pk=314,
                resource='answers',
                pk=666,
            )

        self.assertEqual(1, self.request_count)
        self.assertEqual('42', self.latest_request_header['Authentication'])
        self.assertEqual([{'answer': 666}], data)

    @httpretty.activate
    def test_bound_detail_from_resource_without_id(self):
        with self.patch_token():
            with self.assertRaises(UnboundLocalError):
                client.TsuruClient.get(
                    from_resource='potato',
                    resource='answers',
                    pk=666,
                )

        self.assertEqual(0, self.request_count)
