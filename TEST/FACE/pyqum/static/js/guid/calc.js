$(document).ready(function(){
    // $('div.calccontent').show();
});

$('input.guid.calc-qfreq-predict').on('change', function () {
    var flux_fraction = $('input.guid.calc-qfreq-predict#guid-calc-flux-fraction').val();
    $.getJSON(guidencrpytonian() + '/guide'+'/calc/qfreq/predict', {
        flux_fraction: flux_fraction,
        flux_offset: $('input.guid.calc-qfreq-predict#guid-calc-flux-offset').val(),
        flux_halfill: $('input.guid.calc-qfreq-predict#guid-calc-flux-halfill').val(),
        MT_frequency: $('input.guid.calc-qfreq-predict#guid-calc-MT-frequency').val(),
    }, function (data) {
        $('#guid-calc-freq-range').text("1/" + flux_fraction + ' flux-period of ' + data.fluxrange + ' will tune Qubit frequency down to ' + data.qfrequency);

    });
    return false;
});
