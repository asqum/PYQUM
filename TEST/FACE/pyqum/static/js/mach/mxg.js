//when page is loading:
$(document).ready(function(){
    $('div.mxgcontent').hide();
});

//show debug's page
$(function() {
    $('button.mxg#debug').bind('click', function() {
        $('div.mxgcontent').hide();
        $('div.mxgcontent#debug').show();
        $('button.mxg').removeClass('selected');
        $('button.mxg#debug').addClass('selected');
        return false;
    });
});

//show about's page
$(function () {
    $('button.mxg#about').bind('click', function () { // id become #
        $.getJSON('/mach/mxg/about', {
        }, function (data) {
            $('div.mxgcontent').hide();
            $('div.mxgcontent#about').empty();
            $.each(data.message, function(index, value) {
                $('div.mxgcontent#about').append($('<h4 style="color: darkblue;"></h4>').text(Number(index+1) + ". " + value.split(": ")[0] + ": ").
                append($('<span style="background-color: darkblue; color: white;"></span>').text(value.split(": ")[1])));
              });
              $('div.mxgcontent#about').show();
              $('button.mxg').removeClass('selected');
              $('button.mxg#about').addClass('selected');
        });
        return false;
    });
}); 

//show setting's page
$(function() {
    $('button.mxg#settings').bind('click', function() {
        $('div.mxgcontent').hide();
        $('div.mxgcontent#settings').show();
        $('button.mxg').removeClass('selected');
        $('button.mxg#settings').addClass('selected');
        return false;
    });
});

//setting on key-press
$(function () {
    $('input.mxg#settings').keypress(function(e) {
        var key = e.which;
        if (key == 13) { $('input.mxg#settings').trigger('click'); } }); });
$(function () {
    $('input.mxg#submitsettings').bind('click', function () { // the enter key code
        $.getJSON('/mach/mxg/settings', {
            // input value here:
            freq: $('input.mxg[name="freq"]').val(),
            powa: $('input.mxg[name="powa"]').val(),
            oupt: $('select.mxg[name="oupt"]').val()
        }, function (data) {
            $('div.mxgcontent#debug').append($('<h4 style="background-color: lightgreen;"></h4>').text(Date($.now())));
            $.each(data.message, function(index, value) {
                $('div.mxgcontent#debug').append($('<h4 style="color: black;"></h4>').text(Number(index+1) + ". " + value));
              });
            $('button.mxg#about').trigger('click'); //click on about //or: .click();
        });
        return false;
    });
});

//reset
$(function () {
    $('button.mxg#reset').bind('click', function () { // id become #
        $.getJSON('/mach/mxg/reset', {
        }, function (data) {
            if (data.message == "Success"){
                $('button.mxg').removeClass('error');
                $('button.mxg#close').removeClass('close');
                $('button.mxg#reset').addClass('reset');}
            else {$('button.mxg').addClass('error');}
        });
        return false;
    });
}); 

//close
$(function () {
    $('button.mxg#close').bind('click', function () { // id become #
        $.getJSON('/mach/mxg/close', {
        }, function (data) {
            if (data.message == "Success"){
                $('button.mxg').removeClass('error');
                $('button.mxg#reset').removeClass('reset');
                $('button.mxg#close').addClass('close');}
            else {$('button.mxg').addClass('error');}         
        });
        return false;
    });
}); 