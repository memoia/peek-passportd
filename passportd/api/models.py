from django.db import models
from django.db.models import Q


class AuditingModel(models.Model):
    established = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class Boat(AuditingModel):
    capacity = models.SmallIntegerField(null=False, blank=False)
    name = models.CharField(max_length=128, blank=False, unique=True)


class Timeslot(AuditingModel):
    start_time = models.IntegerField(null=False, blank=False)  # good until 2038
    end_time = models.IntegerField(null=False, blank=False)
    boats = models.ManyToManyField(Boat, through='Assignment')

    @property
    def duration(self):
        return (int(self.end_time) - int(self.start_time)) / 60

    @property
    def customer_count(self):
        """sum of size for all bookings associated with this timeslot"""
        bookings = Booking.objects.filter(assignment__timeslot=self)
        return reduce(lambda x, y: x + y.size, bookings, 0)

    @property
    def availability(self):
        """return maximum space remaining on any associated boats"""
        assignments = Assignment.objects.filter(timeslot=self)
        return (max(assgn.boat_availability for assgn in assignments)
                if len(assignments)
                else 0)


class Assignment(AuditingModel):
    timeslot = models.ForeignKey(Timeslot)
    boat = models.ForeignKey(Boat)

    def save(self, *args, **kwargs):
        # if not self.pk:  # new record ; ensure no-overbooking?
        # todo: prevent assignment of same boat to more than one
        # timeslot within same period? can't; while assumptions
        # imply this requirement, test case 2 assumes this is
        # possible to do.
        super(Assignment, self).save(*args, **kwargs)

    @property
    def boat_availability(self):
        # if any overlapping slots have assignments that
        # use this boat (and have a booking), return 0.
        for slot in self.find_overlapping_slots():
            bookings = Booking.objects.filter(assignment__timeslot=slot)
            if not len(bookings):
                continue
            if self.boat in slot.boats.all():
                return 0

        return self.boat.capacity - reduce(
            lambda x, y: x + y.size,
            Booking.objects.filter(assignment=self), 0)

    @staticmethod
    def find_bookable(timeslot, booking_size):
        """Identify an available boat assignment that can accommodate
        size at given timeslot. Returns accommodating assignment with
        least remaining capacity."""
        assignments = Assignment.objects.filter(timeslot=timeslot)
        room_assgn = [(a.boat_availability, a) for a in assignments]
        available = filter(lambda r: r[0] >= booking_size, room_assgn)
        return min(available)[1] if len(available) else None

    def find_overlapping_slots(self):
        overlap = Timeslot.objects.filter(
            ~Q(pk=self.timeslot.pk),
            end_time__gte=self.timeslot.start_time,
            start_time__lt=self.timeslot.end_time)
        return overlap


class Booking(AuditingModel):
    assignment = models.ForeignKey(Assignment)
    size = models.SmallIntegerField(null=False, blank=False, default=0)

    @staticmethod
    def book_for(timeslot_id, group_size):
        ts = Timeslot.objects.get(pk=timeslot_id)
        asgn = Assignment.find_bookable(ts, group_size)
        if not asgn:
            raise ValueError("No available assignments")
        return Booking.objects.create(assignment=asgn, size=group_size)
