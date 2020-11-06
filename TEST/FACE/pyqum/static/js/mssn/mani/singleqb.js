// CW Sweep: 
$(document).ready(function(){
    $('div.char.singleqb.confirm').hide();
    $('button.char#singleqb-savecsv').hide();
    $("a.new#singleqb-eta").text('ETA: ');
    $("a.new#singleqb-msg").text('Measurement Status');
    get_repeat_singleqb();
    window.singleqbcomment = "";
});

// Global variables:
window.selecteday = ''
window.VdBm_selector = 'select.char.data.singleqb#1d-VdBm'
window.VdBm_selector2 = 'select.char.data.singleqb#2d-VdBm'

// PENDING: Flexible C-Structure:
var singleqb_Parameters = ['repeat', 'Flux-Bias', 'XY-Frequency', 'XY-Power', 'RO-Frequency', 'RO-Power',
'Pulse-Period', 'RO-ifLevel', 'RO-Pulse-Delay', 'RO-Pulse-Width', 'XY-ifLevel', 'XY-Pulse-Delay', 'XY-Pulse-Width', 
'LO-Frequency', 'LO-Power', 'ADC-delay', 'Average', 'Sampling-Time'];
var singleqb_Peripherals = ['data-option','lock-period'];

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
function set_repeat_singleqb() {
    $.getJSON(mssnencrpytonian() + '/mssn/char/singleqb/setrepeat', {
        repeat: $('input.char.singleqb.repeat').is(':checked')?1:0
    }, function(data) {
        $( "i.singleqb-repeat" ).remove(); //clear previous
        if (data.repeat == true) {
            $('button.char#singleqb').prepend("<i class='singleqb-repeat fa fa-repeat fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        };
    });
};
function get_repeat_singleqb() {
    $.getJSON(mssnencrpytonian() + '/mssn/char/singleqb/getrepeat', {
    }, function (data) {
        console.log("Repeat: " + data.repeat);
        $('input.char.singleqb.repeat').prop("checked", data.repeat);
        $( "i.singleqb-repeat" ).remove(); //clear previous
        if (data.repeat == true) {
            $('button.char#singleqb').prepend("<i class='singleqb-repeat fa fa-repeat fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        };
    });
};
function listimes_singleqb() {
    $('input.char.data').removeClass("plotted");
    // make global wday
    window.wday = $('select.char.singleqb#wday').val();
    if (Number(wday) < 0) {
        // brings up parameter-input panel for new measurement:
        $('.modal.new').toggleClass('is-visible');
        // Update Live Informations:
        $.getJSON('/mach/all/mxc', {}, function (data) {
            $("textarea.char.singleqb#ecomment").val(singleqbcomment + "\nUpdate: T6=" + data.mxcmk + "mK");
        });

    } else if (wday == 'm') {
        // brings up manage panel:
        $('.modal.manage.singleqb').toggleClass('is-visible');
    } else {
        selecteday = wday
        $.getJSON(mssnencrpytonian() + '/mssn/char/singleqb/time', {
            wday: wday
        }, function (data) {
            $('select.char.singleqb#wmoment').empty().append($('<option>', { text: 'pick', value: '' }));
            $.each(data.taskentries, function(i,v){ $('select.char.singleqb#wmoment').append($('<option>', { id: i, text: v, value: v })); });
        }); 
    };
};
function accessdata_singleqb() {
    // Make global variable:
    window.wmoment = $('select.char.singleqb#wmoment').val();
    $('.data-progress#singleqb').css({"width": 0}).text('accessing...');
    $.getJSON(mssnencrpytonian() + '/mssn/char/singleqb/access', {
        // input/select value here:
        wmoment: wmoment
    }, function (data) {
        console.log(data.corder);

        // SCROLL: scroll out repeated data (the exact reverse of averaging)
        $.each(singleqb_Parameters, function(i,cparam){
            // console.log('cparam: ' + cparam + '\ndata: ' + data.pdata[cparam]);

            // Loading data into parameter-range selectors:
            // Loading Sweeping Options:
            $('select.char.singleqb#' + cparam).empty();
            if ( data.pdata[cparam].length > 1) {
                $('select.char.singleqb#' + cparam).append($('<option>', { text: 'X-ALL', value: 'x' })).append($('<option>', { text: 'X-COUNT', value: 'xc' }))
                    .append($('<option>', { text: 'SAMPLE', value: 's' })).append($('<option>', { text: 'Y-ALL', value: 'y' }));
            };
            // Loading Constant Values:
            if (data.pdata[cparam].length > 301) {
                // to speed up loading process, it is limited to 301 entries per request.
                $.each(data.pdata[cparam].slice(0,301), function(i,v){ $('select.char.singleqb#' + cparam).append($('<option>', { text: v, value: i })); });
                $('select.char.singleqb#' + cparam).append($('<option>', { text: 'more...', value: 'm' }));
                // Pending:  Use "more" to select/enter value manually!
            } else {
                $.each(data.pdata[cparam], function(i,v){ $('select.char.singleqb#' + cparam).append($('<option>', { text: v, value: i })); });
            };

            // Loading parameter-range into inputs for new run:
            $('input.char.singleqb#' + cparam).val(data.corder[cparam]);

        });

        console.log("C-Config: " + data.corder['C-Config']);
        console.log("C-Config undefined: " + (typeof data.corder['C-Config'] == "undefined")); //detecting undefined
        if (typeof data.corder['C-Config'] != "undefined") { // for backward compatible
            $.each(singleqb_Peripherals, function(i,peripheral){ 
                // Loading peripheral-options into selects for new run:
                if (typeof data.corder['C-Config'][peripheral] == "undefined") {
                    $('select.char.singleqb#' + peripheral).val('default'); } // defaults
                else { $('select.char.singleqb#' + peripheral).val(data.corder['C-Config'][peripheral]); };
            });
        };

        // load edittable comment:
        singleqbcomment = data.comment;
        // load narrated comment:
        $('textarea.char.singleqb#comment').text(data.comment);
        
        // Loading data progress:
        var data_progress = "  " + String(data.data_progress.toFixed(3)) + "%";
        $('.data-progress#singleqb').css({"width": data_progress}).text(data_progress);
        $('.data-eta#singleqb').text("data: " + data.measureacheta + " until completion");
        console.log("Progress: " + data_progress);
    });
    return false;
};
function plot1D_singleqb(x,y1,y2,y3,y5,VdBm_selector,xtitle,mode='lines') {
    // V or dBm
    YConv = VdBm_Conversion(y3, VdBm_selector); 
    y3 = YConv['y'];
    yunit = YConv['yunit'];
    console.log('Converted: ' + YConv);
    
    let traceI = {x: [], y: [], mode: mode, type: 'scatter', 
        name: 'I',
        line: {color: 'red', width: 2.5},
        marker: {symbol: 'square-dot', size: 3.7},
        yaxis: 'y' };
    let traceQ = {x: [], y: [], mode: mode, type: 'scatter', 
        name: 'Q',
        line: {color: 'blue', width: 2.5},
        marker: {symbol: 'square-dot', size: 3.7},
        yaxis: 'y' };
    let traceA = {x: [], y: [], mode: mode, type: 'scatter', 
        name: '$\\sqrt{I^{2}+Q^{2}}$',
        line: {color: 'black', width: 2.5},
        marker: {symbol: 'square-dot', size: 3.7},
        yaxis: 'y' };
    let tracePha = {x: [], y: [], mode: mode, type: 'scatter', 
        name: '$\\tan^{-1}(\\frac{Q}{I})$',
        line: {color: 'orange', width: 2.5},
        marker: {symbol: 'square-dot', size: 3.7},
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
            title: '<b>Signal(' + yunit + ')</b>',
            titlefont: {size: 18},
            tickfont: {size: 18},
            tickwidth: 3,
            linewidth: 3,
        },
        yaxis2: {
            zeroline: false,
            title: '<b>$UFN-Phase(\\frac{rad}{\\Delta x})$</b>', 
            titlefont: {color: 'rgb(148, 103, 189)', size: 18}, 
            tickfont: {color: 'rgb(148, 103, 189)', size: 18},
            tickwidth: 3,
            linewidth: 3, 
            overlaying: 'y', 
            side: 'right'
        },
        title: '',
        };
    
    // I
    $.each(x, function(i, val) {traceI.x.push(val);});
    $.each(y1, function(i, val) {traceI.y.push(val);});
    // Q
    $.each(x, function(i, val) {traceQ.x.push(val);});
    $.each(y2, function(i, val) {traceQ.y.push(val);});
    // Amp
    $.each(x, function(i, val) {traceA.x.push(val);});
    $.each(y3, function(i, val) {traceA.y.push(val);});
    // Pha
    $.each(x, function(i, val) {tracePha.x.push(val);});
    $.each(y5, function(i, val) {tracePha.y.push(val);});

    var Trace = [traceI, traceQ, traceA, tracePha]
    Plotly.newPlot('char-singleqb-chart', Trace, layout, {showSendToCloud: true});
    $( "i.singleqb1d" ).remove(); //clear previous
};
function compare1D_singleqb(x1,y1,x2,y2,normalize=false,direction='dip',VdBm_selector) {
    // V or dBm
    y1 = VdBm_Conversion(y1, VdBm_selector)['y']; 
    y2 = VdBm_Conversion(y2, VdBm_selector)['y']; 
    // yunit = YConv['yunit'];

    // Left:
    let traceA = {x: [], y: [], mode: 'lines', type: 'scatter', 
        name: 'Original',
        line: {color: 'blue', width: 2.5},
        yaxis: 'y' };
    let traceB = {x: [], y: [], mode: 'lines', type: 'scatter', 
        name: 'Compared',
        line: {color: 'red', width: 2.5},
        yaxis: 'y' };
    // Right:
    let traceS = {x: [], y: [], mode: 'lines', type: 'scatter', 
        name: 'Subtracted',
        line: {color: 'grey', width: 2.5},
        yaxis: 'y2' };
    
    let layout = {
        legend: {x: 1.08}, height: $(window).height()*0.8, width: $(window).width()*0.7,
        xaxis: { zeroline: false, title: xtitle, titlefont: {size: 18}, tickfont: {size: 18}, tickwidth: 3, linewidth: 3 },
        yaxis: { zeroline: false, title: '<b>Signal(V)</b>', titlefont: {size: 18}, tickfont: {size: 18}, tickwidth: 3, linewidth: 3 },
        yaxis2: { zeroline: false, title: '<b>Difference(V)</b>', titlefont: {color: 'Grey', size: 18}, 
            tickfont: {color: 'grey', size: 18}, tickwidth: 3, linewidth: 3, overlaying: 'y', side: 'right' },
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
    $.each(x1, function(i, val) {traceA.x.push(val);});
    $.each(y1, function(i, val) {traceA.y.push(val);});
    // Compared
    $.each(x2, function(i, val) {traceB.x.push(val);});
    $.each(y2, function(i, val) {traceB.y.push(val);});
    // Subtracted:
    $.each(x2, function(i, val) { traceS.x.push(val); });
    $.each(y2, function(i, val) { traceS.y.push(y1[i]-y2[i]); });
    
    var Trace = [traceA, traceB, traceS]
    Plotly.newPlot('char-singleqb-chart', Trace, layout, {showSendToCloud: true});
    $( "i.singleqb1d" ).remove(); //clear previous
};
function plot2D_singleqb(x,y,ZZ,xtitle,ytitle,plotype,mission,colorscal,VdBm_selector) {
    // V or dBm
    YConv = VdBm_Conversion(y, VdBm_selector); 
    y = YConv['y'];
    yunit = YConv['yunit'];

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
            zeroline: false, title: ytitle + '{' + yunit + '}',
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
$('.modal-toggle.new.singleqb').on('click', function(e) {
    e.preventDefault();
    $('.modal.new.singleqb').toggleClass('is-visible');
    // revert back to previous option upon leaving dialogue box
    $('select.char.singleqb#wday').val(selecteday);
});
$('.modal-toggle.manage.singleqb').on('click', function(e) {
    e.preventDefault();
    $('.modal.manage.singleqb').toggleClass('is-visible');
    // revert back to previous option upon leaving dialogue box
    $('select.char.singleqb#wday').val(selecteday);
});
$('.modal-toggle.data-reset.singleqb').on('click', function(e) {
    e.preventDefault();
    $('.modal.data-reset.singleqb').toggleClass('is-visible');
});

// show CW-Sweep's daylist
$(function() {
    $('button.char#singleqb').bind('click', function() {
        $('div.charcontent').hide();
        $('div.charcontent#singleqb').show();
        $('button.char').removeClass('selected');
        $('button.char#singleqb').addClass('selected');
        $.getJSON(mssnencrpytonian() + '/mssn/char/singleqb/init', {
        }, function (data) {
            console.log("run status: " + data.run_status);
            if (data.run_status == true) {
                $( "i.singleqb-run" ).remove(); //clear previous
                $('button.char#singleqb').prepend("<i class='singleqb-run fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
            } else {};
            $('select.char.singleqb#wday').empty();
            $('select.char.singleqb#wday').append($('<option>', { text: 'The latest:', value: '' }));
            $.each(data.daylist.reverse(), function(i,v){
                $('select.char.singleqb#wday').append($('<option>', {
                    text: v,
                    value: data.daylist.length - 1 - i
                }));
            });
            $('select.char.singleqb#wday').append($('<option>', { text: '--Manage--', value: 'm' }));
            if (data.run_permission == false) {
                $('input.char#singleqb-run').hide();
                console.log("RUN BUTTON DISABLED");
            } else {
                $('select.char.singleqb#wday').append($('<option>', { text: '--New--', value: -1 }));
            };
        });
        return false;
    });
});

// list times based on day picked
$(function () {
    $('select.char.singleqb#wday').on('change', function () {
        listimes_singleqb();
    });
    return false;
});

// click to run:
$('input.char#singleqb-run').bind('click', function() {
    $( "i.singleqb-run" ).remove(); //clear previous
    $('button.char#singleqb').prepend("<i class='singleqb-run fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
    
    // Assemble CORDER from parameter-inputs:
    var CORDER = {};
    CORDER['C-Config'] = {};
    $.each(singleqb_Peripherals, function(i,peripheral){ CORDER['C-Config'][peripheral] = $('select.char.singleqb#' + peripheral).val(); });
    CORDER['C-Structure'] = singleqb_Parameters;
    $.each(singleqb_Parameters, function(i,cparam){ CORDER[cparam] = $('input.char.singleqb#' + cparam).val(); });
    CORDER['repeat'] = '0'; // factor out repeat for file-size calculation
    console.log('CORDER["repeat"]: ' + CORDER['repeat']);
    console.log('CORDER["Average"]: ' + CORDER['C-Config']);
    
    var comment = JSON.stringify($('textarea.char.singleqb#ecomment').val());
    var simulate = $('input.char.singleqb#simulate').is(':checked')?1:0; //use css to respond to click / touch
    console.log("simulate: " + simulate);
    
    $.getJSON(mssnencrpytonian() + '/mssn/char/singleqb/new', {
        wday: wday, CORDER: JSON.stringify(CORDER), comment: comment, simulate: simulate
    }, function (data) { 
        console.log("test each loop: " + data.testeach);      
        $( "i.singleqb-run" ).remove(); //clear previous
    });
    return false;
});
// click to get MSG about measurement status:
$("a.new#singleqb-msg").bind('click', function() {
    $.getJSON(mssnencrpytonian() + '/mssn/char/singleqb/getmessage', {
    }, function (data) {
        if (data.msg.indexOf('measurement started')==0) {
            $( "i.singleqb-run" ).remove(); //clear previous
            $("a.new#singleqb-msg").text("Running").css("background-color", "mintcream");
            $('button.char#singleqb').prepend("<i class='singleqb-run fa fa-spinner fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        } else if (data.msg.indexOf('measurement concluded')==0) {
            $( "i.singleqb-run" ).remove(); //clear previous
            $("a.new#singleqb-msg").text("Stopped").css("background-color", "cornsilk").css("color", "red");
        } else { $("a.new#singleqb-msg").text(String(data.msg)).css("background-color", "coral").css("color", "red"); }
    });
});
// click to estimate ETA
$("a.new#singleqb-eta").bind('click', function() {
    $.getJSON(mssnencrpytonian() + '/mssn/char/singleqb/eta100', {
    }, function (data) {
        $("a.new#singleqb-eta").text('ETA in\n' + String(data.eta_time_100));
    });
});
// click to set repeat or once
$('input.char.singleqb.repeat').bind('click', function() {
    set_repeat_singleqb();
});

// click to search: (pending)
$('input.char.singleqb#search').change( function() {
    $( "i.singleqb" ).remove(); //clear previous
    $('button.char#singleqb').prepend("<i class='singleqb fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
    // waveform commands
    
    // var comment = $('textarea.char#singleqb[name="comment"]').val();
    $.getJSON(mssnencrpytonian() + '/mssn/char/singleqb/search', {
        
    }, function (data) {
        
        console.log("complete: " + data.filelist);
        $( "i.singleqb" ).remove(); //clear previous
    });
    return false;
});

// click to pause measurement
$(function () {
    $('button.char#singleqb-pause').on('click', function () {
        $( "i.singleqb" ).remove(); //clear previous
        $.getJSON(mssnencrpytonian() + '/mssn/char/singleqb/pause', {
            // direct pause
        }, function(data) {
            console.log("paused: " + data.pause);
        });
        return false;
    });
});

// Click to resume measurement (PENDING: Error(s) to be fixed)
$(function () {
    $('button.char#singleqb-resume').on('click', function () {
        $( "i.singleqb-run" ).remove(); //clear previous
        $('button.char#singleqb').prepend("<i class='singleqb-run fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        
        // Assemble CORDER from parameter-inputs:
        var CORDER = {};
        CORDER['C-Config'] = {};
        $.each(singleqb_Peripherals, function(i,peripheral){ CORDER['C-Config'][peripheral] = $('select.char.singleqb#' + peripheral).val(); });
        CORDER['C-Structure'] = singleqb_Parameters;
        $.each(singleqb_Parameters, function(i,cparam){ CORDER[cparam] = $('input.char.singleqb#' + cparam).val(); });
        CORDER['repeat'] = '0'; // factor out repeat for file-size calculation
        console.log('CORDER["repeat"]: ' + CORDER['repeat']);
        console.log('CORDER["Average"]: ' + CORDER['Average']);

        $.getJSON(mssnencrpytonian() + '/mssn/char/singleqb/resume', {
            wday: selecteday, wmoment: wmoment, CORDER: JSON.stringify(CORDER)
        }, function (data) {
            if (data.resumepoint == data.datasize) {
                console.log("The data was already complete!")
            } else { console.log("The data has just been updated")};
            $( "i.singleqb" ).remove(); //clear previous
        });
        return false;
    });
});

// access data based on time picked
$(function () {
    $('select.char.singleqb#wmoment').on('change', function () {
        accessdata_singleqb();
    });
    return false;
});

// LIVE UPDATE on PROGRESS:
$(function () {
    $('input.singleqb#live-update').click(function () { 
        //indicate it is still running:
        $( "i.singleqblive" ).remove(); //clear previous
        $('button.char#singleqb').prepend("<i class='singleqblive fa fa-wifi fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        var livestat = $('input.singleqb#live-update').is(':checked'); //use css to respond to click / touch
        if (livestat == true) {
            var singleqbloop = setInterval(accessdata_singleqb, 6000);
            $('input.singleqb#live-update').click(function () {
                clearInterval(singleqbloop);
                $( "i.singleqblive" ).remove(); //clear previous
            });
        };
        // 'else' didn't do much to stop it!
    });
});

// tracking data position based on certain parameter
$(function () {
    $('select.char.singleqb').on('change', function () {
        var fixed = this.getAttribute('id');
        var fixedvalue = $('select.char.singleqb#' + fixed).val();
        $.getJSON(mssnencrpytonian() + '/mssn/char/singleqb/trackdata', {
            fixed: fixed, fixedvalue: fixedvalue,
        }, function (data) {
            console.log('data position for branch ' + fixed + ' is ' + data.data_location);
            $('div#char-singleqb-announcement').empty().append($('<h4 style="color: red;"></h4>').text(fixed + ' is fixed at ' + data.data_location))
            .append($('<h4 style="color: blue;"></h4>').text('a location after ' + data.data_location + ' data-point(s)'));
        })
    });
    return false;
});

// assemble 1D-data based on c-parameters picked
$(function () {
    $('input.char.singleqb#1d-data').on('click', function () {
        $('div#char-singleqb-announcement').empty();
        $( "i.singleqb1d" ).remove(); //clear previous
        $('button.char#singleqb').prepend("<i class='singleqb1d fa fa-palette fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        // var irepeat = $('select.char.singleqb#repeat').val();
        var cselect = {};
        $.each(singleqb_Parameters, function(i,cparam){ cselect[cparam] = $('select.char.singleqb#' + cparam).val(); });
        console.log("Picked Flux: " + cselect['Flux-Bias']);
        var srange = $('input.char.data.singleqb#sample-range').val();
        var smode = $('select.char.data.singleqb#sample-mode').val();
        $.getJSON(mssnencrpytonian() + '/mssn/char/singleqb/1ddata', {
            cselect: JSON.stringify(cselect), srange: srange, smode: smode,
        }, function (data) {
            window.x = data.x;
            window.yI = data.yI;
            window.yQ = data.yQ;
            window.yA = data.yA;
            window.yUFNP = data.yUFNP;
            window.xtitle = data.xtitle;
            // Phase option
            // $('select.char.data.singleqb#1d-phase').empty().append($('<option>', { text: 'Pha', value: 'Pha' })).append($('<option>', { text: 'UPha', value: 'UPha' }));
            plot1D_singleqb(x,yI,yQ,yA,yUFNP,VdBm_selector,xtitle);
        })
            .done(function(data) {
                $('button.char#singleqb-savecsv').show(); // to avoid downloading the wrong file
                $('div#char-singleqb-announcement').append($('<h4 style="color: red;"></h4>').text("Successfully Plot 1D:"));
            })
            .fail(function(jqxhr, textStatus, error){
                $('div#char-singleqb-announcement').append($('<h4 style="color: red;"></h4>').text("Oops: " + error));
                $( "i.singleqb1d" ).remove(); //clear the status
            });
    });
    return false;
});
// INSERT 1D-data for comparison
$(function () {
    $('button.char#singleqb-insert-1D').on('click', function () {
        $('div#char-singleqb-announcement').empty();
        $( "i.singleqb1d" ).remove(); //clear previous
        $('button.char#singleqb').prepend("<i class='singleqb1d fa fa-palette fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        // var irepeat = $('select.char.singleqb#repeat').val();
        var cselect = {};
        $.each(singleqb_Parameters, function(i,cparam){ cselect[cparam] = $('select.char.singleqb#' + cparam).val(); });
        console.log("Picked Flux: " + cselect['Flux-Bias']);
        var srange = $('input.char.data.singleqb#sample-range').val();
        var smode = $('select.char.data.singleqb#sample-mode').val();
        $.getJSON(mssnencrpytonian() + '/mssn/char/singleqb/1ddata', {
            cselect: JSON.stringify(cselect), srange: srange, smode: smode,
        }, function (data) {
            window.x2 = data.x;
            window.yI2 = data.yI;
            window.yQ2 = data.yQ;
            window.yA2 = data.yA;
            window.yUFNP2 = data.yUFNP;
            window.xtitle2 = data.xtitle;

            // Normalization Options:
            $('select.char.data.singleqb#compare-nml').empty().append($('<option>', { text: 'direct', value: 'direct' }))
                                                                .append($('<option>', { text: 'normaldip', value: 'normaldip' }))
                                                                .append($('<option>', { text: 'normalpeak', value: 'normalpeak' }));

            console.log('selected: ' + $('select.char.data.singleqb#compare-nml').val());
            normalize = Boolean($('select.char.data.singleqb#compare-nml').val()!='direct');
            direction = $('select.char.data.singleqb#compare-nml').val().split('normal')[1];
            // console.log("yA: " + yA); console.log("yA2: " + yA2);
            compare1D_singleqb(x,yA,x2,yA2,normalize,direction,VdBm_selector);
        })
            .fail(function(jqxhr, textStatus, error){
                $('div#char-singleqb-announcement').append($('<h4 style="color: red;"></h4>').text("Oops: " + error));
                $( "i.singleqb1d" ).remove(); //clear the status
            });
    });
    return false;
});
$('select.char.data.singleqb#compare-nml').on('change', function() {
    normalize = Boolean($('select.char.data.singleqb#compare-nml').val()!='direct');
    direction = $('select.char.data.singleqb#compare-nml').val().split('normal')[1];
    compare1D_singleqb(x,yA,x2,yA2,normalize,direction,VdBm_selector);
    return false;
});
$(VdBm_selector).on('change', function() {
    plot1D_singleqb(x,yI,yQ,yA,yUFNP,VdBm_selector,xtitle);
});
$('select.char.data.singleqb#1d-mode').on('change', function() {
    plot1D_singleqb(x,yI,yQ,yA,yUFNP,VdBm_selector,xtitle,mode=$('select.char.data.singleqb#1d-mode').val());
});

// assemble 2D-data based on c-parameters picked
$(function () {
    $('input.char.singleqb#2d-data').on('click', function () {
        $('div#char-singleqb-announcement').empty().append($('<h4 style="color: red;"></h4>').text("Plotting 2D might takes some time. Please wait... "));
        $( "i.singleqb2d" ).remove(); //clear previous
        $('button.char#singleqb').prepend("<i class='singleqb2d fa fa-palette fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        // var irepeat = $('select.char.singleqb#repeat').val();
        var cselect = {};
        $.each(singleqb_Parameters, function(i,cparam){ cselect[cparam] = $('select.char.singleqb#' + cparam).val(); });
        console.log("Picked Flux: " + cselect['Flux-Bias']);
        var srange = $('input.char.data.singleqb#sample-range').val();
        $.getJSON(mssnencrpytonian() + '/mssn/char/singleqb/2ddata', {
            cselect: JSON.stringify(cselect), srange: srange
        }, function (data) {
            window.x = data.x;
            window.y = data.y;
            console.log("check y: " + y);
            window.ZZA = data.ZZA;
            window.ZZUP = data.ZZUP;
            window.ZZI = data.ZZI;
            window.ZZQ = data.ZZQ;
            window.xtitle = data.xtitle;
            window.ytitle = data.ytitle;
            // Amplitude (default) or Phase
            $('select.char.data.singleqb#2d-iqamphase').empty().append($('<option>', { text: 'Amp', value: 'Amp' })).append($('<option>', { text: 'Pha', value: 'Pha' }))
                                                                .append($('<option>', { text: 'I', value: 'I' })).append($('<option>', { text: 'Q', value: 'Q' }));
            // Data grooming
            $('select.char.data.singleqb#2d-type').empty().append($('<option>', { text: 'direct', value: 'direct' }))
                .append($('<option>', { text: 'normalYdip', value: 'normalYdip' })).append($('<option>', { text: 'normalYpeak', value: 'normalYpeak' }))
                .append($('<option>', { text: 'normalXdip', value: 'normalXdip' })).append($('<option>', { text: 'normalXpeak', value: 'normalXpeak' }));
            // Data color-scaling
            $('select.char.data.singleqb#2d-colorscale').empty().append($('<option>', { text: 'YlOrRd', value: 'YlOrRd' }))
                .append($('<option>', { text: 'YlGnBu', value: 'YlGnBu' })).append($('<option>', { text: 'RdBu', value: 'RdBu' }))
                .append($('<option>', { text: 'Portland', value: 'Portland' })).append($('<option>', { text: 'Picnic', value: 'Picnic' }))
                .append($('<option>', { text: 'Jet', value: 'Jet' })).append($('<option>', { text: 'Hot', value: 'Hot' }))
                .append($('<option>', { text: 'Greys', value: 'Greys' })).append($('<option>', { text: 'Greens', value: 'Greens' }))
                .append($('<option>', { text: 'Electric', value: 'Electric' })).append($('<option>', { text: 'Earth', value: 'Earth' }))
                .append($('<option>', { text: 'Bluered', value: 'Bluered' })).append($('<option>', { text: 'Blackbody', value: 'Blackbody' }))
                .append($('<option>', { text: 'Blues', value: 'Blues' })).append($('<option>', { text: 'Viridis', value: 'Viridis' }));
            // Transpose or not
            $('select.char.data.singleqb#2d-direction').empty().append($('<option>', { text: 'stay', value: 'stay' })).append($('<option>', { text: 'rotate', value: 'rotate' }));
            plot2D_singleqb(x, y, ZZA, xtitle, ytitle, 
                $('select.char.data.singleqb#2d-type').val(),'singleqb',
                $('select.char.data.singleqb#2d-colorscale').val(),
                VdBm_selector2);
            $( "i.singleqb2d" ).remove(); //clear previous
        })
            .fail(function(jqxhr, textStatus, error){
                $('div#char-singleqb-announcement').append($('<h4 style="color: red;"></h4>').text("Oops: " + error + "(" + textStatus + ")"));
                $( "i.singleqb2d" ).remove(); //clear the status
            })
            .always(function(){
                $('div#char-singleqb-announcement').empty().append($('<h4 style="color: red;"></h4>').text("2D Plot Completed"));
                $( "i.singleqb2d" ).remove(); //clear the status
            });
    });
    return false;
});
$('div.2D select.char.data.singleqb').on('change', function() {

    if ($('select.char.data.singleqb#2d-iqamphase').val() == "Amp") {var ZZ = ZZA; }
    else if ($('select.char.data.singleqb#2d-iqamphase').val() == "Pha") {var ZZ = ZZUP; }
    else if ($('select.char.data.singleqb#2d-iqamphase').val() == "I") {var ZZ = ZZI; }
    else if ($('select.char.data.singleqb#2d-iqamphase').val() == "Q") {var ZZ = ZZQ; };
    
    if ($('select.char.data.singleqb#2d-direction').val() == "rotate") {
        plot2D_singleqb(y, x, transpose(ZZ), ytitle, xtitle, 
            $('select.char.data.singleqb#2d-type').val(),'singleqb',
            $('select.char.data.singleqb#2d-colorscale').val(),
            VdBm_selector2);
    } else {
        plot2D_singleqb(x, y, ZZ, xtitle, ytitle, 
            $('select.char.data.singleqb#2d-type').val(),'singleqb',
            $('select.char.data.singleqb#2d-colorscale').val(),
            VdBm_selector2);
    };
    return false;
});

// saving exported csv-data to client's PC:
$('button.char#singleqb-savecsv').on('click', function() {
    console.log("SAVING FILE");
    $.getJSON(mssnencrpytonian() + '/mssn/char/singleqb/export/1dcsv', {
        // merely for security screening purposes
        ifreq: $('select.char.singleqb#RO-Frequency').val()
    }, function (data) {
        console.log("STATUS: " + data.status);
        console.log('User ' + data.user_name + ' is downloading 1D-Data');
        $.ajax({
            url: 'http://qum.phys.sinica.edu.tw:5300/mach/uploads/1Dsingleqb[' + data.user_name + '].csv',
            method: 'GET',
            xhrFields: {
                responseType: 'blob'
            },
            success: function (data) {
                var a = document.createElement('a');
                var url = window.URL.createObjectURL(data);
                a.href = url;
                a.download = '1Dsingleqb.csv';
                document.body.append(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
                $('button.char#singleqb-savecsv').hide();
            }
        });
    });
    return false;
});

// Brings up RESET Modal Box:
$('button.char#singleqb-datareset').on('click', function () {
    $('.modal.data-reset.singleqb').toggleClass('is-visible');
});
$('input.char.singleqb.data-reset#singleqb-reset').on('click', function () {
    $('div.char.singleqb.confirm').show();
    $('button.char.singleqb.reset-yes').on('click', function () {
        $.getJSON(mssnencrpytonian() + '/mssn/char/singleqb/resetdata', {
            ownerpassword: $('input.char.singleqb#ownerpassword').val(),
            truncateafter: $('input.char.singleqb#truncateafter').val(),
        }, function (data) {
            $('div#char-singleqb-announcement').empty().append($('<h4 style="color: red;"></h4>').text(data.message + '. Please refresh by clicking SQE-PULSE.'));
        });
        $('div.char.singleqb.confirm').hide();
        return false;
    });
    return false;
});
$('button.char.singleqb.reset-no').on('click', function () {
    $('div.char.singleqb.confirm').hide();
    return false;
});


