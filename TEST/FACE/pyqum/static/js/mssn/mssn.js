//when page is loading:
$(document).ready(function(){
    // $('.mssn div#STATE').show();
    $('button#ALL-tab').toggleClass('active'); // default show-up of 'ALL' content is set by mssn.css
    window.access_jobids = "";
    window.ref_jobids = "";
});

function tracking_access_jobids(current_jobid, track_limit=7) {
    if (access_jobids.includes(String(current_jobid))==true) { 
        // AVOID RECURRANCE OF JOBID(s), REMOVE REDUNDANT COMMA(s)
        access_jobids = access_jobids.replace(String(current_jobid),"nil").replace("nil,","").replace(",nil","").replace("nil","");
    };
    let jobids_array = [];
    if (access_jobids!="") { 
        for (i = 0; i < Math.min(track_limit-1, access_jobids.split(',').length); i++) { jobids_array.push(access_jobids.split(',')[i]); }; 
    };
    access_jobids = [String(current_jobid)].concat(jobids_array).join(','); // ORDER: NEW -> OLD JOBID(s)
    return access_jobids.split(',')[0];
};
function showing_tracked_jobids() {
    $('.mssn div.tab div.buttons').remove();
    if ($('select.mssn.tracking_type').val()=="access-jobid") {
        $.each(access_jobids.split(','), function(i,jobid) { 
            if (jobid!="") { $('.mssn div.tab').append('<div class="buttons"><a class="all-mssn-access btn yellow" id="jid_' + jobid + '">' + jobid + '</a></div>'); };
        });
    };
    if ($('select.mssn.tracking_type').val()=="ref-jobid") {
        if (typeof ref_jobids!="undefined") {
            $.each(ref_jobids.split(','), function(i,jobid) {
                jobid = parseInt(jobid);
                if (isNaN(jobid)==false) { $('.mssn div.tab').append('<div class="buttons"><a class="all-mssn-access btn blue" id="jid_' + jobid + '">' + jobid + '</a></div>'); };
            });
        };
    };
    
    return false;
};
$(function () {
    $('select.mssn.tracking_type').on('change', function() { showing_tracked_jobids(); });
    return false; 
});

function mssnencrpytonian() {
    return '/' + 'ghhgjad';
};

function openTab(evt, Name) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the link that opened the tab
    document.getElementById(Name).style.display = "block";
    evt.currentTarget.className += " active";
} 

function Normalize_Dip(Z) {
    var Zrow = [];
    var zmin = Math.min.apply(Math, Z);
    var zmax = Math.max.apply(Math, Z);
    $.each(Z, function(i, z) {
        var znml = (z-zmax)/(zmax-zmin);
        Zrow.push(znml);
    });
    return Zrow;
}

function Normalize_Peak(Z) {
    var Zrow = [];
    var zmin = Math.min.apply(Math, Z);
    var zmax = Math.max.apply(Math, Z);
    $.each(Z, function(i, z) {
        var znml = (z-zmin)/(zmax-zmin);
        Zrow.push(znml);
    });
    return Zrow;
}

function VdBm_Conversion(Y, selector) {
    Y_Conv = [];
    yunit = $(selector).val();
    console.log("Converted to: " + yunit);
    if ($(selector).val() == 'V') {
        $.each(Y, function(i, val) {Y_Conv.push(val);});
    } else if ($(selector).val() == 'dBm') {
        $.each(Y, function(i, val) {
            var val = 10*Math.log10(0.5*(val**2)/50*1000);
            Y_Conv.push(val);
        });
    };
    return {'y': Y_Conv, 'yunit': yunit}; 
}

// Compare two 1D-Curves (shared by fresp, cwsweep):
function compare1D(x1,y1,x2,y2,xtitle,ytitle,normalize=false,direction='dip',mission='char-cwsweep') {
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
        xaxis: { zeroline: false, title: xtitle, titlefont: {size: text_size}, tickfont: {size: text_size}, tickwidth: axis_width, linewidth: axis_width },
        yaxis: { zeroline: false, title: ytitle, titlefont: {size: text_size}, tickfont: {size: text_size}, tickwidth: axis_width, linewidth: axis_width },
        yaxis2: { zeroline: false, title: '<b>Difference</b>', titlefont: {color: 'Grey', size: text_size}, 
            tickfont: {color: 'grey', size: text_size}, tickwidth: axis_width, linewidth: axis_width, overlaying: 'y', side: 'right' },
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
    Plotly.newPlot(mission.split("-")[0] + '-' + mission.split("-")[1] + '-chart', Trace, layout, {showSendToCloud: true});
    $( "i." + mission.split("-")[1] + "1d" ).remove(); //clear previous

    console.log("Plotted 1D-Compare for " + mission.split("-")[0] + "-" + mission.split("-")[1]);
};

// *functions are shared across all missions!
function eventHandler(event, selector) {
    event.stopPropagation(); // Stop event bubbling.
    event.preventDefault(); // Prevent default behaviour
    if (event.type === 'touchend') selector.off('click'); // If event type was touch turn off clicks to prevent phantom clicks.
};

