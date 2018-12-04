//when page is loading:
$(document).ready(function(){
    $('div.dsocontent').hide();
});

//show log's page
$(function () {
    $('button#dso').bind('click', function () {
        $.getJSON('/mach/dso/log', {
        }, function (data) {
            $('div.instrlog#dso').empty();
            $.each(data.log, function(index, value) {
                $('div.instrlog#dso').append($('<h4 style="color: white;"></h4>').text(index + ": ").
                append($('<span style="color: yellow;"></span>').text(value)));
              });
              $('div.instrlog#dso').slideToggle('fast');
              $('button#dso').toggleClass('active');
        });
        return false;
    });
});

//show debug's page
$(function() {
    $('button.dso#debug').bind('click', function() {
        $('div.dsocontent').hide();
        $('div.dsocontent#debug').show();
        $('button.dso').removeClass('selected');
        $('button.dso#debug').addClass('selected');
        return false;
    });
});

//show about's page
$(function () {
    $('button.dso#about').bind('click', function () { // id become #
        $.getJSON('/mach/dso/about', {
        }, function (data) {
            $('div.dsocontent').hide();
            $('div.dsocontent#about').empty();
            $.each(data.message, function(index, value) {
                $('div.dsocontent#about').append($('<h4 style="color: darkblue;"></h4>').text(Number(index+1) + ". " + value.split(": ")[0] + ": ").
                append($('<span style="background-color: darkblue; color: white;"></span>').text(value.split(": ").slice(1))));
              });
              $('div.dsocontent#about').attr('src', '/static/img/dso/DSOwaveform.png');
              $('div.dsocontent#about').show();
              $('button.dso').removeClass('selected');
              $('button.dso#about').addClass('selected');
        });
        return false;
    });
}); 

//show setting's page
$(function() {
    $('button.dso#settings').bind('click', function() {
        $('div.dsocontent').hide();
        $('div.dsocontent#settings').show();
        $('button.dso').removeClass('selected');
        $('button.dso#settings').addClass('selected');
        return false;
    });
});

//setting on key-press
$(function () {
    $('input.dso#settings').keypress(function(e) {
        var key = e.which;
        if (key == 13) { $('input.dso#settings').trigger('click'); } }); });
$(function () {
    $('input.dso#submitsettings').bind('click', function () { // the enter key code
        $.getJSON('/mach/dso/settings', {
            // input value here:
            freq: $('input.dso[name="freq"]').val(),
            powa: $('input.dso[name="powa"]').val(),
            oupt: $('select.dso[name="oupt"]').val()
        }, function (data) {
            $('div.dsocontent#debug').append($('<h4 style="background-color: lightgreen;"></h4>').text(Date($.now())));
            $.each(data.message, function(index, value) {
                $('div.dsocontent#debug').append($('<h4 style="color: black;"></h4>').text(Number(index+1) + ". " + value));
              });
            $('button.dso#about').trigger('click'); //click on about //or: .click();
        });
        return false;
    });
});

//reset
$(function () {
    $('button.dso#reset').bind('click', function () { // id become #
        $.getJSON('/mach/dso/reset', {
        }, function (data) {
            if (data.message == "Success"){
                $('button.dso').removeClass('error');
                $('button.dso#close').removeClass('close');
                $('button.dso#reset').addClass('reset');}
            else {$('button.dso').addClass('error');}
        });
        return false;
    });
}); 

//close
$(function () {
    $('button.dso#close').bind('click', function () { // id become #
        $.getJSON('/mach/dso/close', {
        }, function (data) {
            if (data.message == "Success"){
                $('button.dso').removeClass('error');
                $('button.dso#reset').removeClass('reset');
                $('button.dso#close').addClass('close');}
            else {$('button.dso').addClass('error');}         
        });
        return false;
    });
}); 