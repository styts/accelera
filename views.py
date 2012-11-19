from django.shortcuts import render
from django.http import HttpResponse
import simplejson
from main.models import Reading
import datetime


def home(request):
    return render(request, 'index.html')


def data(request):
    ts = request.GET['ts'] if "ts" in request.GET else ""
    if ts == "":
        ts = datetime.datetime.now() - datetime.timedelta(seconds=2)
    else:
        ts = datetime.datetime.fromtimestamp(float(ts))

    result = {
     'x': [], 'y': [], 'z': [], 'ts': [],
    }
    for r in Reading.objects.filter(timeStamp__gt=ts):
        result['x'].append(r.x)
        result['y'].append(r.y)
        result['z'].append(r.z)
        result['ts'].append(r.ts())

    data = simplejson.dumps(result)
    return HttpResponse(data, mimetype='application/json')
