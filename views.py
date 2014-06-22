from django.shortcuts import render
import simplejson
from main.models import Reading
from django_sse.views import BaseSseView
import time
import serial

# dev = '/dev/tty.usbmodemfa131'
dev = '/dev/tty.usbmodemfd121'
BITRATE = 9600


def home(request):
    return render(request, 'index.html')


def get_result(last_ts):
    result = {
     'x': [], 'y': [], 'z': [], 'ts': [],
    }
    for r in Reading.objects.filter(timeStamp__gte=last_ts):
        result['x'].append(r.x)
        result['y'].append(r.y)
        result['z'].append(r.z)
        result['ts'].append(r.ts())
    return result


class MySseEvents(BaseSseView):
    def iterator(self):
        ser = serial.Serial(dev, BITRATE, timeout=2)
        ser.setRTS(True)
        ser.setRTS(False)
        line = ""
        while True:
            try:
                line = ser.readline().strip('\r\n')
                if line == "" or line == ['\n'] or line == "\n":
                    continue
                line = line.split('\t')
                x, y, z = tuple(line)
                result = {
                    "x": x,
                    "y": y,
                    "z": z.strip(),
                    "ts": time.time(),
                }
                s = simplejson.dumps(result)
                time.sleep(0.003)
                self.sse.add_message("result", s)
                yield
            except ValueError:
                print line
            finally:
                ser.close
