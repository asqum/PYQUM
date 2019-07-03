//when page is loading:
$(document).ready(function(){
    $('div.charcontent').hide();
});

//show F-Response's daylist
$(function() {
    $('button.char#fresp').bind('click', function() {
        $('div.charcontent').hide();
        $('div.charcontent#fresp').show();
        $('button.char').removeClass('selected');
        $('button.char#fresp').addClass('selected');
        $.getJSON('/mssn/char/fresp/init', {
            // operation: $('select.char#fresp[name="operation"]').val(),
            // ampstate: $('select.char#fresp[name="ampstate"]').val(),
            // powr: $('input.char#fresp[name="powr"]').val(),
            // freq: $('input.char#fresp[name="freq"]').val(),
            // ifb: $('input.char#fresp[name="ifb"]').val(),
            // comment: $('textarea.char#fresp[name="comment"]').val()
        }, function (data) {
            $('select.char#fresp[name="wday"]').empty();
            $('select.char#fresp[name="wday"]').append($('<option>', { text: 'pick a day', value: '' }));
            $('select.char#fresp[name="wday"]').append($('<option>', { text: '--New--', value: -1 }));
            $.each(data.daylist, function(i,v){
                $('select.char#fresp[name="wday"]').append($('<option>', {
                    text: v,
                    value: i
                }));
            });
        });
        return false;
    });
});

// list time based on day picked
$(function () {
    $('select.char#fresp[name="wday"]').on('change', function () {
        var wday = $('select.char#fresp[name="wday"]').val();
        console.log("Day Picked: " + wday);
        $.getJSON('/mssn/char/fresp/time', {
            wday: wday
        }, function (data) {
            $('select.char#fresp[name="wmoment"]').empty();
            $.each(data.startimes, function(i,v){
                $('select.char#fresp[name="wmoment"]').append($('<option>', {
                    text: v,
                    value: i+1
                }));
            });
        });
    });
});
// plot data based on time picked
$(function () {
    $('select.char#fresp[name="wmoment"]').on('change', function () {
        $.getJSON('/mssn/char/fresp/run', {
            // input/select value here:
            wmoment: $('select.char#fresp[name="wmoment"]').val()
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



 

    

