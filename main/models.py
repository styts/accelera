from django.db import models
import datetime
import time
import random


class Reading(models.Model):
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()

    timeStamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Reading, self).save(*args, **kwargs)

        # clean older entries
        if random.random() <= 0.01:
            Reading.objects.filter(timeStamp__lt=datetime.datetime.now()
                - datetime.timedelta(minutes=10)).delete()

    def ts(self):
        ms = time.mktime(self.timeStamp.timetuple()) + self.timeStamp.microsecond / 1000000.0
        return ms
