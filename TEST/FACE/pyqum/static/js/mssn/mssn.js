//when page is loading:
$(document).ready(function(){
    // $('.mssn div#STATE').show();
    $('button#ALL-tab').toggleClass('active');
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
        xaxis: { zeroline: false, title: xtitle, titlefont: {size: 18}, tickfont: {size: 18}, tickwidth: 3, linewidth: 3 },
        yaxis: { zeroline: false, title: ytitle, titlefont: {size: 18}, tickfont: {size: 18}, tickwidth: 3, linewidth: 3 },
        yaxis2: { zeroline: false, title: '<b>Difference</b>', titlefont: {color: 'Grey', size: 18}, 
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
    Plotly.newPlot(mission.split("-")[0] + '-' + mission.split("-")[1] + '-chart', Trace, layout, {showSendToCloud: true});
    $( "i." + mission.split("-")[1] + "1d" ).remove(); //clear previous

    console.log("Plotted 1D-Compare for " + mission.split("-")[0] + "-" + mission.split("-")[1]);
};
