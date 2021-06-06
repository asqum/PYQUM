//when page is loading:
$(document).ready(function(){
    $('div.bdrcontent').hide();
    $("a.new#bdr-forecast-P").text('Forecast P');
    $("a.new#bdr-forecast-T").text('Forecast T');
    
});

function bdr_plot() {
    var P_Ch = $('select.bdr[name="P_Ch"]').val();
    var T_Ch = $('select.bdr[name="T_Ch"]').val();
    var P_Ch2 = $('select.bdr[name="P_Ch2"]').val();
    var T_Ch2 = $('select.bdr[name="T_Ch2"]').val();
    var OptS = $('select.bdr[name="OptS"]').val();
    var OptV = $('select.bdr[name="OptV"]').val();
    $("a.new#bdr-forecast-P").text('Forecast P' + P_Ch);
    $("a.new#bdr-forecast-T").text('Forecast T' + T_Ch);
    $.getJSON('/mach/bdr/history', {
        // input value here:
        designation: designation,
        wday: $('select.bdr[name="wday"]').val(),
        P_Ch: P_Ch, T_Ch: T_Ch, P_Ch2: P_Ch2, T_Ch2: T_Ch2, OptS: OptS, OptV: OptV
    }, function (data) {
        
        let traceP = {x: [], y: [], mode: 'lines', type: 'scatter', 
            name: 'P' + P_Ch,
            line: {color: 'green', width: 3} };
        let traceP2 = {x: [], y: [], mode: 'lines', type: 'scatter', 
            name: 'P' + P_Ch2,
            line: {color: 'blue', width: 3} };

        let traceT = {x: [], y: [], mode: 'lines', type: 'scatter', 
            name: 'T' + T_Ch,
            line: {color: 'brown', width: 3}, yaxis: 'y2' };
        let traceT2 = {x: [], y: [], mode: 'lines', type: 'scatter', 
            name: 'T' + T_Ch2,
            line: {color: 'red', width: 3}, yaxis: 'y2' };

        let traceOptS = {x: [], y: [], mode: 'lines', type: 'scatter', 
            name: 'OPT-S',
            line: {color: 'purple', width: 3}, yaxis: 'y3' };
        let traceOptV = {x: [], y: [], mode: 'markers', type: 'scatter', 
            name: 'OPT-V',
            marker: {color: [], colorscale: 'Viridis', size: 16}, yaxis: 'y5' };
        
        let layout = {
            legend: {x: 1.08},
            height: $(window).height()*0.8,
            width: $(window).width()*0.75,
            // margin: { b: 0, l: 0, r: 0, t: 0, pad: 2 },
            xaxis: {
                domain: [0.13, 0.88],
                zeroline: false,
                title: "<b>time(hr)</b>",
                titlefont: {size: 18},
                tickfont: {size: 18},
                tickwidth: 3,
                linewidth: 3,
                anchor: 'y1',
                gridcolor: 'rgb(159, 197, 232)',
                zerolinecolor: 'rgb(74, 134, 232)',
            },
            yaxis: {
                zeroline: false,
                title: "<b>P(mbar)</b><br>",
                titlefont: {size: 18},
                tickfont: {size: 18},
                tickwidth: 3,
                linewidth: 3,
                anchor: 'x1',
                gridcolor: 'rgb(159, 197, 232)',
                zerolinecolor: 'rgb(74, 134, 232)',
            },
            yaxis2: {
                zeroline: false,
                title: '<b>T(K)</b>', 
                titlefont: {color: 'rgb(148, 103, 189)', size: 18}, 
                tickfont: {color: 'rgb(148, 103, 189)', size: 18},
                tickwidth: 3,
                linewidth: 3, 
                overlaying: 'y', 
                side: 'right'
            },
            yaxis3: {
                zeroline: false,
                title: '<b>Option-S</b>', 
                titlefont: {color: 'purple', size: 18}, 
                tickfont: {color: 'purple', size: 18},
                tickwidth: 3,
                linewidth: 3, 
                overlaying: 'y', 
                side: 'right',
                position: 1
            },
            yaxis5: {
                zeroline: false,
                title: '<b>Option-V</b>', 
                titlefont: {color: 'grey', size: 18}, 
                tickfont: {color: 'grey', size: 18},
                tickwidth: 3,
                linewidth: 3, 
                overlaying: 'y', 
                side: 'left',
                position: 0.01
            },
            // title: '',
            annotations: [{
                xref: 'paper',
                yref: 'paper',
                x: 0.03,
                xanchor: 'right',
                y: 1.05,
                yanchor: 'bottom',
                text: '',
                font: {size: 18},
                showarrow: false,
                textangle: 0
                }]
            };
        
        $.each(data.tp, function(i, val) {traceP.x.push(val);});
        $.each(data.P, function(i, val) {traceP.y.push(val);});
        $.each(data.tt, function(i, val) {traceT.x.push(val);});
        $.each(data.T, function(i, val) {traceT.y.push(val);});

        $.each(data.tp2, function(i, val) {traceP2.x.push(val);});
        $.each(data.P2, function(i, val) {traceP2.y.push(val);});
        $.each(data.tt2, function(i, val) {traceT2.x.push(val);});
        $.each(data.T2, function(i, val) {traceT2.y.push(val);});

        $.each(data.tos, function(i, val) {traceOptS.x.push(val);});
        $.each(data.Opts, function(i, val) {traceOptS.y.push(val);});
        $.each(data.tov, function(i, val) {traceOptV.x.push(val);});
        $.each(data.Optv, function(i, val) {traceOptV.y.push(val);});
        $.each(data.Optv, function(i, val) {traceOptV.marker.color.push(val);});

        Trace = [traceP, traceT, traceP2, traceT2, traceOptS, traceOptV]; //.concat([]);
        
        Plotly.newPlot('bdr-chart-01', Trace, layout, {showSendToCloud: true});
        console.log(traceP.y[traceP.y.length-1]);
        console.log(traceT.y[traceT.y.length-1]);
        console.log(traceOptV.y[traceOptV.y.length-1]);

        // adjusting number representation:
        var P_current = data.P[data.P.length-1];
        if (Math.log(P_current) / Math.LN10 < 0) { P_current = P_current.toExponential(); };
        var T_current = data.T[data.T.length-1];
        if (Math.log(T_current) / Math.LN10 < 0) { T_current = (T_current*1000).toFixed(2) + "m"; };
        console.log("T Need exponential: " + (Math.log(T_current) / Math.LN10 < 0));
        var P_current2 = data.P2[data.P2.length-1];
        if (Math.log(P_current2) / Math.LN10 < 0) { P_current2 = P_current2.toExponential(); };
        var T_current2 = data.T2[data.T2.length-1];
        if (Math.log(T_current2) / Math.LN10 < 0) { T_current2 = (T_current2*1000).toFixed(2) + "m"; };
        var OptS_current = data.Opts[data.Opts.length-1];
        if (Math.log(OptS_current) / Math.LN10 < -2) { OptS_current = OptS_current.toExponential(); };
        var OptV_current = data.Optv[data.Optv.length-1];
        // if (Math.log(OptV_current) / Math.LN10 < -2) { OptV_current = OptV_current.toExponential(); };

        // adjusting precision:
        try{ if (P_current.toString().split(".")[1].length > 3) {  P_current = P_current.toFixed(3); }; } catch(e) {};
        try{ if (P_current2.toString().split(".")[1].length > 3) {  P_current2 = P_current2.toFixed(3); }; } catch(e) {};
        try{ if (T_current.toString().split(".")[1].length > 3) {  T_current = T_current.toFixed(3); }; } catch(e) {};
        try{ if (T_current2.toString().split(".")[1].length > 3) {  T_current2 = T_current2.toFixed(3);  }; } catch(e) {};
        try{ if (OptS_current.toString().split(".")[1].length > 3) {  OptS_current = OptS_current.toFixed(3); }; } catch(e) {};
        // try{ if (OptV_current.toString().split(".")[1].length > 3) {  OptV_current = OptV_current.toFixed(3); }; } catch(e) {};

        // For Pressure
        $('div.bdr#P_recent').empty();
        $('div.bdr#P_recent').//append($('<h4 style="color: darkblue;"></h4>').text("Latest: ")).
        append($('<h4 style="color: red;"></h4>').text(P_current + "mbar"));
        $('div.bdr#P_recent2').empty();
        $('div.bdr#P_recent2').//append($('<h4 style="color: darkblue;"></h4>').text("Latest: ")).
        append($('<h4 style="color: red;"></h4>').text(P_current2 + "mbar"));
        
        // For Temperature
        $('div.bdr#T_recent').empty();
        $('div.bdr#T_recent').//append($('<h4 style="color: darkblue;"></h4>').text("Latest: ")).
        append($('<h4 style="color: red;"></h4>').text(T_current + "K"));
        $('div.bdr#T_recent2').empty();
        $('div.bdr#T_recent2').//append($('<h4 style="color: darkblue;"></h4>').text("Latest: ")).
        append($('<h4 style="color: red;"></h4>').text(T_current2 + "K"));

        // For Option
        $('div.bdr#OptS_recent').empty();
        $('div.bdr#OptS_recent').//append($('<h4 style="color: darkblue;"></h4>').text("Latest: ")).
        append($('<h4 style="color: red;"></h4>').text(OptS_current));
        $('div.bdr#OptV_recent').empty();
        $('div.bdr#OptV_recent').//append($('<h4 style="color: darkblue;"></h4>').text("Latest: ")).
        append($('<h4 style="color: red;"></h4>').text(OptV_current));

        // access sessions:
        // console.log("User: " + $.session.get('abc'));
    });
    return false;
};

//show history's page and load Days
$(function() {
    $('button.bdr.history').bind('click', function() {
        window.designation = $(this).attr('id');
        $('div.bdrcontent').hide();
        $('div.bdrcontent#history').show();
        $('button.bdr').removeClass('selected');
        $('button.bdr.history#' + designation).addClass('selected');
        $.getJSON('/mach/bdr/init', {
            designation: designation
        }, function (data) {
            // Select Day:
            $('select.bdr#history[name="wday"]').empty();
            $('select.bdr#history[name="wday"]').append($('<option>', { text: 'Currently:', value: '' }));
            $.each(data.Days.reverse(), function(i,v){
                $('select.bdr#history[name="wday"]').append($('<option>', {
                    text: v,
                    value: data.Days.length - 1 - i
                }));
            });
            // Compare Day:
            $('select.bdr#history[name="compareday"]').empty();
            $('select.bdr#history[name="compareday"]').append($('<option>', { text: 'Compared:', value: '' }));
            $.each(data.Days.reverse(), function(i,v){
                $('select.bdr#history[name="compareday"]').append($('<option>', {
                    text: v,
                    value: data.Days.length - 1 - i
                }));
            });
        });
        return false;
    });
});
// manual update
$(function () {
    $('select.bdr#history').on('change', function () {
        bdr_plot();
    });
});
// live update
$(function () {
    $('input.bdr#live-update').click(function () { 
        var livestat = $('input.bdr#live-update').is(':checked'); //use css to respond to click / touch
        if (livestat == true) {
            bdr_plot();
            //indicate it is still running:
            $( "i.bdr" ).remove(); //clear previous
            console.log("LIVE ON " + designation);
            $('button.bdr.history#' + designation).prepend("<i class='bdr fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
            var bdrloop = setInterval(bdr_plot, 15000);
            $('input.bdr#live-update').click(function () {
                clearInterval(bdrloop); 
                $( "i.bdr" ).remove(); //clear previous
            });
        };
        // 'else' didn't do much to stop it!
    });
});
// Forecast P
$("a.new#bdr-forecast-P").bind('click', function() {
    $.getJSON('/mach/bdr/history/forecast', {
        target: $('input.bdr#history[name="forecast"]').val(),
        predicting: "P"
    }, function (data) {
        $("a.new#bdr-forecast-P").text('ETA in >' + String(data.eta_time) + ' hours');
    });
});
// Forecast T
$("a.new#bdr-forecast-T").bind('click', function() {
    $.getJSON('/mach/bdr/history/forecast', {
        target: $('input.bdr#history[name="forecast"]').val(),
        predicting: "T"
    }, function (data) {
        $("a.new#bdr-forecast-T").text('ETA in >' + String(data.eta_time) + ' hours');
    });
});

// Samples-Allocation by Management:
$(function() {
    $('button.bdr#samples').bind('click', function() {
        $('div.bdrcontent').hide();
        $('div.bdrcontent#samples').show();
        $('button.bdr').removeClass('selected');
        $('button.bdr#samples').addClass('selected');
        // QUEUE SYSTEMS:
        $('table.BDR-QUEUE thead.samples.bdr-queue-update tr').empty();
        $('table.BDR-QUEUE tbody.samples.bdr-queue-update tr').empty();
        $.getJSON('/mach/bdr/samples/queues', { }, function (data) {
            $.each(data.bdrqlist, function (i,val) {
                $('table.BDR-QUEUE thead.samples.bdr-queue-update tr').append('<th>' + val.system + '</th>');
                $('table.BDR-QUEUE tbody.samples.bdr-queue-update tr').append('<td>' + val.samplename + '</td>');
            });
            
        });
        
        return false;
    });
});
$(function() {
    $('select.bdr.samples-allocation').on('change', function() {
        var set_system = $(this).attr('id').split('-')[1];
        $.getJSON('/mach/bdr/samples/allocate', {
            set_system: set_system,
            set_sample: $('select.bdr.samples-allocation.' + set_system).val(),
         }, function (data) {
            setTimeout(() => { $('button.bdr#samples').trigger('click'); }, 100);

        });

        return false;
    });
});

//show wiring's page
$(function() {
    $('button.bdr#wiring').bind('click', function() {
        $('div.bdrcontent').hide();
        $('div.bdrcontent#wiring').show();
        $('button.bdr').removeClass('selected');
        $('button.bdr#wiring').addClass('selected');
        return false;
    });
});

// Plotly Chart
// var trace1 = {
//     x: [1, 2, 3, 4, 5],
//     y: [1, 6, 3, 6, 1],
//     mode: 'markers',
//     type: 'scatter',
//     name: 'Team A',
//     text: ['A-1', 'A-2', 'A-3', 'A-4', 'A-5'],
//     marker: { size: 12 }
//     };
    
// var trace2 = {
//     x: [1.5, 2.5, 3.5, 4.5, 5.5],
//     y: [4, 1, 7, 1, 4],
//     mode: 'markers',
//     type: 'scatter',
//     name: 'Team B',
//     text: ['B-a', 'B-b', 'B-c', 'B-d', 'B-e'],
//     marker: { size: 12 }
//     };



    

