//when page is loading:
$(document).ready(function(){
    $('div.dccontent').hide();
    $('a.dc.ampscan').hide();
});

// show yokogawa's page
$(function() {
    $('button.dc#yokogawa').bind('click', function() {
        window.ykwhich = $('select.dc#yk-which').val();
        window.ykvaunit = $('select.dc#yk-va-unit').val();
        $('div.dccontent').hide();
        $('div.dccontent#yokogawa').show();
        $('button.dc').removeClass('selected');
        $('button.dc#yokogawa').addClass('selected');
        return false;
    });
});
// update yokogawa which
$(function () {
    $('select.dc#yk-which').on('change', function () {
        ykwhich = $('select.dc#yk-which').val();
    });
    return false;
});
// update yokogawa unit
$(function () {
    $('select.dc#yk-va-unit').on('change', function () {
        ykvaunit = $('select.dc#yk-va-unit').val();
        if (ykvaunit == 1) {
            $('input.dc.yokogawa.vaunit').val('A');
            $('input.dc.yokogawa.vasunit').val('A/s');
        } else if (ykvaunit == 0) {
            $('input.dc.yokogawa.vaunit').val('V');
            $('input.dc.yokogawa.vasunit').val('V/s');
        }
    });
    return false;
});
// toggle yokogawa connection
$(function () {
    $('input.dc#init-yokogawa').click(function () { 
        //indicate it is still running:
        $( "i.dc" ).remove(); //clear previous
        $('button.dc#yokogawa[name="init"]').prepend("<i class='dc fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        var yokostat = $('input.dc#init-yokogawa').is(':checked'); //use css to respond to click / touch // toggle ON-OFF connection with yokogawa
        $.getJSON('/mach'+'/dc/yokogawa', {
            yokostat: yokostat, ykvaunit: ykvaunit, ykwhich: ykwhich
        }, function (data) {
            $( "i.dc" ).remove(); //clear previous
            console.log("Previous: " + data.prev);
        });
        // return false; //this would prevent toggle effect!!!
    });
});
// send yokogawa V-Pulse
$(function() {
    $('button.dc.yokogawa#yk-vpulse-send').bind('click', function() {
        $.getJSON('/mach/dc/yokogawa/vpulse', {
            vset: $('input.dc.yokogawa#yk-vpulse').val(),
            pwidth: $('input.dc.yokogawa#yk-vpulse-dur').val()
        }, function(data) {
            console.log("SweepTime: " + data.SweepTime);
        });
        return false;
    });
});
// send yokogawa on-off
$(function() {
    $('button.dc.yokogawa#yk-onoff-send').bind('click', function() {
        $.getJSON('/mach/dc/yokogawa/onoff', {
        }, function(data) {
        });
        return false;
    });
});
// send yokogawa V-Wave
$(function() {
    $('button.dc.yokogawa#yk-vwave-sweep').bind('click', function() {
        $.getJSON('/mach/dc/yokogawa/vwave', {
            vwave: $('input.dc.yokogawa#yk-vwave').val(),
            pwidth: $('input.dc.yokogawa#yk-vwave-dur').val(),
            swprate: $('input.dc.yokogawa#yk-vwave-rate').val(),
        }, function(data) {
            console.log("SweepTime: " + data.SweepTime);
        });
        return false;
    });
});

// show keithley's page
$(function() {
    $('button.dc#keithley').bind('click', function() {
        $('div.dccontent').hide();
        $('div.dccontent.keithley').show();
        $('button.dc').removeClass('selected');
        $('button.dc#keithley').addClass('selected');
        return false;
    });
});
// toggle keithley connection
$(function () {
    $('input.dc#init-keithley').click(function () { 
        //indicate it is still running:
        $( "i.dc" ).remove(); //clear previous
        $('button.dc.keithley[name="init"]').prepend("<i class='dc fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        var keitstat = $('input.dc#init-keithley').is(':checked'); //use css to respond to click / touch
        // toggle ON-OFF connection with keithley
        $.getJSON('/mach'+'/dc/keithley', {
            keitstat: keitstat
        }, function (data) {
            $( "i.dc" ).remove(); //clear previous
            console.log("Previous: " + data.prev);
        });
        // return false;
    });
});
// send keithley V-Pulse
$(function() {
    $('button.dc.keithley[name="vpulse-send"]').bind('click', function() {
        $.getJSON('/mach/dc/keithley/vpulse', {
            vset: $('input.dc.keithley[name="vpulse"]').val(),
            pwidth: $('input.dc.keithley[name="vpulse-dur"]').val()
        }, function(data) {
            console.log("time(s): " + data.t);
            console.log("V(V): " + data.V);
            console.log("I(A): " + data.I);
            // $('p.keit.status').text("Return: " + String(data.I));
            
            let traceL = {x: [], y: [], mode: 'lines', type: 'scatter', 
                name: 'V',
                line: {color: 'rgb(23, 151, 6)', width: 2.5},
                yaxis: 'y' };
            let traceR = {x: [], y: [], mode: 'lines', type: 'scatter', 
                name: 'I',
                line: {color: 'blue', width: 2.5},
                yaxis: 'y2' };

            let layout = {
                legend: {x: 1.08},
                height: $(window).height()*0.8,
                width: $(window).width()*0.7,
                xaxis: {
                    zeroline: false,
                    title: "<b>time(s)</b>",
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
                    title: '<b>I(A)</b>', 
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
                    text: '<b>V(V)</b>',
                    font: {size: 18},
                    showarrow: false,
                    textangle: 0
                  }]
                };
            
            $.each(data.t, function(i, val) {traceL.x.push(val);});
            $.each(data.V, function(i, val) {traceL.y.push(val);});
            $.each(data.t, function(i, val) {traceR.x.push(val);});
            $.each(data.I, function(i, val) {traceR.y.push(val);});

            var Trace = [traceL, traceR]
            Plotly.newPlot('dc-keith-chart', Trace, layout, {showSendToCloud: true});
        });
    });
    return false;
});

    

