import json
from datetime import datetime, timedelta
from django.test import TestCase
from django.core.urlresolvers import reverse
from api import models
from api import util


class TimeslotModelTests(TestCase):
    def bookit(self, *groupsizes, **kwargs):
        capacity = kwargs.get('capacity', 5)
        ts = models.Timeslot.objects.create(start_time=10, end_time=20)
        bt = models.Boat.objects.create(capacity=capacity, name='ABoat')
        an = models.Assignment.objects.create(boat=bt, timeslot=ts)
        for size in groupsizes:
            models.Booking.objects.create(assignment=an, size=size)
        return (ts, an)

    def test_customer_count_zero(self):
        ts = models.Timeslot.objects.create(start_time=10, end_time=20)
        self.assertEqual(ts.customer_count, 0)

    def test_customer_count_more_than_zero(self):
        ts, _ = self.bookit(2, 2)
        self.assertEqual(ts.customer_count, 4)

    def test_overbooking_a_boat_can_be_done_by_not_using_book_for(self):
        ts, _ = self.bookit(2, 4, capacity=5)
        self.assertEqual(ts.customer_count, 6)

    def test_availability_zero_assignments(self):
        ts = models.Timeslot.objects.create(start_time=10, end_time=20)
        self.assertEqual(ts.availability, 0)

    def test_availability_with_assignments(self):
        ts, assgn = self.bookit(2, 2, capacity=5)
        self.assertEqual(ts.availability, 1)


class AssignmentModelTests(TestCase):
    def setUp(self):
        self.slots = self.slotmachine()

    def slotmachine(self):
        times = (
            (5, 14),
            (10, 20),
            (10, 30),
            (15, 18),
            (21, 30),
        )
        slots = []
        for (start, end) in times:
            slots.append(models.Timeslot.objects.create(start_time=start, end_time=end))
        return slots

    def boatmaker(self, capacity):
        return models.Boat.objects.create(capacity=capacity, name=str(capacity*capacity))

    def assign(self, slot, boat):
        return models.Assignment.objects.create(timeslot=slot, boat=boat)

    def test_boat_availability_one_boat(self):
        asgn = self.assign(self.slots[0], self.boatmaker(5))
        book = models.Booking.book_for(self.slots[0].pk, 3)
        self.assertEqual(asgn.boat_availability, 2)

    def test_boat_availability_multiboat(self):
        asgn = self.assign(self.slots[0], self.boatmaker(2))
        asgn = self.assign(self.slots[0], self.boatmaker(4))
        book = models.Booking.book_for(self.slots[0].pk, 1)
        self.assertEqual(book.assignment.timeslot.availability, 4)
        self.assertEqual(asgn.boat_availability, 4)

    def test_boat_availability_multiboat_case2(self):
        asgn1 = self.assign(self.slots[0], self.boatmaker(2))
        asgn2 = self.assign(self.slots[0], self.boatmaker(4))
        book = models.Booking.book_for(self.slots[0].pk, 3)
        self.assertEqual(book.assignment.timeslot.availability, 2)
        self.assertEqual(asgn1.boat_availability, 2)
        self.assertEqual(asgn2.boat_availability, 1)

    def test_boat_availability_multiboat_case3(self):
        asgn1 = self.assign(self.slots[0], self.boatmaker(2))
        asgn2 = self.assign(self.slots[0], self.boatmaker(4))
        book = models.Booking.book_for(self.slots[0].pk, 3)
        book = models.Booking.book_for(self.slots[0].pk, 2)
        self.assertEqual(book.assignment.timeslot.availability, 1)
        self.assertEqual(asgn1.boat_availability, 0)
        self.assertEqual(asgn2.boat_availability, 1)

    def conflicting_schedule(self, slot1, slot2, flip=False):
        boat = self.boatmaker(5)
        asgn1 = self.assign(slot1, boat)
        asgn2 = self.assign(slot2, boat)
        if flip:
            book1 = models.Booking.book_for(slot1.pk, 3)
        else:
            book1 = models.Booking.book_for(slot2.pk, 3)
        self.assertEqual(book1.assignment.timeslot.availability, 2)
        if flip:
            self.assertEqual(asgn2.boat_availability, 0)
            self.assertEqual(asgn1.boat_availability, 2)
        else:
            self.assertEqual(asgn2.boat_availability, 2)
            self.assertEqual(asgn1.boat_availability, 0)

    def test_boat_availability_conflicting_schedules_case1(self):
        self.conflicting_schedule(self.slots[0], self.slots[1])

    def test_boat_availability_conflicting_schedules_case2(self):
        self.conflicting_schedule(self.slots[0], self.slots[1], True)

    def test_boat_availability_conflicting_schedules_case3(self):
        self.conflicting_schedule(self.slots[1], self.slots[2])

    def test_boat_availability_conflicting_schedules_case4(self):
        self.conflicting_schedule(self.slots[1], self.slots[3])

    def test_boat_availability_conflicting_schedules_case5(self):
        self.conflicting_schedule(self.slots[2], self.slots[4])

    def test_boat_availability_edge_schedule(self):
        boat = self.boatmaker(5)
        asgn1 = self.assign(self.slots[1], boat)
        asgn2 = self.assign(self.slots[4], boat)
        book1 = models.Booking.book_for(self.slots[1].pk, 3)
        self.assertEqual(book1.assignment.timeslot.availability, 2)
        self.assertEqual(asgn2.boat_availability, 5)
        self.assertEqual(asgn1.boat_availability, 2)


class PingViewTests(TestCase):
    def test_returns_ok(self):
        resp = self.client.get(reverse('api:ping'))
        self.assertEqual(resp.status_code, 200)
        status = json.loads(resp.content).get('status')
        self.assertEqual(status, "OK")


class TimeslotsViewTests(TestCase):
    url = reverse('api:timeslots')

    def test_post_returns_new_slot_with_extra_attrs(self):
        resp = self.client.post(self.url, {
            'timeslot[start_time]': '1406052000',
            'timeslot[duration]': '120',
        })
        self.assertTrue(all(k in json.loads(resp.content)
                            for k in ('id', 'start_time', 'boats', 'availability')))

    def test_gets_timeslots_when_available(self):
        ts = models.Timeslot.objects.create(start_time=1414886400,
                                            end_time=1414886800)
        resp = self.client.get(self.url + '?date=2014-11-02')
        data = json.loads(resp.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['duration'], 6)

    def test_gets_empty_when_no_slot(self):
        resp = self.client.get(self.url + '?date=2039-01-01')
        data = json.loads(resp.content)
        self.assertEqual(len(json.loads(resp.content)), 0)

    def test_400s_without_date(self):
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 400)

    def test_400s_with_bad_date(self):
        resp = self.client.get(self.url + '?date=abc')
        self.assertEqual(resp.status_code, 400)


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


class BookingsViewTests(TestCase):
    url = reverse('api:bookings')

    def test_post_happy_path(self):
        ts = models.Timeslot.objects.create(start_time=1, end_time=2)
        bt = models.Boat.objects.create(capacity=10, name='Bubbles')
        asgn = models.Assignment.objects.create(boat=bt, timeslot=ts)

        resp = self.client.post(self.url, {
            'timeslot_id': ts.pk,
            'size': 8,
        })
        data = json.loads(resp.content)
        self.assertEqual(data['size'], 8)

    def test_post_cant_book_it(self):
        ts = models.Timeslot.objects.create(start_time=1, end_time=2)
        bt = models.Boat.objects.create(capacity=5, name='Salts')
        asgn = models.Assignment.objects.create(boat=bt, timeslot=ts)

        resp = self.client.post(self.url, {
            'timeslot_id': ts.pk,
            'size': 8,
        })
        data = json.loads(resp.content)
        self.assertEqual(resp.status_code, 409)
        self.assertTrue('error' in data)


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

    def test_duration_to_timestamp(self):
        self.assertEquals(util.duration_to_timestamp('10', '20'), 620)

    def test_timestamps_to_duration_minutes(self):
        self.assertEquals(util.timestamps_to_duration_minutes('120', '240'), 2)
