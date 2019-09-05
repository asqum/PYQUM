//when page is loading:
$(document).ready(function(){
    $('div.vsacontent').hide();
});

//show debug's page
$(function() {
    $('button.vsa#debug').bind('click', function() {
        $('div.vsacontent').hide();
        $('div.vsacontent#debug').show();
        $('button.vsa').removeClass('selected');
        $('button.vsa#debug').addClass('selected');
        return false;
    });
});

//show about's page
$(function () {
    $('button.vsa#about').bind('click', function () { // id become #
        $.getJSON('/mach/vsa/about', {
        }, function (data) {
            $('div.vsacontent').hide();
            $('div.vsacontent#about').empty();
            $.each(data.message, function(index, value) {
                $('div.vsacontent#about').append($('<h4 style="color: darkblue;"></h4>').text(Number(index+1) + ". " + value.split(": ")[0] + ": ").
                append($('<span style="background-color: darkblue; color: white;"></span>').text(value.split(": ")[1])));
              });
              $('div.vsacontent#about').show();
              $('button.vsa').removeClass('selected');
              $('button.vsa#about').addClass('selected');
        });
        return false;
    });
}); 

//show setting's page
$(function() {
    $('button.vsa#settings').bind('click', function() {
        $('div.vsacontent').hide();
        $('div.vsacontent#settings').show();
        $('button.vsa').removeClass('selected');
        $('button.vsa#settings').addClass('selected');
        return false;
    });
});

//setting on key-press
$(function () {
    $('input.vsa#settings').keypress(function(e) {
        var key = e.which;
        if (key == 13) { $('input.vsa#settings').trigger('click'); } }); });
$(function () {
    $('input.vsa#submitsettings').bind('click', function () { // the enter key code
        $.getJSON('/mach/vsa/settings', {
            // input value here:
            acquis: $('input.vsa[name="acquis"]').val(),
            lofreq: $('input.vsa[name="lofreq"]').val(),
            lopowa: $('input.vsa[name="lopowa"]').val(),
            lobwd: $('input.vsa[name="lobwd"]').val(),
            preselect: $('select.vsa[name="preselect"]').val()
        }, function (data) {
            $('div.vsacontent#debug').append($('<h4 style="background-color: lightgreen;"></h4>').text(Date($.now())));
            $.each(data.message, function(index, value) {
                $('div.vsacontent#debug').append($('<h4 style="color: black;"></h4>').text(Number(index+1) + ". " + value));
              });
            $('button.vsa#about').trigger('click'); //click on about //or: .click();
        });
        return false;
    });
});

//reset
$(function () {
    $('button.vsa#reset').bind('click', function () { // id become #
        $.getJSON('/mach/vsa/reset', {
        }, function (data) {
            if (data.message != 0){
                $('button.vsa').removeClass('error');
                $('button.vsa#close').removeClass('close');
                $('button.vsa#reset').addClass('reset');}
            else {$('button.vsa').addClass('error');}
        });
        return false;
    });
}); 

//close
$(function () {
    $('button.vsa#close').bind('click', function () { // id become #
        $.getJSON('/mach/vsa/close', {
        }, function (data) {
            if (data.message == 0){
                $('button.vsa').removeClass('error');
                $('button.vsa#reset').removeClass('reset');
                $('button.vsa#close').addClass('close');}
            else {$('button.vsa').addClass('error');}         
        });
        return false;
    });
}); 

//measure
$(function () {
    $('button.vsa#measure').bind('click', function () { // id become #
        $.getJSON('/mach/vsa/measure', {
        }, function (data) {
            console.log(data.message);
        });
        return false;
    });
});