import json
from datetime import datetime, timedelta
from django.test import TestCase
from django.core.urlresolvers import reverse
from api import models
from api import util


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


class BoatsViewTests(TestCase):
    url = reverse('api:boats')

    def test_returns_keys_on_post(self):
        resp = self.client.post(self.url, {
            'boat[capacity]': '5',
            'boat[name]': 'Test Boat',
        })
        data = json.loads(resp.content)
        self.assertTrue(all(k in data for k in ('id', 'name', 'capacity')))

    def test_gets_boats_on_get(self):
        models.Boat.objects.create(capacity=1, name='Boat1')
        models.Boat.objects.create(capacity=2, name='Boat2')
        models.Boat.objects.create(capacity=3, name='Boat3')
        resp = self.client.get(self.url)
        data = json.loads(resp.content)
        self.assertTrue(len(data) >= 3)

    def test_ignores_bad_args(self):
        assert self.client.post(self.url, dict(capacity=1, arg1='huh?'))


class AssignmentsViewTests(TestCase):
    url = reverse('api:assignments')

    def test_returns_keys_on_post(self):
        ts = models.Timeslot.objects.create(start_time=1, end_time=2)
        bt = models.Boat.objects.create(capacity=1, name='Wobbly')
        resp = self.client.post(self.url, {
            'timeslot_id': ts.pk,
            'boat_id': bt.pk,
        })
        data = json.loads(resp.content)
        self.assertEqual(data['boat'], bt.pk)
        self.assertEqual(data['timeslot'], ts.pk)

class UtilTests(TestCase):
    def test_prepare_record(self):
        inrec = {
            'something[fun]': 'foo',
            'else[cool-yay]': 'bar',
            'not.applicable': 'baz',
            'also[not]match': 'xyz',
        }
        outrec = {
            'fun': 'foo',
            'not.applicable': 'baz',
        }
        self.assertEqual(util.prepare_record(inrec, ('fun', 'not.applicable')),
                         outrec)

    def test_date_bounds(self):
        right_now = datetime.now()
        today_start = int(right_now.date().strftime("%s"))
        tomorrow_start = int((right_now + timedelta(days=1)).date().strftime("%s"))
        self.assertEqual(util.date_bounds(right_now), (today_start, tomorrow_start))
