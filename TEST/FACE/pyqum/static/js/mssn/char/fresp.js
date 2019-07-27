// Frequency Response 
$(document).ready(function(){
    $("a.new#fresp-eta").text('ETA: ');
});

// Global variables:
window.selecteday = ''

// hiding parameter settings:
$('.modal-toggle.new').on('click', function(e) {
    e.preventDefault();
    $('.modal.new').toggleClass('is-visible');
    // revert back to previous option upon leaving dialogue box
    $('select.char#fresp[name="wday"]').val(selecteday);
});
$('.modal-toggle.search').on('click', function(e) {
    e.preventDefault();
    $('.modal.search').toggleClass('is-visible');
    // revert back to previous option upon leaving dialogue box
    $('select.char#fresp[name="wday"]').val(selecteday);
});

// show F-Response's daylist
$(function() {
    $('button.char#fresp').bind('click', function() {
        $('div.charcontent').hide();
        $('div.charcontent#fresp').show();
        $('button.char').removeClass('selected');
        $('button.char#fresp').addClass('selected');
        $.getJSON('/mssn/char/fresp/init', {
        }, function (data) {
            $('select.char#fresp[name="wday"]').empty();
            $('select.char#fresp[name="wday"]').append($('<option>', { text: 'pick a day', value: '' }));
            $('select.char#fresp[name="wday"]').append($('<option>', { text: '--Search--', value: 's' }));
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

// actions based on day picked
$(function () {
    $('select.char#fresp[name="wday"]').on('change', function () {
        $('input.char.data').removeClass("plotted");
        // make global wday
        window.wday = $('select.char#fresp[name="wday"]').val();
        if (Number(wday) < 0) {
            // brings up parameter-input panel for new measurement:
            $('.modal.new').toggleClass('is-visible');

        } else if (wday == 's') {
            // brings up search panel:
            $('.modal.search').toggleClass('is-visible');
        } else {
            selecteday = wday
            $.getJSON('/mssn/char/fresp/time', {
                wday: wday
            }, function (data) {
                $('select.char#fresp[name="wmoment"]').empty().append($('<option>', { text: 'pick', value: '' }));
                $.each(data.taskentries, function(i,v){ $('select.char#fresp[name="wmoment"]').append($('<option>', { text: v, value: i+1 })); });
            }); 
        };
    });
    return false;
});

// click to run:
$('input.char#fresp-run').bind('click', function() {
    $( "i.fresp" ).remove(); //clear previous
    $('button.char#fresp').prepend("<i class='fresp fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
    // waveform commands
    var sparam = $('input.char#fresp[name="sparam"]').val();
    var ifb = $('input.char#fresp[name="ifb"]').val();
    var powa = $('input.char#fresp[name="powa"]').val();
    var freq = $('input.char#fresp[name="freq"]').val();
    var comment = JSON.stringify($('textarea.char#fresp[name="ecomment"]').val());
    // Simulate or Real run?
    var simulate = $('input.char#fresp[name="simulate"]').is(':checked')?1:0; //use css to respond to click / touch
    console.log("simulate: " + simulate);
    // var comment = $('textarea.char#fresp[name="comment"]').val();
    $.getJSON('/mssn/char/fresp/new', {
        wday: wday, sparam: sparam, ifb: ifb, powa: powa, freq: freq, comment: comment, simulate: simulate
    }, function (data) { 
        console.log("test each loop: " + data.testeach);      
        $( "i.fresp" ).remove(); //clear previous
    });
    return false;
});
// click to estimate ETA
$("a.new#fresp-eta").bind('click', function() {
    $.getJSON('/mssn/char/fresp/eta100', {
    }, function (data) {
        $("a.new#fresp-eta").text('ETA in ' + String(data.eta_time_100));
    });
});
// click to set repeat or once
$('input.char#fresp[name="repeat"]').bind('click', function() {
    $.getJSON('/mssn/char/fresp/repeat', {
        repeat: $('input.char#fresp[name="repeat"]').is(':checked')?1:0
    }, function (data) {
        console.log("Repeat: " + data.repeat);
    });
});

// click to search:
$('input.char#fresp[name="search"]').change( function() {
    $( "i.fresp" ).remove(); //clear previous
    $('button.char#fresp').prepend("<i class='fresp fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
    // waveform commands
    
    // var comment = $('textarea.char#fresp[name="comment"]').val();
    $.getJSON('/mssn/char/fresp/search', {
        
    }, function (data) {
        
        console.log("complete: " + data.filelist);
        $( "i.fresp" ).remove(); //clear previous
    });
    return false;
});

// Click to resume File
$(function () {
    $('button.char#fresp-resume').on('click', function () {
        $( "i.fresp" ).remove(); //clear previous
        $('button.char#fresp').prepend("<i class='fresp fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        // waveform commands
        var sparam = $('input.char#fresp[name="sparam"]').val();
        var ifb = $('input.char#fresp[name="ifb"]').val();
        var powa = $('input.char#fresp[name="powa"]').val();
        var freq = $('input.char#fresp[name="freq"]').val();
        $.getJSON('/mssn/char/fresp/resume', {
            wday: wday, wmoment: wmoment, sparam: sparam, ifb: ifb, powa: powa, freq: freq
        }, function (data) {
        });
    });
    return false;
});

// access data based on time picked
$(function () {
    $('select.char#fresp[name="wmoment"]').on('change', function () {
        // Make global variable:
        window.wmoment = $('select.char#fresp[name="wmoment"]').val();
        $('.data-progress#fresp').css({"width": 0}).text('accessing...');
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
            // load edittable comment:
            $('textarea.char#fresp[name="ecomment"]').val(data.comment);
            // load narrated comment:
            $('textarea.char#fresp[name="comment"]').text(data.comment);
            // load c-range for each command:
            $('select.char#fresp[name="c-sparam"]').empty().append($('<option>', { text: 'All', value: 'all' }));
            $.each(data.csparam, function(i,v){ $('select.char#fresp[name="c-sparam"]').append($('<option>', { text: v, value: i })); });
            $('select.char#fresp[name="c-ifb"]').empty().append($('<option>', { text: 'All', value: 'all' }));
            $.each(data.cifb, function(i,v){ $('select.char#fresp[name="c-ifb"]').append($('<option>', { text: v, value: i })); });
            $('select.char#fresp[name="c-powa"]').empty().append($('<option>', { text: 'All', value: 'all' }));
            $.each(data.cpowa, function(i,v){ $('select.char#fresp[name="c-powa"]').append($('<option>', { text: v, value: i })); });
            $('select.char#fresp[name="c-freq"]').empty().append($('<option>', { text: 'All', value: 'all' }));
            $.each(data.cfreq, function(i,v){ $('select.char#fresp[name="c-freq"]').append($('<option>', { text: v, value: i })); });
            // load data progress:
            var data_progress = "  " + String(data.data_progress) + "%"
            console.log("Progress: " + data_progress)
            $('.data-progress#fresp').css({"width": data_progress}).text(data_progress);
        });
    });
    return false;
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
                line: {color: 'rgb(23, 151, 6)', width: 2.5},
                yaxis: 'y' };
            let traceR = {x: [], y: [], mode: 'lines', type: 'scatter', 
                name: 'R (' + wday + ', ' + wmoment + ')',
                line: {color: 'blue', width: 2.5},
                yaxis: 'y2' };

            let layout = {
                legend: {x: 1.08},
                height: $(window).height()*0.8,
                width: $(window).width()*0.7,
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
                    // title: '<b>Amp(dB)</b>',
                    titlefont: {size: 18},
                    tickfont: {size: 18},
                    tickwidth: 3,
                    linewidth: 3
                },
                yaxis2: {
                    zeroline: false,
                    title: '<b>U-Pha(rad)</b>', 
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
            $.each(data.x1, function(i, val) {traceR.x.push(val);});
            $.each(data.y2, function(i, val) {traceR.y.push(val);});

            var Trace = [traceL, traceR]
            Plotly.newPlot('char-fresp-chart', Trace, layout, {showSendToCloud: true});
            
        });
        $('input.char#1d-data').addClass("plotted");
    });
    return false;
});



