from dateutil import parser as dateparser
from restless.views import Endpoint
from restless.http import Http400
from restless.models import serialize

from api.models import Timeslot, Boat, Assignment, Booking
from api.util import prepare_record, date_bounds


class PingView(Endpoint):
    def get(self, request):
        return {"status": "OK"}


class TimeslotsView(Endpoint):
    all_fields = Timeslot._meta.get_all_field_names()

    def _augment(self, record):
        data = {}
        for k in self.all_fields:
            if hasattr(record, k):
                data[k] = getattr(record, k)
        data['customer_count'] = record.customer_count
        data['boats'] = [boat.pk for boat in record.boats.all()]
        return data

    def post(self, request):
        """Create a timeslot."""
        fields = ('start_time', 'duration')
        rec = prepare_record(request.data, fields)
        return serialize(self._augment(Timeslot.objects.create(**rec)))

    def get(self, request):
        """List timeslots. ?date: YYYY-MM-DD format."""
        try:
            dt = dateparser.parse(request.params.get('date'))
        except:
            return Http400("date param missing or invalid format")
        match = dict(zip(('start_time__gte', 'start_time__lt'),
                         date_bounds(dt)))
        return serialize([self._augment(rec) for rec in Timeslot.objects.filter(**match)])


class BoatsView(Endpoint):
    def post(self, request):
        """Create a boat."""
        fields = ('capacity', 'name')
        rec = prepare_record(request.data, fields)
        return serialize(Boat.objects.create(**rec))

    def get(self, request):
        """List all boats."""
        return serialize(Boat.objects.all())


class AssignmentsView(Endpoint):
    def post(self, request):
        """Assign boat to timeslot."""
        fields = ('timeslot_id', 'boat_id')
        ids = prepare_record(request.data, fields)
        ts = Timeslot.objects.get(pk=int(ids['timeslot_id']))
        boat = Boat.objects.get(pk=int(ids['boat_id']))
        return serialize(Assignment.objects.create(boat=boat, timeslot=ts))


class BookingsView(Endpoint):
    def post(self, request):
        """Create a booking."""
        fields = ('timeslot_id', 'size')
        rec = prepare_record(request.data, fields)
        tsid = int(rec['timeslot_id'])
        size = int(rec['size'])
        booking = Booking.book_for(tsid, size)
        return serialize(booking)
