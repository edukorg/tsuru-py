import unittest

from tsuru import models, exceptions
from tests.unit.tests_models import ModelTestMixin


class TestAppModel(ModelTestMixin, unittest.TestCase):
    MODEL_KLASS = models.App

    def test_fields(self):
        data = self.sample_detail()
        app = models.App(data=data)

        self.assertEqual('hufflepuff-api-prd', app.name)

    def test_invalid_field(self):
        with self.assertRaises(exceptions.UnexpectedDataFormat):
            models.App(data={})

    def test_list(self):
        data = self.sample_list()
        with self.patch_get(data=data) as get:
            list(models.App.list())

        self.assertEqual(1, get.call_count)

    def test_detail(self):
        data = self.sample_detail()
        with self.patch_get(data=data) as get:
            models.App.get(pk=666)

        self.assertEqual(1, get.call_count)

    def test_not_found(self):
        with self.patch_get_error(status_code=404) as get:
            with self.assertRaises(exceptions.DoesNotExist):
                models.App.get(pk=666)

        self.assertEqual(1, get.call_count)
