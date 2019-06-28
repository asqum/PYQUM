//when page is loading:
$(document).ready(function(){
    console.log("user is ready");
    $('select#sample').empty();
    $('select#sample').append('<option value="-select-">-select-</option>');
    $.getJSON('/auth/user/samples', {
    }, function (data) {
        console.log(data.samples);
        $.each(data.samples, function(i,value) {
            $('select#sample').append('<option value="'+value+'">'+(i+1)+'. '+value+'</option>');
        });
    });
});