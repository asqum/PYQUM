//when page is loading:
$(document).ready(function(){
    $('div.charcontent').hide();
});








//autoscale on submit (override input defaults)
$('input.char#autoscale').bind('click', function () {
    $( "i.char" ).remove(); //clear previous
    $('button.char#settings').prepend("<i class='char fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
    $.getJSON('/mssn'+'/char/autoscale', {
    }, function (data) {
        $( "i.char" ).remove(); //clear previous
        $('input.char[name="rnge"]').val(data.yrange);
        $('input.char[name="scal"]').val(data.yscale);
        $('input.char[name="ofset"]').val(data.yoffset);
        $('input.char[name="rnge2"]').val(data.yrange2);
        $('input.char[name="scal2"]').val(data.yscale2);
        $('input.char[name="ofset2"]').val(data.yoffset2);
        $('input.char[name="trnge"]').val(data.trange);
        $('input.char[name="tdelay"]').val(data.tdelay);
        $('input.char[name="tscal"]').val(data.tscale);
    });
    return false;
});

 

    

