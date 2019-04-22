//when page is loading:
$(document).ready(function(){
    $('div.charcontent').hide();
});

//show RT Amp's page
$(function() {
    $('button.char#rtamp').bind('click', function() {
        $('div.charcontent').hide();
        $('div.charcontent#rtamp').show();
        $('button.char').removeClass('selected');
        $('button.char#rtamp').addClass('selected');
        return false;
    });
});
// list day based on operation type
$(function () {
    $('select.char#rtamp[name="operation"]').on('change', function () {
        $.getJSON('/mssn/char/rtamp/init', {
            operation: $('select.char#rtamp[name="operation"]').val(),
            ampstate: $('select.char#rtamp[name="ampstate"]').val(),
            powr: $('input.char#rtamp[name="powr"]').val(),
            freq: $('input.char#rtamp[name="freq"]').val(),
            ifb: $('input.char#rtamp[name="ifb"]').val(),
            comment: $('textarea.char#rtamp[name="comment"]').val()
        }, function (data) {
            $('select.char#rtamp[name="wday"]').empty();
            $.each(data.dayslot, function(i,v){
                $('select.char#rtamp[name="wday"]').append($('<option>', {
                    text: v,
                    value: i
                }));
            });
        });
    });
});
// list time based on day picked
$(function () {
    $('select.char#rtamp[name="wday"]').on('change', function () {
        $.getJSON('/mssn/char/rtamp/time', {
            wday: $('select.char#rtamp[name="wday"]').val()
        }, function (data) {
            $('select.char#rtamp[name="wmoment"]').empty();
            $.each(data.timeslot, function(i,v){
                $('select.char#rtamp[name="wmoment"]').append($('<option>', {
                    text: v,
                    value: i+1
                }));
            });
        });
    });
});
// plot data based on time picked
$(function () {
    $('select.char#rtamp[name="wmoment"]').on('change', function () {
        $.getJSON('/mssn/char/rtamp/run', {
            // input/select value here:
            wmoment: $('select.char#rtamp[name="wmoment"]').val()
        }, function (data) {
            console.log(data.Idata);
            
            let traceI = {x: [], y: [], mode: 'lines', type: 'scatter', 
                name: 'I (' + wday + ', ' + wmoment + ')',
                line: {color: 'rgb(23, 151, 6)', width: 3} };
            let traceQ = {x: [], y: [], mode: 'lines', type: 'scatter', 
                name: 'Q (' + wday + ', ' + wmoment + ')',
                line: {color: 'blue', width: 3} };

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
            
            Plotly.newPlot('char-chart-01', Trace, layout, {showSendToCloud: true});
            console.log(traceP.x);
            console.log(traceP.y);
            console.log(traceT.y);
            $('div.char#startP').empty();
            $('div.char#startP').append($('<h4 style="color: darkblue;"></h4>').text("starting: ")).
            append($('<span style="color: red;"></span>').text(data.startimeP));
            $('div.char#startT').empty();
            $('div.char#startT').append($('<h4 style="color: darkblue;"></h4>').text("starting: ")).
            append($('<span style="color: red;"></span>').text(data.startimeT));;
        });
        return false;
    });
});

//autoscale on submit (override input defaults)
$('input.char#autoscale').bind('click', function () {
    $( "i.char" ).remove(); //clear previous
    $('button.char#settings').prepend("<i class='char fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
    $.getJSON('/mssn'+'/char/autoscale', {
    }, function (data) {
        $( "i.char" ).remove(); //clear previous
        $('input.char[name="rnge"]').val(data.yrange);
        $('input.char[name="scal"]').val(data.yscale);
        $('input.char[name="ofset"]').val(data.yoffset);
        $('input.char[name="rnge2"]').val(data.yrange2);
        $('input.char[name="scal2"]').val(data.yscale2);
        $('input.char[name="ofset2"]').val(data.yoffset2);
        $('input.char[name="trnge"]').val(data.trange);
        $('input.char[name="tdelay"]').val(data.tdelay);
        $('input.char[name="tscal"]').val(data.tscale);
    });
    return false;
});



 

    

