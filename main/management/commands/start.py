import serial
from datetime import datetime
from django.core.management.base import BaseCommand
from main.models import Reading

dev = '/dev/tty.usbmodemfa131'


class Command(BaseCommand):
    def handle(self, *args, **options):
        ser = serial.Serial(dev, 9600, timeout=2)
        ser.setRTS(True)
        ser.setRTS(False)
        while True:
            try:
                line = ser.readline()
                ts = datetime.now()
                l = line.split("\t")
                x, y, z = tuple(l)
                r = Reading(x=x, y=y, z=z, timeStamp=ts)
                r.save()
            except Exception, e:
                print e
        ser.close
