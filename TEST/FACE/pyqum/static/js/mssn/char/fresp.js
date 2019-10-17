// Frequency Response 
$(document).ready(function(){
    $("a.new#fresp-eta").text('ETA: ');
    $("a.new#fresp-rcount").text('R#: ');
});

// Global variables:
window.selecteday = ''

// *functions are shared across all missions!
function set_repeat_fresp() {
    $.getJSON('/mssn/char/fresp/setrepeat', {
        repeat: $('input.char#fresp[name="repeat"]').is(':checked')?1:0
    });
};
function get_repeat_fresp() {
    $.getJSON('/mssn/char/fresp/getrepeat', {
    }, function (data) {
        console.log("Repeat: " + data.repeat);
        $('input.char#fresp[name="repeat"]').prop("checked", data.repeat);
    });
};
function listimes_fresp() {
    $('input.char.data').removeClass("plotted");
    // make global wday
    window.wday = $('select.char#fresp[name="wday"]').val();
    if (Number(wday) < 0) {
        // brings up parameter-input panel for new measurement:
        $('.modal.new').toggleClass('is-visible');
        get_repeat_fresp();

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
};
function accessdata_fresp() {
    $('.data-progress#fresp').css({"width": 0}).text('accessing...');
    $.getJSON('/mssn/char/fresp/access', {
        // input/select value here:
        wmoment: wmoment
    }, function (data) {
        console.log(data.corder);
        // load each command:
        console.log("Flux-Bias undefined: " + (typeof data.corder['Flux-Bias'] == "undefined")); //detecting undefined
        if (typeof data.corder['Flux-Bias'] == "undefined") { $('input.char#fresp[name="fluxbias"]').val("OPT,");
        } else { $('input.char#fresp[name="fluxbias"]').val(data.corder['Flux-Bias']); };
        $('input.char#fresp[name="sparam"]').val(data.corder['S-Parameter']);
        $('input.char#fresp[name="ifb"]').val(data.corder['IF-Bandwidth']);
        $('input.char#fresp[name="powa"]').val(data.corder['Power']);
        $('input.char#fresp[name="freq"]').val(data.corder['Frequency']);
        // load edittable comment:
        $('textarea.char#fresp[name="ecomment"]').val(data.comment);
        // load narrated comment:
        $('textarea.char#fresp[name="comment"]').text(data.comment);
        
        // load c-range for each command:
        $('select.char#fresp[name="c-fluxbias"]').empty();
        if (data.cfluxbias_data.length > 1) {
            $('select.char#fresp[name="c-fluxbias"]').append($('<option>', { text: 'X-ALL', value: 'x' })).append($('<option>', { text: 'Y-ALL', value: 'y' }));
        };
        $.each(data.cfluxbias_data, function(i,v){ $('select.char#fresp[name="c-fluxbias"]').append($('<option>', { text: v, value: i })); });
        
        $('select.char#fresp[name="c-sparam"]').empty();
        if (data.csparam_data.length > 1) {
            $('select.char#fresp[name="c-sparam"]').append($('<option>', { text: 'X-ALL', value: 'x' })).append($('<option>', { text: 'Y-ALL', value: 'y' }));
        };
        $.each(data.csparam_data, function(i,v){ $('select.char#fresp[name="c-sparam"]').append($('<option>', { text: v, value: i })); });

        $('select.char#fresp[name="c-ifb"]').empty();
        if (data.cifb_data.length > 1) {
            $('select.char#fresp[name="c-ifb"]').append($('<option>', { text: 'X-ALL', value: 'x' })).append($('<option>', { text: 'Y-ALL', value: 'y' }));
        };
        $.each(data.cifb_data, function(i,v){ $('select.char#fresp[name="c-ifb"]').append($('<option>', { text: v, value: i })); });
        
        $('select.char#fresp[name="c-powa"]').empty();
        if (data.cpowa_data.length > 1) {
            $('select.char#fresp[name="c-powa"]').append($('<option>', { text: 'X-ALL', value: 'x' })).append($('<option>', { text: 'Y-ALL', value: 'y' }));
        };
        $.each(data.cpowa_data, function(i,v){ $('select.char#fresp[name="c-powa"]').append($('<option>', { text: v, value: i })); });

        $('select.char#fresp[name="c-freq"]').empty();
        if (data.cfreq_data.length > 1) {
            $('select.char#fresp[name="c-freq"]').append($('<option>', { text: 'X-ALL', value: 'x' })).append($('<option>', { text: 'Y-ALL', value: 'y' }));
        };
        $.each(data.cfreq_data, function(i,v){ $('select.char#fresp[name="c-freq"]').append($('<option>', { text: v, value: i })); });
        
        // load data progress:
        var data_progress = "  " + String(data.data_progress.toFixed(3)) + "%";
        $('.data-progress#fresp').css({"width": data_progress}).text(data_progress);
        $('.data-eta#fresp').text("data: " + data.measureacheta + " until completion");
        console.log("Progress: " + data_progress);
    });
}

// hiding parameter settings:
$('.modal-toggle.new.fresp').on('click', function(e) {
    e.preventDefault();
    $('.modal.new.fresp').toggleClass('is-visible');
    // revert back to previous option upon leaving dialogue box
    $('select.char#fresp[name="wday"]').val(selecteday);
});
$('.modal-toggle.search.fresp').on('click', function(e) {
    e.preventDefault();
    $('.modal.search.fresp').toggleClass('is-visible');
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
            console.log("run status: " + data.run_status);
            if (data.run_status == true) {
                $( "i.fresp" ).remove(); //clear previous
                $('button.char#fresp').prepend("<i class='fresp fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
            } else {};
            $('select.char#fresp[name="wday"]').empty();
            $('select.char#fresp[name="wday"]').append($('<option>', { text: 'The latest:', value: '' }));
            $.each(data.daylist.reverse(), function(i,v){
                $('select.char#fresp[name="wday"]').append($('<option>', {
                    text: v,
                    value: data.daylist.length - 1 - i
                }));
            });
            $('select.char#fresp[name="wday"]').append($('<option>', { text: '--Search--', value: 's' }));
            if (data.run_permission == false) {
                $('input.char#fresp-run').hide();
                console.log("RUN BUTTON DISABLED");
            } else {
                $('select.char#fresp[name="wday"]').append($('<option>', { text: '--New--', value: -1 }));
            };
        });
        return false;
    });
});

// list times based on day picked
$(function () {
    $('select.char#fresp[name="wday"]').on('change', function () {
        listimes_fresp();
    });
    return false;
});

// click to run:
$('input.char#fresp-run').bind('click', function() {
    $( "i.fresp" ).remove(); //clear previous
    $('button.char#fresp').prepend("<i class='fresp fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
    // waveform commands
    var fluxbias = $('input.char#fresp[name="fluxbias"]').val();
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
        wday: wday, fluxbias: fluxbias, sparam: sparam, ifb: ifb, powa: powa, freq: freq, comment: comment, simulate: simulate
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
        $("a.new#fresp-eta").text('ETA in\n' + String(data.eta_time_100));
    });
});
// click to set repeat or once
$('input.char#fresp[name="repeat"]').bind('click', function() {
    set_repeat_fresp();
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

// click to pause measurement
$(function () {
    $('button.char#fresp-pause').on('click', function () {
        $( "i.fresp" ).remove(); //clear previous
        $.getJSON('/mssn/char/fresp/pause', {
            // direct pause
        }, function(data) {
            console.log("paused: " + data.pause);
        });
        return false;
    });
});

// Click to resume measurement
$(function () {
    $('button.char#fresp-resume').on('click', function () {
        $( "i.fresp" ).remove(); //clear previous
        $('button.char#fresp').prepend("<i class='fresp fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        // waveform commands
        var fluxbias = $('input.char#fresp[name="fluxbias"]').val();
        var sparam = $('input.char#fresp[name="sparam"]').val();
        var ifb = $('input.char#fresp[name="ifb"]').val();
        var powa = $('input.char#fresp[name="powa"]').val();
        var freq = $('input.char#fresp[name="freq"]').val();
        $.getJSON('/mssn/char/fresp/resume', {
            wday: wday, wmoment: wmoment, fluxbias: fluxbias, sparam: sparam, ifb: ifb, powa: powa, freq: freq
        }, function (data) {
            if (data.resumepoint == data.datasize) {
                console.log("The data was already complete!")
            } else { console.log("The data has just been completed")};
            $( "i.fresp" ).remove(); //clear previous
        });
        return false;
    });
});

// access data based on time picked
$(function () {
    $('select.char#fresp[name="wmoment"]').on('change', function () {
        // Make global variable:
        window.wmoment = $('select.char#fresp[name="wmoment"]').val();
        console.log(wmoment);
        accessdata_fresp();
    });
    return false;
});

// LIVE UPDATE on PROGRESS:
$(function () {
    $('input.fresp#live-update').click(function () { 
        //indicate it is still running:
        $( "i.fresplive" ).remove(); //clear previous
        $('button.char#fresp').prepend("<i class='fresplive fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        var livestat = $('input.fresp#live-update').is(':checked'); //use css to respond to click / touch
        if (livestat == true) {
            var fresploop = setInterval(accessdata_fresp, 6000);
            $('input.fresp#live-update').click(function () {
                clearInterval(fresploop);
                $( "i.fresplive" ).remove(); //clear previous
            });
        };
        // 'else' didn't do much to stop it!
    });
});

// plot 1D-data based on c-parameters picked
$(function () {
    $('input.char#fresp[name="1d-data"]').on('click', function () {
        $( "i.frespplot" ).remove(); //clear previous
        $('button.char#fresp').prepend("<i class='frespplot fa fa-palette fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        var ifluxbias = $('select.char#fresp[name="c-fluxbias"]').val();
        var isparam = $('select.char#fresp[name="c-sparam"]').val();
        var iifb = $('select.char#fresp[name="c-ifb"]').val();
        var ipowa = $('select.char#fresp[name="c-powa"]').val();
        var ifreq = $('select.char#fresp[name="c-freq"]').val();
        console.log("Picked: " + isparam);
        $.getJSON('/mssn/char/fresp/1ddata', {
            ifluxbias: ifluxbias, isparam: isparam, iifb: iifb, ipowa: ipowa, ifreq: ifreq
        }, function (data) {
            console.log(data.title);
            
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
                    title: data.title,
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
            $( "i.frespplot" ).remove(); //clear previous
        });
    });
    return false;
});

// assemble 2D-data based on c-parameters picked
$(function () {
    $('input.char#fresp[name="2d-data"]').on('click', function () {
        $( "i.fresp2d" ).remove(); //clear previous
        $('button.char#fresp').prepend("<i class='fresp2d fa fa-palette fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        var ifluxbias = $('select.char#fresp[name="c-fluxbias"]').val();
        var isparam = $('select.char#fresp[name="c-sparam"]').val();
        var iifb = $('select.char#fresp[name="c-ifb"]').val();
        var ipowa = $('select.char#fresp[name="c-powa"]').val();
        var ifreq = $('select.char#fresp[name="c-freq"]').val();
        console.log("Picked: " + isparam);
        $.getJSON('/mssn/char/fresp/2ddata', {
            ifluxbias: ifluxbias, isparam: isparam, iifb: iifb, ipowa: ipowa, ifreq: ifreq
        }, function (data) {
            window.x = data.x;
            window.y = data.y;
            window.ZZA = data.ZZA;
            window.ZZP = data.ZZP;
            window.xtitle = data.xtitle;
            window.ytitle = data.ytitle;
            // Amplitude (default) or Phase
            $('select.char.data#fresp[name="2d-amphase"]').empty().append($('<option>', { text: 'Amp', value: 'Amp' })).append($('<option>', { text: 'Pha', value: 'Pha' }));
            // Data grooming
            $('select.char.data#fresp[name="2d-type"]').empty().append($('<option>', { text: 'direct', value: 'direct' }))
            .append($('<option>', { text: 'normalYdip', value: 'normalYdip' })).append($('<option>', { text: 'normalYpeak', value: 'normalYpeak' }))
            .append($('<option>', { text: 'normalXdip', value: 'normalXdip' })).append($('<option>', { text: 'normalXpeak', value: 'normalXpeak' }));
            plot2D(x, y, ZZA, xtitle, ytitle, $('select.char.data#fresp[name="2d-type"]').val(),'fresp');
            $( "i.fresp2d" ).remove(); //clear previous
        });
    });
    return false;
});

$('select.char.data#fresp').on('change', function() {
    if ($('select.char.data#fresp[name="2d-amphase"]').val() == "Amp") {var ZZ = ZZA; }
    else if ($('select.char.data#fresp[name="2d-amphase"]').val() == "Pha") {var ZZ = ZZP; };
    plot2D(x, y, ZZ, xtitle, ytitle, $('select.char.data#fresp[name="2d-type"]').val(),'fresp');
    return false;
});

// saving exported csv-data to client's PC:
$('button.char#fresp-savecsv').on('click', function () {
    console.log("SAVING FILE");
    $.getJSON('/mssn/char/fresp/export/1dcsv', {
        ifreq: $('select.char#fresp[name="c-freq"]').val()
    }, function (data) {
        console.log("STATUS: " + data.status);
        $.ajax({
            url: 'http://qum.phys.sinica.edu.tw:5300/mach/uploads/1Dfresp.csv',
            method: 'GET',
            xhrFields: {
                responseType: 'blob'
            },
            success: function (data) {
                var a = document.createElement('a');
                var url = window.URL.createObjectURL(data);
                a.href = url;
                a.download = 'data.csv';
                document.body.append(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
            }
        });
    });
    return false;
});