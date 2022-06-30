// CW Sweep: 
$(document).ready(function(){
    $('div.char.cwsweep.confirm').hide();
    $("a.new#cwsweep-job").text('JOBID: ');
    // get_repeat_cwsweep();
    window.cwsweepcomment = "";
    $('button.char#cwsweep-savecsv').hide();
    $('button.char#cwsweep-savemat').hide();
    $('div input.cwsweep.notification').hide();
});

// Global variables:
window.selecteday = '';

// Local variables:
var cwsweep_Perimeters = ['dcsweepch', 'z-idle', 'sg-locked',  'sweep-config', 'R-JSON']

// Pull the file from server and send it to user end:
function pull_n_send(server_URL, qumport, user_name, filename='1Dcwsweep.csv') {
    $.ajax({
        url: 'http://' + server_URL + ':' + qumport + '/mach/uploads/' + filename.split('.')[0] + '[' + user_name + '].' + filename.split('.')[1],
        method: 'GET',
        xhrFields: {
            responseType: 'blob'
        },
        success: function (data) {
            var a = document.createElement('a');
            var url = window.URL.createObjectURL(data);
            a.href = url;
            a.download = filename;
            document.body.append(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
            $('button.char#cwsweep-save' + filename.split('.')[1]).hide();
            $('div#char-cwsweep-announcement').empty().append($('<h4 style="color: red;"></h4>').text(a.download + ' has been downloaded'));
        }
    });
    return false;
};
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
function listimes_cwsweep() {
    // console.log("test_var: " + test_var);
    
    if (Number(wday) < 0) {
        // brings up parameter-input panel for new measurement:
        $('.modal.new.cwsweep').toggleClass('is-visible');
        // Update Live Informations:
        $.getJSON('/mach/all/mxc', {}, function (data) {
            $("textarea.char.cwsweep[name='ecomment']").val(cwsweepcomment.replace("\n"+cwsweepcomment.split("\n")[cwsweepcomment.split("\n").length-1], '')
                 + "\nUpdate: T6=" + data.mxcmk + "mK, REF#" + access_jobids); // directly replace the old T6
        });

    } else if (wday == 's') {
        // brings up search panel:
        $('.modal.search.cwsweep').toggleClass('is-visible');
    } else {
        selecteday = wday
        $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/time', {
            wday: wday
        }, function (data) {
            $('select.char.cwsweep[name="wmoment"]').empty().append($('<option>', { text: 'pick', value: '' }));
            $.each(data.taskentries, function(i,v){ $('select.char.cwsweep[name="wmoment"]').append($('<option>', { id: i, text: v, value: v })); });
        }); 
    };
};
function accessdata_cwsweep() {
    $('.data-progress.cwsweep').css({"width": 0}).text('accessing...');
    $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/access', {
        // input/select value here:
        wmoment: wmoment
    }, function (data) {
        // Indicate JOBID:
        window.ACCESSED_JOBID = data.JOBID;
        $("a.new#cwsweep-job").text('JOBID: ' + String(data.JOBID));
        console.log("Last accessed Job: " + tracking_access_jobids(data.JOBID));
        // load ref-jobids from comment:
        ref_jobids = data.comment.split("REF#")[1];
        showing_tracked_jobids();
        
        // checking parameters:
        console.log(data.corder);

        // LOAD each command:
        // 1. Loading Perimeters for NEW RUN:
        $.each(cwsweep_Perimeters, function(i,perimeter){ 
            if (typeof data.perimeter[perimeter] != "undefined") { $('input.char.cwsweep.perimeter#cwsweep-' + perimeter).val(data.perimeter[perimeter]); };
            console.log((i+1) + ". " + perimeter + ": " + data.perimeter[perimeter]);
        });
        $.each(DC_PATH_Matrix, function(i,channel_set) {
            $.each(channel_set, function(j,channel) {
                let QPC_Pathway = "-QPC-" + DC_Role[i][j] + "-" + String(i+1) + "-" + String(channel); 
                $('textarea.char.cwsweep.MACE-JSON.pathway-' + QPC_Pathway).val(data.perimeter['MACE-JSON']["PATH" + QPC_Pathway]); 
            });
        });
        $.each(SG_PATH_Matrix, function(i,channel_set) {
            $.each(channel_set, function(j,channel) {
                let QPC_Pathway = "-QPC-" + SG_Role[i][j] + "-" + String(i+1) + "-" + String(channel); 
                $('textarea.char.cwsweep.MACE-JSON.pathway-' + QPC_Pathway).val(data.perimeter['MACE-JSON']["PATH" + QPC_Pathway]); 
            });
        });
        

        // 2. optional parameter inputs for NEW RUN:
        if (typeof data.corder['Flux-Bias'] == "undefined") { $('input.char.cwsweep[name="fluxbias"]').val("OPT,");
        } else { $('input.char.cwsweep[name="fluxbias"]').val(data.corder['Flux-Bias']); };
        if (typeof data.corder['XY-Frequency'] == "undefined") { $('input.char.cwsweep[name="xyfreq"]').val("OPT,");
        } else { $('input.char.cwsweep[name="xyfreq"]').val(data.corder['XY-Frequency']); };
        if (typeof data.corder['XY-Power'] == "undefined") { $('input.char.cwsweep[name="xypowa"]').val("OPT,");
        } else { $('input.char.cwsweep[name="xypowa"]').val(data.corder['XY-Power']); };
        
        // 3. Basic parameter inputs for NEW RUN:
        $('input.char.cwsweep[name="sparam"]').val(data.corder['S-Parameter']);
        $('input.char.cwsweep[name="ifb"]').val(data.corder['IF-Bandwidth']);
        $('input.char.cwsweep[name="freq"]').val(data.corder['Frequency']);
        $('input.char.cwsweep[name="powa"]').val(data.corder['Power']);
        
        // 4. load edittable comment for NEW RUN:
        cwsweepcomment = data.comment;
        
        // 5. load narrated comment for ACCESS:
        $('textarea.char.cwsweep[name="comment"]').text(data.comment);
        // 6. load narrated note for ACCESS:
        $('textarea.char.cwsweep[name="note"]').val(data.note);

        // 7. load narrated perimeter-JSON for ACCESS:
        $('div#char-cwsweep-perimeters').empty().append($('<h4 style="color: blue;"></h4>').text(JSON.stringify(data.perimeter)));

        // 8. load c-range for each command for ACCESS:
        // 8.1 SCROLL: scroll out repeated data (the exact reverse of averaging)
        
        // 8.2 REPEATS:
        $('select.char.cwsweep.parameter#c-repeat').empty();
        if (data.data_repeat > 1) {
            $('select.char.cwsweep.parameter#c-repeat').append($('<option>', { text: 'X-ALL', value: 'x' })).append($('<option>', { text: 'X-COUNT', value: 'xc' }))
                .append($('<option>', { text: 'SCROLL', value: 'sc' })).append($('<option>', { text: 'Y-ALL', value: 'y' }));
        };
        for (i = 0; i < data.data_repeat; i++) { $('select.char.cwsweep.parameter#c-repeat').append($('<option>', { text: i+1, value: i })); };

        // 8.3 OPTIONALS:
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
        
        // 8.4 BASICS:
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
        
        // 9. load data progress for ACCESS:
        var data_progress = "  " + String(data.data_progress.toFixed(3)) + "%";
        $('.data-progress.cwsweep').css({"width": data_progress}).text(data_progress);
        $('.data-eta.cwsweep').text("data: " + data.measureacheta + " until completion");
        console.log("Progress: " + data_progress);

    });
    return false;
};
function plot1D_cwsweep(x1,y1,y2,y3,y4,xtitle,phasetype) {
    console.log(xtitle);
    
    let traceL = {x: [], y: [], mode: 'lines', type: 'scatter', 
        name: 'Amplitude (' + wday + ', ' + wmoment + ')',
        line: {color: 'rgb(23, 151, 6)', width: 2.5},
        yaxis: 'y' };
    let traceR = {x: [], y: [], mode: 'lines', type: 'scatter', 
        name: 'Phase (' + wday + ', ' + wmoment + ')',
        line: {color: 'blue', width: 2.5},
        yaxis: 'y2' };

    let traceI = {x: [], y: [], mode: 'lines', type: 'scatter', 
        name: 'I (' + wday + ', ' + wmoment + ')',
        line: {color: 'rgb(255, 151, 6)', width: 2.5},
        yaxis: 'y' };
    let traceQ = {x: [], y: [], mode: 'lines', type: 'scatter', 
        name: 'Q (' + wday + ', ' + wmoment + ')',
        line: {color: 'rgb(255, 6, 151)', width: 2.5},
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

    $.each(x1, function(i, val) {traceI.x.push(val);});
    $.each(y3, function(i, val) {traceI.y.push(val);});
    $.each(x1, function(i, val) {traceQ.x.push(val);});
    $.each(y4, function(i, val) {traceQ.y.push(val);});
    var Trace = [traceL, traceR, traceI, traceQ]
    Plotly.newPlot('char-cwsweep-chart', Trace, layout, {showSendToCloud: true});
    $( "i.cwsweep1d" ).remove(); //clear previous
};
function plot2D_cwsweep(x,y,ZZ,xtitle,ytitle,plotype,mission,colorscal,zsmooth) {
    console.log("Plotting 2D");
         
    // Frame assembly:
    let trace = {
        z: [], x: [], y: [], zsmooth: zsmooth,
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
function Perimeter_Assembler_cwsweep() {
    var PERIMETER = {};
    // 1. Assemble Preset Perimeters into PERIMETER:
    $.each(cwsweep_Perimeters, function(i,perimeter) {
        PERIMETER[perimeter] = $('.char.cwsweep.perimeter#cwsweep-' + perimeter).val();
        console.log("PERIMETER[" + perimeter + "]: " + PERIMETER[perimeter]);
    });
    // 2. Assemble Flexible MACE-JSON into PERIMETER:
    PERIMETER['MACE-JSON'] = {}
    $.each(DC_PATH_Matrix, function(i,channel_set) {
        $.each(channel_set, function(j,channel) {
            let QPC_Pathway = "-QPC-" + DC_Role[i][j] + "-" + String(i+1) + "-" + String(channel); 
            PERIMETER['MACE-JSON']["PATH" + QPC_Pathway] = $('textarea.char.cwsweep.MACE-JSON.pathway-' + QPC_Pathway).val(); 
        });
    });
    $.each(SG_PATH_Matrix, function(i,channel_set) {
        $.each(channel_set, function(j,channel) {
            let QPC_Pathway = "-QPC-" + SG_Role[i][j] + "-" + String(i+1) + "-" + String(channel); 
            PERIMETER['MACE-JSON']["PATH" + QPC_Pathway] = $('textarea.char.cwsweep.MACE-JSON.pathway-' + QPC_Pathway).val(); 
        });
    });
    return PERIMETER;
};

// hiding parameter settings when click outside the modal box:
$('.modal-toggle.new.cwsweep').on('click', function(e) {
    e.preventDefault();
    $('.modal.new.cwsweep').toggleClass('is-visible');
    // revert back to previous option upon leaving dialogue box
    $('select.char.cwsweep[name="wday"]').val(selecteday);
});
$('.modal-toggle.search.cwsweep').on('click', function(e) {
    e.preventDefault();
    $('.modal.search.cwsweep').toggleClass('is-visible');
});
$('.modal-toggle.data-reset.cwsweep').on('click', function(e) {
    e.preventDefault();
    $('.modal.data-reset.cwsweep').toggleClass('is-visible');
});

// show CW-Sweep's daylist (also switch content-page to CW-Sweep)
$(function() {
    $('button.char.access.cwsweep').bind('click', function() {
        $('div.cwsweep.queue-system').empty().append($('<h4 style="color: blue;"></h4>').text(qsystem));
        $('div.charcontent').hide();
        $('div.charcontent.cwsweep').show();
        $('button.char.access').removeClass('selected');
        $('button.char.access.cwsweep').addClass('selected');
        $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/init', {
        }, function (data) {
            // 1. Check Run Permission: (PENDING: Use Global run_permission to notify user whenever certain disabled button is click)
            window.run_permission = data.run_permission;
            window.DAYLIST = data.daylist;
            console.log("run permission: " + run_permission);
            if (run_permission == false) {
                $('input.char#cwsweep-run').hide();
                $('button.char.cwsweep.run').hide();
                $('div#char-cwsweep-announcement').empty().append($('<h4 style="color: red;"></h4>').text("RUN & RESUME BUTTON DISABLED"));
            } else {
                $('input.char#cwsweep-run').show(); // RUN
                $('button.char.cwsweep.run').show(); // RESUME
                $('div#char-cwsweep-announcement').empty().append($('<h4 style="color: red;"></h4>').text("RUN & RESUME BUTTON ENABLED"));
            };
            
            // 2. Loading Day-List and relevant Options:
            $('select.char.cwsweep[name="wday"]').empty();
            $('select.char.cwsweep[name="wday"]').append($('<option>', { text: 'The latest:', value: '' }));
            $.each(data.daylist.reverse(), function(i,v){
                $('select.char.cwsweep[name="wday"]').append($('<option>', {
                    text: v,
                    value: data.daylist.length - 1 - i
                }));
            });
            $('select.char.cwsweep[name="wday"]').append($('<option>', { text: '--Search--', value: 's' }));
            $('select.char.cwsweep[name="wday"]').append($('<option>', { text: '--New--', value: -1 }));
            $('select.char.cwsweep[name="wday"]').append($('<option>', { text: '--Temp--', value: -3 }));

            // 3. Pre-arrange Channel-inputs accordingly based on the WIRING-settings:
            $('select.char-pathway-matrix').empty();
            $('div.char-pathway-matrix').empty();
            // DC MaRoW:
            window.DC_PATH_Matrix = data.DC_PATH_Matrix;
            window.DC_Role = data.DC_Role;
            window.DC_Which = data.DC_Which;
            $.each(DC_PATH_Matrix, function(i,channel_set) {
                $.each(channel_set, function(j,channel) {
                    let QPC_Pathway = "-QPC-" + DC_Role[i][j] + "-" + String(i+1) + "-" + String(channel);
                    $('select.char-pathway-matrix').append($('<option>', { text: QPC_Pathway + " (" + DC_Which[i] + ")", value: QPC_Pathway }));
                    $('div.char-pathway-matrix').append($("<div class='row perimeter mace PATH" + QPC_Pathway + "'>").append($("<div class='col-97' id='left'>")
                        .append($('<label>').text( QPC_Pathway + " (" + DC_Which[i] + ")" ))));
                    $('div.char-pathway-matrix').append($("<div class='row perimeter mace PATH" + QPC_Pathway + "'>").append($("<div class='col-97' id='left'>")
                        .append($('<textarea class="char cwsweep MACE-JSON pathway-' + QPC_Pathway + '" type="text" rows="3" cols="13" style="color:red;">').val('sweep=0'))));
                    if (i!=0 || j!=0) { $("div.row.perimeter.mace.PATH" + QPC_Pathway).hide(); }; // only shows the 1st option when first load
                });
            });
            // SG MaRoW:
            window.SG_PATH_Matrix = data.SG_PATH_Matrix;
            window.SG_Role = data.SG_Role;
            window.SG_Which = data.SG_Which;
            $.each(SG_PATH_Matrix, function(i,channel_set) {
                $.each(channel_set, function(j,channel) {
                    let QPC_Pathway = "-QPC-" + SG_Role[i][j] + "-" + String(i+1) + "-" + String(channel);
                    $('select.char-pathway-matrix').append($('<option>', { text: QPC_Pathway + " (" + SG_Which[i] + ")", value: QPC_Pathway }));
                    $('div.char-pathway-matrix').append($("<div class='row perimeter mace PATH" + QPC_Pathway + "'>").append($("<div class='col-97' id='left'>")
                        .append($('<label>').text( QPC_Pathway + " (" + SG_Which[i] + ")" ))));
                    $('div.char-pathway-matrix').append($("<div class='row perimeter mace PATH" + QPC_Pathway + "'>").append($("<div class='col-97' id='left'>")
                        .append($('<textarea class="char cwsweep MACE-JSON pathway-' + QPC_Pathway + '" type="text" rows="3" cols="13" style="color:red;">').val('frequency=6, power=0'))));
                    $("div.row.perimeter.mace.PATH" + QPC_Pathway).hide(); // hide the rest first
                });
            });
            // Display ALL MaRoW:
            $('select.char-pathway-matrix').append($('<option>', { text: "ALL", value: "ALL" }));

        });
        return false;
    });
});

// list times based on day picked
$(function () {
    $('select.char.cwsweep[name="wday"]').on('change', function () {
        // make global wday
        window.wday = $('select.char.cwsweep[name="wday"]').val();
        listimes_cwsweep();
    });
    return false;
});

// Surfing through Pathways One-by-one or Altogether:
$('select.char-pathway-matrix').on('change', function() {
    $("div.row.perimeter.mace").hide();
    if ($(this).val()=="ALL") { $("div.row.perimeter.mace").show(); 
    } else { $("div.row.perimeter.mace.PATH" + $(this).val()).show(); };
    return false;
});

// click to run:
$('input.char#cwsweep-run').on('touchend click', function(event) {
    eventHandler(event, $(this)); // Prevent phantom clicks from touch-click.
    setTimeout(() => { $('button.tablinks#ALL-tab').trigger('click'); }, 371);
    $('h3.all-mssn-warning').text(">> JOB STARTED >>");
    // Assemble PARAMETER:
    var fluxbias = $('input.char.cwsweep[name="fluxbias"]').val();
    var xyfreq = $('input.char.cwsweep[name="xyfreq"]').val();
    var xypowa = $('input.char.cwsweep[name="xypowa"]').val();
    var sparam = $('input.char.cwsweep[name="sparam"]').val();
    var ifb = $('input.char.cwsweep[name="ifb"]').val();
    var freq = $('input.char.cwsweep[name="freq"]').val();
    var powa = $('input.char.cwsweep[name="powa"]').val();
    var comment = JSON.stringify($('textarea.char.cwsweep[name="ecomment"]').val());
    
    // Assemble PERIMETER:
    var PERIMETER = {};
    $.each(cwsweep_Perimeters, function(i,perimeter) {
        PERIMETER[perimeter] = $('input.char.cwsweep.perimeter#cwsweep-' + perimeter).val();
        console.log("PERIMETER[" + perimeter + "]: " + PERIMETER[perimeter]);
    });

    $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/new', {
        wday: wday, 
        fluxbias: fluxbias, xyfreq: xyfreq, xypowa: xypowa, 
        sparam: sparam, ifb: ifb, freq: freq, powa: powa, 
        comment: comment, PERIMETER: JSON.stringify(PERIMETER),
    }, function (data) { 
        // setTimeout(() => { $('button.tablinks#ALL-tab').trigger('click'); }, 7);
        setTimeout(() => { $('button.tablinks#ALL-tab').trigger('click'); }, 371);
        $('h3.all-mssn-warning').text("JOB STATUS: " + data.status);
    });
    return false;
});

// click to search: (pending)
$('input.char.cwsweep[name="search"]').change( function() {
    $( "i.cwsweep" ).remove(); //clear previous
    $('button.char.cwsweep').prepend("<i class='cwsweep fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
    // waveform commands
    
    // var comment = $('textarea.char.cwsweep[name="comment"]').val();
    $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/search', {
        
    }, function (data) {
        
        console.log("complete: " + data.filelist);
        $( "i.cwsweep" ).remove(); //clear previous
    });
    return false;
});

// Click to resume measurement
$(function () {
    $('button.char#cwsweep-resume').on('touchend click', function(event) {
        eventHandler(event, $(this)); // Prevent phantom clicks from touch-click.
        setTimeout(() => { $('button.tablinks#ALL-tab').trigger('click'); }, 371);
        $('h3.all-mssn-warning').text(">> JOB STARTED >>");
        // Assemble PARAMETER:
        var fluxbias = $('input.char.cwsweep[name="fluxbias"]').val();
        var xyfreq = $('input.char.cwsweep[name="xyfreq"]').val();
        var xypowa = $('input.char.cwsweep[name="xypowa"]').val();
        var sparam = $('input.char.cwsweep[name="sparam"]').val();
        var ifb = $('input.char.cwsweep[name="ifb"]').val();
        var freq = $('input.char.cwsweep[name="freq"]').val();
        var powa = $('input.char.cwsweep[name="powa"]').val();

        // Assemble PERIMETER:
        var PERIMETER = {};
        $.each(cwsweep_Perimeters, function(i,perimeter) {
            PERIMETER[perimeter] = $('input.char.cwsweep.perimeter#cwsweep-' + perimeter).val();
            console.log("PERIMETER[" + perimeter + "]: " + PERIMETER[perimeter]);
        });

        $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/resume', {
            wday: wday, wmoment: wmoment, 
            fluxbias: fluxbias, xyfreq: xyfreq, xypowa: xypowa, 
            sparam: sparam, ifb: ifb, freq: freq, powa: powa, PERIMETER: JSON.stringify(PERIMETER),
        }, function (data) {
            if (data.resumepoint == data.datasize) {
                console.log("The data was already complete!")
            } else { console.log("The data has just been updated")};
            // setTimeout(() => { $('button.tablinks#ALL-tab').trigger('click'); }, 7);
            setTimeout(() => { $('button.tablinks#ALL-tab').trigger('click'); }, 371);
            $('h3.all-mssn-warning').text("JOB COMPLETE: " + data.status);
        });
        return false;
    });
});

// access data based on time picked
$(function () {
    $('select.char.cwsweep[name="wmoment"]').on('change', function () {
        // Make global variable:
        window.wmoment = $('select.char.cwsweep[name="wmoment"]').val();
        accessdata_cwsweep();
    });
    return false;
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
    $('input.char.cwsweep[name="1d-data"]').on('click', function () {
        $( "i.cwsweep1d" ).remove(); //clear previous
        $('button.char.access.cwsweep').prepend("<i class='cwsweep1d fa fa-palette fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        var irepeat = $('select.char.cwsweep.parameter#c-repeat').val();
        var ifluxbias = $('select.char.cwsweep.parameter#c-fluxbias').val();
        var ixyfreq = $('select.char.cwsweep.parameter#c-xyfreq').val();
        var ixypowa = $('select.char.cwsweep.parameter#c-xypowa').val();
        var isparam = $('select.char.cwsweep.parameter#c-sparam').val();
        var iifb = $('select.char.cwsweep.parameter#c-ifb').val();
        var ifreq = $('select.char.cwsweep.parameter#c-freq').val();
        var ipowa = $('select.char.cwsweep.parameter#c-powa').val();
        var noise = $('input.char.cwsweep.bottomost-data-block#c-noise-data').is(':checked')?1:0;
        console.log("Picked: " + isparam + ", Noise-data: " + noise);
        $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/1ddata', {
            irepeat: irepeat, ifluxbias: ifluxbias, ixyfreq: ixyfreq, ixypowa: ixypowa, isparam: isparam, iifb: iifb, ifreq: ifreq, ipowa: ipowa, noise: noise,
        }, function (data) {
            window.x1 = data.x1;
            window.y1 = new Object();
            window.y1.A = data.y1;
            window.y1.P = data.yp;
            window.y1.UP = data.yup;
            window.x1title = data.x1title;
            window.y1.I = data.selected_I;
            window.y1.Q = data.selected_Q;
            // Phase option
            $('select.char.data.cwsweep[name="1d-phase-type"]').empty().append($('<option>', { text: 'Pha', value: 'Pha' })).append($('<option>', { text: 'UPha', value: 'UPha' }));
            plot1D_cwsweep(x1,y1.A,y1.P,y1.I,y1.Q,x1title,'<b>Raw-Pha(rad)</b>');
            $('button.char#cwsweep-savecsv').show();
        });
    });
    return false;
});
$('select.char.data.cwsweep').on('change', function() {
    if ($('select.char.data.cwsweep[name="1d-phase-type"]').val() == "Pha") {
        console.log("Pha mode");
        plot1D_cwsweep(x1,y1.A,y1.P,y1.I,y1.Q,x1title,'<b>Raw-Pha(rad)</b>');
    } else if ($('select.char.data.cwsweep[name="1d-phase-type"]').val() == "UPha") {
        console.log("UPha mode");
        plot1D_cwsweep(x1,y1.A,y1.UP,y1.I,y1.Q,x1title,'<b>UFN-Pha(rad)</b>');
    };
    return false;
});
// INSERT 1D-data for comparison
$(function () {
    $('button.char#cwsweep-insert-1D').on('click', function () {
        $('div#char-cwsweep-announcement').empty();
        $( "i.cwsweep1d" ).remove(); //clear previous
        $('button.char.access.cwsweep').prepend("<i class='cwsweep1d fa fa-palette fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        var irepeat = $('select.char.cwsweep.parameter#c-repeat').val();
        var ifluxbias = $('select.char.cwsweep.parameter#c-fluxbias').val();
        var ixyfreq = $('select.char.cwsweep.parameter#c-xyfreq').val();
        var ixypowa = $('select.char.cwsweep.parameter#c-xypowa').val();
        var isparam = $('select.char.cwsweep.parameter#c-sparam').val();
        var iifb = $('select.char.cwsweep.parameter#c-ifb').val();
        var ifreq = $('select.char.cwsweep.parameter#c-freq').val();
        var ipowa = $('select.char.cwsweep.parameter#c-powa').val();
        var noise = $('input.char.cwsweep.bottomost-data-block#c-noise-data').is(':checked')?1:0;
        console.log("Picked: " + isparam + ", Noise-data: " + noise);
        $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/1ddata', {
            irepeat: irepeat, ifluxbias: ifluxbias, ixyfreq: ixyfreq, ixypowa: ixypowa, isparam: isparam, iifb: iifb, ifreq: ifreq, ipowa: ipowa, noise: noise,
        }, function (data) {
            window.x1C = data.x1;
            window.y1C = new Object();
            window.y1C.A = data.y1;
            window.y1C.P = data.yp;
            window.y1C.UP = data.yup;
            window.x1titleC = data.x1title;
            window.y1C.I = data.selected_I;
            window.y1C.Q = data.selected_Q;
            // Normalization Options:
            $('select.char.data.cwsweep#cwsweep-compare-nml').empty().append($('<option>', { text: 'direct', value: 'direct' }))
                                                                .append($('<option>', { text: 'normaldip', value: 'normaldip' }))
                                                                .append($('<option>', { text: 'normalpeak', value: 'normalpeak' }));
            console.log('selected: ' + $('select.char.data.cwsweep#cwsweep-compare-nml').val());
            normalize = Boolean($('select.char.data.cwsweep#cwsweep-compare-nml').val()!='direct');
            direction = $('select.char.data.cwsweep#cwsweep-compare-nml').val().split('normal')[1];

            // APUP Options:
            $('select.char.data.cwsweep#cwsweep-compare-apup').empty().append($('<option>', { text: 'Amplitude', value: 'A' }))
                                                                .append($('<option>', { text: 'Phase', value: 'P' }))
                                                                .append($('<option>', { text: 'UPhase', value: 'UP' }))
                                                                .append($('<option>', { text: 'I', value: 'I' }))
                                                                .append($('<option>', { text: 'Q', value: 'Q' }));

            var APUPIQ = $('select.char.data.cwsweep#cwsweep-compare-apup').val();
            compare1D(x1,y1[APUPIQ],x1C,y1C[APUPIQ],x1titleC,APUPIQ,normalize,direction,'char-cwsweep');
        })
            .fail(function(jqxhr, textStatus, error){
                $('div#char-cwsweep-announcement').append($('<h4 style="color: red;"></h4>').text("Oops: " + error));
                $( "i.cwsweep1d" ).remove(); //clear the status
            });
    });
    return false;
});
$('.char.data.cwsweep.compare').on('change', function() {
    normalize = Boolean($('select.char.data.cwsweep#cwsweep-compare-nml').val()!='direct');
    direction = $('select.char.data.cwsweep#cwsweep-compare-nml').val().split('normal')[1];
    var APUPIQ = $('select.char.data.cwsweep#cwsweep-compare-apup').val();
    compare1D(x1,y1[APUPIQ],x1C,y1C[APUPIQ],x1titleC,APUPIQ,normalize,direction,'char-cwsweep');
    return false;
});

// assemble 2D-data based on c-parameters picked
$(function () {
    $('input.char.cwsweep[name="2d-data"]').on('click', function () {
        $('div#char-cwsweep-announcement').empty().append($('<h4 style="color: red;"></h4>').text("Plotting 2D might takes some time. Please wait... "));
        $( "i.cwsweep2d" ).remove(); //clear previous
        $('button.char.access.cwsweep').prepend("<i class='cwsweep2d fa fa-palette fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
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
            window.plot2dmessage = data.message;
            // console.log("PLOTTING 2D: " + plot2dmessage);
            // Amplitude (default) or Phase
            $('select.char.data.cwsweep[name="2d-amphase"]').empty().append($('<option>', { text: 'Amp', value: 'Amp' })).append($('<option>', { text: 'Pha (Raw)', value: 'Pha' }));
            // Data grooming
            $('select.char.data.cwsweep[name="2d-type"]').empty().append($('<option>', { text: 'direct', value: 'direct' }))
                .append($('<option>', { text: 'normalYdip', value: 'normalYdip' })).append($('<option>', { text: 'normalYpeak', value: 'normalYpeak' }))
                .append($('<option>', { text: 'normalXdip', value: 'normalXdip' })).append($('<option>', { text: 'normalXpeak', value: 'normalXpeak' }));
            // Data color-scaling
            $('select.char.data.cwsweep[name="2d-colorscale"]').empty().append($('<option>', { text: 'YlOrRd', value: 'YlOrRd' }))
                .append($('<option>', { text: 'YlGnBu', value: 'YlGnBu' })).append($('<option>', { text: 'RdBu', value: 'RdBu' }))
                .append($('<option>', { text: 'Portland', value: 'Portland' })).append($('<option>', { text: 'Picnic', value: 'Picnic' }))
                .append($('<option>', { text: 'Jet', value: 'Jet' })).append($('<option>', { text: 'Hot', value: 'Hot' }))
                .append($('<option>', { text: 'Greys', value: 'Greys' })).append($('<option>', { text: 'Greens', value: 'Greens' }))
                .append($('<option>', { text: 'Electric', value: 'Electric' })).append($('<option>', { text: 'Earth', value: 'Earth' }))
                .append($('<option>', { text: 'Bluered', value: 'Bluered' })).append($('<option>', { text: 'Blackbody', value: 'Blackbody' }))
                .append($('<option>', { text: 'Blues', value: 'Blues' })).append($('<option>', { text: 'Viridis', value: 'Viridis' }));
            // Transpose or not
            $('select.char.data.cwsweep[name="2d-direction"]').empty().append($('<option>', { text: 'stay', value: 'stay' })).append($('<option>', { text: 'rotate', value: 'rotate' }));
            // Z-Smooth options:
            $('select.char.data.cwsweep[name="2d-zsmooth"]').empty().append($('<option>', { text: 'Best', value: 'best' })).append($('<option>', { text: 'Fast', value: 'fast' })).append($('<option>', { text: 'False', value: 'false' }));
            plot2D_cwsweep(x, y, ZZA, xtitle, ytitle, 
                $('select.char.data.cwsweep[name="2d-type"]').val(),'cwsweep',
                $('select.char.data.cwsweep[name="2d-colorscale"]').val(),
                $('select.char.data.cwsweep[name="2d-zsmooth"]').val());
        })
        .done(function(){
            $('button.char#cwsweep-savemat').show();
            $('div#char-cwsweep-announcement').empty().append($('<h4 style="color: red;"></h4>').text(plot2dmessage));
            $( "i.cwsweep2d" ).remove(); //clear the status
        })
        .fail(function(jqxhr, textStatus, error){
            $('div#char-cwsweep-announcement').empty().append($('<h4 style="color: red;"></h4>').text("Oops: " + error + ". MAYBE TRY TO REVERSE X-Y-ORDER."));
            $( "i.cwsweep2d" ).remove(); //clear the status
        });
    });
    return false;
});
$('select.char.data.cwsweep.2d').on('change', function() {
    if ($('select.char.data.cwsweep[name="2d-amphase"]').val() == "Amp") {var ZZ = ZZA; }
    else if ($('select.char.data.cwsweep[name="2d-amphase"]').val() == "Pha") {var ZZ = ZZP; };
    if ($('select.char.data.cwsweep[name="2d-direction"]').val() == "rotate") {
        plot2D_cwsweep(y, x, transpose(ZZ), ytitle, xtitle, 
            $('select.char.data.cwsweep[name="2d-type"]').val(),'cwsweep',
            $('select.char.data.cwsweep[name="2d-colorscale"]').val(),
            $('select.char.data.cwsweep[name="2d-zsmooth"]').val());
    } else {
        plot2D_cwsweep(x, y, ZZ, xtitle, ytitle, 
            $('select.char.data.cwsweep[name="2d-type"]').val(),'cwsweep',
            $('select.char.data.cwsweep[name="2d-colorscale"]').val(),
            $('select.char.data.cwsweep[name="2d-zsmooth"]').val());
    };
    return false;
});

// saving exported csv-data to client's PC:
$('button.char#cwsweep-savecsv').on('click', function() {
    console.log("SAVING CSV FILE");

    // in order to trigger href send-file request: (PENDING: FIND OUT THE WEIRD LOGIC BEHIND THIS NECCESITY)
    $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/access', { wmoment: wmoment }, function (data) {});

    $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/export/1dcsv', {
        // merely for security screening purposes
        ifreq: $('select.char.cwsweep.parameter#c-freq').val()
    }, function (data) {
        console.log("STATUS: " + data.status + ", URL: " + data.server_URL + ", PORT: " + data.qumport);
        pull_n_send(data.server_URL, data.qumport, data.user_name, filename='1Dcwsweep.csv');
    });
    return false;
});
// saving exported mat-data to client's PC:
$('button.char#cwsweep-savemat').on('click', function() {
    console.log("SAVING MAT FILE");

    // in order to trigger href send-file request: (PENDING: FIND OUT THE WEIRD LOGIC BEHIND THIS NECCESITY)
    $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/access', { wmoment: wmoment }, function (data) {});

    $.getJSON(mssnencrpytonian() + '/mssn/char/cwsweep/export/2dmat', {
        // merely for security screening purposes
        ifreq: $('select.char.cwsweep.parameter#c-freq').val()
    }, function (data) {
        console.log("STATUS: " + data.status + ", URL: " + data.server_URL + ", PORT: " + data.qumport);
        pull_n_send(data.server_URL, data.qumport, data.user_name, filename='2Dcwsweep.mat');
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
            ownerpassword: $('input.char.cwsweep[name="ownerpassword"]').val(),
            truncateafter: $('input.char.cwsweep[name="truncateafter"]').val(),
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

// Notification on click:
$('input.cwsweep.notification').click( function(){
    var Day = $('input.cwsweep.notification').val().split(' > ')[1];
    var Moment = $('input.cwsweep.notification').val().split(' > ')[2];
    console.log('Day: ' + Day + ', Moment: ' + Moment);

    // Setting global Day & Moment index:
    wday = DAYLIST.length - 1 - DAYLIST.indexOf(Day);
    wmoment = Moment;
    // Digesting Day & Moment on the back:
    $.when( listimes_cwsweep() ).done(function () { accessdata_cwsweep(); });
    // Setting Day & Moment on the front:
    $('select.char.cwsweep[name="wday"]').val(wday);
    setTimeout(() => {
        console.log('wmoment: ' + wmoment);
        $('select.char.cwsweep[name="wmoment"]').val(wmoment); 
    }, 160); //.trigger('change'); //listing time is a bit slower than selecting option => conflict

    return false;
});

// SAVE NOTE:
$('textarea.char.cwsweep[name="note"]').change( function () {
    $.getJSON(mssnencrpytonian() + '/mssn'+'/all/save/jobnote', {
        ACCESSED_JOBID: ACCESSED_JOBID,
        note: $('textarea.char.cwsweep[name="note"]').val(),
    }, function (data) {
        $('div#char-cwsweep-announcement').empty().append($('<h4 style="color: red;"></h4>').text(data.message));
    });
    return false;
});