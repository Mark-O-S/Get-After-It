from django.db import models

class PersonalTraining(models.Model):
    """ 
    Defines personal training object
    """
    available = models.BooleanField(null=False, blank=False, default=True)
    user_id = models.CharField(max_length=50, null=True, blank=True)
    date_time = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return self.date_time
