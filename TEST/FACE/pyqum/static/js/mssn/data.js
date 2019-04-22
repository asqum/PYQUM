//when page is loading:
$(document).ready(function(){
    $('div.datacontent').hide();
});

//show temperature's page
$(function() {
    $('button.data#temperature').bind('click', function() {
        $('div.datacontent').hide();
        $('div.datacontent#temperature').show();
        $('button.data').removeClass('selected');
        $('button.data#temperature').addClass('selected');
        return false;
    });
});

//show history's page
$(function() {
    $('button.data#history').bind('click', function() {
        $('div.datacontent').hide();
        $('div.datacontent#history').show();
        $('button.data').removeClass('selected');
        $('button.data#history').addClass('selected');
        return false;
    });
});

$(function () {
    $('select.data#history').on('change', function () {
        var P_Ch = $('select.data[name="P_Ch"]').val();
        var T_Ch = $('select.data[name="T_Ch"]').val();
        var P_Ch2 = $('select.data[name="P_Ch2"]').val();
        var T_Ch2 = $('select.data[name="T_Ch2"]').val();
        $.getJSON('/mach/data/history', {
            // input value here:
            wday: $('select.data[name="wday"]').val(),
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
            
            Plotly.newPlot('data-chart-01', Trace, layout, {showSendToCloud: true});
            console.log(traceP.x);
            console.log(traceP.y);
            console.log(traceT.y);
            $('div.data#startP').empty();
            $('div.data#startP').append($('<h4 style="color: darkblue;"></h4>').text("starting: ")).
            append($('<span style="color: red;"></span>').text(data.startimeP));
            $('div.data#startT').empty();
            $('div.data#startT').append($('<h4 style="color: darkblue;"></h4>').text("starting: ")).
            append($('<span style="color: red;"></span>').text(data.startimeT));;
        });
        return false;
    });
});

//autoscale on submit (override input defaults)
$('input.data#autoscale').bind('click', function () {
    $( "i.data" ).remove(); //clear previous
    $('button.data#settings').prepend("<i class='data fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
    $.getJSON('/mach'+'/data/autoscale', {
    }, function (data) {
        $( "i.data" ).remove(); //clear previous
        $('input.data[name="rnge"]').val(data.yrange);
        $('input.data[name="scal"]').val(data.yscale);
        $('input.data[name="ofset"]').val(data.yoffset);
        $('input.data[name="rnge2"]').val(data.yrange2);
        $('input.data[name="scal2"]').val(data.yscale2);
        $('input.data[name="ofset2"]').val(data.yoffset2);
        $('input.data[name="trnge"]').val(data.trange);
        $('input.data[name="tdelay"]').val(data.tdelay);
        $('input.data[name="tscal"]').val(data.tscale);
    });
    return false;
});



 

    

