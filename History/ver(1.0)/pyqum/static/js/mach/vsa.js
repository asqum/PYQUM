//when page is loading:
$(document).ready(function(){
    $('div.vsacontent').hide();
});

// Global variables:
window.count = 1;
window.sample_I = [];
window.sample_Q = [];
window.sample_A = [];

// Functions:
function vsaplotIQA(x1,y1,y2,y3,xtitle,ytitle) {
    console.log(xtitle);
    
    let trace1 = {x: [], y: [], mode: 'lines', type: 'scatter', 
        name: 'I',
        line: {color: 'blue', width: 2.5},
        yaxis: 'y' };
    let trace2 = {x: [], y: [], mode: 'lines', type: 'scatter', 
        name: 'Q',
        line: {color: 'red', width: 2.5},
        yaxis: 'y' };
    let trace3 = {x: [], y: [], mode: 'lines', type: 'scatter', 
        name: 'A',
        line: {color: 'black', width: 2.5},
        yaxis: 'y' };

    let layout = {
        legend: {x: 1.08},
        height: $(window).height()*0.66,
        width: $(window).width()*0.7,
        xaxis: {
            zeroline: false,
            title: xtitle,
            titlefont: {size: 18},
            tickfont: {size: 18},
            tickwidth: 3,
            linewidth: 3,
            gridcolor: 'rgb(159, 197, 232)',
            zerolinecolor: 'rgb(74, 134, 232)',
        },
        yaxis: {
            zeroline: false,
            title: ytitle,
            titlefont: {size: 18},
            tickfont: {size: 18},
            tickwidth: 3,
            linewidth: 5,
            gridcolor: 'rgb(159, 197, 232)',
            zerolinecolor: 'rgb(74, 134, 232)',
        },
        title: 'Digitized IQ Signal',
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
    
    $.each(x1, function(i, val) {trace1.x.push(val);});
    $.each(y1, function(i, val) {trace1.y.push(val);});
    $.each(x1, function(i, val) {trace2.x.push(val);});
    $.each(y2, function(i, val) {trace2.y.push(val);});
    $.each(x1, function(i, val) {trace3.x.push(val);});
    $.each(y3, function(i, val) {trace3.y.push(val);});

    var Trace = [trace1, trace2, trace3];
    Plotly.newPlot('vsa-IQAP-chart', Trace, layout, {showSendToCloud: true});
    // $( "i.cwsweep1d" ).remove(); //clear previous
};

function vsaplotPhase(x1,y1,xtitle,ytitle) {
    console.log(xtitle);
    
    let trace1 = {x: [], y: [], mode: 'markers', marker: { line_width: 1, symbol: 'circle', size: 16}, 
        name: 'I',
        line: {color: 'blue', width: 2.5},
        yaxis: 'y' };

    let layout = {
        legend: {x: 1.08},
        height: $(window).height()*0.66,
        width: $(window).width()*0.7,
        xaxis: {
            zeroline: false,
            title: xtitle,
            titlefont: {size: 18},
            tickfont: {size: 18},
            tickwidth: 3,
            linewidth: 3,
            gridcolor: 'rgb(159, 197, 232)',
            zerolinecolor: 'rgb(74, 134, 232)',
        },
        yaxis: {
            zeroline: false,
            title: ytitle,
            titlefont: {size: 18},
            tickfont: {size: 18},
            tickwidth: 3,
            linewidth: 5,
            gridcolor: 'rgb(159, 197, 232)',
            zerolinecolor: 'rgb(74, 134, 232)',
        },
        title: 'Digitized IQ Signal',
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
    
    $.each(x1, function(i, val) {trace1.x.push(val);});
    $.each(y1, function(i, val) {trace1.y.push(val);});

    var Trace = [trace1];
    Plotly.newPlot('vsa-IQAP-chart', Trace, layout, {showSendToCloud: true});
    // $( "i.cwsweep1d" ).remove(); //clear previous
};

function vsaplay() {
    $.getJSON('/mach/vsa/play', {
    }, function (data) {
        console.log(data.log);

        window.t = data.t;
        window.I = data.I;
        window.Q = data.Q;
        window.A = data.A;

        if ($('select.vsa#average').val()==1) {
            console.log("averaging mode");

        };

        vsaplotIQA(t, I, Q, A, "time(s)", "IQA(V)");
        $( "i.vsaplay" ).remove(); //clear previous
    });
};

//show debug's page
$(function() {
    $('button.vsa#debug').bind('click', function() {
        $('div.vsacontent').hide();
        $('div.vsacontent#debug').show();
        $('button.vsa').removeClass('selected');
        $('button.vsa#debug').addClass('selected');
        return false;
    });
});

//show about's page
$(function () {
    $('button.vsa#about').bind('click', function () { // id become #
        $.getJSON('/mach/vsa/about', {
        }, function (data) {
            $('div.vsacontent').hide();
            $('div.vsacontent#about').empty();
            $.each(data.message, function(index, value) {
                $('div.vsacontent#about').append($('<h4 style="color: darkblue;"></h4>').text(Number(index+1) + ". " + value.split(": ")[0] + ": ").
                append($('<span style="background-color: darkblue; color: white;"></span>').text(value.split(": ")[1])));
              });
              $('div.vsacontent#about').show();
              $('button.vsa').removeClass('selected');
              $('button.vsa#about').addClass('selected');
        });
        return false;
    });
}); 

//show setting's page
$(function() {
    $('button.vsa#settings').bind('click', function() {
        $('div.vsacontent').hide();
        $('div.vsacontent#settings').show();
        $('button.vsa').removeClass('selected');
        $('button.vsa#settings').addClass('selected');
        return false;
    });
});

//setting on key-press
$(function () {
    $('input.vsa#settings').keypress(function(e) {
        var key = e.which;
        if (key == 13) { $('input.vsa#settings').trigger('click'); } }); });
$(function () {
    $('input.vsa#set').bind('click', function () { // the enter key code
        $.getJSON('/mach/vsa/settings', {
            // input value here:
            acquis: $('input.vsa[name="acquis"]').val(),
            lofreq: $('input.vsa[name="lofreq"]').val(),
            lopowa: $('input.vsa[name="lopowa"]').val(),
            lobwd: $('input.vsa[name="lobwd"]').val(),
            preselect: $('select.vsa[name="preselect"]').val(),
            triggersource: $('select.vsa[name="triggersource"]').val(),
            triggerdelay: $('input.vsa[name="triggerdelay"]').val(),
            extlevel: $('input.vsa[name="extlevel"]').val(),
            extslope: $('select.vsa[name="extslope"]').val(),
            triggertimeout: $('input.vsa[name="triggertimeout"]').val(),
            
        }, function (data) {
            $('div.vsacontent#debug').append($('<h4 style="background-color: lightgreen;"></h4>').text(Date($.now())));
            $.each(data.message, function(index, value) {
                $('div.vsacontent#debug').append($('<h4 style="color: black;"></h4>').text(Number(index+1) + ". " + value));
              });
            $('button.vsa#play').trigger('click'); //click on play automatically after finished setting parameters //or: .click();
            $('select.vsa.data#IQAP').empty().append($('<option>', { text: 'IQA', value: 'IQA' })).append($('<option>', { text: 'Phase', value: 'Phase' }));
        });
        return false;
    });
});

//reset
$(function () {
    $('button.vsa#reset').bind('click', function () { // id become #
        $.getJSON('/mach/vsa/reset', {
        }, function (data) {
            if (data.message != 0){
                $('button.vsa').removeClass('error');
                $('button.vsa#close').removeClass('close');
                $('button.vsa#reset').addClass('reset');}
            else {$('button.vsa').addClass('error');}
        });
        return false;
    });
}); 

//close
$(function () {
    $('button.vsa#close').bind('click', function () { // id become #
        $.getJSON('/mach/vsa/close', {
        }, function (data) {
            if (data.message == 0){
                $('button.vsa').removeClass('error');
                $('button.vsa#reset').removeClass('reset');
                $('button.vsa#close').addClass('close');}
            else {$('button.vsa').addClass('error');}         
        });
        return false;
    });
}); 

//Arm & measure
$(function () {
    $('button.vsa#play').bind('click', function () { // id become #
        $( "i.vsaplay" ).remove(); //clear previous
        $('button.vsa#play').prepend("<i class='vsaplay fas fa-circle-notch fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        vsaplay();
        return false;
    });
});
$('select.vsa.data#IQAP').on('change', function() {
    if ($('select.vsa.data#IQAP').val() == "IQA") {
        vsaplotIQA(t, I, Q, A, "time(s)", "IQA(V)");
    } else {
        vsaplotPhase(I, Q, "I(V)", "Q(V)");
    };
    return false;
});

// live update
$(function () {
    $('input.vsa#settings[name="stream"]').click(function () { 
        var stream = $('input.vsa#settings[name="stream"]').is(':checked'); //use css to respond to click / touch
        if (stream == true) {
            $( "i.vsaplay" ).remove(); //clear previous
            $('button.vsa#play').prepend("<i class='vsaplay fas fa-circle-notch fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
            vsaplay();
            var vsastream = setInterval(vsaplay, 100);
            $('input.vsa#settings[name="stream"]').click(function () {
                clearInterval(vsastream); 
                $( "i.vsaplay" ).remove(); //clear previous
            });
        };
    });
});
