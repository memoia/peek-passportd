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

    def _update_availability(self):
        """set maximum space remaining on any associated boats"""
        assignments = Assignment.objects.filter(timeslot=self)
        self.availability = max(assgn.boat_availability for assgn in assignments)
        self.save()


class Assignment(AuditingModel):
    timeslot = models.ForeignKey(Timeslot)
    boat = models.ForeignKey(Boat)

    @property
    def boat_availability(self):
        return boat.capacity - reduce(
            lambda x, y: x + y.size,
            Booking.objects.filter(assignment=self), 0)


class Booking(AuditingModel):
    assignment = models.ForeignKey(Assignment)
    size = models.SmallIntegerField(null=False, blank=False, default=0)
    group_name = models.CharField(max_length=256, null=False, blank=False)

    def find_boat(self, timeslot_id):
        # identify an available boat that can accommodate size at given
        # timeslot, and create assignment if necessary.
        pass
