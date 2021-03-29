// Frequency Response 
$(document).ready(function(){
    $("a.new#fresp-job").text('JOBID: ');
    $("a.new#fresp-rcount").text('R#: ');
    // console.log('encryptonian length: ' + mssnencrpytonian().length);
    // get_repeat_fresp();
    window.frespcomment = "";
    $('button.char#fresp-savecsv').hide();
    $('button.char#fresp-savemat').hide();
    $('div input.fresp.notification').hide();
});

// Global variables:
window.selecteday = ''
window.frespcryption = 'hfhajfjkafh'

// *functions are shared across all missions!
// function set_repeat_fresp() {
//     $.getJSON(mssnencrpytonian() + '/mssn/char/' + frespcryption + '/setrepeat', {
//         repeat: $('input.char#fresp[name="repeat"]').is(':checked')?1:0
//     });
// };
// function get_repeat_fresp() {
//     $.getJSON(mssnencrpytonian() + '/mssn/char/' + frespcryption + '/getrepeat', {
//     }, function (data) {
//         console.log("Repeat: " + data.repeat);
//         $('input.char#fresp[name="repeat"]').prop("checked", data.repeat);
//     });
// };
function listimes_fresp() {
    // $('input.char.data').removeClass("plotted");
    
    if (Number(wday) < 0) {
        // brings up parameter-input panel for new measurement:
        $('.modal.new.fresp').toggleClass('is-visible');
        // Update Live Informations:
        $.getJSON('/mach/all/mxc', {}, function (data) {
            $("textarea.char#fresp[name='ecomment']").val(frespcomment + "\nUpdate: T6=" + data.mxcmk + "mK");
        });

    } else if (wday == 's') {
        // brings up search panel:
        // $('.modal.search').toggleClass('is-visible');
        $('div.fresp#fresp-search').width("100%"); //default: 21%
        console.log("bring up search...");

    } else {
        selecteday = wday
        $.getJSON(mssnencrpytonian() + '/mssn/char/' + frespcryption + '/time', {
            wday: wday
        }, function (data) {
            $('select.char#fresp[name="wmoment"]').empty().append($('<option>', { text: 'pick', value: '' }));
            $.each(data.taskentries, function(i,v){ $('select.char#fresp[name="wmoment"]').append($('<option>', { text: v, value: i+1 })); });
        }); 
    };
    return;
};
function accessdata_fresp() {
    $('.data-progress#fresp').css({"width": 0}).text('accessing...');
    $.getJSON(mssnencrpytonian() + '/mssn/char/' + frespcryption + '/access', {
        // input/select value here:
        wmoment: wmoment
    }, function (data) {
        // Indicate JOBID:
        $("a.new#fresp-job").text('JOBID: ' + String(data.JOBID));
        // checking parameters:
        console.log("CORDER: " + JSON.stringify(data.corder) + "\nPERIMETER: " + JSON.stringify(data.perimeter));
        // load each command:
        console.log("Flux-Bias undefined: " + (typeof data.corder['Flux-Bias'] == "undefined")); //detecting undefined
        if (typeof data.corder['Flux-Bias'] == "undefined") { $('input.char#fresp[name="fluxbias"]').val("OPT,");
        } else { $('input.char#fresp[name="fluxbias"]').val(data.corder['Flux-Bias']); };
        $('input.char#fresp[name="sparam"]').val(data.corder['S-Parameter']);
        $('input.char#fresp[name="ifb"]').val(data.corder['IF-Bandwidth']);
        $('input.char#fresp[name="powa"]').val(data.corder['Power']);
        $('input.char#fresp[name="freq"]').val(data.corder['Frequency']);
        // load edittable comment:
        frespcomment = data.comment;
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
        $.each(data.cfreq_data.slice(0,101), function(i,v){ $('select.char#fresp[name="c-freq"]').append($('<option>', { text: v, value: i })); });
        if (data.cfreq_data.length > 101) {
            $('select.char#fresp[name="c-freq"]').append($('<option>', { text: 'more...', value: 'm' }));
            // Pending: to speed up loading process, it is limited to 101 entries per request. Use "more" to select/enter value manually!
        };
        
        // load data progress:
        var data_progress = "  " + String(data.data_progress.toFixed(3)) + "%";
        $('.data-progress#fresp').css({"width": data_progress}).text(data_progress);
        $('.data-eta#fresp').text("data: " + data.measureacheta + " until completion");
        console.log("Progress: " + data_progress);
    });
    return;
};

function plot2D_fresp(x,y,ZZ,xtitle,ytitle,plotype,mission,colorscal) {
    console.log("Plotting 2D");
         
    // Frame assembly:
    let trace = {
        z: [], x: [], y: [], zsmooth: 'best',
        mode: 'lines', type: 'heatmap', colorscale: colorscal,
        name: 'L (' + wday + ', ' + wmoment + ')',
        line: {color: 'rgb(23, 151, 6)', width: 2.5}, yaxis: 'y' };
    
    let layout = {
        legend: {x: 1.08},
        height: $(window).height()*0.8,
        width: $(window).width()*0.7,
        xaxis: {
            zeroline: false, title: xtitle, titlefont: {size: 18}, tickfont: {size: 18}, tickwidth: 3, linewidth: 3, mirror: true },
        yaxis: {
            zeroline: false, title: ytitle,
            titlefont: {size: 18}, tickfont: {size: 18}, tickwidth: 3, linewidth: 3, mirror: true },
        title: '',
        annotations: [{ xref: 'paper', yref: 'paper',  x: 0.03, xanchor: 'right', y: 1.05, yanchor: 'bottom',
            text: "", font: {size: 18}, showarrow: false, textangle: 0 }] };

    // Data GROOMING:
    // 1. Normalization along x-axis (dip)
    if (plotype == 'normalXdip') {
        var ZZNML = [];
        $.each(ZZ, function(i, Z) {
            var Zrow = []
            var zmin = Math.min.apply(Math, Z);
            var zmax = Math.max.apply(Math, Z);
            $.each(Z, function(i, z) {
                var znml = (z-zmax)/(zmax-zmin);
                Zrow.push(znml);
            });
            ZZNML.push(Zrow);
        });
        ZZ = ZZNML;

    // 2. Normalization along x-axis (peak)
    } else if (plotype == 'normalXpeak') {
        var ZZNML = [];
        $.each(ZZ, function(i, Z) {
            var Zrow = []
            var zmin = Math.min.apply(Math, Z);
            var zmax = Math.max.apply(Math, Z);
            $.each(Z, function(i, z) {
                var znml = (z-zmin)/(zmax-zmin);
                Zrow.push(znml);
            });
            ZZNML.push(Zrow);
        });
        ZZ = ZZNML;

    // 3. Normalization along y-axis (dip)
    } else if (plotype == 'normalYdip') {
        ZZ = transpose(ZZ);
        var ZZNML = [];
        $.each(ZZ, function(i, Z) {
            var Zrow = []
            var zmin = Math.min.apply(Math, Z);
            var zmax = Math.max.apply(Math, Z);
            $.each(Z, function(i, z) {
                var znml = (z-zmax)/(zmax-zmin);
                Zrow.push(znml);
            });
            ZZNML.push(Zrow);
        });
        ZZ = transpose(ZZNML);

    // 4. Normalization along y-axis (peak)
    } else if (plotype == 'normalYpeak') {
        ZZ = transpose(ZZ);
        var ZZNML = [];
        $.each(ZZ, function(i, Z) {
            var Zrow = []
            var zmin = Math.min.apply(Math, Z);
            var zmax = Math.max.apply(Math, Z);
            $.each(Z, function(i, z) {
                var znml = (z-zmin)/(zmax-zmin);
                Zrow.push(znml);
            });
            ZZNML.push(Zrow);
        });
        ZZ = transpose(ZZNML);
    };

    // Pushing Data into TRACE:
    $.each(x, function(i, val) {trace.x.push(val);});
    $.each(y, function(i, val) {trace.y.push(val);});
    $.each(ZZ, function(i, Z) {
        var Zrow = []
        $.each(Z, function(i, val) { Zrow.push(val); });
        trace.z.push(Zrow);
    });
    console.log("1st z-trace: " + trace.z[0][0]);

    // Plotting the Chart using assembled TRACE:
    var Trace = [trace]
    Plotly.newPlot('char-' + mission + '-chart', Trace, layout, {showSendToCloud: true});
};

// hiding parameter settings:
$('.modal-toggle.new.fresp').on('click', function(e) {
    e.preventDefault();
    $('.modal.new.fresp').toggleClass('is-visible');
    // revert back to previous option upon leaving dialogue box
    $('select.char#fresp[name="wday"]').val(selecteday);
});
// $('.modal-toggle.search.fresp').on('click', function(e) {
//     e.preventDefault();
//     $('.modal.search.fresp').toggleClass('is-visible');
//     // revert back to previous option upon leaving dialogue box
//     $('select.char#fresp[name="wday"]').val(selecteday);
// });

// show F-Response's daylist
$(function() {
    $('button.char#fresp').bind('click', function() {
        $('div.fresp.queue-system').empty().append($('<h4 style="color: blue;"></h4>').text(qsystem));
        $('div.charcontent').hide();
        $('div.charcontent#fresp').show();
        $('button.char').removeClass('selected');
        $('button.char#fresp').addClass('selected');
        $.getJSON(mssnencrpytonian() + '/mssn/char/' + frespcryption + '/init', {
        }, function (data) {
            // Check Run Permission: (PENDING: Use Global run_permission to notify user whenever certain disabled button is click)
            window.run_permission = data.run_permission;
            window.DAYLIST = data.daylist;
            console.log("run permission: " + run_permission);
            if (run_permission == false) {
                $('input.char#fresp-run').hide();
                $('button.char.fresp.run').hide();
                console.log("RUN BUTTON DISABLED");
            } else {
                $('input.char#fresp-run').show(); // RUN
                $('button.char.fresp.run').show(); // RESUME
                console.log("RUN BUTTON ENABLED");
            };
            // Check Run Status:
            // console.log("run status: " + data.run_status);
            // if (data.run_status == true) {
            //     $( "i.fresp" ).remove(); //clear previous
            //     $('button.char#fresp').prepend("<i class='fresp fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
            // } else {};
            // List Days:
            $('select.char#fresp[name="wday"]').empty();
            $('select.char#fresp[name="wday"]').append($('<option>', { text: 'The latest:', value: '' }));
            $.each(data.daylist.reverse(), function(i,v){
                $('select.char#fresp[name="wday"]').append($('<option>', {
                    text: v,
                    value: data.daylist.length - 1 - i
                }));
            });
            $('select.char#fresp[name="wday"]').append($('<option>', { text: '--Search--', value: 's' }));
            $('select.char#fresp[name="wday"]').append($('<option>', { text: '--New--', value: -1 }));
            $('select.char#fresp[name="wday"]').append($('<option>', { text: '--Temp--', value: -3 }));
        });
        return false;
    });
});

// list times based on day picked
$(function () {
    $('select.char#fresp[name="wday"]').on('change', function () {
        // make global wday
        window.wday = $('select.char#fresp[name="wday"]').val();
        listimes_fresp();
    });
    return false;
});

// click to run:
$('input.char#fresp-run').bind('click', function() {
    setTimeout(() => { $('button.tablinks#ALL-tab').trigger('click'); }, 160);
    $( "i.fresp" ).remove(); //clear previous
    // $('button.char#fresp').prepend("<i class='fresp fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
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
    $.getJSON(mssnencrpytonian() + '/mssn/char/' + frespcryption + '/new', {
        wday: wday, fluxbias: fluxbias, sparam: sparam, ifb: ifb, powa: powa, freq: freq, comment: comment, simulate: simulate
    }, function (data) { 
        console.log("test each loop: " + data.testeach); 
        // $('button.tablinks#ALL-tab').trigger('click');  
        $( "i.fresp" ).remove(); //clear previous
        $('h3.all-mssn-warning').text("JOB STATUS: " + data.status);
    });
    return false;
});
// click to estimate ETA (PENDING: DATA-ANALYSIS FUNCTIONS?)
// $("a.new#fresp-job").bind('click', function() {
//     $.getJSON(mssnencrpytonian() + '/mssn/char/' + frespcryption + '/eta100', {
//     }, function (data) {
//         
//     });
// });
// // click to set repeat or once
// $('input.char#fresp[name="repeat"]').bind('click', function() {
//     set_repeat_fresp();
// });

// click to search:
$('button.char.fresp[name="search"]').click( function() {
    var keyword = $('input.char.fresp[name="search"]').val();
    $.getJSON(mssnencrpytonian() + '/mssn/char/' + frespcryption + '/search', {
        wday: wday,
        keyword: keyword
    }, function (data) {
        $("div#fresp-search-result").html(`<div class='link' id='left' style='color: white;'>Searching for &nbsp</div>`)
                                    .append(`<div class='link' id='left'><a href='https://www.google.com'> ${keyword} </a></div>`);
    });
    return false;
});

// click to pause measurement
// $(function () {
//     $('button.char#fresp-pause').on('click', function () {
//         $( "i.fresp" ).remove(); //clear previous
//         $.getJSON(mssnencrpytonian() + '/mssn/char/' + frespcryption + '/pause', {
//             // direct pause
//         }, function(data) {
//             console.log("paused: " + data.pause);
//         });
//         return false;
//     });
// });

// Click to resume measurement
$(function () {
    $('button.char#fresp-resume').on('click', function () {
        setTimeout(() => { $('button.tablinks#ALL-tab').trigger('click'); }, 160);
        $( "i.fresp" ).remove(); //clear previous
        // $('button.char#fresp').prepend("<i class='fresp fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        // waveform commands
        var fluxbias = $('input.char#fresp[name="fluxbias"]').val();
        var sparam = $('input.char#fresp[name="sparam"]').val();
        var ifb = $('input.char#fresp[name="ifb"]').val();
        var powa = $('input.char#fresp[name="powa"]').val();
        var freq = $('input.char#fresp[name="freq"]').val();
        $.getJSON(mssnencrpytonian() + '/mssn/char/' + frespcryption + '/resume', {
            wday: wday, wmoment: wmoment, fluxbias: fluxbias, sparam: sparam, ifb: ifb, powa: powa, freq: freq
        }, function (data) {
            if (data.resumepoint == data.datasize) {
                console.log("The data was already complete!")
            } else { console.log("The data has just been completed")};
            // $('button.tablinks#ALL-tab').trigger('click');
            $( "i.fresp" ).remove(); //clear previous
            $('h3.all-mssn-warning').text("JOB COMPLETE: " + data.status);
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
// $(function () {
//     $('input.fresp#live-update').click(function () { 
//         //indicate it is still running:
//         $( "i.fresplive" ).remove(); //clear previous
//         $('button.char#fresp').prepend("<i class='fresplive fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
//         var livestat = $('input.fresp#live-update').is(':checked'); //use css to respond to click / touch
//         if (livestat == true) {
//             var fresploop = setInterval(accessdata_fresp, 6000);
//             $('input.fresp#live-update').click(function () {
//                 clearInterval(fresploop);
//                 $( "i.fresplive" ).remove(); //clear previous
//             });
//         };
//         // 'else' didn't do much to stop it!
//     });
// });

// plot 1D-data based on c-parameters picked
$(function () {
    $('input.char#fresp[name="1d-data"]').on('click', function () {
        $( "i.fresp1d" ).remove(); //clear previous
        $('button.char#fresp').prepend("<i class='fresp1d fa fa-palette fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        var ifluxbias = $('select.char#fresp[name="c-fluxbias"]').val();
        var isparam = $('select.char#fresp[name="c-sparam"]').val();
        var iifb = $('select.char#fresp[name="c-ifb"]').val();
        var ipowa = $('select.char#fresp[name="c-powa"]').val();
        var ifreq = $('select.char#fresp[name="c-freq"]').val();
        console.log("Picked: " + isparam);
        $.getJSON(mssnencrpytonian() + '/mssn/char/' + frespcryption + '/1ddata', {
            ifluxbias: ifluxbias, isparam: isparam, iifb: iifb, ipowa: ipowa, ifreq: ifreq
        }, function (data) {
            window.x1 = data.x1;
            window.y1 = new Object();
            window.y1.A = data.y1;
            window.y1.UP = data.y2;
            window.xtitle1 = data.title;
            console.log(xtitle1);
            
            let traceL = {x: [], y: [], mode: 'lines', type: 'scatter', 
                name: 'Amplitude',
                line: {color: 'rgb(23, 151, 6)', width: 2.5},
                yaxis: 'y' };
            let traceR = {x: [], y: [], mode: 'lines', type: 'scatter', 
                name: 'UFN-Phase',
                line: {color: 'blue', width: 2.5},
                yaxis: 'y2' };

            let layout = {
                legend: {x: 1.08},
                height: $(window).height()*0.8,
                width: $(window).width()*0.7,
                xaxis: {
                    zeroline: false,
                    title: xtitle1,
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
            
            $.each(x1, function(i, val) {traceL.x.push(val);});
            $.each(y1.A, function(i, val) {traceL.y.push(val);});
            $.each(x1, function(i, val) {traceR.x.push(val);});
            $.each(y1.UP, function(i, val) {traceR.y.push(val);});

            var Trace = [traceL, traceR]
            Plotly.newPlot('char-fresp-chart', Trace, layout, {showSendToCloud: true});
            $( "i.fresp1d" ).remove(); //clear previous
            $('button.char#fresp-savecsv').show();
        });
    });
    return false;
});
// INSERT 1D-data for comparison
$(function () {
    $('button.char#fresp-insert-1D').on('click', function () {
        $('div#char-fresp-announcement').empty();
        $( "i.fresp1d" ).remove(); //clear previous
        $('button.char#fresp').prepend("<i class='fresp1d fa fa-palette fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        var ifluxbias = $('select.char#fresp[name="c-fluxbias"]').val();
        var isparam = $('select.char#fresp[name="c-sparam"]').val();
        var iifb = $('select.char#fresp[name="c-ifb"]').val();
        var ipowa = $('select.char#fresp[name="c-powa"]').val();
        var ifreq = $('select.char#fresp[name="c-freq"]').val();
        console.log("Picked: " + isparam);
        $.getJSON(mssnencrpytonian() + '/mssn/char/' + frespcryption + '/1ddata', {
            ifluxbias: ifluxbias, isparam: isparam, iifb: iifb, ipowa: ipowa, ifreq: ifreq
        }, function (data) {
            window.x1C = data.x1;
            window.y1C = new Object();
            window.y1C.A = data.y1;
            window.y1C.UP = data.y2;
            window.x1titleC = data.title;

            // Normalization Options:
            $('select.char.data.fresp#fresp-compare-nml').empty().append($('<option>', { text: 'direct', value: 'direct' }))
                                                                .append($('<option>', { text: 'normaldip', value: 'normaldip' }))
                                                                .append($('<option>', { text: 'normalpeak', value: 'normalpeak' }));
            console.log('selected: ' + $('select.char.data.fresp#fresp-compare-nml').val());
            normalize = Boolean($('select.char.data.fresp#fresp-compare-nml').val()!='direct');
            direction = $('select.char.data.fresp#fresp-compare-nml').val().split('normal')[1];

            // AUP Options:
            $('select.char.data.fresp#fresp-compare-aup').empty().append($('<option>', { text: 'Amplitude', value: 'A' }))
                                                                .append($('<option>', { text: 'UPhase', value: 'UP' }));

            var AUP = $('select.char.data.fresp#fresp-compare-aup').val();
            compare1D(x1,y1[AUP],x1C,y1C[AUP],x1titleC,AUP,normalize,direction,'char-fresp');
        })
            .fail(function(jqxhr, textStatus, error){
                $('div#char-fresp-announcement').append($('<h4 style="color: red;"></h4>').text("Oops: " + error));
                $( "i.fresp1d" ).remove(); //clear the status
            });
    });
    return false;
});
$('.char.data.fresp.compare').on('change', function() {
    normalize = Boolean($('select.char.data.fresp#fresp-compare-nml').val()!='direct');
    direction = $('select.char.data.fresp#fresp-compare-nml').val().split('normal')[1];
    var AUP = $('select.char.data.fresp#fresp-compare-aup').val();
    compare1D(x1,y1[AUP],x1C,y1C[AUP],x1titleC,AUP,normalize,direction,'char-fresp');
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
        $.getJSON(mssnencrpytonian() + '/mssn/char/' + frespcryption + '/2ddata', {
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
            plot2D_fresp(x, y, ZZA, xtitle, ytitle, $('select.char.data#fresp[name="2d-type"]').val(),'fresp');
            $( "i.fresp2d" ).remove(); //clear previous
            $('button.char#fresp-savemat').show();
        });
    });
    return false;
});

$('select.char.data#fresp').on('change', function() {
    if ($('select.char.data#fresp[name="2d-amphase"]').val() == "Amp") {var ZZ = ZZA; }
    else if ($('select.char.data#fresp[name="2d-amphase"]').val() == "Pha") {var ZZ = ZZP; };
    plot2D_fresp(x, y, ZZ, xtitle, ytitle, $('select.char.data#fresp[name="2d-type"]').val(),'fresp');
    return false;
});

// saving exported csv-data to client's PC:
$('button.char#fresp-savecsv').on('click', function () {
    console.log("SAVING CSV FILE");

    // in order to trigger href send-file request: (PENDING: FIND OUT THE WEIRD LOGIC BEHIND THIS NECCESITY)
    $.getJSON(mssnencrpytonian() + '/mssn/char/' + frespcryption + '/access', { wmoment: wmoment }, function (data) {});

    $.getJSON(mssnencrpytonian() + '/mssn/char/' + frespcryption + '/export/1dcsv', {
        ifreq: $('select.char#fresp[name="c-freq"]').val()
    }, function (data) {
        console.log("STATUS: " + data.status);
        $.ajax({
            url: 'http://qum.phys.sinica.edu.tw:5301/mach/uploads/1Dfresp[' + data.user_name + '].csv',
            method: 'GET',
            xhrFields: {
                responseType: 'blob'
            },
            success: function (data) {
                console.log("USER HAS DOWNLOADED 1Dfresp DATA from " + String(window.URL));
                var a = document.createElement('a');
                var url = window.URL.createObjectURL(data);
                a.href = url;
                a.download = '1Dfresp.csv';
                document.body.append(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
                $('button.char#fresp-savecsv').hide();
            }
        });
    });
    return false;
});
// saving exported mat-data to client's PC:
$('button.char#fresp-savemat').on('click', function () {
    console.log("SAVING MAT FILE");

    // in order to trigger href send-file request: (PENDING: FIND OUT THE WEIRD LOGIC BEHIND THIS NECCESITY)
    $.getJSON(mssnencrpytonian() + '/mssn/char/' + frespcryption + '/access', { wmoment: wmoment }, function (data) {});

    $.getJSON(mssnencrpytonian() + '/mssn/char/' + frespcryption + '/export/2dmat', {
        ifreq: $('select.char#fresp[name="c-freq"]').val()
    }, function (data) {
        console.log("STATUS: " + data.status);
        $.ajax({
            url: 'http://qum.phys.sinica.edu.tw:5301/mach/uploads/2Dfresp[' + data.user_name + '].mat',
            method: 'GET',
            xhrFields: {
                responseType: 'blob'
            },
            success: function (data) {
                console.log("USER HAS DOWNLOADED 2Dfresp DATA from " + String(window.URL));
                var a = document.createElement('a');
                var url = window.URL.createObjectURL(data);
                a.href = url;
                a.download = '2Dfresp.mat';
                document.body.append(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
                $('button.char#fresp-savemat').hide();
            }
        });
    });
    return false;
});

// Search box:
$('a.fresp.closebtn').on('click', function () {
    console.log("closing search box");
    $('div.fresp#fresp-search').width("0");
    // revert back to previous option upon leaving dialogue box
    $('select.char#fresp[name="wday"]').val(selecteday);
});

// Notification on click:
$('input.fresp.notification').click( function(){
    var Day = $('input.fresp.notification').val().split(' > ')[1];
    var Moment = $('input.fresp.notification').val().split(' > ')[2];
    console.log('Day: ' + Day + ', Moment: ' + Moment);

    // Setting global Day & Moment index:
    wday = DAYLIST.length - 1 - DAYLIST.indexOf(Day);
    wmoment = Moment;
    // Digesting Day & Moment on the back:
    listimes_fresp();
    accessdata_fresp();
    // Setting Day & Moment on the front:
    $('select.char#fresp[name="wday"]').val(wday);
    setTimeout(() => {
        $('select.char#fresp[name="wmoment"]').val(wmoment);
    }, 160); //.trigger('change'); //listing time is a bit slower than selecting option => conflict

    return false;
});
