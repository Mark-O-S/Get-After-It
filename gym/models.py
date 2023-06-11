from django.db import models
from django.contrib.auth.models import User


class PersonalTraining(models.Model):
    """
    Defines personal training object
    """

    available = models.BooleanField(null=False, blank=False, default=True)
    booked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                  blank=True, related_name="booked_by")
    date_time = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return str(self.date_time)

    class Meta:
        ordering = ('date_time',)
