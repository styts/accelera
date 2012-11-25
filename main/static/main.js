var last_ts = "";
var data = {'x': [], 'y': [], 'z': [], 'ts': []};

function zip(arrays) {
    return arrays[0].map(function(_,i){
        return arrays.map(function(array){return array[i];
        });
    });
}

$(document).ready(function() {
    var source = new EventSource('/sse');

    // setup plot
    var options = {
        yaxis: { min: -100, max: 100 },
        xaxis: { mode: "time", minTickSize: [1, "millisecond"] },
        series: { shadowSize: 0 } // drawing is faster without shadows
    };
    var plot = $.plot($("#graph"), [[1, 0]], options);

    source.addEventListener("result", function(e) {
        series = jQuery.parseJSON(e.data);

    // append new data to local storage
    data['x'] = data['x'].concat(jQuery.parseJSON(series.x));
    data['y'] = data['y'].concat(jQuery.parseJSON(series.y));
    data['z'] = data['z'].concat(jQuery.parseJSON(series.z));
    data['ts'] = data['ts'].concat(series.ts);

    // remove "old" local storage (> 1m)
    k = 200; //keep
    l = data.ts.length;
    data.ts = data.ts.slice(l-k, l);
    data.x = data.x.slice(l-k, l);
    data.y = data.y.slice(l-k, l);
    data.z = data.z.slice(l-k, l);

    plot.setData(
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
        ]
        );
    plot.setupGrid();
    plot.draw();
});
});
