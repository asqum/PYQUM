//when page is loading:
$(document).ready(function(){
    $('div.sgcontent').hide();
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

//show about's page
$(function () {
    $('button.sg#about').bind('click', function () { // id become #
        $.getJSON('/mach/sg/about', {
        }, function (data) {
            $('div.sgcontent').hide();
            $('div.sgcontent#about').empty();
            $.each(data.message, function(index, value) {
                $('div.sgcontent#about').append($('<h4 style="color: darkblue;"></h4>').text(Number(index+1) + ". " + value.split(": ")[0] + ": ").
                append($('<span style="background-color: darkblue; color: white;"></span>').text(value.split(": ")[1])));
              });
              $('div.sgcontent#about').show();
              $('button.sg').removeClass('selected');
              $('button.sg#about').addClass('selected');
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
$(function () {
    $('input.sg#submitsettings').bind('click', function () { // the enter key code
        $.getJSON('/mach/sg/settings', {
            // input value here:
            freq: $('input.sg[name="freq"]').val(),
            powa: $('input.sg[name="powa"]').val(),
            oupt: $('select.sg[name="oupt"]').val()
        }, function (data) {
            $('div.sgcontent#debug').append($('<h4 style="background-color: lightgreen;"></h4>').text(Date($.now())));
            $.each(data.message, function(index, value) {
                $('div.sgcontent#debug').append($('<h4 style="color: black;"></h4>').text(Number(index+1) + ". " + value));
              });
            $('button.sg#about').trigger('click'); //click on about //or: .click();
        });
        return false;
    });
});

//reset
$(function () {
    $('button.sg#reset').bind('click', function () { // id become #
        $.getJSON('/mach/sg/reset', {
            // input value here:
            sgtype: $('input.sg[name="sgtype"]').val()
        }, function (data) {
            if (data.message == "Success"){
                $('button.sg').removeClass('error');
                $('button.sg#close').removeClass('close');
                $('button.sg#reset').addClass('reset');}
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
                $('button.sg#reset').removeClass('reset');
                $('button.sg#close').addClass('close');}
            else {$('button.sg').addClass('error');}         
        });
        return false;
    });
}); 