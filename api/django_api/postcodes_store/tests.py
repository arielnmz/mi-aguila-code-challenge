from django.test import TestCase

from postcodes_store.api_tools import get_geolocations_gen


class ApiTools(TestCase):
    # Simple test for the CSV processing logic
    def test_get_geolocations_gen(self):
        gen = get_geolocations_gen([(1, 2), (3, 4)])

        self.assertEqual(next(gen), [(1, 2), (3, 4)])
        self.assertEqual(next(gen), [])
