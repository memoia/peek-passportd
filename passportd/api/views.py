from dateutil import parser as dateparser
from restless.views import Endpoint
from restless.http import Http400
from restless.models import serialize

from api.models import Timeslot, Boat, Assignment
from api.util import prepare_record, date_bounds


class PingView(Endpoint):
    def get(self, request):
        return {"status": "OK"}


class TimeslotsView(Endpoint):
    # XXX customer_count and boats need to be returned, too

    def post(self, request):
        """Create a timeslot.

        {"timeslot[start_time]": start time of timeslot as unixtime,
         "timeslot[duration]": length of timeslot in minutes}
        """
        return serialize(Timeslot.objects.create(**prepare_record(request.data)))

    def get(self, request):
        """List timeslots.

        ?date: YYYY-MM-DD format for day to return timeslots
        """
        try:
            dt = dateparser.parse(request.params.get('date'))
        except:
            return Http400("date param missing or invalid format")
        match = dict(zip(('start_time__gte', 'start_time__lt'),
                         date_bounds(dt)))
        return serialize(Timeslot.objects.filter(**match))


class BoatsView(Endpoint):
    def post(self, request):
        """Create a boat.

        {"boat[capacity]": number of passengers boat can carry,
         "boat[name]": name of the boat}
        """
        return serialize(Boat.objects.create(**prepare_record(request.data)))

    def get(self, request):
        """List all boats."""
        return serialize(Boat.objects.all())


class AssignmentsView(Endpoint):
    def post(self, request):
        """Assign boat to timeslot.

        {"assignment[timeslot_id]": existing timeslot id,
         "assignment[boat_id]": existing boat id}
        """
        ids = prepare_record(request.data)
        ts = Timeslot.objects.get(pk=int(ids['timeslot_id']))
        boat = Boat.objects.get(pk=int(ids['boat_id']))
        return serialize(Assignment.objects.create(boat=boat, timeslot=ts))


class BookingsView(Endpoint):
    def post(self, request):
        """Create a booking.

        {"booking[timeslot_id]": existing timeslot id,
         "booking[size]": the size of the booking party}
        """
        rec = prepare_record(request.data)
        ts = Timeslot.objects.get(pk=int(rec['timeslot_id']))
        size = int(rec['size'])
        #return serialize(Assignment.objects.create(boat=boat, timeslot=ts))
        return Http400("not implemented")
