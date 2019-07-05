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
        // Make global variable:
        window.wday = $('select.char#fresp[name="wday"]').val();
        console.log("Day Picked: " + wday);
        $.getJSON('/mssn/char/fresp/time', {
            wday: wday
        }, function (data) {
            $('select.char#fresp[name="wmoment"]').empty().append($('<option>', { text: 'pick', value: '' }));
            $.each(data.taskentries, function(i,v){ $('select.char#fresp[name="wmoment"]').append($('<option>', { text: v, value: i+1 })); });
        });
    });
});

// access data based on time picked
$(function () {
    $('select.char#fresp[name="wmoment"]').on('change', function () {
        // Make global variable:
        window.wmoment = $('select.char#fresp[name="wmoment"]').val();
        $.getJSON('/mssn/char/fresp/access', {
            // input/select value here:
            wmoment: wmoment
        }, function (data) {
            console.log(data.corder);
            // load each command:
            $('input.char#fresp[name="sparam"]').val(data.corder['S-Parameter']);
            $('input.char#fresp[name="ifb"]').val(data.corder['IF-Bandwidth']);
            $('input.char#fresp[name="powa"]').val(data.corder['Power']);
            $('input.char#fresp[name="freq"]').val(data.corder['Frequency']);
            // load comment:
            $('textarea.char#fresp[name="comment"]').val(data.comment);
            // load c-range for each command:
            $('select.char#fresp[name="c-sparam"]').empty().append($('<option>', { text: 'All', value: 'all' }));
            $.each(data.csparam, function(i,v){ $('select.char#fresp[name="c-sparam"]').append($('<option>', { text: v, value: i })); });
            $('select.char#fresp[name="c-ifb"]').empty().append($('<option>', { text: 'All', value: 'all' }));
            $.each(data.cifb, function(i,v){ $('select.char#fresp[name="c-ifb"]').append($('<option>', { text: v, value: i })); });
            $('select.char#fresp[name="c-powa"]').empty().append($('<option>', { text: 'All', value: 'all' }));
            $.each(data.cpowa, function(i,v){ $('select.char#fresp[name="c-powa"]').append($('<option>', { text: v, value: i })); });
            $('select.char#fresp[name="c-freq"]').empty().append($('<option>', { text: 'All', value: 'all' }));
            $.each(data.cfreq, function(i,v){ $('select.char#fresp[name="c-freq"]').append($('<option>', { text: v, value: i })); });
        });
    });
});

// plot 1D-data based on c-parameters picked
$(function () {
    $('input.char#1d-data').on('click', function () {
        var isparam = $('select.char#fresp[name="c-sparam"]').val();
        var iifb = $('select.char#fresp[name="c-ifb"]').val();
        var ipowa = $('select.char#fresp[name="c-powa"]').val();
        var ifreq = $('select.char#fresp[name="c-freq"]').val();
        console.log("Picked: " + isparam);
        $.getJSON('/mssn/char/fresp/1ddata', {
            isparam: isparam, iifb: iifb, ipowa: ipowa, ifreq: ifreq
        }, function (data) {
            console.log(data.y1);
            
            let traceL = {x: [], y: [], mode: 'lines', type: 'scatter', 
                name: 'L (' + wday + ', ' + wmoment + ')',
                line: {color: 'rgb(23, 151, 6)', width: 3} };
            let traceR = {x: [], y: [], mode: 'lines', type: 'scatter', 
                name: 'R (' + wday + ', ' + wmoment + ')',
                line: {color: 'blue', width: 3} };

            let layout = {
                legend: {x: 1.08},
                height: $(window).height()*0.8,
                width: $(window).width()*0.75,
                xaxis: {
                    zeroline: false,
                    title: "<b>frequency(GHz)</b>",
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
                    title: '<b>Pha(rad)</b>', 
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
                    text: '<b>Amp(dB)</b>',
                    font: {size: 18},
                    showarrow: false,
                    textangle: 0
                  }]
                };
            
            $.each(data.x1, function(i, val) {traceL.x.push(val);});
            $.each(data.y1, function(i, val) {traceL.y.push(val);});
            $.each(data.x2, function(i, val) {traceR.x.push(val);});
            $.each(data.y2, function(i, val) {traceR.y.push(val);});

            var Trace = [traceL, traceR]
            Plotly.newPlot('char-chart-01', Trace, layout, {showSendToCloud: true});
            
            // $('div.char#startP').empty();
            // $('div.char#startP').append($('<h4 style="color: darkblue;"></h4>').text("starting: ")).
            // append($('<span style="color: red;"></span>').text(data.startimeP));
            // $('div.char#startT').empty();
            // $('div.char#startT').append($('<h4 style="color: darkblue;"></h4>').text("starting: ")).
            // append($('<span style="color: red;"></span>').text(data.startimeT));;
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

$('.modal-toggle').on('click', function(e) {
    e.preventDefault();
    $('.modal').toggleClass('is-visible');
  });

 

    

