// Single-QB: 
$(document).ready(function(){
    $('div.mani.singleqb.confirm').hide();
    $('button.mani#singleqb-savecsv').hide();
    $('button.mani#singleqb-savemat').hide();
    $("a.new#singleqb-msg").text('Measurement Status');
    window.singleqbcomment = "";
    // $('input.singleqb.notification').hide();
    $('input.singleqb.setchannels.pulse-width').parent().hide();
    $('input.singleqb.setchannels.' + $('select.singleqb.setchannels.finite-variable.pulse-width').val() + '.pulse-width').parent().show();
    $('input.singleqb.setchannels.pulse-height').parent().hide();
    $('input.singleqb.setchannels.' + $('select.singleqb.setchannels.finite-variable.pulse-height').val() + '.pulse-height').parent().show();
    $('input.singleqb.setchannels.check').hide();
    $('select.mani.scheme.singleqb#SCHEME_LIST').hide();
    $('input.singleqb.perimeter-settings.save').hide();
});

// Global variables:
window.selecteday = ''
window.VdBm_selector = 'select.mani.data.singleqb#singleqb-1d-VdBm'
window.VdBm_selector2 = 'select.mani.data.singleqb#singleqb-2d-VdBm'

// Parameter, Perimeter & Channel LIST for INITIATING NEW RUN:
var singleqb_Parameters = ['Flux-Bias', 'XY-LO-Frequency', 'RO-LO-Frequency'];
var singleqb_Perimeters = ['DIGIHOME', 'IF_ALIGN_KHZ', 'BIASMODE', 'XY-LO-Power', 'RO-LO-Power', 'TRIGGER_DELAY_NS', 'RECORD-SUM', 'RECORD_TIME_NS', 'READOUTYPE', 'R-JSON']; // SCORE-JSON requires special treatment
var singleqb_Channels = ['RO-I', 'RO-Q', 'XY-I', 'XY-Q'];

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

function listimes_singleqb() {
    $('input.mani.data').removeClass("plotted");
    
    if (Number(wday) < 0) {
        // brings up parameter-input panel for new measurement:
        $('.modal.new.singleqb').toggleClass('is-visible');
        // disable RUN BUTTON before validation via CHECK:
        $('input.mani#singleqb-run').hide(); // RUN
        // Update T6 Informations:
        $.getJSON('/mach/all/mxc', {}, function (data) {
            window.mxcmk = data.mxcmk;
            $("textarea.mani.singleqb#singleqb-ecomment").val(singleqbcomment + "\nUpdate: T6=" + mxcmk + "mK");
        });

    } else if (wday == 'm') {
        // brings up manage panel:
        $('.modal.manage.singleqb').toggleClass('is-visible');
    } else {
        selecteday = wday
        $.getJSON(mssnencrpytonian() + '/mssn/mani/singleqb/time', {
            wday: wday
        }, function (data) {
            $('select.mani.singleqb.wmoment').empty().append($('<option>', { text: 'pick', value: '' }));
            $.each(data.taskentries, function(i,v){ $('select.mani.singleqb.wmoment').append($('<option>', { id: i, text: v, value: v })); });
        }); 
    };
};
function accessdata_singleqb() {
    $('.bar.data-progress.singleqb').css({"width": 0}).text('accessing...');
    $.getJSON(mssnencrpytonian() + '/mssn/mani/singleqb/access', {
        wmoment: wmoment
    }, function (data) {
        // 0. Collecting data from route:
        var R_COUNT = parseInt(Object.keys(JSON.parse(data.perimeter['R-JSON'])).length);
        console.log("R-JSON-length: " + R_COUNT);
        window.SQ_CParameters = data.SQ_CParameters;

        // 1. Creating parameter-range selectors:
        $('table.mani-singleqb-extra').remove();
        $.each(SQ_CParameters, function(i,cparam){
            var colperow = 8; // row density
            var row = parseInt(i/colperow);
            if (i%colperow==0 || i==0) {
                $('div.row.parameter').append('<table class="content-table mani-singleqb-extra E' + row + '"></table>');
                $('table.mani-singleqb-extra.E' + row).append($('<thead></thead>').append($('<tr></tr>')));
                $('table.mani-singleqb-extra.E' + row).append($('<tbody class="mani-singleqb parameter"></tbody>').append($('<tr></tr>')));
            };
            // console.log('cparam: ' + cparam + '\ndata: ' + data.pdata[cparam]);
            $('table.mani-singleqb-extra.E' + row + ' thead tr').append('<th class="mani singleqb ' + String(cparam) + '">' + cparam + '</th>');
            $('table.mani-singleqb-extra.E' + row + ' tbody tr').append('<th><select class="mani singleqb" id="' + cparam + '" type="text"></select></th>');
        });

        // 2. Loading data into parameter-range selectors:
        $.each(SQ_CParameters, function(i,cparam){
            // console.log('cparam: ' + cparam + '\ndata: ' + data.pdata[cparam]);
            // 2.1 Loading Sweeping Options:
            $('select.mani.singleqb#' + cparam).empty();
            if ( data.pdata[cparam].length > 1) {
                $('select.mani.singleqb#' + cparam).append($('<option>', { text: 'X-ALL', value: 'x' })).append($('<option>', { text: 'X-COUNT', value: 'xc' }))
                    .append($('<option>', { text: 'SAMPLE', value: 's' })).append($('<option>', { text: 'Y-ALL', value: 'y' }));
            };
            // 2.2 Loading Constant Values:
            var max_selection = 1001; // to speed up loading process, entries per request is limited.
            if (data.pdata[cparam].length > max_selection) {
                $.each(data.pdata[cparam].slice(0,max_selection), function(i,v){ $('select.mani.singleqb#' + cparam).append($('<option>', { text: v, value: i })); });
                $('select.mani.singleqb#' + cparam).append($('<option>', { text: 'more...', value: 'm' }));
                // Pending:  Use "more" to select/enter value manually!
            } else {
                $.each(data.pdata[cparam], function(i,v){ $('select.mani.singleqb#' + cparam).append($('<option>', { text: v, value: i })); });
            };

            // 2.3 Loading parameter-range into inputs for NEW RUN:
            $('input.mani.singleqb#' + cparam).val(data.corder[cparam]);
        });

        // 3. load edittable comment for NEW RUN:
        singleqbcomment = data.comment;
        // 4. load narrated comment:
        $('textarea.mani.singleqb.comment').text(data.comment);
        
        // 5. Loading data progress:
        var data_progress = "  " + String(data.data_progress.toFixed(3)) + "%";
        $('.bar.data-progress.singleqb').css({"width": data_progress}).text(data_progress);
        $('.data-eta.singleqb').text("Job-" + data.JOBID + ": " + data.measureacheta + " until completion");
        console.log("Progress: " + data_progress);

        // 6. Loading Perimeters for NEW RUN:
        $.each(singleqb_Perimeters, function(i,perimeter) { $('.mani.config.singleqb#' + perimeter).val(data.perimeter[perimeter]); });
        $.each(Array(4), function(i,v){ $('textarea.mani.singleqb.SCORE-JSON.channel-' + String(i+1)).val(data.perimeter['SCORE-JSON']["CH" + String(i+1)]); });
        $('select.mani.scheme.singleqb#SCHEME_LIST').show();
        $('input.singleqb.perimeter-settings.save').show();

        // 7. PERIMETER Statement:
        var sheet = '';
        $.each(Object.values(data.perimeter['SCORE-JSON']), function(i,val){
            sheet += "CH" + String(i+1) + " > " + singleqb_Channels[i] + ":\n" + val.replaceAll("\n"," ") + "\n\n";
        });
        $.each(Object.keys(data.perimeter), function(i,key){
            if (key!='SCORE-JSON' && key!='R-JSON'){
                sheet += key + ": " + Object.values(data.perimeter)[i] + "\n\n";
            }; 
        });
        $('textarea.mani.singleqb.PSTATEMENT').val(sheet).show();

        // 8. Adjustment(s) based on perimeter:
        if (data.perimeter['BIASMODE']==1) { $('table th.mani.singleqb.Flux-Bias').text('Flux-Bias (A)') }
        else { $('table th.mani.singleqb.Flux-Bias').text('Flux-Bias (V)') };

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
    Plotly.newPlot('mani-singleqb-chart', Trace, layout, {showSendToCloud: true});
    $( "i.singleqb1d" ).remove(); //clear previous
};
function compare1D_singleqb(x1,y1,x2,y2,normalize=false,direction='dip',VdBm_selector) {
    // V or dBm
    y1 = VdBm_Conversion(y1, VdBm_selector)['y']; 
    y2 = VdBm_Conversion(y2, VdBm_selector); 
    yunit = y2['yunit'];
    y2 = y2['y'];

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
        yaxis: { zeroline: false, title: '<b>Signal(' + yunit + ')</b>', titlefont: {size: 18}, tickfont: {size: 18}, tickwidth: 3, linewidth: 3 },
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
    Plotly.newPlot('mani-singleqb-chart', Trace, layout, {showSendToCloud: true});
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
    Plotly.newPlot('mani-' + mission + '-chart', Trace, layout, {showSendToCloud: true});
};
function compareIQ_singleqb(x1,y1,x2,y2,mission="singleqb") {
    // selecting points:
    x1 = x1.slice(parseInt($('input.mani.data.singleqb#singleqb-shot-range').val().split(',')[0]), parseInt($('input.mani.data.singleqb#singleqb-shot-range').val().split(',')[1]));
    y1 = y1.slice(parseInt($('input.mani.data.singleqb#singleqb-shot-range').val().split(',')[0]), parseInt($('input.mani.data.singleqb#singleqb-shot-range').val().split(',')[1]));
    x2 = x2.slice(parseInt($('input.mani.data.singleqb#singleqb-shot-range').val().split(',')[0]), parseInt($('input.mani.data.singleqb#singleqb-shot-range').val().split(',')[1]));
    y2 = y2.slice(parseInt($('input.mani.data.singleqb#singleqb-shot-range').val().split(',')[0]), parseInt($('input.mani.data.singleqb#singleqb-shot-range').val().split(',')[1]));
    // MAX RANGE:
    var maxscal = Math.max(Math.max(...x1.map(Math.abs)), Math.max(...y1.map(Math.abs)));
    maxscal = maxscal * 1.2;
    // console.log("Limit: " + maxscal);
    
    let traceIQ_1 = {x: [], y: [], mode: 'markers', type: 'scattergl',
        name: 'IQ-1',
        // line: {color: 'blue', width: 2.5},
        marker: {symbol: 'circle', size: 1.37, color: 'blue'},
        yaxis: 'y' };
    let traceIQ_2 = {x: [], y: [], mode: 'markers', type: 'scattergl',
        name: 'IQ-2',
        // line: {color: 'blue', width: 2.5},
        marker: {symbol: 'circle', size: 1.37, color: 'red'},
        yaxis: 'y' };

    let layout = {
        legend: {x: 1.08},
        height: $(window).height()*0.6,
        width: $(window).width()*0.6,
        xaxis: {
            range: [-maxscal, maxscal],
            zeroline: true,
            title: "I",
            titlefont: {size: 18},
            tickfont: {size: 18},
            tickwidth: 3,
            zerolinewidth: 3.5,
            gridcolor: 'rgb(159, 197, 232)',
            zerolinecolor: 'grey',
        },
        yaxis: {
            range: [-maxscal, maxscal],
            zeroline: true,
            title: "Q",
            titlefont: {size: 18},
            tickfont: {size: 18},
            tickwidth: 3,
            zerolinewidth: 3.5,
            gridcolor: 'rgb(159, 197, 232)',
            zerolinecolor: 'grey',
        },
        title: 'IQ-cluster between |0> and |1>',
        annotations: [{
            xref: 'paper',
            yref: 'paper',
            x: 0.03,
            xanchor: 'right',
            y: 1.05,
            yanchor: 'bottom',
            text: '',
            font: {size: 18},
            showarrow: false,
            textangle: 0
          }]
        };
    
    $.each(x1, function(i, val) {traceIQ_1.x.push(val);});
    $.each(y1, function(i, val) {traceIQ_1.y.push(val);});
    $.each(x2, function(i, val) {traceIQ_2.x.push(val);});
    $.each(y2, function(i, val) {traceIQ_2.y.push(val);});

    var Trace = [traceIQ_1, traceIQ_2];
    Plotly.react('mani-' + mission + '-chart', Trace, layout);

};

// hiding parameter settings when click outside the modal box:
$('.modal-toggle.new.singleqb').on('click', function(e) {
    e.preventDefault();
    $('.modal.new.singleqb').toggleClass('is-visible');
    // revert back to previous option upon leaving dialogue box
    $('select.mani.singleqb.wday').val(selecteday);
});
$('.modal-toggle.manage.singleqb').on('click', function(e) {
    e.preventDefault();
    $('.modal.manage.singleqb').toggleClass('is-visible');
    // revert back to previous option upon leaving dialogue box
    $('select.mani.singleqb.wday').val(selecteday);
});
$('.modal-toggle.data-reset.singleqb').on('click', function(e) {
    e.preventDefault();
    $('.modal.data-reset.singleqb').toggleClass('is-visible');
});

// Perimeter setup:
// Switch between finite and variable
$('select.singleqb.setchannels.finite-variable').on('change', function() {
    $('input.singleqb.setchannels.pulse-width').parent().hide();
    $('input.singleqb.setchannels.' + $('select.singleqb.setchannels.finite-variable.pulse-width').val() + '.pulse-width').parent().show();
    $('input.singleqb.setchannels.pulse-height').parent().hide();
    $('input.singleqb.setchannels.' + $('select.singleqb.setchannels.finite-variable.pulse-height').val() + '.pulse-height').parent().show();
});
// Initiate ALL Scores with Pulse-period:
$("input.singleqb.set-period").bind('click', function () {
    var pperiod = $('input.singleqb.setchannels.pulse-period').val();
    $.each(Array(4), function(i,v){ $('textarea.mani.singleqb.SCORE-JSON.channel-' + String(i+1)).val("NS=" + pperiod + ";\n"); });
    $('textarea.mani.singleqb#R-JSON').val(JSON.stringify({}));
    $('div.singleqb.settingstatus').empty().append($('<h4 style="color: blue;"></h4>').text("ALL SCORES INITIATED WITH LENGTH " + pperiod + "ns"));
    return false;
});
// Inserting shapes into respective score sheet:
$('input.singleqb.setchannels.insert').bind('click', function () {
    var channel = $('select.singleqb.setchannels.score-channel').val();
    var lascore = $('textarea.mani.singleqb.SCORE-JSON.channel-' + channel).val();
    var shape = $('select.singleqb.setchannels.pulse-shape').val();
    var RJSON = JSON.parse($('textarea.mani.singleqb#R-JSON').val());

    // Pulse Width:
    if ($('select.singleqb.setchannels.finite-variable.pulse-width').val()=='finite') {
        var pwidth = $('input.singleqb.setchannels.finite.pulse-width').val();
    } else {
        var porder = $('input.singleqb.setchannels.variable.pulse-width').val().replaceAll(' ','').split('=');
        var pwidth = "{" + porder[0] + "}";
        RJSON[porder[0]] = porder[1];
        $('textarea.mani.singleqb#R-JSON').val(JSON.stringify(RJSON));
    };
    // Pulse Height:
    if ($('select.singleqb.setchannels.finite-variable.pulse-height').val()=='finite') {
        var pheight = $('input.singleqb.setchannels.finite.pulse-height').val();
    } else {
        var porder = $('input.singleqb.setchannels.variable.pulse-height').val().replaceAll(' ','').split('=');
        var pheight = "{" + porder[0] + "}";
        RJSON[porder[0]] = porder[1];
        $('textarea.mani.singleqb#R-JSON').val(JSON.stringify(RJSON));
    };

    $('textarea.mani.singleqb.SCORE-JSON.channel-' + channel).val(lascore + shape + '/,' + pwidth + ',' + pheight + ';\n');
    $('div.singleqb.settingstatus').empty().append($('<h4 style="color: blue;"></h4>').text("EXTENDING SCORE-" + channel + " WITH " + shape + " (" + pwidth + ", " + pheight + ")"));
    return false;
});
// Take a step back in Score:
$('input.singleqb.setchannels.back').bind('click', function() {
    var channel = $('select.singleqb.setchannels.score-channel').val();
    var lascore = $('textarea.mani.singleqb.SCORE-JSON.channel-' + channel).val();
    if (lascore.split(';').length > 2) {
        $('textarea.mani.singleqb.SCORE-JSON.channel-' + channel).val(lascore.split(';').slice(0,-2).join(";") + ';\n');
    };
    return false;
});
// Check before RUN (PENDING: CHECK IFFREQ CONSISTENCY BETWEEN SCORE & rotation_compensate_MHz):
// 0. Reset validity when values changed:
$('.mani.config.singleqb').on('change', function() {
    $('input.singleqb.setchannels.check').hide();
    $('input.mani#singleqb-run').hide();
    $('div.singleqb.settingstatus').empty().append($('<h4 style="color: red;"></h4>').text("!!! VALUES CHANGED !!!"));
});
// 1. Check ALZDG TIMSUM:
$('input.singleqb.alzdg-timsum.check').bind('click', function() {
    $('div.singleqb.settingstatus').empty().append($('<h4 style="color: red;"></h4>').text(">> VALIDATING TIMSUM >>"));
    $.getJSON(mssnencrpytonian() + '/mssn/mani/singleqb/check/timsum', {
        record_time_ns: $('.mani.config.singleqb#RECORD_TIME_NS').val(),
        record_sum: $('.mani.config.singleqb#RECORD-SUM').val(),
    }, function (data) {
        $('.mani.config.singleqb#RECORD_TIME_NS').val(data.record_time_ns);
        $('.mani.config.singleqb#RECORD-SUM').val(data.record_sum);
    })
    .done(function(data) {
        $('input.singleqb.setchannels.check').show();
        $('div.singleqb.settingstatus').empty().append($('<h4 style="color: blue;"></h4>').text("RECORD TIMSUM VALIDATED. PROCEED TO CHECK R-JSON"));
    })
    .fail(function(jqxhr, textStatus, error){
        $('div.singleqb.settingstatus').empty().append($('<h4 style="color: red;"></h4>').text("Please Check ALZDG Status"));
    });
    return false;
});
// 2. Check consistency between R-JSON & Score
$('input.singleqb.setchannels.check').bind('click', function() {
    var RJSON = JSON.parse($('textarea.mani.singleqb#R-JSON').val());
    var allscores = '';
    var allfilled = 1;

    // accumulate all the scores
    $.each(Array(4), function(i,v){
        allscores += $('textarea.mani.singleqb.SCORE-JSON.channel-' + String(i+1)).val();
        allfilled *= $('textarea.mani.singleqb.SCORE-JSON.channel-' + String(i+1)).val().replaceAll(" ","").replaceAll("\n","").length;
    });
    allscores = allscores.replaceAll(" ","");
    console.log("allscores's length: " + allscores.length);

    // take out all {R-JSON's keys}
    $.each(Object.keys(RJSON), function(i,v) {
        allscores = allscores.replaceAll("{"+v+"}","");
    });

    // VALIDATE RUN based on total absence of unsolicited {stranger}
    if (allscores.includes("{") || allscores.includes("}") || allfilled==0) {
        $('input.mani#singleqb-run').hide(); // RUN
    } else {
        $('input.mani#singleqb-run').show(); // RUN
    };

    return false;
});
// 3a. Save the past perimeter settings:
$('input.singleqb.perimeter-settings.save').on('touchend click', function(event) {
    eventHandler(event, $(this)); // Prevent phantom clicks from touch-click.
    $.getJSON(mssnencrpytonian() + '/mssn/mani/singleqb/perisettings/save', {
        scheme_name: $('select.mani.scheme.singleqb#SCHEME_LIST').val(),
    }, function (data) {
        console.log(data.scheme_name + " has been saved.");
        $('div#mani-singleqb-announcement').empty().append($('<h4 style="color: red;"></h4>').text("Perimeter history has been saved in " + data.scheme_name));
    });
    return false;
});
// 3b. Load the past perimeter settings:
$('input.singleqb.perimeter-settings.load').on('touchend click', function(event) {
    eventHandler(event, $(this)); // Prevent phantom clicks from touch-click.
    var scheme_name = $('select.mani.config.singleqb#SCHEME_LIST').val();
    $.getJSON(mssnencrpytonian() + '/mssn/mani/singleqb/perisettings/load', {
        scheme_name: scheme_name,
    }, function (data) {
        $('div.singleqb.settingstatus').empty().append($('<h4 style="color: red;"></h4>').text(scheme_name + " " + data.status));
        console.log(scheme_name + " " + data.status);
        // """6. Loading Perimeters for NEW RUN:"""
        $.each(singleqb_Perimeters, function(i,perimeter) { $('.mani.config.singleqb#' + perimeter).val(data.perimeter[perimeter]); });
        $.each(Array(4), function(i,v){ $('textarea.mani.singleqb.SCORE-JSON.channel-' + String(i+1)).val(data.perimeter['SCORE-JSON']["CH" + String(i+1)]); });
        // Pre-scribe comment / reference accordingly:
        $("textarea.mani.singleqb#singleqb-ecomment").val("Cavity/Qubit-?: CHECK/SCOUT/FIND/GET WHAT?" + "\n[RO -??dB EXT, IQ-CAL: XY(0) + RO(0), SPAN: ??, RES: ??, ...]"  + "\n" + scheme_name + " from " + data.perimeter["jobid"] + "\nT6=" + mxcmk + "mK");
        $('div.singleqb.settingstatus').empty().append($('<h4 style="color: blue;"></h4>').text(scheme_name + " " + data.status + data.perimeter["jobid"]));
    });
    return false;
});
    

// show Single-QB's daylist
$(function() {
    $('button.mani#singleqb').bind('click', function() {
        $('div.singleqb.queue-system').empty().append($('<h4 style="color: blue;"></h4>').text(qsystem));
        $('div.manicontent').hide();
        $('div.manicontent#singleqb').show();
        $('button.mani').removeClass('selected');
        $('button.mani#singleqb').addClass('selected');
        $.getJSON(mssnencrpytonian() + '/mssn/mani/singleqb/init', {
        }, function (data) {
            // Check Run Permission: (PENDING: Use Global run_permission to notify user whenever certain disabled button is click)
            window.run_permission = data.run_permission;
            window.DAYLIST = data.daylist;
            console.log("run permission: " + run_permission);
            if (run_permission == false) {
                $('button.mani.singleqb.run').hide();
                console.log("RESUME BUTTON DISABLED");
            } else {
                $('button.mani.singleqb.run').show(); // RESUME
                console.log("RESUME BUTTON ENABLED");
            };
            
            $('select.mani.singleqb.wday').empty();
            $('select.mani.singleqb.wday').append($('<option>', { text: 'The latest:', value: '' }));
            $.each(data.daylist.reverse(), function(i,v){
                $('select.mani.singleqb.wday').append($('<option>', {
                    text: v,
                    value: data.daylist.length - 1 - i
                }));
            });
            $('select.mani.singleqb.wday').append($('<option>', { text: '--Manage--', value: 'm' }));

            if (run_permission == true) {
                $('select.mani.singleqb.wday').append($('<option>', { text: '--New--', value: -1 }));
            };
            
        });
        return false;
    });
});

// list times based on day picked
$(function () {
    $('select.mani.singleqb.wday').on('change', function () {
        // make global wday
        window.wday = $('select.mani.singleqb.wday').val();
        listimes_singleqb();
    });
    return false;
});

// click to RUN:
$('input.mani#singleqb-run').on('touchend click', function(event) {
    eventHandler(event, $(this)); // Prevent phantom clicks from touch-click.
    setTimeout(() => { $('button.tablinks#ALL-tab').trigger('click'); }, 160);
    // Assemble PERIMETER:
    var PERIMETER = {};
    $.each(singleqb_Perimeters, function(i,perimeter) {
        PERIMETER[perimeter] = $('.mani.config.singleqb#' + perimeter).val();
        console.log("PERIMETER[" + perimeter + "]: " + PERIMETER[perimeter]);
    });
    // Assemble SCORE-JSON for PERIMETER:
    PERIMETER['SCORE-JSON'] = {}
    $.each(Array(4), function(i,v){ PERIMETER['SCORE-JSON']["CH" + String(i+1)] = $('textarea.mani.singleqb.SCORE-JSON.channel-' + String(i+1)).val(); });
    console.log("PERIMETER: " + PERIMETER)

    // Assemble CORDER:
    var CORDER = {};
    CORDER['C-Structure'] = singleqb_Parameters;
    $.each(singleqb_Parameters, function(i,cparam){ CORDER[cparam] = $('input.mani.singleqb#' + cparam).val(); });
    console.log("C-Structure: " + CORDER['C-Structure']);

    var comment = JSON.stringify($('textarea.mani.singleqb#singleqb-ecomment').val());
    
    // START RUNNING
    $.getJSON(mssnencrpytonian() + '/mssn/mani/singleqb/new', {
        wday: wday, PERIMETER: JSON.stringify(PERIMETER), CORDER: JSON.stringify(CORDER), comment: comment
    }, function (data) {       
        console.log("Status: " + data.status);
    });
    return false;
});

// Click to resume measurement (PENDING: Error(s) to be fixed)
$(function () {
    $('button.mani#singleqb-resume').on('click', function () {
        setTimeout(() => { $('button.tablinks#ALL-tab').trigger('click'); }, 160);
        $.getJSON(mssnencrpytonian() + '/mssn/mani/singleqb/resume', {
            wday: selecteday, wmoment: wmoment
        }, function (data) {
            if (data.resumepoint == data.datasize) {
                console.log("The data was already complete!");
            } else { console.log("The data has just been updated")};
        });
        return false;
    });
});

// access data based on time picked
$(function () {
    $('select.mani.singleqb.wmoment').on('change', function () {
        // Make global variable:
        window.wmoment = $('select.mani.singleqb.wmoment').val();
        accessdata_singleqb();
    });
    return false;
});

// tracking data position based on certain parameter
$(function () {
    $(document).on('change', 'table tbody tr th select.mani.singleqb', function () {
        var fixed = this.getAttribute('id');
        var fixedvalue = $('table tbody tr th select.mani.singleqb#' + fixed).val();
        $.getJSON(mssnencrpytonian() + '/mssn/mani/singleqb/trackdata', {
            fixed: fixed, fixedvalue: fixedvalue,
        }, function (data) {
            console.log('data position for branch ' + fixed + ' is ' + data.data_location);
            $('div#mani-singleqb-announcement').empty().append($('<h4 style="color: red;"></h4>').text(fixed + ' is fixed at ' + data.data_location))
            .append($('<h4 style="color: blue;"></h4>').text('a location after ' + data.data_location + ' data-point(s)'));
        })
    });
    return false;
});

// assemble 1D-data based on c-parameters picked
$(function () {
    $('input.mani.data.singleqb#singleqb-1d-data').on('click', function () {
        console.log("HIIIIII");
        $('div#mani-singleqb-announcement').empty();
        $( "i.singleqb1d" ).remove(); //clear previous
        $('button.mani#singleqb').prepend("<i class='singleqb1d fa fa-palette fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        // var irepeat = $('select.mani.singleqb#repeat').val();
        var cselect = {};
        $.each(SQ_CParameters, function(i,cparam){ cselect[cparam] = $('select.mani.singleqb#' + cparam).val(); });
        console.log("Picked Flux: " + cselect['Flux-Bias']);
        var srange = $('input.mani.data.singleqb#singleqb-sample-range').val();
        var smode = $('select.mani.data.singleqb#singleqb-sample-mode').val();
        $.getJSON(mssnencrpytonian() + '/mssn/mani/singleqb/1ddata', {
            cselect: JSON.stringify(cselect), srange: srange, smode: smode,
        }, function (data) {
            window.x = data.x;
            window.y = new Object();
            window.y.I = data.yI;
            window.y.Q = data.yQ;
            window.y.A = data.yA;
            window.y.P = data.yUFNP;
            window.xtitle = data.xtitle;
            // Phase option
            // $('select.mani.data.singleqb#1d-phase').empty().append($('<option>', { text: 'Pha', value: 'Pha' })).append($('<option>', { text: 'UPha', value: 'UPha' }));
            plot1D_singleqb(x,y.I,y.Q,y.A,y.P,VdBm_selector,xtitle);
            // console.log("yA: " + yA);
        })
            .done(function(data) {
                $('button.mani#singleqb-savecsv').show(); // to avoid downloading the wrong file
                $('div#mani-singleqb-announcement').append($('<h4 style="color: red;"></h4>').text("Successfully Plot 1D:"));
            })
            .fail(function(jqxhr, textStatus, error){
                $('div#mani-singleqb-announcement').append($('<h4 style="color: red;"></h4>').text("Oops: " + error));
                $( "i.singleqb1d" ).remove(); //clear the status
            });
    });
    return false;
});
// INSERT 1D-data for comparison
$(function () {
    $('button.mani#singleqb-insert-1D').on('click', function () {
        $('div#mani-singleqb-announcement').empty();
        $( "i.singleqb1d" ).remove(); //clear previous
        $('button.mani#singleqb').prepend("<i class='singleqb1d fa fa-palette fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        // var irepeat = $('select.mani.singleqb#repeat').val();
        var cselect = {};
        $.each(SQ_CParameters, function(i,cparam){ cselect[cparam] = $('select.mani.singleqb#' + cparam).val(); });
        console.log("Picked Flux: " + cselect['Flux-Bias']);
        var srange = $('input.mani.data.singleqb#singleqb-sample-range').val();
        var smode = $('select.mani.data.singleqb#singleqb-sample-mode').val();
        $.getJSON(mssnencrpytonian() + '/mssn/mani/singleqb/1ddata', {
            cselect: JSON.stringify(cselect), srange: srange, smode: smode,
        }, function (data) {
            window.xC = data.x;
            window.yC = new Object();
            window.yC.I = data.yI;
            window.yC.Q = data.yQ;
            window.yC.A = data.yA;
            window.yC.P = data.yUFNP;
            window.xtitle2 = data.xtitle;

            // Normalization Options:
            $('select.mani.data.singleqb#singleqb-compare-nml').empty().append($('<option>', { text: 'direct', value: 'direct' }))
                                                                .append($('<option>', { text: 'normaldip', value: 'normaldip' }))
                                                                .append($('<option>', { text: 'normalpeak', value: 'normalpeak' }));
            console.log('selected: ' + $('select.mani.data.singleqb#singleqb-compare-nml').val());
            normalize = Boolean($('select.mani.data.singleqb#singleqb-compare-nml').val()!='direct');
            direction = $('select.mani.data.singleqb#singleqb-compare-nml').val().split('normal')[1];

            // IQAP Options:
            $('select.mani.data.singleqb#singleqb-compare-iqap').empty().append($('<option>', { text: 'Amplitude', value: 'A' }))
                                                                .append($('<option>', { text: 'In-plane', value: 'I' }))
                                                                .append($('<option>', { text: 'Quadrature', value: 'Q' }))
                                                                .append($('<option>', { text: 'Phase', value: 'P' }))
                                                                .append($('<option>', { text: 'IQ-Plot', value: 'IQ' }));
            
            compare1D_singleqb(x,y[$('select.mani.data.singleqb#singleqb-compare-iqap').val()],xC,yC[$('select.mani.data.singleqb#singleqb-compare-iqap').val()],normalize,direction,VdBm_selector);
        })
            .fail(function(jqxhr, textStatus, error){
                $('div#mani-singleqb-announcement').append($('<h4 style="color: red;"></h4>').text("Oops: " + error));
                $( "i.singleqb1d" ).remove(); //clear the status
            });
    });
    return false;
});
$('.mani.data.singleqb.compare').on('change', function() {
    normalize = Boolean($('select.mani.data.singleqb#singleqb-compare-nml').val()!='direct');
    direction = $('select.mani.data.singleqb#singleqb-compare-nml').val().split('normal')[1];
    if ($('select.mani.data.singleqb#singleqb-compare-iqap').val()=="IQ") {
        compareIQ_singleqb(y["I"],y["Q"],yC["I"],yC["Q"]);
    } else {
        compare1D_singleqb(x,y[$('select.mani.data.singleqb#singleqb-compare-iqap').val()],xC,yC[$('select.mani.data.singleqb#singleqb-compare-iqap').val()],normalize,direction,VdBm_selector);
    };
    return false;
});
$(VdBm_selector).on('change', function() {
    console.log("Selector: " + VdBm_selector)
    plot1D_singleqb(x,y.I,y.Q,y.A,y.P,VdBm_selector,xtitle);
});
$('select.mani.data.singleqb#singleqb-1d-mode').on('change', function() {
    plot1D_singleqb(x,y.I,y.Q,y.A,y.P,VdBm_selector,xtitle,mode=$('select.mani.data.singleqb#singleqb-1d-mode').val());
});

// assemble 2D-data based on c-parameters picked
$(function () {
    $('input.mani.singleqb#singleqb-2d-data').on('click', function () {
        $('div#mani-singleqb-announcement').empty().append($('<h4 style="color: red;"></h4>').text("Plotting 2D might takes some time. Please wait... "));
        $( "i.singleqb2d" ).remove(); //clear previous
        $('button.mani#singleqb').prepend("<i class='singleqb2d fa fa-palette fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        // var irepeat = $('select.mani.singleqb#repeat').val();
        var cselect = {};
        $.each(SQ_CParameters, function(i,cparam){ cselect[cparam] = $('select.mani.singleqb#' + cparam).val(); });
        console.log("Picked Flux: " + cselect['Flux-Bias']);
        var srange = $('input.mani.data.singleqb#singleqb-sample-range').val();
        var smode = $('select.mani.data.singleqb#singleqb-sample-mode').val();
        $.getJSON(mssnencrpytonian() + '/mssn/mani/singleqb/2ddata', {
            cselect: JSON.stringify(cselect), srange: srange, smode: smode
        }, function (data) {
            window.X = data.x;
            window.Y = data.y;
            console.log("check Y: " + Y);
            window.ZZA = data.ZZA;
            window.ZZUP = data.ZZUP;
            window.ZZI = data.ZZI;
            window.ZZQ = data.ZZQ;
            window.xtitle = data.xtitle;
            window.ytitle = data.ytitle;
            // Amplitude (default) or Phase
            $('select.mani.data.singleqb#singleqb-2d-iqamphase').empty().append($('<option>', { text: 'Amp', value: 'Amp' })).append($('<option>', { text: 'Pha', value: 'Pha' }))
                                                                .append($('<option>', { text: 'I', value: 'I' })).append($('<option>', { text: 'Q', value: 'Q' }));
            // Data grooming
            $('select.mani.data.singleqb#singleqb-2d-type').empty().append($('<option>', { text: 'direct', value: 'direct' }))
                .append($('<option>', { text: 'normalYdip', value: 'normalYdip' })).append($('<option>', { text: 'normalYpeak', value: 'normalYpeak' }))
                .append($('<option>', { text: 'normalXdip', value: 'normalXdip' })).append($('<option>', { text: 'normalXpeak', value: 'normalXpeak' }));
            // Data color-scaling
            $('select.mani.data.singleqb#singleqb-2d-colorscale').empty().append($('<option>', { text: 'YlOrRd', value: 'YlOrRd' }))
                .append($('<option>', { text: 'YlGnBu', value: 'YlGnBu' })).append($('<option>', { text: 'RdBu', value: 'RdBu' }))
                .append($('<option>', { text: 'Portland', value: 'Portland' })).append($('<option>', { text: 'Picnic', value: 'Picnic' }))
                .append($('<option>', { text: 'Jet', value: 'Jet' })).append($('<option>', { text: 'Hot', value: 'Hot' }))
                .append($('<option>', { text: 'Greys', value: 'Greys' })).append($('<option>', { text: 'Greens', value: 'Greens' }))
                .append($('<option>', { text: 'Electric', value: 'Electric' })).append($('<option>', { text: 'Earth', value: 'Earth' }))
                .append($('<option>', { text: 'Bluered', value: 'Bluered' })).append($('<option>', { text: 'Blackbody', value: 'Blackbody' }))
                .append($('<option>', { text: 'Blues', value: 'Blues' })).append($('<option>', { text: 'Viridis', value: 'Viridis' }));
            // Transpose or not
            $('select.mani.data.singleqb#singleqb-2d-direction').empty().append($('<option>', { text: 'stay', value: 'stay' })).append($('<option>', { text: 'rotate', value: 'rotate' }));
            plot2D_singleqb(X, Y, ZZA, xtitle, ytitle, 
                $('select.mani.data.singleqb#singleqb-2d-type').val(),'singleqb',
                $('select.mani.data.singleqb#singleqb-2d-colorscale').val(),
                VdBm_selector2);
            $( "i.singleqb2d" ).remove(); //clear previous
        })
            .fail(function(jqxhr, textStatus, error){
                $('div#mani-singleqb-announcement').append($('<h4 style="color: red;"></h4>').text("Oops: " + error + "(" + textStatus + ")"));
                $( "i.singleqb2d" ).remove(); //clear the status
            })
            .always(function(){
                $('button.mani#singleqb-savemat').show();
                $('div#mani-singleqb-announcement').empty().append($('<h4 style="color: red;"></h4>').text("2D Plot Completed"));
                $( "i.singleqb2d" ).remove(); //clear the status
            });
    });
    return false;
});
$('div.2D select.mani.data.singleqb').on('change', function() {

    if ($('select.mani.data.singleqb#singleqb-2d-iqamphase').val() == "Amp") {var ZZ = ZZA; }
    else if ($('select.mani.data.singleqb#singleqb-2d-iqamphase').val() == "Pha") {var ZZ = ZZUP; }
    else if ($('select.mani.data.singleqb#singleqb-2d-iqamphase').val() == "I") {var ZZ = ZZI; }
    else if ($('select.mani.data.singleqb#singleqb-2d-iqamphase').val() == "Q") {var ZZ = ZZQ; };
    
    if ($('select.mani.data.singleqb#singleqb-2d-direction').val() == "rotate") {
        plot2D_singleqb(Y, X, transpose(ZZ), ytitle, xtitle, 
            $('select.mani.data.singleqb#singleqb-2d-type').val(),'singleqb',
            $('select.mani.data.singleqb#singleqb-2d-colorscale').val(),
            VdBm_selector2);
    } else {
        plot2D_singleqb(X, Y, ZZ, xtitle, ytitle, 
            $('select.mani.data.singleqb#singleqb-2d-type').val(),'singleqb',
            $('select.mani.data.singleqb#singleqb-2d-colorscale').val(),
            VdBm_selector2);
    };
    return false;
});

// saving exported csv-data to client's PC:
$('button.mani#singleqb-savecsv').on('click', function() {
    console.log("SAVING CSV FILE");

    // in order to trigger href send-file request: (PENDING: FIND OUT THE WEIRD LOGIC BEHIND THIS NECCESITY)
    $.getJSON(mssnencrpytonian() + '/mssn/mani/singleqb/access', { wmoment: wmoment }, function (data) {});

    $.getJSON(mssnencrpytonian() + '/mssn/mani/singleqb/export/1dcsv', {
        // merely for security screening purposes
        ifreq: $('select.mani.singleqb#RO-LO-Frequency').val()
    }, function (data) {
        console.log("STATUS: " + data.status);
        console.log('User ' + data.user_name + ' is downloading 1D-Data');
        $.ajax({
            url: 'http://qum.phys.sinica.edu.tw:5301/mach/uploads/1Dsingleqb[' + data.user_name + '].csv',
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
                $('button.mani#singleqb-savecsv').hide();
            }
        });
    });
    return false;
});
// saving exported mat-data to client's PC:
$('button.mani#singleqb-savemat').on('click', function() {
    console.log("SAVING MAT FILE");

    // in order to trigger href send-file request: (PENDING: FIND OUT THE WEIRD LOGIC BEHIND THIS NECCESITY)
    $.getJSON(mssnencrpytonian() + '/mssn/mani/singleqb/access', { wmoment: wmoment }, function (data) {});

    $.getJSON(mssnencrpytonian() + '/mssn/mani/singleqb/export/2dmat', {
        // merely for security screening purposes
        interaction: $('select.mani.singleqb#RO-LO-Frequency').val()
    }, function (data) {
        console.log("STATUS: " + data.status);
        console.log('User ' + data.user_name + ' is downloading 2D-Data');
        $.ajax({
            url: 'http://qum.phys.sinica.edu.tw:5301/mach/uploads/2Dsingleqb[' + data.user_name + '].mat',
            method: 'GET',
            xhrFields: {
                responseType: 'blob'
            },
            success: function (data) {
                var a = document.createElement('a');
                var url = window.URL.createObjectURL(data);
                a.href = url;
                a.download = '2Dsingleqb.mat';
                document.body.append(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
                $('button.mani#singleqb-savemat').hide();
            }
        });
    });
    return false;
});

// Brings up RESET Modal Box:
$('button.mani#singleqb-datareset').on('click', function () {
    $('.modal.data-reset.singleqb').toggleClass('is-visible');
});
$('input.mani.singleqb.data-reset#singleqb-reset').on('click', function () {
    $('div.mani.singleqb.confirm').show();
    $('button.mani.singleqb.reset-yes').on('click', function () {
        $.getJSON(mssnencrpytonian() + '/mssn/mani/singleqb/resetdata', {
            ownerpassword: $('input.mani.singleqb#ownerpassword').val(),
            truncateafter: $('input.mani.singleqb#truncateafter').val(),
        }, function (data) {
            $('div#mani-singleqb-announcement').empty().append($('<h4 style="color: red;"></h4>').text(data.message + '. Please refresh by clicking SQE-PULSE.'));
        });
        $('div.mani.singleqb.confirm').hide();
        return false;
    });
    return false;
});
$('button.mani.singleqb.reset-no').on('click', function () {
    $('div.mani.singleqb.confirm').hide();
    return false;
});

// Notification on click:
$('input.singleqb.notification').click( function(){
    if ($('input.singleqb.notification').val().includes("ALL")){ $('button.tablinks#ALL-tab').trigger('click'); };
    var Day = $('input.singleqb.notification').val().split(' > ')[1];
    var Moment = $('input.singleqb.notification').val().split(' > ')[2];
    console.log('Day: ' + Day + ', Moment: ' + Moment);

    // Setting global Day & Moment index:
    wday = DAYLIST.length - 1 - DAYLIST.indexOf(Day);
    wmoment = Moment;
    console.log('wday: ' + wday + ', wmoment: ' + wmoment);

    if (Day != null) {
        // Digesting Day & Moment on the back:
        listimes_singleqb();
        accessdata_singleqb();
    };
    
    // Setting Day & Moment on the front:
    $('select.mani.singleqb.wday').val(wday);
    setTimeout(() => {
        $('select.mani.singleqb.wmoment').val(wmoment);
    }, 160); //.trigger('change'); //listing time is a bit slower than selecting option => conflict

    return false;
});

// click to search: (pending)
$('input.mani.singleqb#search').change( function() {
    $( "i.singleqb" ).remove(); //clear previous
    $('button.mani#singleqb').prepend("<i class='singleqb fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
    // waveform commands
    
    // var comment = $('textarea.mani#singleqb[name="comment"]').val();
    $.getJSON(mssnencrpytonian() + '/mssn/mani/singleqb/search', {
        
    }, function (data) {
        
        console.log("complete: " + data.filelist);
        $( "i.singleqb" ).remove(); //clear previous
    });
    return false;
});

// (PENDING: DATA ANALYSIS FUNCTIONS)