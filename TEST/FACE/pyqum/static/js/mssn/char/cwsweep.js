// CW Sweep: 
$(document).ready(function(){
    $('div.char.cwsweep.confirm').hide();
    $("a.new#cwsweep-eta").text('ETA: ');
    get_repeat_cwsweep();
    window.cwsweepcomment = "";
});

// Global variables:
window.selecteday = ''

// *functions are shared across all missions!
function transpose(a) {
    // Calculate the width and height of the Array
    var w = a.length || 0;
    var h = a[0] instanceof Array ? a[0].length : 0;
    // In case it is a zero matrix, no transpose routine needed.
    if(h === 0 || w === 0) { return []; }
    /**
     * @var {Number} i Counter
     * @var {Number} j Counter
     * @var {Array} t Transposed data is stored in this array.
     */
    var i, j, t = [];
    // Loop through every item in the outer array (height)
    for(i=0; i<h; i++) {
      // Insert a new row (array)
      t[i] = [];
      // Loop through every item per item in outer array (width)
      for(j=0; j<w; j++) {
        // Save transposed data.
        t[i][j] = a[j][i];
      }
    }
    return t;
  };
function set_repeat_cwsweep() {
    $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/setrepeat', {
        repeat: $('input.char#cwsweep[name="repeat"]').is(':checked')?1:0
    }, function(data) {
        $( "i.cwsweep-repeat" ).remove(); //clear previous
        if (data.repeat == true) {
            $('button.char#cwsweep').prepend("<i class='cwsweep-repeat fa fa-repeat fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        };
    });
};
function get_repeat_cwsweep() {
    $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/getrepeat', {
    }, function (data) {
        console.log("Repeat: " + data.repeat);
        $('input.char#cwsweep[name="repeat"]').prop("checked", data.repeat);
        $( "i.cwsweep-repeat" ).remove(); //clear previous
        if (data.repeat == true) {
            $('button.char#cwsweep').prepend("<i class='cwsweep-repeat fa fa-repeat fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        };
    });
};
function listimes_cwsweep() {
    $('input.char.data').removeClass("plotted");
    // make global wday
    window.wday = $('select.char#cwsweep[name="wday"]').val();
    if (Number(wday) < 0) {
        // brings up parameter-input panel for new measurement:
        $('.modal.new').toggleClass('is-visible');
        // Update Live Informations:
        $.getJSON('/mach/all/mxc', {}, function (data) {
            $("textarea.char#cwsweep[name='ecomment']").val(cwsweepcomment + "\nUpdate: T6=" + data.mxcmk + "mK");
        });

    } else if (wday == 's') {
        // brings up search panel:
        $('.modal.search.cwsweep').toggleClass('is-visible');
    } else {
        selecteday = wday
        $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/time', {
            wday: wday
        }, function (data) {
            $('select.char#cwsweep[name="wmoment"]').empty().append($('<option>', { text: 'pick', value: '' }));
            $.each(data.taskentries, function(i,v){ $('select.char#cwsweep[name="wmoment"]').append($('<option>', { id: i, text: v, value: v })); });
        }); 
    };
};
function accessdata_cwsweep() {
    // Make global variable:
    window.wmoment = $('select.char#cwsweep[name="wmoment"]').val();
    $('.data-progress#cwsweep').css({"width": 0}).text('accessing...');
    $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/access', {
        // input/select value here:
        wmoment: wmoment
    }, function (data) {
        console.log(data.corder);
        // load each command:
        console.log("Flux-Bias undefined: " + (typeof data.corder['Flux-Bias'] == "undefined")); //detecting undefined
        
        // Scale up optional parameter inputs:
        if (typeof data.corder['Flux-Bias'] == "undefined") { $('input.char#cwsweep[name="fluxbias"]').val("OPT,");
        } else { $('input.char#cwsweep[name="fluxbias"]').val(data.corder['Flux-Bias']); };
        if (typeof data.corder['XY-Frequency'] == "undefined") { $('input.char#cwsweep[name="xyfreq"]').val("OPT,");
        } else { $('input.char#cwsweep[name="xyfreq"]').val(data.corder['XY-Frequency']); };
        if (typeof data.corder['XY-Power'] == "undefined") { $('input.char#cwsweep[name="xypowa"]').val("OPT,");
        } else { $('input.char#cwsweep[name="xypowa"]').val(data.corder['XY-Power']); };
        
        // Basic parameter inputs:
        $('input.char#cwsweep[name="sparam"]').val(data.corder['S-Parameter']);
        $('input.char#cwsweep[name="ifb"]').val(data.corder['IF-Bandwidth']);
        $('input.char#cwsweep[name="freq"]').val(data.corder['Frequency']);
        $('input.char#cwsweep[name="powa"]').val(data.corder['Power']);
        // load edittable comment:
        cwsweepcomment = data.comment;
        // load narrated comment:
        $('textarea.char#cwsweep[name="comment"]').text(data.comment);

        // load c-range for each command:
        // SCROLL: scroll out repeated data (the exact reverse of averaging)
        
        // REPEATS:
        $('select.char.cwsweep.parameter#c-repeat').empty();
        if (data.data_repeat > 1) {
            $('select.char.cwsweep.parameter#c-repeat').append($('<option>', { text: 'X-ALL', value: 'x' })).append($('<option>', { text: 'X-COUNT', value: 'xc' }))
                .append($('<option>', { text: 'SCROLL', value: 'sc' })).append($('<option>', { text: 'Y-ALL', value: 'y' }));
        };
        for (i = 0; i < data.data_repeat; i++) { $('select.char.cwsweep.parameter#c-repeat').append($('<option>', { text: i+1, value: i })); };

        // OPTIONALS:
        $('select.char.cwsweep.parameter#c-fluxbias').empty();
        if (data.cfluxbias_data.length > 1) {
            $('select.char.cwsweep.parameter#c-fluxbias').append($('<option>', { text: 'X-ALL', value: 'x' })).append($('<option>', { text: 'X-COUNT', value: 'xc' }))
                .append($('<option>', { text: 'SCROLL', value: 'sc' })).append($('<option>', { text: 'Y-ALL', value: 'y' }));
        };
        $.each(data.cfluxbias_data, function(i,v){ $('select.char.cwsweep.parameter#c-fluxbias').append($('<option>', { text: v, value: i })); });

        $('select.char.cwsweep.parameter#c-xyfreq').empty()
        if (data.cxyfreq_data.length > 1) {
            $('select.char.cwsweep.parameter#c-xyfreq').append($('<option>', { text: 'X-ALL', value: 'x' })).append($('<option>', { text: 'X-COUNT', value: 'xc' }))
                .append($('<option>', { text: 'SCROLL', value: 'sc' })).append($('<option>', { text: 'Y-ALL', value: 'y' }));
        };
        $.each(data.cxyfreq_data, function(i,v){ $('select.char.cwsweep.parameter#c-xyfreq').append($('<option>', { text: v, value: i })); });
        
        $('select.char.cwsweep.parameter#c-xypowa').empty()
        if (data.cxypowa_data.length > 1) {
            $('select.char.cwsweep.parameter#c-xypowa').append($('<option>', { text: 'X-ALL', value: 'x' })).append($('<option>', { text: 'X-COUNT', value: 'xc' }))
                .append($('<option>', { text: 'SCROLL', value: 'sc' })).append($('<option>', { text: 'Y-ALL', value: 'y' }));
        };
        $.each(data.cxypowa_data, function(i,v){ $('select.char.cwsweep.parameter#c-xypowa').append($('<option>', { text: v, value: i })); });
        
        // BASICS:
        $('select.char.cwsweep.parameter#c-sparam').empty()
        if (data.csparam_data.length > 1) {
            $('select.char.cwsweep.parameter#c-sparam').append($('<option>', { text: 'X-ALL', value: 'x' })).append($('<option>', { text: 'X-COUNT', value: 'xc' }))
                .append($('<option>', { text: 'SCROLL', value: 'sc' })).append($('<option>', { text: 'Y-ALL', value: 'y' }));
        };
        $.each(data.csparam_data, function(i,v){ $('select.char.cwsweep.parameter#c-sparam').append($('<option>', { text: v, value: i })); });
        
        $('select.char.cwsweep.parameter#c-ifb').empty()
        if (data.cifb_data.length > 1) {
            $('select.char.cwsweep.parameter#c-ifb').append($('<option>', { text: 'X-ALL', value: 'x' })).append($('<option>', { text: 'X-COUNT', value: 'xc' }))
                .append($('<option>', { text: 'SCROLL', value: 'sc' })).append($('<option>', { text: 'Y-ALL', value: 'y' }));
        };
        $.each(data.cifb_data, function(i,v){ $('select.char.cwsweep.parameter#c-ifb').append($('<option>', { text: v, value: i })); });
        
        $('select.char.cwsweep.parameter#c-freq').empty()
        if (data.cfreq_data.length > 1) {
            $('select.char.cwsweep.parameter#c-freq').append($('<option>', { text: 'X-ALL', value: 'x' })).append($('<option>', { text: 'X-COUNT', value: 'xc' }))
                .append($('<option>', { text: 'SCROLL', value: 'sc' })).append($('<option>', { text: 'Y-ALL', value: 'y' }));
        };
        $.each(data.cfreq_data, function(i,v){ $('select.char.cwsweep.parameter#c-freq').append($('<option>', { text: v, value: i })); });
        
        $('select.char.cwsweep.parameter#c-powa').empty()
        if (data.cpowa_data.length > 1) {
            $('select.char.cwsweep.parameter#c-powa').append($('<option>', { text: 'X-ALL', value: 'x' })).append($('<option>', { text: 'X-COUNT', value: 'xc' }))
                .append($('<option>', { text: 'SCROLL', value: 'sc' })).append($('<option>', { text: 'Y-ALL', value: 'y' }));
        };
        $.each(data.cpowa_data, function(i,v){ $('select.char.cwsweep.parameter#c-powa').append($('<option>', { text: v, value: i })); });
        
        // load data progress:
        var data_progress = "  " + String(data.data_progress.toFixed(3)) + "%";
        $('.data-progress#cwsweep').css({"width": data_progress}).text(data_progress);
        $('.data-eta#cwsweep').text("data: " + data.measureacheta + " until completion");
        console.log("Progress: " + data_progress);
    });
    return false;
};
function plot1D_cwsweep(x1,y1,y2,xtitle,phasetype) {
    console.log(xtitle);
    
    let traceL = {x: [], y: [], mode: 'lines', type: 'scatter', 
        name: 'Amplitude (' + wday + ', ' + wmoment + ')',
        line: {color: 'rgb(23, 151, 6)', width: 2.5},
        yaxis: 'y' };
    let traceR = {x: [], y: [], mode: 'lines', type: 'scatter', 
        name: 'Phase (' + wday + ', ' + wmoment + ')',
        line: {color: 'blue', width: 2.5},
        yaxis: 'y2' };

    let layout = {
        legend: {x: 1.08},
        height: $(window).height()*0.8,
        width: $(window).width()*0.7,
        xaxis: {
            zeroline: false,
            title: xtitle,
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
            title: phasetype, 
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
    $.each(y1, function(i, val) {traceL.y.push(val);});
    $.each(x1, function(i, val) {traceR.x.push(val);});
    $.each(y2, function(i, val) {traceR.y.push(val);});

    var Trace = [traceL, traceR]
    Plotly.newPlot('char-cwsweep-chart', Trace, layout, {showSendToCloud: true});
    $( "i.cwsweep1d" ).remove(); //clear previous
};
function plot2D_cwsweep(x,y,ZZ,xtitle,ytitle,plotype,mission,colorscal) {
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

// hiding parameter settings when click outside the modal box:
$('.modal-toggle.new.cwsweep').on('click', function(e) {
    e.preventDefault();
    $('.modal.new.cwsweep').toggleClass('is-visible');
    // revert back to previous option upon leaving dialogue box
    $('select.char#cwsweep[name="wday"]').val(selecteday);
});
$('.modal-toggle.search.cwsweep').on('click', function(e) {
    e.preventDefault();
    $('.modal.search.cwsweep').toggleClass('is-visible');
});
$('.modal-toggle.data-reset.cwsweep').on('click', function(e) {
    e.preventDefault();
    $('.modal.data-reset.cwsweep').toggleClass('is-visible');
});

// show CW-Sweep's daylist
$(function() {
    $('button.char#cwsweep').bind('click', function() {
        $('div.charcontent').hide();
        $('div.charcontent#cwsweep').show();
        $('button.char').removeClass('selected');
        $('button.char#cwsweep').addClass('selected');
        $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/init', {
        }, function (data) {
            console.log("run status: " + data.run_status);
            if (data.run_status == true) {
                $( "i.cwsweep-run" ).remove(); //clear previous
                $('button.char#cwsweep').prepend("<i class='cwsweep-run fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
            } else {};
            $('select.char#cwsweep[name="wday"]').empty();
            $('select.char#cwsweep[name="wday"]').append($('<option>', { text: 'The latest:', value: '' }));
            $.each(data.daylist.reverse(), function(i,v){
                $('select.char#cwsweep[name="wday"]').append($('<option>', {
                    text: v,
                    value: data.daylist.length - 1 - i
                }));
            });
            $('select.char#cwsweep[name="wday"]').append($('<option>', { text: '--Search--', value: 's' }));
            if (data.run_permission == false) {
                $('input.char#cwsweep-run').hide();
                console.log("RUN BUTTON DISABLED");
            } else {
                $('select.char#cwsweep[name="wday"]').append($('<option>', { text: '--New--', value: -1 }));
            };
        });
        return false;
    });
});

// list times based on day picked
$(function () {
    $('select.char#cwsweep[name="wday"]').on('change', function () {
        listimes_cwsweep();
    });
    return false;
});

// click to run:
$('input.char#cwsweep-run').bind('click', function() {
    $( "i.cwsweep-run" ).remove(); //clear previous
    $('button.char#cwsweep').prepend("<i class='cwsweep-run fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
    // waveform commands
    var fluxbias = $('input.char#cwsweep[name="fluxbias"]').val();
    var xyfreq = $('input.char#cwsweep[name="xyfreq"]').val();
    var xypowa = $('input.char#cwsweep[name="xypowa"]').val();
    var sparam = $('input.char#cwsweep[name="sparam"]').val();
    var ifb = $('input.char#cwsweep[name="ifb"]').val();
    var freq = $('input.char#cwsweep[name="freq"]').val();
    var powa = $('input.char#cwsweep[name="powa"]').val();
    var comment = JSON.stringify($('textarea.char#cwsweep[name="ecomment"]').val());
    // Simulate or Real run?
    var simulate = $('input.char#cwsweep[name="simulate"]').is(':checked')?1:0; //use css to respond to click / touch
    console.log("simulate: " + simulate);
    // var comment = $('textarea.char#cwsweep[name="comment"]').val();
    $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/new', {
        wday: wday, 
        fluxbias: fluxbias, xyfreq: xyfreq, xypowa: xypowa, 
        sparam: sparam, ifb: ifb, freq: freq, powa: powa, 
        comment: comment, simulate: simulate
    }, function (data) { 
        console.log("test each loop: " + data.testeach);      
        $( "i.cwsweep-run" ).remove(); //clear previous
    });
    return false;
});
// click to estimate ETA
$("a.new#cwsweep-eta").bind('click', function() {
    $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/eta100', {
    }, function (data) {
        $("a.new#cwsweep-eta").text('ETA in\n' + String(data.eta_time_100));
    });
});
// click to set repeat or once
$('input.char#cwsweep[name="repeat"]').bind('click', function() {
    set_repeat_cwsweep();
});

// click to search: (pending)
$('input.char#cwsweep[name="search"]').change( function() {
    $( "i.cwsweep" ).remove(); //clear previous
    $('button.char#cwsweep').prepend("<i class='cwsweep fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
    // waveform commands
    
    // var comment = $('textarea.char#cwsweep[name="comment"]').val();
    $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/search', {
        
    }, function (data) {
        
        console.log("complete: " + data.filelist);
        $( "i.cwsweep" ).remove(); //clear previous
    });
    return false;
});

// click to pause measurement
$(function () {
    $('button.char#cwsweep-pause').on('click', function () {
        $( "i.cwsweep" ).remove(); //clear previous
        $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/pause', {
            // direct pause
        }, function(data) {
            console.log("paused: " + data.pause);
        });
        return false;
    });
});

// Click to resume measurement
$(function () {
    $('button.char#cwsweep-resume').on('click', function () {
        $( "i.cwsweep" ).remove(); //clear previous
        $('button.char#cwsweep').prepend("<i class='cwsweep fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        // waveform commands
        var fluxbias = $('input.char#cwsweep[name="fluxbias"]').val();
        var xyfreq = $('input.char#cwsweep[name="xyfreq"]').val();
        var xypowa = $('input.char#cwsweep[name="xypowa"]').val();
        var sparam = $('input.char#cwsweep[name="sparam"]').val();
        var ifb = $('input.char#cwsweep[name="ifb"]').val();
        var freq = $('input.char#cwsweep[name="freq"]').val();
        var powa = $('input.char#cwsweep[name="powa"]').val();
        $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/resume', {
            wday: wday, wmoment: wmoment, 
            fluxbias: fluxbias, xyfreq: xyfreq, xypowa: xypowa, 
            sparam: sparam, ifb: ifb, freq: freq, powa: powa
        }, function (data) {
            if (data.resumepoint == data.datasize) {
                console.log("The data was already complete!")
            } else { console.log("The data has just been updated")};
            $( "i.cwsweep" ).remove(); //clear previous
        });
        return false;
    });
});

// access data based on time picked
$(function () {
    $('select.char#cwsweep[name="wmoment"]').on('change', function () {
        accessdata_cwsweep();
    });
    return false;
});

// LIVE UPDATE on PROGRESS:
$(function () {
    $('input.cwsweep#live-update').click(function () { 
        //indicate it is still running:
        $( "i.cwsweeplive" ).remove(); //clear previous
        $('button.char#cwsweep').prepend("<i class='cwsweeplive fa fa-wifi fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        var livestat = $('input.cwsweep#live-update').is(':checked'); //use css to respond to click / touch
        if (livestat == true) {
            var cwsweeploop = setInterval(accessdata_cwsweep, 6000);
            $('input.cwsweep#live-update').click(function () {
                clearInterval(cwsweeploop);
                $( "i.cwsweeplive" ).remove(); //clear previous
            });
        };
        // 'else' didn't do much to stop it!
    });
});

// tracking data position based on certain parameter (PENDING: Need to be tested after code modification been done)
$(function () {
    $('select.char.cwsweep.parameter').on('change', function () {
        var fixed = this.getAttribute('id').split('c-')[1];
        var fixedvalue = $('select.char.cwsweep.parameter#c-' + fixed).val();
        $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/trackdata', {
            fixed: fixed, fixedvalue: fixedvalue,
        }, function (data) {
            console.log('data position for branch ' + fixed + ' is ' + data.data_location);
            $('div#char-cwsweep-announcement').empty().append($('<h4 style="color: red;"></h4>').text(fixed + ' is fixed at ' + data.data_location));
        })
    });
    return false;
});

// assemble 1D-data based on c-parameters picked
$(function () {
    $('input.char#cwsweep[name="1d-data"]').on('click', function () {
        $( "i.cwsweep1d" ).remove(); //clear previous
        $('button.char#cwsweep').prepend("<i class='cwsweep1d fa fa-palette fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        var irepeat = $('select.char.cwsweep.parameter#c-repeat').val();
        var ifluxbias = $('select.char.cwsweep.parameter#c-fluxbias').val();
        var ixyfreq = $('select.char.cwsweep.parameter#c-xyfreq').val();
        var ixypowa = $('select.char.cwsweep.parameter#c-xypowa').val();
        var isparam = $('select.char.cwsweep.parameter#c-sparam').val();
        var iifb = $('select.char.cwsweep.parameter#c-ifb').val();
        var ifreq = $('select.char.cwsweep.parameter#c-freq').val();
        var ipowa = $('select.char.cwsweep.parameter#c-powa').val();
        console.log("Picked: " + isparam);
        $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/1ddata', {
            irepeat: irepeat, ifluxbias: ifluxbias, ixyfreq: ixyfreq, ixypowa: ixypowa, isparam: isparam, iifb: iifb, ifreq: ifreq, ipowa: ipowa
        }, function (data) {
            window.x1 = data.x1;
            window.y1 = data.y1;
            window.yp = data.yp;
            window.yup = data.yup;
            window.x1title = data.x1title;
            // Phase option
            $('select.char.data#cwsweep[name="1d-phase"]').empty().append($('<option>', { text: 'Pha', value: 'Pha' })).append($('<option>', { text: 'UPha', value: 'UPha' }));
            plot1D_cwsweep(x1,y1,yp,x1title,'<b>Raw-Pha(rad)</b>');
        });
    });
    return false;
});
$('select.char.data#cwsweep').on('change', function() {
    if ($('select.char.data#cwsweep[name="1d-phase"]').val() == "Pha") {
        console.log("Pha mode");
        plot1D_cwsweep(x1,y1,yp,x1title,'<b>Raw-Pha(rad)</b>');
    } else if ($('select.char.data#cwsweep[name="1d-phase"]').val() == "UPha") {
        console.log("UPha mode");
        plot1D_cwsweep(x1,y1,yup,x1title,'<b>UFN-Pha(rad)</b>');
    };
    return false;
});

// assemble 2D-data based on c-parameters picked
$(function () {
    $('input.char#cwsweep[name="2d-data"]').on('click', function () {
        $( "i.cwsweep2d" ).remove(); //clear previous
        $('button.char#cwsweep').prepend("<i class='cwsweep2d fa fa-palette fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        var irepeat = $('select.char.cwsweep.parameter#c-repeat').val();
        var ifluxbias = $('select.char.cwsweep.parameter#c-fluxbias').val();
        var ixyfreq = $('select.char.cwsweep.parameter#c-xyfreq').val();
        var ixypowa = $('select.char.cwsweep.parameter#c-xypowa').val();
        var isparam = $('select.char.cwsweep.parameter#c-sparam').val();
        var iifb = $('select.char.cwsweep.parameter#c-ifb').val();
        var ifreq = $('select.char.cwsweep.parameter#c-freq').val();
        var ipowa = $('select.char.cwsweep.parameter#c-powa').val();
        console.log("Picked: " + isparam);
        $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/2ddata', {
            irepeat: irepeat, ifluxbias: ifluxbias, ixyfreq: ixyfreq, ixypowa: ixypowa, isparam: isparam, iifb: iifb, ifreq: ifreq, ipowa: ipowa
        }, function (data) {
            window.x = data.x;
            window.y = data.y;
            window.ZZA = data.ZZA;
            window.ZZP = data.ZZP;
            window.xtitle = data.xtitle;
            window.ytitle = data.ytitle;
            // Amplitude (default) or Phase
            $('select.char.data#cwsweep[name="2d-amphase"]').empty().append($('<option>', { text: 'Amp', value: 'Amp' })).append($('<option>', { text: 'Pha (Raw)', value: 'Pha' }));
            // Data grooming
            $('select.char.data#cwsweep[name="2d-type"]').empty().append($('<option>', { text: 'direct', value: 'direct' }))
                .append($('<option>', { text: 'normalYdip', value: 'normalYdip' })).append($('<option>', { text: 'normalYpeak', value: 'normalYpeak' }))
                .append($('<option>', { text: 'normalXdip', value: 'normalXdip' })).append($('<option>', { text: 'normalXpeak', value: 'normalXpeak' }));
            // Data color-scaling
            $('select.char.data#cwsweep[name="2d-colorscale"]').empty().append($('<option>', { text: 'YlOrRd', value: 'YlOrRd' }))
                .append($('<option>', { text: 'YlGnBu', value: 'YlGnBu' })).append($('<option>', { text: 'RdBu', value: 'RdBu' }))
                .append($('<option>', { text: 'Portland', value: 'Portland' })).append($('<option>', { text: 'Picnic', value: 'Picnic' }))
                .append($('<option>', { text: 'Jet', value: 'Jet' })).append($('<option>', { text: 'Hot', value: 'Hot' }))
                .append($('<option>', { text: 'Greys', value: 'Greys' })).append($('<option>', { text: 'Greens', value: 'Greens' }))
                .append($('<option>', { text: 'Electric', value: 'Electric' })).append($('<option>', { text: 'Earth', value: 'Earth' }))
                .append($('<option>', { text: 'Bluered', value: 'Bluered' })).append($('<option>', { text: 'Blackbody', value: 'Blackbody' }))
                .append($('<option>', { text: 'Blues', value: 'Blues' })).append($('<option>', { text: 'Viridis', value: 'Viridis' }));
            // Transpose or not
            $('select.char.data#cwsweep[name="2d-direction"]').empty().append($('<option>', { text: 'stay', value: 'stay' })).append($('<option>', { text: 'rotate', value: 'rotate' }));
            plot2D_cwsweep(x, y, ZZA, xtitle, ytitle, 
                $('select.char.data#cwsweep[name="2d-type"]').val(),'cwsweep',
                $('select.char.data#cwsweep[name="2d-colorscale"]').val());
            $( "i.cwsweep2d" ).remove(); //clear previous
        });
    });
    return false;
});
$('select.char.data#cwsweep').on('change', function() {
    if ($('select.char.data#cwsweep[name="2d-amphase"]').val() == "Amp") {var ZZ = ZZA; }
    else if ($('select.char.data#cwsweep[name="2d-amphase"]').val() == "Pha") {var ZZ = ZZP; };
    if ($('select.char.data#cwsweep[name="2d-direction"]').val() == "rotate") {
        plot2D_cwsweep(y, x, transpose(ZZ), ytitle, xtitle, 
            $('select.char.data#cwsweep[name="2d-type"]').val(),'cwsweep',
            $('select.char.data#cwsweep[name="2d-colorscale"]').val());
    } else {
        plot2D_cwsweep(x, y, ZZ, xtitle, ytitle, 
            $('select.char.data#cwsweep[name="2d-type"]').val(),'cwsweep',
            $('select.char.data#cwsweep[name="2d-colorscale"]').val());
    };
    return false;
});

// saving exported csv-data to client's PC:
$('button.char#cwsweep-savecsv').on('click', function() {
    console.log("SAVING FILE");
    $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/export/1dcsv', {
        // merely for security screening purposes
        ifreq: $('select.char#cwsweep[name="c-freq"]').val()
    }, function (data) {
        console.log("STATUS: " + data.status);
        $.ajax({
            url: 'http://qum.phys.sinica.edu.tw:5300/mach/uploads/1Dcwsweep.csv',
            method: 'GET',
            xhrFields: {
                responseType: 'blob'
            },
            success: function (data) {
                var a = document.createElement('a');
                var url = window.URL.createObjectURL(data);
                a.href = url;
                a.download = '1dcwsweepdata.csv';
                document.body.append(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
            }
        });
    });
    return false;
});

// Brings up RESET Modal Box:
$('button.char#cwsweep-datareset').on('click', function () {
    $('.modal.data-reset.cwsweep').toggleClass('is-visible');
});
$('input.char.cwsweep.data-reset#cwsweep-reset').on('click', function () {
    $('div.char.cwsweep.confirm').show();
    $('button.char.cwsweep.reset-yes').on('click', function () {
        $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/resetdata', {
            ownerpassword: $('input.char#cwsweep[name="ownerpassword"]').val(),
            truncateafter: $('input.char#cwsweep[name="truncateafter"]').val(),
        }, function (data) {
            $('div#char-cwsweep-announcement').empty().append($('<h4 style="color: red;"></h4>').text(data.message + '. Please refresh by clicking CWSWEEP.'));
        });
        $('div.char.cwsweep.confirm').hide();
        return false;
    });
    return false;
});
$('button.char.cwsweep.reset-no').on('click', function () {
    $('div.char.cwsweep.confirm').hide();
    return false;
});


