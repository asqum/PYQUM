// Important notes:
// No keypress for security reason

//when page is loading:
$(document).ready(function(){
    $('div.awgcontent').hide();
    $('label.awg.ch1').parent().hide();
    $('input.awg.ch1').parent().hide();
    $('label.awg.ch1.cosin').parent().show();
    $('input.awg.ch1.cosin').parent().show();
    $('label.awg.ch2').parent().hide();
    $('input.awg.ch2').parent().hide();
    $('label.awg.ch2.cosin').parent().show();
    $('input.awg.ch2.cosin').parent().show();
});

// Functions:
function awgplot1D(x1,y1,y2,xtitle,ytitle) {
    console.log(xtitle);
    
    let trace1 = {x: [], y: [], mode: 'lines', type: 'scatter', 
        name: 'Channel-1',
        line: {color: 'green', width: 2.5},
        yaxis: 'y' };
    let trace2 = {x: [], y: [], mode: 'lines', type: 'scatter', 
        name: 'Channel-2',
        line: {color: 'magenta', width: 2.5},
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
        // yaxis2: {
        //     zeroline: false,
        //     title: ytitle2, 
        //     titlefont: {color: 'rgb(148, 103, 189)', size: 18}, 
        //     tickfont: {color: 'rgb(148, 103, 189)', size: 18},
        //     tickwidth: 3,
        //     linewidth: 3, 
        //     overlaying: 'y', 
        //     side: 'right'
        // },
        title: '3-Periods Waveform from AWG Channel Output:',
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

    var Trace = [trace1, trace2]
    Plotly.newPlot('awg-waveform-chart', Trace, layout, {showSendToCloud: true});
    // $( "i.cwsweep1d" ).remove(); //clear previous
};

//show debug's page
$(function() {
    $('button.awg#debug').bind('click', function() {
        $('div.awgcontent').hide();
        $('div.awgcontent#debug').show();
        $('button.awg').removeClass('selected');
        $('button.awg#debug').addClass('selected');
        return false;
    });
});

// log debug
function logdebug (data) {
    if ($(".dh4").parent().hasClass("container")) {$(".dh4").unwrap();}
    $('div.awgcontent#debug').append($('<h4 class="dh4" style="background-color: lightgreen;"></h4>')
    .text(Date($.now())));
    $.each(data.message, function(index, value) {
        $('div.awgcontent#debug').append($('<h4 class="dh4" style="color: black;"></h4>')
        .text(Number(index+1) + ". " + value));});
    $(".dh4").wrapAll("<div class='container'></div>");
    // $('button.awg#about').trigger('click'); //or: .click();
    console.log("logging debug status");
}

//show about's page (directly inquire from instrument)
$(function () {
    $('button.awg#about').bind('click', function () { // id become #
        console.log("displaying ABOUTs");
        $.getJSON('/mach/awg/about', {
        }, function (data) {
            console.log("Data: " + data.message);
            $('div.awgcontent').hide();
            $('div.awgcontent#about').empty();
            $.each(data.message, function(index, value) {
                $('div.awgcontent#about').append($('<h4 style="color: darkblue;"></h4>').text(Number(index+1) + ". " + value.split(": ")[0] + ": ").
                append($('<span style="background-color: darkblue; color: white;"></span>').text(value.split(": ")[1])));
              });
              $('div.awgcontent#about').show();
              $('button.awg').removeClass('selected');
              $('button.awg#about').addClass('selected');
        });
        return false;
    });
}); 

//show setting's page
$(function() {
    $('button.awg#settings').bind('click', function() {
        $('div.awgcontent').hide();
        $('div.awgcontent#settings-main').show(); //first-page of settings
        $('button.awg').removeClass('selected');
        $('button.awg#settings').addClass('selected');
        return false;
    });
});

// main settings
function awgmain () {
    $.getJSON('/mach/awg/settings-main', {
        refclk: $('select.awg[name="refclk"]').val(),
        predist: $('select.awg[name="predist"]').val(),
        outpmode: $('select.awg[name="outpmode"]').val(),
        samprat: $('select.awg[name="samprat"]').val(), 

        active: $('select.awg[name="active"]').val(),
        delay: $('input.awg[name="delay"]').val(),
        pulsew: $('input.awg[name="pulsew"]').val(),
        source: $('select.awg[name="source"]').val()
    },    
    function(data) {
        logdebug(data);
        console.log("setting awg-main: " + data.message);
    }); 
};

// construct IF-wave:
function awgifwave () {
    $.getJSON('/mach/awg/settings-ifwave', {
        ifperiod: $('input.awg#settings[name="ifperiod"]').val(),

        iffunction1: $('select.awg.ch1[name="iffunction"]').val(),
        ifdesign1: $('input.awg.ch1[name="ifdesign"]').val(),
        iffreq1: $('input.awg.ch1[name="iffreq"]').val(),
        ifvoltag1: $('input.awg.ch1[name="ifvoltag"]').val(),
        ifoffset1: $('input.awg.ch1[name="ifoffset"]').val(),
        ifphase1: $('input.awg.ch1[name="ifphase"]').val(),
        ifontime1: $('input.awg.ch1[name="ifontime"]').val(),
        ifscale1: $('input.awg.ch1[name="ifscale"]').val(),
        ifdelay1: $('input.awg.ch1[name="ifdelay"]').val(),
        
        iffunction2: $('select.awg.ch2[name="iffunction"]').val(),
        ifdesign2: $('input.awg.ch2[name="ifdesign"]').val(),
        iffreq2: $('input.awg.ch2[name="iffreq"]').val(),
        ifvoltag2: $('input.awg.ch2[name="ifvoltag"]').val(),
        ifoffset2: $('input.awg.ch2[name="ifoffset"]').val(),
        ifphase2: $('input.awg.ch2[name="ifphase"]').val(),
        ifontime2: $('input.awg.ch2[name="ifontime"]').val(),
        ifscale2: $('input.awg.ch2[name="ifscale"]').val(),
        ifdelay2: $('input.awg.ch2[name="ifdelay"]').val(),

        outputch1: $('select.awg.ch1[name="outputch"]').val(),
        oupfiltr1: $('select.awg.ch1[name="oupfiltr"]').val(),
        oupconfig1: $('select.awg.ch1[name="oupconfig"]').val(),

        outputch2: $('select.awg.ch2[name="outputch"]').val(),
        oupfiltr2: $('select.awg.ch2[name="oupfiltr"]').val(),
        oupconfig2: $('select.awg.ch2[name="oupconfig"]').val()
    }, 
    function(data) {
        logdebug(data);
        console.log("setting awg-ifwave: " + data.message);
        console.log(data.WaveForms);
        awgplot1D(data.t, data.WaveForms[0], data.WaveForms[1], 'time(ns)', 'V(V)');
    }); 
};

// main -> ifwave
$(function () {
    $('input.awg#set-main').bind('click', function () {
        $('div.awgcontent#settings-main').hide();
        $('div.awgcontent#settings-ifwave').show(); }); 
    return false;
});

// Adjust input based on different function type:
$(function () {
    $('select.awg.ch1#settings[name="iffunction"]').on('change', function () {
        $('label.awg.ch1').parent().hide();
        $('input.awg.ch1').parent().hide();
        if ($('select.awg.ch1#settings[name="iffunction"]').val()=="arb") {
            $('label.awg.ch1.arb').parent().show();
            $('input.awg.ch1.arb').parent().show();
        } else if ($('select.awg.ch1#settings[name="iffunction"]').val()=="cos") {
            $('label.awg.ch1.cosin').parent().show();
            $('input.awg.ch1.cosin').parent().show();
        } else if ($('select.awg.ch1#settings[name="iffunction"]').val()=="sin") {
            $('label.awg.ch1.cosin').parent().show();
            $('input.awg.ch1.cosin').parent().show();
        } else if ($('select.awg.ch1#settings[name="iffunction"]').val()=="sqe") {
            $('label.awg.ch1.sqe').parent().show();
            $('input.awg.ch1.sqe').parent().show();
        };
        return false;
    });
});
$(function () {
    $('select.awg.ch2#settings[name="iffunction"]').on('change', function () {
        $('label.awg.ch2').parent().hide();
        $('input.awg.ch2').parent().hide();
        if ($('select.awg.ch2#settings[name="iffunction"]').val()=="arb") {
            $('label.awg.ch2.arb').parent().show();
            $('input.awg.ch2.arb').parent().show();
        } else if ($('select.awg.ch2#settings[name="iffunction"]').val()=="cos") {
            $('label.awg.ch2.cosin').parent().show();
            $('input.awg.ch2.cosin').parent().show();
        } else if ($('select.awg.ch2#settings[name="iffunction"]').val()=="sin") {
            $('label.awg.ch2.cosin').parent().show();
            $('input.awg.ch2.cosin').parent().show();
        } else if ($('select.awg.ch2#settings[name="iffunction"]').val()=="sqe") {
            $('label.awg.ch2.sqe').parent().show();
            $('input.awg.ch2.sqe').parent().show();
        };
        return false;
    });
});

// settings: execution
$(function () {
    $('input.awg#set-main').bind('click', function () {
        console.log("set-up main");
        awgmain(); return false; }); });
$(function () {
    $('input.awg#set-ifwave').bind('click', function () {
        console.log("set-up if-wave");
        awgifwave(); return false; }); });

//reset
$(function () {
    $('button.awg#reset').bind('click', function () { // id become #
        $.getJSON('/mach/awg/reset', {
        }, function (data) {
            if (data.message != 0){
                $('button.awg').removeClass('error');
                $('button.awg#close').removeClass('close');
                $('button.awg#reset').addClass('reset');}
            else {$('button.awg').addClass('error');}
        });
        return false;
    });
}); 

//close
$(function () {
    $('button.awg#close').bind('click', function () { // id become #
        $.getJSON('/mach/awg/close', {
        }, function (data) {
            if (data.message == 0){
                $('button.awg').removeClass('error');
                $('button.awg#reset').removeClass('reset');
                $('button.awg#close').addClass('close');}
            else {$('button.awg').addClass('error');}         
        });
        return false;
    });
}); 

//generate
$(function () {
    $('button.awg#generate').bind('click', function () { // id become #
        $.getJSON('/mach/awg/generate', {
        }, function (data) {
            console.log(data.message);
            if (data.gstatus == 0){
                $('button.awg').removeClass('error');
                $('button.awg#abort').removeClass('abort');
                $('button.awg#generate').addClass('generate');}
            else {$('button.awg').addClass('error');}
        });
        return false;
    });
});

//abort
$(function () {
    $('button.awg#abort').bind('click', function () { // id become #
        $.getJSON('/mach/awg/abort', {
        }, function (data) {
            if (data.message == 0){
                $('button.awg').removeClass('error');
                $('button.awg#generate').removeClass('generate');
                $('button.awg#abort').addClass('abort');}
            else {$('button.awg').addClass('error');}         
        });
        return false;
    });
});