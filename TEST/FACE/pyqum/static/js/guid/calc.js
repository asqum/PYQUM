$(document).ready(function(){
    // $('div.calccontent').show();
});

$('input.guid.calc-qfreq-predict').on('change', function () {
    var flux_fraction = $('input.guid.calc-qfreq-predict#guid-calc-flux-fraction').val();
    var flux_offset = $('input.guid.calc-qfreq-predict#guid-calc-flux-offset').val();
    $.getJSON(guidencrpytonian() + '/guide'+'/calc/qfreq/predict', {
        flux_fraction: flux_fraction,
        flux_offset: flux_offset,
        flux_halfill: $('input.guid.calc-qfreq-predict#guid-calc-flux-halfill').val(),
        MT_frequency: $('input.guid.calc-qfreq-predict#guid-calc-MT-frequency').val(),
    }, function (data) {
        var lower_flux_point = parseFloat(flux_offset) - parseFloat(data.fluxrange)
        var upper_flux_point = parseFloat(flux_offset) + parseFloat(data.fluxrange)
        $('#guid-calc-freq-range').text("(1/" + flux_fraction + ')*flux-period: ' + parseFloat(data.fluxrange).toFixed(7) + '; (' + 
            lower_flux_point.toFixed(7) + ', ' + upper_flux_point.toFixed(7) + ')' + ' will give ' + parseFloat(data.qfrequency).toFixed(3) + ' GHz');

    });
    return false;
});
