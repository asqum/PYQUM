//when page is loading:
$(document).ready(function(){
    // $('div.all.good').hide()
    $('div.all.clock').append($('<h4 style="background-color: lightgreen;"></h4>').text(Date($.now())));
});

//showing good
$(function () {
    $('button#how').click(function () {
        $('div.all.good').toggle("slow"); 
    });
});

//detect option
$(function () {
    $('button.msson#test').click(function () {
        $.getJSON('/mssn'+'/all/test', {
            idea: $('select.msson[name="idea"]').val()
        });
    });
});

//insert option
$(function () {
    $('button.msson#insertopt').click(function () {
        $.getJSON('/mssn'+'/all/insertopt', {}, function(data) {
            $('select.msson').empty();
            $.each(data.x, function(i,v){
                $('select.msson').append($('<option>', {
                    text: v,
                    value: i
                }));
            });
        });
    });
});