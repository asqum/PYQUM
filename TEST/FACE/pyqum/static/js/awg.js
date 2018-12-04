//when page is loading:
$(document).ready(function(){
    $('div.awgcontent').hide();
});

//show log's page
$(function () {
    $('button#awg').bind('click', function () {
        $.getJSON('/mach/awg/log', {
        }, function (data) {
            $('div.instrlog#awg').empty();
            $.each(data.log, function(index, value) {
                $('div.instrlog#awg').append($('<h4 style="color: white;"></h4>').text(index + ": ").
                append($('<span style="color: yellow;"></span>').text(value)));
              });
              $('div.instrlog#awg').slideToggle('fast');
              $('button#awg').toggleClass('active');
        });
        return false;
    });
});

//show debug's page
$(function() {
    $('button.awg#debug').bind('click', function() {
        $('div.awgcontent').hide();
        $('div.awgcontent#debug').show();
        $('button.awg').removeClass('selected');
        $('button.awg#debug').addClass('selected');
        return false;
    });
});

//show about's page
$(function () {
    $('button.awg#about').bind('click', function () { // id become #
        $.getJSON('/mach/awg/about', {
        }, function (data) {
            $('div.awgcontent').hide();
            $('div.awgcontent#about').empty();
            $.each(data.message, function(index, value) {
                $('div.awgcontent#about').append($('<h4 style="color: darkblue;"></h4>').text(Number(index+1) + ". " + value.split(": ")[0] + ": ").
                append($('<span style="background-color: darkblue; color: white;"></span>').text(value.split(": ")[1])));
              });
              $('div.awgcontent#about').show();
              $('button.awg').removeClass('selected');
              $('button.awg#about').addClass('selected');
        });
        return false;
    });
}); 

//show setting's page
$(function() {
    $('button.awg#settings').bind('click', function() {
        $('div.awgcontent').hide();
        $('div.awgcontent#settings').show();
        $('button.awg').removeClass('selected');
        $('button.awg#settings').addClass('selected');
        return false;
    });
});

//settings (keypress) -> about
$(function () {
    $('input.awg#settings').keypress(function(e) {
        var key = e.which;
        if (key == 13) { $('input.awg#settings').trigger('click'); } }); });
$(function () {
    $('input.awg#submitsettings').bind('click', function () { // the enter key code
        $.getJSON('/mach/awg/settings', {
            // input value here:
            active: $('select.awg[name="active"]').val(),
            delay: $('input.awg[name="delay"]').val(),
            pulsew: $('input.awg[name="pulsew"]').val(),
            source: $('select.awg[name="source"]').val(),
            predist: $('select.awg[name="predist"]').val()
        }, function (data) {
            $('div.awgcontent#debug').append($('<h4 style="background-color: lightgreen;"></h4>').text(Date($.now())));
            $.each(data.message, function(index, value) {
                $('div.awgcontent#debug').append($('<h4 style="color: black;"></h4>').text(Number(index+1) + ". " + value));
              });
            $('button.awg#about').trigger('click'); //click on about //or: .click();
        });
        return false;
    });
});

//reset
$(function () {
    $('button.awg#reset').bind('click', function () { // id become #
        $.getJSON('/mach/awg/reset', {
        }, function (data) {
            if (data.message != 0){
                $('button.awg').removeClass('error');
                $('button.awg#close').removeClass('close');
                $('button.awg#reset').addClass('reset');}
            else {$('button.awg').addClass('error');}
        });
        return false;
    });
}); 

//close
$(function () {
    $('button.awg#close').bind('click', function () { // id become #
        $.getJSON('/mach/awg/close', {
        }, function (data) {
            if (data.message == 0){
                $('button.awg').removeClass('error');
                $('button.awg#reset').removeClass('reset');
                $('button.awg#close').addClass('close');}
            else {$('button.awg').addClass('error');}         
        });
        return false;
    });
}); 