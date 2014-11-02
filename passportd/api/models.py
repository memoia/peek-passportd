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

    def customer_count(self):
        # return sum of size for all bookings associated with this timeslot
        pass


class Assignment(AuditingModel):
    timeslot = models.ForeignKey(Timeslot)
    boat = models.ForeignKey(Boat)


class Booking(AuditingModel):
    assignment = models.ForeignKey(Assignment)
    size = models.SmallIntegerField(null=False, blank=False, default=0)
    group_name = models.CharField(max_length=256, null=False, blank=False)

    def find_boat(self, timeslot_id):
        # identify an available boat that can accommodate size at given
        # timeslot, and create assignment if necessary.
        pass
