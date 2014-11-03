import time
import unittest
import requests


SERVICE = 'http://localhost:3000/api'


def url(ep):
    return '{}/{}'.format(SERVICE, ep)

def post(ep, **params):
    return requests.post(url(ep), data=params).json()

def get(ep, **params):
    return requests.get(url(ep), params=params).json()


class TestCases(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b1 = post('boats', capacity=8, name="Amazon Express")
        cls.b2 = post('boats', capacity=4, name="Amazon Express Mini")

    def test_case_1(self):
        ts = post('timeslots', start_time=1406052000, duration=120)
        an1 = post('assignments', timeslot_id=ts['id'], boat_id=self.b1['id'])
        an2 = post('assignments', timeslot_id=ts['id'], boat_id=self.b2['id'])
        result = get('timeslots', date='2014-07-22')
        self.assertDictContainsSubset({
            'id': ts['id'],
            'start_time': 1406052000,
            'duration': 120,
            'availability': 8,
            'customer_count': 0,
            'boats': [self.b1['id'], self.b2['id']]
        }, result[0])

        bk = post('bookings', timeslot_id=ts['id'], size=6)
        result = get('timeslots', date="2014-07-22")
        self.assertDictContainsSubset({
            'id': ts['id'],
            'start_time': 1406052000,
            'duration': 120,
            'availability': 4,
            'customer_count': 6,
            'boats': [self.b1['id'], self.b2['id']]
        }, result[0])


    def test_case_2(self):
        ts1 = post('timeslots', start_time=1414904400, duration=120)
        ts2 = post('timeslots', start_time=1414908000, duration=120)
        an1 = post('assignments', timeslot_id=ts1['id'], boat_id=self.b1['id'])
        an2 = post('assignments', timeslot_id=ts2['id'], boat_id=self.b1['id'])
        result = get('timeslots', date='2014-11-02')
        self.assertDictContainsSubset({
            'id': ts1['id'],
            'start_time': 1414904400,
            'duration': 120,
            'availability': 8,
            'customer_count': 0,
            'boats': [self.b1['id']]
        }, result[0])
        self.assertDictContainsSubset({
            'id': ts2['id'],
            'start_time': 1414908000,
            'duration': 120,
            'availability': 8,
            'customer_count': 0,
            'boats': [self.b1['id']]
        }, result[1])

        bk1 = post('bookings', timeslot_id=ts2['id'], size=2)
        result = get('timeslots', date='2014-11-02')
        self.assertDictContainsSubset({
            'id': ts1['id'],
            'start_time': 1414904400,
            'duration': 120,
            'availability': 0,
            'customer_count': 0,
            'boats': [self.b1['id']]
        }, result[0])
        self.assertDictContainsSubset({
            'id': ts2['id'],
            'start_time': 1414908000,
            'duration': 120,
            'availability': 6,
            'customer_count': 2,
            'boats': [self.b1['id']]
        }, result[1])


if __name__ == "__main__":
    time.sleep(3)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCases)
    unittest.TextTestRunner(verbosity=2).run(suite)
