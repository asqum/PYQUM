//when page is loading:
$(document).ready(function(){
    $('div.charcontent').hide();
    $.getJSON('/mssn'+'/char/loadusers', {
    }, function (data){
        $('select.char#users').empty().append($('<option>', { text: 'Pick', value: 'pick' }));
        $.each(data.shared_users, function(i,v){ $('select.char#users').append($('<option>', { text: v, value: v })); });
    });
    return false;
});

// pick people from users list:
$('select.char#users').on('change', function () {
    $('div.charcontent').hide();
    var people = $('select.char#users').val();
    $.getJSON('/mssn'+'/char/activeuser', {
        people: people
    }, function (data){
        console.log(data.message);
        console.log("Permission to run: " + data.run_permission);
    });
    return false;
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
    });
    return false;
});

 

    

