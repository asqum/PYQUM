// Important notes:
// No keypress for security reason

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
            $('div.instrlog#awg').append($('<p style="margin-top:32px;"></p>'));
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

// log debug
function logdebug (data) {
    if ($(".dh4").parent().hasClass("container")) {$(".dh4").unwrap();}
    $('div.awgcontent#debug').append($('<h4 class="dh4" style="background-color: lightgreen;"></h4>')
    .text(Date($.now())));
    $.each(data.message, function(index, value) {
        $('div.awgcontent#debug').append($('<h4 class="dh4" style="color: black;"></h4>')
        .text(Number(index+1) + ". " + value));});
    $(".dh4").wrapAll("<div class='container'></div>");
    $('button.awg#about').trigger('click'); //or: .click();
    console.log("logging debug status");
}

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
$(function () {
    $('input.awg#set-marker').bind('click', function () {
        awgmarker();
        return false; }); }); 
         
// set prepare
function awgprepare () {
    $.getJSON('/mach/awg/settings-prepare', {
        predist: $('select.awg[name="predist"]').val(),
        outpmode: $('select.awg[name="outpmode"]').val(),
        samprat: $('select.awg[name="samprat"]').val()}, 
    function(data) {logdebug(data);}); 
    console.log("setting awg-prepare!");
}

//settings-marker to settings-prepare
$(function () {
    $('input.awg#goto-prepare').bind('click', function () {
        $('div.awgcontent#settings-marker').hide();
        $('div.awgcontent#settings-prepare').show(); }); });
//settings-prepare to settings-marker
$(function () {
    $('input.awg#bato-marker').bind('click', function () {
        $('div.awgcontent#settings-prepare').hide();
        $('div.awgcontent#settings-marker').show(); }); });
   
// submit it all (finish-all)
$(function () {
    $('input.awg#submit-all').bind('click', function () {
        console.log("click submit all");
        awgmarker();
        awgprepare();
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