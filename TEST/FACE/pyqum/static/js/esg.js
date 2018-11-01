//when page is loading:
$(document).ready(function(){
    $('div.esgcontent').hide();
});

//show log's page
$(function () {
    $('button#esg').bind('click', function () {
        $.getJSON('/mach/esg/log', {
        }, function (data) {
            $('div.instrlog#esg').empty();
            $.each(data.log, function(index, value) {
                $('div.instrlog#esg').append($('<h4 style="color: white;"></h4>').text(index + ": ").
                append($('<span style="color: yellow;"></span>').text(value)));
              });
              $('div.instrlog#esg').slideToggle('fast');
              $('button#esg').toggleClass('active');
        });
        return false;
    });
});

//show debug's page
$(function() {
    $('button.esg#debug').bind('click', function() {
        $('div.esgcontent').hide();
        $('div.esgcontent#debug').show();
        $('button.esg').removeClass('selected');
        $('button.esg#debug').addClass('selected');
        return false;
    });
});

//show about's page
$(function () {
    $('button.esg#about').bind('click', function () { // id become #
        $.getJSON('/mach/esg/about', {
        }, function (data) {
            $('div.esgcontent').hide();
            $('div.esgcontent#about').empty();
            $.each(data.message, function(index, value) {
                $('div.esgcontent#about').append($('<h4 style="color: darkblue;"></h4>').text(Number(index+1) + ". " + value.split(": ")[0] + ": ").
                append($('<span style="background-color: darkblue; color: white;"></span>').text(value.split(": ")[1])));
              });
              $('div.esgcontent#about').show();
              $('button.esg').removeClass('selected');
              $('button.esg#about').addClass('selected');
        });
        return false;
    });
}); 

//show setting's page
$(function() {
    $('button.esg#settings').bind('click', function() {
        $('div.esgcontent').hide();
        $('div.esgcontent#settings').show();
        $('button.esg').removeClass('selected');
        $('button.esg#settings').addClass('selected');
        return false;
    });
});

//setting on key-press
$(function () {
    $('input.esg#settings').keypress(function(e) {
        var key = e.which;
        if (key == 13) { $('input.esg#settings').trigger('click'); } }); });
$(function () {
    $('input.esg#submitsettings').bind('click', function () { // the enter key code
        $.getJSON('/mach/esg/settings', {
            // input value here:
            freq: $('input.esg[name="freq"]').val(),
            powa: $('input.esg[name="powa"]').val(),
            oupt: $('select.esg[name="oupt"]').val()
        }, function (data) {
            $('div.esgcontent#debug').append($('<h4 style="background-color: lightgreen;"></h4>').text(Date($.now())));
            $.each(data.message, function(index, value) {
                $('div.esgcontent#debug').append($('<h4 style="color: black;"></h4>').text(Number(index+1) + ". " + value));
              });
            $('button.esg#about').trigger('click'); //click on about //or: .click();
        });
        return false;
    });
});

//reset
$(function () {
    $('button.esg#reset').bind('click', function () { // id become #
        $.getJSON('/mach/esg/reset', {
        }, function (data) {
            if (data.message == "Success"){
                $('button.esg').removeClass('error');
                $('button.esg#close').removeClass('close');
                $('button.esg#reset').addClass('reset');}
            else {$('button.esg').addClass('error');}
        });
        return false;
    });
}); 

//close
$(function () {
    $('button.esg#close').bind('click', function () { // id become #
        $.getJSON('/mach/esg/close', {
        }, function (data) {
            if (data.message == "Success"){
                $('button.esg').removeClass('error');
                $('button.esg#reset').removeClass('reset');
                $('button.esg#close').addClass('close');}
            else {$('button.esg').addClass('error');}         
        });
        return false;
    });
}); 