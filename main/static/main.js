var last_ts = "";
var data = {'x': [], 'y': [], 'z': [], 'ts': []};
var log = [];

function zip(arrays) {
    return arrays[0].map(function(_,i){
        return arrays.map(function(array){return array[i];
        });
    });
}

function log_data(data){
    // console.log(data);
    // log.push("<span>"+data.x+"</span></br>");
    // $("#log").prepend(log);
    $("#val_x").text(data.x);
    $("#val_y").text(data.y);
    $("#val_z").text(data.z);
}

$(document).ready(function() {
    var source = new EventSource('/sse');

    // setup plot
    var options = {
        yaxis: { min: -90, max: 90 },
        xaxis: { mode: "time", minTickSize: [1, "millisecond"] },
        series: { shadowSize: 0 } // drawing is faster without shadows
    };
    var plot = $.plot($("#graph"), [[1, 0]], options);

    source.addEventListener("result", function(e) {
        series = jQuery.parseJSON(e.data);
        log_data(series);
        // return;

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
        // if (Math.random() > 0){
            plot.setupGrid();
        // }
        plot.draw();
});
});
