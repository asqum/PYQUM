$(document).ready(function(){
    // $('div.calccontent').show();
    window.fQ_predict_params = {};
    window.fQ = {};
    window.zQ = {};
});

function plot_fQ_modulation(X,Y,xtitle,ytitle,mode='lines',chart_ID='guide-flux-fq-modulation') {
    // Some kind of Multiplots:
    console.log("Number of Traces: " + Object.keys(Y).length);
    
    let Trace = [];
    $.each(Object.keys(Y), function(i, Q_name) {
        Trace.push( {name: Q_name, x: X[Q_name], y: Y[Q_name], mode: mode, type: 'scatter', line: {width: 2.5}, marker: {symbol: 'square-dot', size: 3.7}, yaxis: 'y' } );
    });
    
    let layout = {
        legend: {x: 1.08}, height: $(window).height()*0.8, width: $(window).width()*0.7, title: '',
        xaxis: { zeroline: false, title: xtitle, titlefont: {size: 18}, tickfont: {size: 18}, tickwidth: 3, linewidth: 3 },
        yaxis: { zeroline: false, title: ytitle, titlefont: {size: 18}, tickfont: {size: 18}, tickwidth: 3, linewidth: 3 },
        };

    Plotly.newPlot(chart_ID, Trace, layout, {showSendToCloud: true});
};

// Calculating, plotting & saving on the fly:
$('input.guid.calc-qfreq-predict').on('change', function () {
    console.log("fQ empty: " + jQuery.isEmptyObject(fQ));
    console.log("fQ-keys includes Q1: " + Object.keys(fQ).includes('Q1'));
    var Qubit_name = $('input.guid#guid-calc-qubit-name').val();
    var filling_factor = $('input.guid.calc-qfreq-predict#guid-calc-filling-factor').val();
    var flux_offset = $('input.guid.calc-qfreq-predict#guid-calc-flux-offset').val();
    var flux_halfill = $('input.guid.calc-qfreq-predict#guid-calc-flux-halfill').val();
    var MT_frequency = $('input.guid.calc-qfreq-predict#guid-calc-MT-frequency').val();
    fQ_predict_params[Qubit_name] = { filling_factor: filling_factor, flux_offset: flux_offset, flux_halfill: flux_halfill, MT_frequency: MT_frequency }
    
    $.getJSON(guidencrpytonian() + '/guide'+'/calc/qfreq/predict', {
        Qubit_name: Qubit_name, filling_factor: filling_factor, flux_offset: flux_offset, flux_halfill: flux_halfill, MT_frequency: MT_frequency,
    }, function (data) {
        var lower_flux_point = parseFloat(flux_offset) - parseFloat(data.fluxrange)
        var upper_flux_point = parseFloat(flux_offset) + parseFloat(data.fluxrange)
        $('#guid-calc-freq-range').text("(" + filling_factor + ')*flux-period: ' + parseFloat(data.fluxrange).toFixed(7) + '; (' + 
            lower_flux_point.toFixed(7) + ', ' + upper_flux_point.toFixed(7) + ')' + ' will give ' + parseFloat(data.qfrequency[Qubit_name]).toFixed(3) + ' GHz');
            console.log("Qubit-frequencies: " + data.qfrequency[Qubit_name]);
            zQ[Qubit_name] = data.qzvalue[Qubit_name];
            fQ[Qubit_name] = data.qfrequency[Qubit_name];
            plot_fQ_modulation(zQ,fQ,'<b>filling factor</b>','<b>Predicted Qubit frequency (GHz)</b>');

        // Auto-complete:
        $('input.guid#guid-calc-qubit-name').autocomplete({
            source: Object.keys(fQ)
        });
    });
    return false;
});

// Retrieving parameters for each Qubits:
$('input.guid#guid-calc-qubit-name').on('change', function () {
    // load perimeters if it is already there logged by the qubit-name
    if (Object.keys(fQ_predict_params).includes($(this).val())) {
        console.log(fQ_predict_params[$(this).val()]);
        $('input.guid.calc-qfreq-predict#guid-calc-filling-factor').val(fQ_predict_params[$(this).val()].filling_factor);
        $('input.guid.calc-qfreq-predict#guid-calc-flux-offset').val(fQ_predict_params[$(this).val()].flux_offset);
        $('input.guid.calc-qfreq-predict#guid-calc-flux-halfill').val(fQ_predict_params[$(this).val()].flux_halfill);
        $('input.guid.calc-qfreq-predict#guid-calc-MT-frequency').val(fQ_predict_params[$(this).val()].MT_frequency);
    };

    return false;
});

