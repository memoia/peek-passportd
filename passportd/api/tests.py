import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from api import models


class TimeslotModelTests(TestCase):
    def test_customer_count(self):
        pass


class BookingModelTests(TestCase):
    def test_find_boat_finds_a_boat(self):
        pass

    def test_find_boat_cannot_find_boat(self):
        pass


class PingViewTests(TestCase):
    def test_returns_ok(self):
        resp = self.client.get(reverse('api:ping'))
        self.assertEqual(resp.status_code, 200)
        status = json.loads(resp.content).get('status')
        self.assertEqual(status, "OK")
