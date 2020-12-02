//when page is loading:
$(document).ready(function(){
    $('div.charcontent').hide();

    return false;
});

// RETURN to Sample selection page:
$('input.char.loaded#sample-name').on('click', function() {
    window.location.href='/auth/user';
    return false;
});


// //autoscale on submit (override input defaults)
// $('input.char#autoscale').bind('click', function () {
//     $( "i.char" ).remove(); //clear previous
//     $('button.char#settings').prepend("<i class='char fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
//     $.getJSON('/mssn'+'/char/autoscale', {
//     }, function (data) {
//         $( "i.char" ).remove(); //clear previous
//         $('input.char[name="rnge"]').val(data.yrange);
//         $('input.char[name="scal"]').val(data.yscale);
//         $('input.char[name="ofset"]').val(data.yoffset);
//     });
//     return false;
// });

 
