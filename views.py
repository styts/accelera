from django.shortcuts import render
from django.http import HttpResponse
import simplejson
from main.models import Reading
import datetime
from django_sse.views import BaseSseView
from django.utils.timezone import now
import time


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


def data(request):
    ts = request.GET['ts'] if "ts" in request.GET else ""
    if ts == "" or ts == "undefined":
        ts = datetime.datetime.now() - datetime.timedelta(seconds=2)
    else:
        ts = datetime.datetime.fromtimestamp(float(ts))

    result = get_result(ts)

    data = simplejson.dumps(result)
    return HttpResponse(data, mimetype='application/json')

# class MySseEvents(BaseSseView):
#     pass


class MySseEvents(BaseSseView):
    last_ts = now()

    def iterator(self):
        while True:
            result = get_result(MySseEvents.last_ts)
            self.sse.add_message("result", simplejson.dumps(result))
            MySseEvents.last_ts = now()
            time.sleep(1)
            yield
