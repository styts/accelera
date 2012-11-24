from django.core.management.base import BaseCommand

import serial
from datetime import datetime
from main.models import Reading

dev = '/dev/tty.usbmodemfa131'


class Reader(object):
    def __init__(self):
        ser = serial.Serial(dev, 57600, timeout=2)
        ser.setRTS(True)
        ser.setRTS(False)
        while True:
            try:
                line = ser.readline()
                # print line
                ts = datetime.now()
                l = line.split("\t")
                x, y, z = tuple(l)
                r = Reading(x=x, y=y, z=z, timeStamp=ts)
                r.save()
            except Exception:
                pass
        ser.close


class Command(BaseCommand):
    def handle(self, *args, **options):
        Reader()
