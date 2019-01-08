//when page is loading:
$(document).ready(function(){
    $('div.all.good').hide()
    $('div.all.clock').append($('<h4 style="background-color: lightgreen;"></h4>').text(Date($.now())));
});

//showing good
$(function () {
    $('button#how').click(function () {
        $('div.all.good').toggle(); 
    });
});