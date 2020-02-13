// CW Sweep: 
$(document).ready(function(){
    $('div.char.sqepulse.confirm').hide();
    $("a.new#sqepulse-eta").text('ETA: ');
    get_repeat_sqepulse();
});

// Global variables:
window.selecteday = ''

// PENDING: Flexible C-Structure:
var SQEPulse_Parameters = ['repeat', 'Flux-Bias', 'XY-Frequency', 'XY-Power', 'RO-Frequency', 'RO-Power',
'Pulse-Period', 'RO-ifLevel', 'RO-Pulse-Delay', 'RO-Pulse-Width', 'XY-ifLevel', 'XY-Pulse-Delay', 'XY-Pulse-Width', 
'LO-Frequency', 'LO-Power', 'ADC-delay', 'Average', 'Sampling-Time'];

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
function set_repeat_sqepulse() {
    $.getJSON('/mssn/char/sqepulse/setrepeat', {
        repeat: $('input.char.sqepulse.repeat').is(':checked')?1:0
    }, function(data) {
        $( "i.sqepulse-repeat" ).remove(); //clear previous
        if (data.repeat == true) {
            $('button.char#sqepulse').prepend("<i class='sqepulse-repeat fa fa-repeat fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        };
    });
};
function get_repeat_sqepulse() {
    $.getJSON('/mssn/char/sqepulse/getrepeat', {
    }, function (data) {
        console.log("Repeat: " + data.repeat);
        $('input.char.sqepulse.repeat').prop("checked", data.repeat);
        $( "i.sqepulse-repeat" ).remove(); //clear previous
        if (data.repeat == true) {
            $('button.char#sqepulse').prepend("<i class='sqepulse-repeat fa fa-repeat fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        };
    });
};
function listimes_sqepulse() {
    $('input.char.data').removeClass("plotted");
    // make global wday
    window.wday = $('select.char.sqepulse#wday').val();
    if (Number(wday) < 0) {
        // brings up parameter-input panel for new measurement:
        $('.modal.new').toggleClass('is-visible');

    } else if (wday == 's') {
        // brings up search panel:
        $('.modal.search.sqepulse').toggleClass('is-visible');
    } else {
        selecteday = wday
        $.getJSON('/mssn/char/sqepulse/time', {
            wday: wday
        }, function (data) {
            $('select.char.sqepulse#wmoment').empty().append($('<option>', { text: 'pick', value: '' }));
            $.each(data.taskentries, function(i,v){ $('select.char.sqepulse#wmoment').append($('<option>', { id: i, text: v, value: v })); });
        }); 
    };
};
function accessdata_sqepulse() {
    // Make global variable:
    window.wmoment = $('select.char.sqepulse#wmoment').val();
    $('.data-progress#sqepulse').css({"width": 0}).text('accessing...');
    $.getJSON('/mssn/char/sqepulse/access', {
        // input/select value here:
        wmoment: wmoment
    }, function (data) {
        console.log(data.corder);

        // SCROLL: scroll out repeated data (the exact reverse of averaging)
        $.each(SQEPulse_Parameters, function(i,cparam){
            // console.log('cparam: ' + cparam + '\ndata: ' + data.pdata[cparam]);

            // Loading data into parameter-range selectors:
            $('select.char.sqepulse#' + cparam).empty();
            if ( data.pdata[cparam].length > 1) {
                $('select.char.sqepulse#' + cparam).append($('<option>', { text: 'X-ALL', value: 'x' })).append($('<option>', { text: 'X-COUNT', value: 'xc' }))
                    .append($('<option>', { text: 'SAMPLE', value: 's' })).append($('<option>', { text: 'Y-ALL', value: 'y' }));
            };
            $.each(data.pdata[cparam], function(i,v){ $('select.char.sqepulse#' + cparam).append($('<option>', { text: v, value: i })); });

            // Loading parameter-range into inputs for new run:
            $('input.char.sqepulse#' + cparam).val(data.corder[cparam]);

        });

        // load edittable comment:
        $('textarea.char.sqepulse#ecomment').val(data.comment);
        // load narrated comment:
        $('textarea.char.sqepulse#comment').text(data.comment);
        
        // Loading data progress:
        var data_progress = "  " + String(data.data_progress.toFixed(3)) + "%";
        $('.data-progress#sqepulse').css({"width": data_progress}).text(data_progress);
        $('.data-eta#sqepulse').text("data: " + data.measureacheta + " until completion");
        console.log("Progress: " + data_progress);
    });
    return false;
};
function plot1D_sqepulse(x,y1,y2,y3,xtitle) {
    console.log(xtitle);
    
    let traceI = {x: [], y: [], mode: 'lines', type: 'scatter', 
        name: 'I',
        line: {color: 'red', width: 2.5},
        yaxis: 'y' };
    let traceQ = {x: [], y: [], mode: 'lines', type: 'scatter', 
        name: 'Q',
        line: {color: 'blue', width: 2.5},
        yaxis: 'y' };
    let traceA = {x: [], y: [], mode: 'lines', type: 'scatter', 
        name: '$\\sqrt{I^{2}+Q^{2}}$',
        line: {color: 'black', width: 2.5},
        yaxis: 'y' };
    
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
            title: '<b>Signal(V)</b>',
            titlefont: {size: 18},
            tickfont: {size: 18},
            tickwidth: 3,
            linewidth: 3
        },
        
        title: ''
        };
    
    // I
    $.each(x, function(i, val) {traceI.x.push(val);});
    $.each(y1, function(i, val) {traceI.y.push(val);});
    // Q
    $.each(x, function(i, val) {traceQ.x.push(val);});
    $.each(y2, function(i, val) {traceQ.y.push(val);});
    // A (V or dBm)
    $.each(x, function(i, val) {traceA.x.push(val);});
    if ($('select.char.data.sqepulse#1d-VdBm').val() == 'V') {
        $.each(y3, function(i, val) {traceA.y.push(val);});
    } else if ($('select.char.data.sqepulse#1d-VdBm').val() == 'dBm') {
        $.each(y3, function(i, val) {
            var val = 10*Math.log10(val**2/50*1000);
            traceA.y.push(val);
        });
    };

    var Trace = [traceI, traceQ, traceA]
    Plotly.newPlot('char-sqepulse-chart', Trace, layout, {showSendToCloud: true});
    $( "i.sqepulse1d" ).remove(); //clear previous
};
function compare1D_sqepulse(x,y1,y2,normalize=false,direction='dip') {
    
    let traceA = {x: [], y: [], mode: 'lines', type: 'scatter', 
        name: 'Original',
        line: {color: 'blue', width: 2.5},
        yaxis: 'y' };
    let traceB = {x: [], y: [], mode: 'lines', type: 'scatter', 
        name: 'Added',
        line: {color: 'red', width: 2.5},
        yaxis: 'y' };
    
    let layout = {
        legend: {x: 1.08}, height: $(window).height()*0.8, width: $(window).width()*0.7,
        xaxis: { zeroline: false, title: xtitle, titlefont: {size: 18}, tickfont: {size: 18}, tickwidth: 3, linewidth: 3 },
        yaxis: { zeroline: false, title: '<b>Signal(V)</b>', titlefont: {size: 18}, tickfont: {size: 18}, tickwidth: 3, linewidth: 3 },
        
        title: ''
        };
    
    if (normalize == true) {
        if (direction == 'dip') {
            y1 = Normalize_Dip(y1);
            y2 = Normalize_Dip(y2);
        } else if (direction == 'peak') {
            y1 = Normalize_Peak(y1);
            y2 = Normalize_Peak(y2);
        };
    };

    // Original
    $.each(x, function(i, val) {traceA.x.push(val);});
    $.each(y1, function(i, val) {traceA.y.push(val);});
    // Added
    $.each(x, function(i, val) {traceB.x.push(val);});
    $.each(y2, function(i, val) {traceB.y.push(val);});
    
    var Trace = [traceA, traceB]
    Plotly.newPlot('char-sqepulse-chart', Trace, layout, {showSendToCloud: true});
    $( "i.sqepulse1d" ).remove(); //clear previous
};
function plot2D_sqepulse(x,y,ZZ,xtitle,ytitle,plotype,mission,colorscal) {
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
$('.modal-toggle.new.sqepulse').on('click', function(e) {
    e.preventDefault();
    $('.modal.new.sqepulse').toggleClass('is-visible');
    // revert back to previous option upon leaving dialogue box
    $('select.char.sqepulse#wday').val(selecteday);
});
$('.modal-toggle.search.sqepulse').on('click', function(e) {
    e.preventDefault();
    $('.modal.search.sqepulse').toggleClass('is-visible');
});
$('.modal-toggle.data-reset.sqepulse').on('click', function(e) {
    e.preventDefault();
    $('.modal.data-reset.sqepulse').toggleClass('is-visible');
});

// show CW-Sweep's daylist
$(function() {
    $('button.char#sqepulse').bind('click', function() {
        $('div.charcontent').hide();
        $('div.charcontent#sqepulse').show();
        $('button.char').removeClass('selected');
        $('button.char#sqepulse').addClass('selected');
        $.getJSON('/mssn/char/sqepulse/init', {
        }, function (data) {
            console.log("run status: " + data.run_status);
            if (data.run_status == true) {
                $( "i.sqepulse-run" ).remove(); //clear previous
                $('button.char#sqepulse').prepend("<i class='sqepulse-run fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
            } else {};
            $('select.char.sqepulse#wday').empty();
            $('select.char.sqepulse#wday').append($('<option>', { text: 'The latest:', value: '' }));
            $.each(data.daylist.reverse(), function(i,v){
                $('select.char.sqepulse#wday').append($('<option>', {
                    text: v,
                    value: data.daylist.length - 1 - i
                }));
            });
            $('select.char.sqepulse#wday').append($('<option>', { text: '--Search--', value: 's' }));
            if (data.run_permission == false) {
                $('input.char#sqepulse-run').hide();
                console.log("RUN BUTTON DISABLED");
            } else {
                $('select.char.sqepulse#wday').append($('<option>', { text: '--New--', value: -1 }));
            };
        });
        return false;
    });
});

// list times based on day picked
$(function () {
    $('select.char.sqepulse#wday').on('change', function () {
        listimes_sqepulse();
    });
    return false;
});

// click to run:
$('input.char#sqepulse-run').bind('click', function() {
    $( "i.sqepulse-run" ).remove(); //clear previous
    $('button.char#sqepulse').prepend("<i class='sqepulse-run fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
    
    // Assemble CORDER from parameter-inputs:
    var CORDER = {};
    CORDER['C-Structure'] = SQEPulse_Parameters;
    $.each(SQEPulse_Parameters, function(i,cparam){ CORDER[cparam] = $('input.char.sqepulse#' + cparam).val(); });
    CORDER['repeat'] = '0'; // factor out repeat for file-size calculation
    console.log('CORDER["repeat"]: ' + CORDER['repeat']);
    console.log('CORDER["Average"]: ' + CORDER['Average']);
    
    var comment = JSON.stringify($('textarea.char.sqepulse#ecomment').val());
    var simulate = $('input.char#sqepulse[name="simulate"]').is(':checked')?1:0; //use css to respond to click / touch
    console.log("simulate: " + simulate);
    
    $.getJSON('/mssn/char/sqepulse/new', {
        wday: wday, CORDER: JSON.stringify(CORDER), comment: comment, simulate: simulate
    }, function (data) { 
        console.log("test each loop: " + data.testeach);      
        $( "i.sqepulse-run" ).remove(); //clear previous
    });
    return false;
});
// click to estimate ETA
$("a.new#sqepulse-eta").bind('click', function() {
    $.getJSON('/mssn/char/sqepulse/eta100', {
    }, function (data) {
        $("a.new#sqepulse-eta").text('ETA in\n' + String(data.eta_time_100));
    });
});
// click to set repeat or once
$('input.char.sqepulse.repeat').bind('click', function() {
    set_repeat_sqepulse();
});

// click to search: (pending)
$('input.char.sqepulse#search').change( function() {
    $( "i.sqepulse" ).remove(); //clear previous
    $('button.char#sqepulse').prepend("<i class='sqepulse fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
    // waveform commands
    
    // var comment = $('textarea.char#sqepulse[name="comment"]').val();
    $.getJSON('/mssn/char/sqepulse/search', {
        
    }, function (data) {
        
        console.log("complete: " + data.filelist);
        $( "i.sqepulse" ).remove(); //clear previous
    });
    return false;
});

// click to pause measurement
$(function () {
    $('button.char#sqepulse-pause').on('click', function () {
        $( "i.sqepulse" ).remove(); //clear previous
        $.getJSON('/mssn/char/sqepulse/pause', {
            // direct pause
        }, function(data) {
            console.log("paused: " + data.pause);
        });
        return false;
    });
});

// Click to resume measurement
$(function () {
    $('button.char#sqepulse-resume').on('click', function () {
        $( "i.sqepulse" ).remove(); //clear previous
        $('button.char#sqepulse').prepend("<i class='sqepulse fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        
        // Assemble CORDER from parameter-inputs:
        var CORDER = {};
        CORDER['C-Structure'] = SQEPulse_Parameters;
        $.each(SQEPulse_Parameters, function(i,cparam){ CORDER[cparam] = $('input.char.sqepulse#' + cparam).val(); });
        CORDER['repeat'] = '0'; // factor out repeat for file-size calculation
        console.log('CORDER["repeat"]: ' + CORDER['repeat']);
        console.log('CORDER["Average"]: ' + CORDER['Average']);

        $.getJSON('/mssn/char/sqepulse/resume', {
            wday: wday, wmoment: wmoment, CORDER: JSON.stringify(CORDER)
        }, function (data) {
            if (data.resumepoint == data.datasize) {
                console.log("The data was already complete!")
            } else { console.log("The data has just been updated")};
            $( "i.sqepulse" ).remove(); //clear previous
        });
        return false;
    });
});

// access data based on time picked
$(function () {
    $('select.char.sqepulse#wmoment').on('change', function () {
        accessdata_sqepulse();
    });
    return false;
});

// LIVE UPDATE on PROGRESS:
$(function () {
    $('input.sqepulse#live-update').click(function () { 
        //indicate it is still running:
        $( "i.sqepulselive" ).remove(); //clear previous
        $('button.char#sqepulse').prepend("<i class='sqepulselive fa fa-wifi fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        var livestat = $('input.sqepulse#live-update').is(':checked'); //use css to respond to click / touch
        if (livestat == true) {
            var sqepulseloop = setInterval(accessdata_sqepulse, 6000);
            $('input.sqepulse#live-update').click(function () {
                clearInterval(sqepulseloop);
                $( "i.sqepulselive" ).remove(); //clear previous
            });
        };
        // 'else' didn't do much to stop it!
    });
});

// tracking data position based on certain parameter
$(function () {
    $('select.char#sqepulse').on('change', function () {
        var fixed = this.getAttribute('name').split('c-')[1];
        $.getJSON('/mssn/char/sqepulse/trackdata', {
            ifluxbias: $('select.char#sqepulse[name="c-fluxbias"]').val(),
            ixyfreq: $('select.char#sqepulse[name="c-xyfreq"]').val(),
            ixypowa: $('select.char#sqepulse[name="c-xypowa"]').val(),
        }, function (data) {
            console.log('data position for xyfreq is ' + data.data_location.xyfreq);
            console.log('data position for xypowa is ' + data.data_location.xypowa);
            $('div#char-sqepulse-announcement').empty().append($('<h4 style="color: red;"></h4>').text(fixed + ' is fixed at ' + data.data_location[fixed]));
        })
    });
    return false;
});

// assemble 1D-data based on c-parameters picked
$(function () {
    $('input.char.sqepulse#1d-data').on('click', function () {
        $( "i.sqepulse1d" ).remove(); //clear previous
        $('button.char#sqepulse').prepend("<i class='sqepulse1d fa fa-palette fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        // var irepeat = $('select.char.sqepulse#repeat').val();
        var cselect = {};
        $.each(SQEPulse_Parameters, function(i,cparam){ cselect[cparam] = $('select.char.sqepulse#' + cparam).val(); });
        console.log("Picked Flux: " + cselect['Flux-Bias']);
        var srange = $('input.char.data.sqepulse#sample-range').val();
        $.getJSON('/mssn/char/sqepulse/1ddata', {
            cselect: JSON.stringify(cselect), srange: srange
        }, function (data) {
            window.x = data.x;
            window.yI = data.yI;
            window.yQ = data.yQ;
            window.yA = data.yA;
            window.xtitle = data.xtitle;
            // Phase option
            // $('select.char.data.sqepulse#1d-phase').empty().append($('<option>', { text: 'Pha', value: 'Pha' })).append($('<option>', { text: 'UPha', value: 'UPha' }));
            plot1D_sqepulse(x,yI,yQ,yA,xtitle);
        });
    });
    return false;
});
// INSERT 1D-data for comparison
$(function () {
    $('button.char#sqepulse-insert-1D').on('click', function () {
        $( "i.sqepulse1d" ).remove(); //clear previous
        $('button.char#sqepulse').prepend("<i class='sqepulse1d fa fa-palette fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        // var irepeat = $('select.char.sqepulse#repeat').val();
        var cselect = {};
        $.each(SQEPulse_Parameters, function(i,cparam){ cselect[cparam] = $('select.char.sqepulse#' + cparam).val(); });
        console.log("Picked Flux: " + cselect['Flux-Bias']);
        var srange = $('input.char.data.sqepulse#sample-range').val();
        $.getJSON('/mssn/char/sqepulse/1ddata', {
            cselect: JSON.stringify(cselect), srange: srange
        }, function (data) {
            window.x2 = data.x;
            window.yI2 = data.yI;
            window.yQ2 = data.yQ;
            window.yA2 = data.yA;
            window.xtitle2 = data.xtitle;

            // Normalization Options:
            $('select.char.data.sqepulse#compare-nml').empty().append($('<option>', { text: 'direct', value: 'direct' }))
                                                                .append($('<option>', { text: 'normaldip', value: 'normaldip' }))
                                                                .append($('<option>', { text: 'normalpeak', value: 'normalpeak' }));

            console.log('selected: ' + $('select.char.data.sqepulse#compare-nml').val());
            normalize = Boolean($('select.char.data.sqepulse#compare-nml').val()!='direct');
            direction = $('select.char.data.sqepulse#compare-nml').val().split('normal')[1];
            compare1D_sqepulse(x,yA,yA2,normalize,direction);
        });
    });
    return false;
});
$('select.char.data.sqepulse#compare-nml').on('change', function() {
    normalize = Boolean($('select.char.data.sqepulse#compare-nml').val()!='direct');
    direction = $('select.char.data.sqepulse#compare-nml').val().split('normal')[1];
    compare1D_sqepulse(x,yA,yA2,normalize,direction);
    return false;
});

// assemble 2D-data based on c-parameters picked
$(function () {
    $('input.char#sqepulse[name="2d-data"]').on('click', function () {
        $( "i.sqepulse2d" ).remove(); //clear previous
        $('button.char#sqepulse').prepend("<i class='sqepulse2d fa fa-palette fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        var irepeat = $('select.char#sqepulse[name="c-repeat"]').val();
        var ifluxbias = $('select.char#sqepulse[name="c-fluxbias"]').val();
        var ixyfreq = $('select.char#sqepulse[name="c-xyfreq"]').val();
        var ixypowa = $('select.char#sqepulse[name="c-xypowa"]').val();
        var isparam = $('select.char#sqepulse[name="c-sparam"]').val();
        var iifb = $('select.char#sqepulse[name="c-ifb"]').val();
        var ifreq = $('select.char#sqepulse[name="c-freq"]').val();
        var ipowa = $('select.char#sqepulse[name="c-powa"]').val();
        console.log("Picked: " + isparam);
        $.getJSON('/mssn/char/sqepulse/2ddata', {
            irepeat: irepeat, ifluxbias: ifluxbias, ixyfreq: ixyfreq, ixypowa: ixypowa, isparam: isparam, iifb: iifb, ifreq: ifreq, ipowa: ipowa
        }, function (data) {
            window.x = data.x;
            window.y = data.y;
            window.ZZA = data.ZZA;
            window.ZZP = data.ZZP;
            window.xtitle = data.xtitle;
            window.ytitle = data.ytitle;
            // Amplitude (default) or Phase
            $('select.char.data#sqepulse[name="2d-amphase"]').empty().append($('<option>', { text: 'Amp', value: 'Amp' })).append($('<option>', { text: 'Pha', value: 'Pha' }));
            // Data grooming
            $('select.char.data#sqepulse[name="2d-type"]').empty().append($('<option>', { text: 'direct', value: 'direct' }))
                .append($('<option>', { text: 'normalYdip', value: 'normalYdip' })).append($('<option>', { text: 'normalYpeak', value: 'normalYpeak' }))
                .append($('<option>', { text: 'normalXdip', value: 'normalXdip' })).append($('<option>', { text: 'normalXpeak', value: 'normalXpeak' }));
            // Data color-scaling
            $('select.char.data#sqepulse[name="2d-colorscale"]').empty().append($('<option>', { text: 'YlOrRd', value: 'YlOrRd' }))
                .append($('<option>', { text: 'YlGnBu', value: 'YlGnBu' })).append($('<option>', { text: 'RdBu', value: 'RdBu' }))
                .append($('<option>', { text: 'Portland', value: 'Portland' })).append($('<option>', { text: 'Picnic', value: 'Picnic' }))
                .append($('<option>', { text: 'Jet', value: 'Jet' })).append($('<option>', { text: 'Hot', value: 'Hot' }))
                .append($('<option>', { text: 'Greys', value: 'Greys' })).append($('<option>', { text: 'Greens', value: 'Greens' }))
                .append($('<option>', { text: 'Electric', value: 'Electric' })).append($('<option>', { text: 'Earth', value: 'Earth' }))
                .append($('<option>', { text: 'Bluered', value: 'Bluered' })).append($('<option>', { text: 'Blackbody', value: 'Blackbody' }))
                .append($('<option>', { text: 'Blues', value: 'Blues' })).append($('<option>', { text: 'Viridis', value: 'Viridis' }));
            // Transpose or not
            $('select.char.data#sqepulse[name="2d-direction"]').empty().append($('<option>', { text: 'stay', value: 'stay' })).append($('<option>', { text: 'rotate', value: 'rotate' }));
            plot2D_sqepulse(x, y, ZZA, xtitle, ytitle, 
                $('select.char.data#sqepulse[name="2d-type"]').val(),'sqepulse',
                $('select.char.data#sqepulse[name="2d-colorscale"]').val());
            $( "i.sqepulse2d" ).remove(); //clear previous
        });
    });
    return false;
});
$('select.char.data#sqepulse').on('change', function() {
    if ($('select.char.data#sqepulse[name="2d-amphase"]').val() == "Amp") {var ZZ = ZZA; }
    else if ($('select.char.data#sqepulse[name="2d-amphase"]').val() == "Pha") {var ZZ = ZZP; };
    if ($('select.char.data#sqepulse[name="2d-direction"]').val() == "rotate") {
        plot2D_sqepulse(y, x, transpose(ZZ), ytitle, xtitle, 
            $('select.char.data#sqepulse[name="2d-type"]').val(),'sqepulse',
            $('select.char.data#sqepulse[name="2d-colorscale"]').val());
    } else {
        plot2D_sqepulse(x, y, ZZ, xtitle, ytitle, 
            $('select.char.data#sqepulse[name="2d-type"]').val(),'sqepulse',
            $('select.char.data#sqepulse[name="2d-colorscale"]').val());
    };
    return false;
});

// saving exported csv-data to client's PC:
$('button.char#sqepulse-savecsv').on('click', function() {
    console.log("SAVING FILE");
    $.getJSON('/mssn/char/sqepulse/export/1dcsv', {
        // merely for security screening purposes
        ifreq: $('select.char#sqepulse[name="c-freq"]').val()
    }, function (data) {
        console.log("STATUS: " + data.status);
        $.ajax({
            url: 'http://qum.phys.sinica.edu.tw:5300/mach/uploads/1Dsqepulse.csv',
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

// Brings up RESET Modal Box:
$('button.char#sqepulse-datareset').on('click', function () {
    $('.modal.data-reset.sqepulse').toggleClass('is-visible');
});
$('input.char.sqepulse.data-reset#sqepulse-reset').on('click', function () {
    $('div.char.sqepulse.confirm').show();
    $('button.char.sqepulse.reset-yes').on('click', function () {
        $.getJSON('/mssn/char/sqepulse/resetdata', {
            ownerpassword: $('input.char#sqepulse[name="ownerpassword"]').val(),
            truncateafter: $('input.char#sqepulse[name="truncateafter"]').val(),
        }, function (data) {
            $('div#char-sqepulse-announcement').empty().append($('<h4 style="color: red;"></h4>').text(data.message + '. Please refresh by clicking SQE-PULSE.'));
        });
        $('div.char.sqepulse.confirm').hide();
        return false;
    });
    return false;
});
$('button.char.sqepulse.reset-no').on('click', function () {
    $('div.char.sqepulse.confirm').hide();
    return false;
});


