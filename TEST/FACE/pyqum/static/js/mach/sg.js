//when page is loading:
$(document).ready(function(){
    $('div.sgcontent').hide();
    $('div.sgcontent#settings').show();
});

//show debug's page
$(function() {
    $('button.sg#debug').bind('click', function() {
        $('div.sgcontent').hide();
        $('div.sgcontent#debug').show();
        $('button.sg').removeClass('selected');
        $('button.sg#debug').addClass('selected');
        return false;
    });
});

// display log based on sg-model selected
$('select.sg[name="sgtype"]').change( function() {
    $('button.sg#log').trigger('click'); //click on log
});

//show log's page
$(function () {
    $('button.sg#log').bind('click', function () { // id become #
        $.getJSON('/mach/sg/log', {
            sgtype: $('select.sg[name="sgtype"]').val()
        }, function (data) {
            $('div.sgcontent').hide();
            $('div.sgcontent#log').empty();
            console.log(data.log['frequency']);
            $.each(data.log, function(key, value) {
                $('div.sgcontent#log').append($('<h4 style="color: darkblue;"></h4>').text(key + ":\n").
                append($('<span style="background-color: darkblue; color: white;"></span>').text(JSON.stringify(value))));
              });
              $('div.sgcontent#log').show();
              $('button.sg').removeClass('selected');
              $('button.sg#log').addClass('selected');
        });
        return false;
    });
}); 

//show setting's page
$(function() {
    $('button.sg#settings').bind('click', function() {
        $('div.sgcontent').hide();
        $('div.sgcontent#settings').show();
        $('button.sg').removeClass('selected');
        $('button.sg#settings').addClass('selected');
        return false;
    });
});

//setting on key-press
$(function () {
    $('input.sg#settings').keypress(function(e) {
        var key = e.which;
        if (key == 13) { $('input.sg#settings').trigger('click'); } }); }); // the enter key code //trigger next click below?

//update settings
$(function () {
    $('button.sg#update').bind('click', function () { // the enter key code
        $.getJSON('/mach/sg/settings', {
            // input value here:
            freq: $('input.sg[name="freq"]').val(),
            powa: $('input.sg[name="powa"]').val(),
            oupt: $('input.sg[name="oupt"]').is(':checked')?1:0
        }, function (data) {
            console.log($('input.sg[name="oupt"]').is(':checked')?1:0);
            $('div.sgcontent#debug').append($('<h4 style="background-color: lightgreen;"></h4>').text(Date($.now())));
            $.each(data.message, function(index, value) {
                $('div.sgcontent#debug').append($('<h4 style="color: black;"></h4>').text(Number(index+1) + ". " + value));
              });
            
        });
        return false;
    });
});

//connect
$(function () {
    $('button.sg#connect').bind('click', function () { // id become #
        $.getJSON('/mach/sg/connect', {
            // input value here:
            sgtype: $('select.sg[name="sgtype"]').val()
        }, function (data) {
            if (data.message == "Success"){
                $('button.sg').removeClass('error');
                $('button.sg#close').removeClass('close');
                $('button.sg#connect').addClass('connect');}
            else {$('button.sg').addClass('error');}
        });
        return false;
    });
}); 

//close
$(function () {
    $('button.sg#close').bind('click', function () { // id become #
        $.getJSON('/mach/sg/close', {
        }, function (data) {
            if (data.message == "Success"){
                $('button.sg').removeClass('error');
                $('button.sg#connect').removeClass('connect');
                $('button.sg#close').addClass('close');}
            else {$('button.sg').addClass('error');}         
        });
        return false;
    });
}); 