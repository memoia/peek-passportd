from django.db import models


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
    duration = models.SmallIntegerField(null=False, blank=False)
    availability = models.IntegerField(null=False, blank=False, default=0)
    boats = models.ManyToManyField(Boat, through='Assignment')

    @property
    def customer_count(self):
        """sum of size for all bookings associated with this timeslot"""
        bookings = Booking.objects.filter(assignment__timeslot=self)
        return reduce(lambda x, y: x + y.size, bookings, 0)

    def update_availability(self):
        """set maximum space remaining on any associated boats"""
        assignments = Assignment.objects.filter(timeslot=self)
        self.availability = max(assgn.boat_availability for assgn in assignments)
        self.save()


class Assignment(AuditingModel):
    timeslot = models.ForeignKey(Timeslot)
    boat = models.ForeignKey(Boat)

    def save(self, *args, **kwargs):
        if not self.pk:  # new record
            # TODO ensure a boat isn't used in more than
            # one timeslot for any given time; this needs
            # to return an error.
            pass
        super(Assignment, self).save(*args, **kwargs)
        self.timeslot.update_availability()

    @property
    def boat_availability(self):
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
        return min(available)[1]


class Booking(AuditingModel):
    assignment = models.ForeignKey(Assignment)
    size = models.SmallIntegerField(null=False, blank=False, default=0)
    group_name = models.CharField(max_length=256, null=False, blank=False,
                                  default='Unknown')

    @staticmethod
    def book_for(timeslot_id, group_size):
        ts = Timeslot.objects.get(pk=timeslot_id)
        asgn = Assignment.find_bookable(ts, group_size)
        bk = Booking.objects.create(assignment=asgn, size=group_size)
        ts.update_availability()
        return bk
