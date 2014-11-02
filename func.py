import time
import unittest
import requests


class TestCases(unittest.TestCase):
    def case_1(self):
        """
        POST /api/timeslots, params={ start_time: 1406052000, duration: 120 }
        POST /api/boats, params={ capacity: 8, name: "Amazon Express" }
        POST /api/boats, params={ capacity: 4, name: "Amazon Express Mini" }
        POST /api/assignments, params={ timeslot_id: <timeslot-1-id>, boat_id: <boat-1-id> }
        POST /api/assignments, params={ timeslot_id: <timeslot-1-id>, boat_id: <boat-2-id> }
        GET /api/timeslots, params={ date: '2014-07-22' }
        ASSERT!
        [
          {
            id:  <timeslot-1-id>,
            start_time: 1406052000,
            duration: 120,
            availability: 8,
            customer_count: 0,
            boats: [<boat-1-id>, <boat-2-id>]
          }
        ]

        POST /api/bookings, params={ timeslot_id: <timeslot-1-id>, size: 6 }
        GET /api/timeslots, params={ date: "2014-07-22" }
        ASSERT!
        [
          {
            id:  <timeslot-1-id>,
            start_time: 1406052000,
            duration: 120,
            availability: 4,
            customer_count: 6,
            boats: [<boat-1-id>, <boat-2-id>]
          }
        ]
        """
        pass

    def case_2(self):
        """
        POST /api/timeslots, params={ start_time: 1406052000, duration: 120 }
        POST /api/timeslots, params={ start_time: 1406055600, duration: 120 }
        POST /api/boats, params={ capacity: 8, name: "Amazon Express" }
        POST /api/assignments, params={ timeslot_id: <timeslot-1-id>, boat_id: <boat-1-id> }
        POST /api/assignments, params={ timeslot_id: <timeslot-2-id>, boat_id: <boat-1-id> }
        GET /api/timeslots, params={ date: '2014-07-22' }
        ASSERT!
        [
          {
            id:  <timeslot-1-id>,
            start_time: 1406052000,
            duration: 120,
            availability: 8,
            customer_count: 0,
            boats: [<boat-1-id>]
          },
          {
            id:  <timeslot-2-id>,
            start_time: 1406055600,
            duration: 120,
            availability: 8,
            customer_count: 0,
            boats: [<boat-1-id>]
          }
        ]

        POST /api/bookings, params={ timeslot_id: <timeslot-2-id>, size: 2 }
        GET /api/timeslots, params={ date: '2014-07-22' }
        ASSERT!
        [
          {
            id:  <timeslot-1-id>,
            start_time: 1406052000,
            duration: 120,
            availability: 0,
            customer_count: 0,
            boats: [<boat-1-id>]
          },
          {
            id:  <timeslot-2-id>,
            start_time: 1406055600,
            duration: 120,
            availability: 6,
            customer_count: 2,
            boats: [<boat-1-id>]
          }
        ]
        """
        pass


if __name__ == "__main__":
    time.sleep(3)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCases)
    unittest.TextTestRunner(verbosity=2).run(suite)
