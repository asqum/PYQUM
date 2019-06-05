// Important notes:
// No keypress for security reason

//when page is loading:
$(document).ready(function(){
    $('div.awgcontent').hide();
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

// log debug
function logdebug (data) {
    if ($(".dh4").parent().hasClass("container")) {$(".dh4").unwrap();}
    $('div.awgcontent#debug').append($('<h4 class="dh4" style="background-color: lightgreen;"></h4>')
    .text(Date($.now())));
    $.each(data.message, function(index, value) {
        $('div.awgcontent#debug').append($('<h4 class="dh4" style="color: black;"></h4>')
        .text(Number(index+1) + ". " + value));});
    $(".dh4").wrapAll("<div class='container'></div>");
    // $('button.awg#about').trigger('click'); //or: .click();
    console.log("logging debug status");
}

//show about's page (directly inquire from instrument)
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
        $('div.awgcontent#settings-marker').show(); //first-page of settings
        $('button.awg').removeClass('selected');
        $('button.awg#settings').addClass('selected');
        return false;
    });
});

// set marker
function awgmarker () {
    $.getJSON('/mach/awg/settings-marker', {
        active: $('select.awg[name="active"]').val(),
        delay: $('input.awg[name="delay"]').val(),
        pulsew: $('input.awg[name="pulsew"]').val(),
        source: $('select.awg[name="source"]').val()}, 
    function(data) {logdebug(data);}); 
        console.log("setting awg-marker!");
}
         
// set prepare
function awgprepare () {
    $.getJSON('/mach/awg/settings-prepare', {
        predist: $('select.awg[name="predist"]').val(),
        outpmode: $('select.awg[name="outpmode"]').val(),
        samprat: $('select.awg[name="samprat"]').val()}, 
    function(data) {logdebug(data);}); 
        console.log("setting awg-prepare!");
}

// set squarewave
function awgsquarewave () {
    $.getJSON('/mach/awg/settings-squarewave', {
        voltag1: $('input.awg[name="voltag1"]').val(),
        pointnum1: $('input.awg[name="pointnum1"]').val(),
        voltag2: $('input.awg[name="voltag2"]').val(),
        pointnum2: $('input.awg[name="pointnum2"]').val()}, 
    function(data) {logdebug(data);
        console.log("setting awg-squarewave");
    }); 
}

// set channel
function awgchannel () {
    $.getJSON('/mach/awg/settings-channel', {
        channel: $('select.awg[name="channel"]').val(),
        outputch: $('select.awg[name="outputch"]').val(),
        oupfiltr: $('select.awg[name="oupfiltr"]').val()}, 
    function(data) {logdebug(data);}); 
        console.log("setting awg-channel!");
}

//settings' forward sequences
$(function () {
    $('input.awg#set-marker').bind('click', function () {
        $('div.awgcontent#settings-marker').hide();
        $('div.awgcontent#settings-prepare').show(); }); });
$(function () {
    $('input.awg#set-prepare').bind('click', function () {
        $('div.awgcontent#settings-prepare').hide();
        $('div.awgcontent#settings-squarewave').show(); }); });
//settings' backward sequences
$(function () {
    $('input.awg#bato-marker').bind('click', function () {
        $('div.awgcontent#settings-prepare').hide();
        $('div.awgcontent#settings-marker').show(); }); });
$(function () {
    $('input.awg#bato-prepare').bind('click', function () {
        $('div.awgcontent#settings-squarewave').hide();
        $('div.awgcontent#settings-prepare').show(); }); });
//settings:  looping squarewave <-> channel
$(function () {
    $('input.awg#set-squarewave').bind('click', function () {
        $('div.awgcontent#settings-squarewave').hide();
        $('div.awgcontent#settings-channel').show(); }); });
$(function () {
    $('input.awg#set-channel').bind('click', function () {
        $('div.awgcontent#settings-channel').hide();
        $('div.awgcontent#settings-squarewave').show(); }); });

// settings: execution
$(function () {
    $('input.awg#set-marker').bind('click', function () {
        console.log("set-up marker");
        awgmarker(); return false; }); });
$(function () {
    $('input.awg#set-prepare').bind('click', function () {
        console.log("set-up prepare");
        awgprepare(); return false; }); });
$(function () {
    $('input.awg#set-squarewave').bind('click', function () {
        console.log("set-up square-wave");
        awgsquarewave(); return false; }); });
$(function () {
    $('input.awg#set-channel').bind('click', function () {
        console.log("set-up channels");
        awgchannel(); return false; }); });

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

//generate
$(function () {
    $('button.awg#generate').bind('click', function () { // id become #
        $.getJSON('/mach/awg/generate', {
        }, function (data) {
            if (data.message == 0){
                $('button.awg').removeClass('error');
                $('button.awg#abort').removeClass('abort');
                $('button.awg#generate').addClass('generate');}
            else {$('button.awg').addClass('error');}
        });
        return false;
    });
});

//abort
$(function () {
    $('button.awg#abort').bind('click', function () { // id become #
        $.getJSON('/mach/awg/abort', {
        }, function (data) {
            if (data.message == 0){
                $('button.awg').removeClass('error');
                $('button.awg#generate').removeClass('generate');
                $('button.awg#abort').addClass('abort');}
            else {$('button.awg').addClass('error');}         
        });
        return false;
    });
});