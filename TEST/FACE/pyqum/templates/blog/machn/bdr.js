//when page is loading:
$(document).ready(function(){
    $('div.bdrcontent').hide();
});

//show history's page
$(function() {
    $('button.bdr#history').bind('click', function() {
        $('div.bdrcontent').hide();
        $('div.bdrcontent#history').show();
        $('button.bdr').removeClass('selected');
        $('button.bdr#history').addClass('selected');
        return false;
    });
});
$(function () {
    $('select.bdr#history').on('change', function () {
        var P_Ch = $('select.bdr[name="P_Ch"]').val();
        var T_Ch = $('select.bdr[name="T_Ch"]').val();
        var P_Ch2 = $('select.bdr[name="P_Ch2"]').val();
        var T_Ch2 = $('select.bdr[name="T_Ch2"]').val();
        $.getJSON('/mach/bdr/history', {
            // input value here:
            wday: $('select.bdr[name="wday"]').val(),
            P_Ch: P_Ch, T_Ch: T_Ch, P_Ch2: P_Ch2, T_Ch2: T_Ch2
        }, function (data) {
            
            let traceP = {x: [], y: [], mode: 'lines', type: 'scatter', 
                name: 'P' + P_Ch,
                line: {color: 'rgb(23, 151, 6)', width: 3} };
            let traceP2 = {x: [], y: [], mode: 'lines', type: 'scatter', 
                name: 'P' + P_Ch2,
                line: {color: 'blue', width: 3} };

            let traceT = {x: [], y: [], mode: 'lines', type: 'scatter', 
                name: 'T' + T_Ch,
                line: {color: 'brown', width: 3}, yaxis: 'y2' };
            let traceT2 = {x: [], y: [], mode: 'lines', type: 'scatter', 
                name: 'T' + T_Ch2,
                line: {color: 'red', width: 3}, yaxis: 'y2' };
            
            let layout = {
                legend: {x: 1.08},
                height: $(window).height()*0.8,
                width: $(window).width()*0.75,
                xaxis: {
                    zeroline: false,
                    title: "<b>time(hr)</b>",
                    titlefont: {size: 18},
                    tickfont: {size: 18},
                    tickwidth: 3,
                    linewidth: 3 
                },
                yaxis: {
                    zeroline: false,
                    //title: "<b>P(mbar)</b><br>",
                    titlefont: {size: 18},
                    tickfont: {size: 18},
                    tickwidth: 3,
                    linewidth: 3
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
                title: '',
                annotations: [{
                    xref: 'paper',
                    yref: 'paper',
                    x: 0.03,
                    xanchor: 'right',
                    y: 1.05,
                    yanchor: 'bottom',
                    text: '<b>P(mbar)</b>',
                    font: {size: 18},
                    showarrow: false,
                    textangle: 0
                  }]
                };
            
            $.each(data.tp, function(i, val) {traceP.x.push(val);});
            $.each(data.P, function(i, val) {traceP.y.push(val);});
            $.each(data.tt, function(i, val) {traceT.x.push(val);});
            $.each(data.T, function(i, val) {traceT.y.push(val);});
            if (P_Ch2 > 0 && T_Ch2 > 0) {
                $.each(data.tp2, function(i, val) {traceP2.x.push(val);});
                $.each(data.P2, function(i, val) {traceP2.y.push(val);});
                $.each(data.tt2, function(i, val) {traceT2.x.push(val);});
                $.each(data.T2, function(i, val) {traceT2.y.push(val);});
                var Trace = [traceP, traceT].concat([traceP2, traceT2]);
            } else if (P_Ch2 > 0) {
                $.each(data.tp2, function(i, val) {traceP2.x.push(val);});
                $.each(data.P2, function(i, val) {traceP2.y.push(val);});
                var Trace = [traceP, traceT].concat([traceP2]);
            } else if (T_Ch2 > 0) {
                $.each(data.tt2, function(i, val) {traceT2.x.push(val);});
                $.each(data.T2, function(i, val) {traceT2.y.push(val);});
                var Trace = [traceP, traceT].concat([traceT2]);
            } else {
                var Trace = [traceP, traceT]
            };
            
            Plotly.newPlot('bdr-chart-01', Trace, layout, {showSendToCloud: true});
            console.log(traceP.x);
            console.log(traceP.y);
            console.log(traceT.y);
            $('div.bdr#startP').empty();
            $('div.bdr#startP').append($('<h4 style="color: darkblue;"></h4>').text("starting: ")).
            append($('<span style="color: red;"></span>').text(data.startimeP));
            $('div.bdr#startT').empty();
            $('div.bdr#startT').append($('<h4 style="color: darkblue;"></h4>').text("starting: ")).
            append($('<span style="color: red;"></span>').text(data.startimeT));;
        });
        return false;
    });
});

//autoscale on submit (override input defaults)
$('input.bdr#autoscale').bind('click', function () {
    $( "i.bdr" ).remove(); //clear previous
    $('button.bdr#settings').prepend("<i class='bdr fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
    $.getJSON('/mach'+'/bdr/autoscale', {
    }, function (data) {
        $( "i.bdr" ).remove(); //clear previous
        $('input.bdr[name="rnge"]').val(data.yrange);
        $('input.bdr[name="scal"]').val(data.yscale);
        $('input.bdr[name="ofset"]').val(data.yoffset);
        $('input.bdr[name="rnge2"]').val(data.yrange2);
        $('input.bdr[name="scal2"]').val(data.yscale2);
        $('input.bdr[name="ofset2"]').val(data.yoffset2);
        $('input.bdr[name="trnge"]').val(data.trange);
        $('input.bdr[name="tdelay"]').val(data.tdelay);
        $('input.bdr[name="tscal"]').val(data.tscale);
    });
    return false;
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

//show warmup's page
$(function() {
    $('button.bdr#warmup').bind('click', function() {
        $('div.bdrcontent').hide();
        $('div.bdrcontent#warmup').show();
        $('button.bdr').removeClass('selected');
        $('button.bdr#warmup').addClass('selected');
        return false;
    });
});

    

