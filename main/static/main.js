var last_ts = "";
var data = {'x': [], 'y': [], 'z': [], 'ts': []};

function zip(arrays) {
    return arrays[0].map(function(_,i){
        return arrays.map(function(array){return array[i];
        });
    });
}

function foo(){
    dataurl = '/sse';

    $.ajax({
        url: dataurl,
        type: 'GET',
        dataType: 'json',
        success: onDataReceived
    });
}

function onDataReceived(series) {
    // last TS needed to fetch next series
    last_ts = series.ts[series.ts.length-1];

    // append new data to local storage
    data['x'] = data['x'].concat(series.x);
    data['y'] = data['y'].concat(series.y);
    data['z'] = data['z'].concat(series.z);
    data['ts'] = data['ts'].concat(series.ts);

    // remove "old" local storage (> 1m)
    k = 1000; //keep
    l = data.ts.length;
    data.ts = data.ts.slice(l-k, l);
    data.x = data.x.slice(l-k, l);
    data.y = data.y.slice(l-k, l);
    data.z = data.z.slice(l-k, l);

    $.plot($("#graph"),
        [
        {
            data: zip([data.ts, data.x]),
            label: 'x'
        },
        {
            data: zip([data.ts, data.y]),
            label: 'y'
        },
        {
            data: zip([data.ts, data.z]),
            label: 'z'
        }
        ],
        { xaxis: { mode: "time",
        minTickSize: [1, "millisecond"] }
    }
    );

    // poll().delay(300);
    setTimeout(foo, 50);
} // end of onDataReceived()


$(document).ready(function() {
    var source = new EventSource('/sse');

    source.addEventListener("result", function(e) {
        series = jQuery.parseJSON(e.data);

    // append new data to local storage
    data['x'] = data['x'].concat(series.x);
    data['y'] = data['y'].concat(series.y);
    data['z'] = data['z'].concat(series.z);
    data['ts'] = data['ts'].concat(series.ts);

    // remove "old" local storage (> 1m)
    k = 1000; //keep
    l = data.ts.length;
    data.ts = data.ts.slice(l-k, l);
    data.x = data.x.slice(l-k, l);
    data.y = data.y.slice(l-k, l);
    data.z = data.z.slice(l-k, l);

    $.plot($("#graph"),
        [
        {
            data: zip([data.ts, data.x]),
            label: 'x'
        },
        {
            data: zip([data.ts, data.y]),
            label: 'y'
        },
        {
            data: zip([data.ts, data.z]),
            label: 'z'
        }
        ],
        { xaxis: { mode: "time",
        minTickSize: [1, "millisecond"] }
    }
    );
});
});
