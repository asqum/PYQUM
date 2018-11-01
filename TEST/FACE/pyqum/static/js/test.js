//when page is loading:
$(document).ready(function(){
    $('div.test').append($('<h4 style="background-color: lightgreen;"></h4>').text(Date($.now())));
});