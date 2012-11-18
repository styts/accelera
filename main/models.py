from django.db import models
import datetime


class Reading(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    z = models.IntegerField()

    timeStamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Reading, self).save(*args, **kwargs)

        # clean older entries
        Reading.objects.filter(timeStamp__lt=datetime.datetime.now()
            - datetime.timedelta(minutes=1)).delete()
