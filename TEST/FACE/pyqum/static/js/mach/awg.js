// Important notes:
// No keypress for security reason

//when page is loading:
$(document).ready(function(){
    $('div.awgcontent').hide();
    $('input.awg.ch1').parent().hide();
    $('input.awg.ch1.cosin').parent().show();
    $('input.awg.ch2').parent().hide();
    $('input.awg.ch2.cosin').parent().show();
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
        console.log("displaying ABOUTs");
        $.getJSON('/mach/awg/about', {
        }, function (data) {
            console.log("Data: " + data.message);
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
        $('div.awgcontent#settings-main').show(); //first-page of settings
        $('button.awg').removeClass('selected');
        $('button.awg#settings').addClass('selected');
        return false;
    });
});

// main settings
function awgmain () {
    $.getJSON('/mach/awg/settings-main', {
        active: $('select.awg[name="active"]').val(),
        delay: $('input.awg[name="delay"]').val(),
        pulsew: $('input.awg[name="pulsew"]').val(),
        source: $('select.awg[name="source"]').val(),
        predist: $('select.awg[name="predist"]').val(),
        outpmode: $('select.awg[name="outpmode"]').val(),
        samprat: $('select.awg[name="samprat"]').val()}, 
    function(data) {
        logdebug(data);
        console.log("setting awg-main: " + data.message);
    }); 
};

// set ifwave
function awgifwave () {
    $.getJSON('/mach/awg/settings-ifwave', {
        iffunction1: $('select.awg.ch1[name="iffunction"]').val(),
        ifdesign1: $('input.awg.ch1[name="ifdesign"]').val(),
        iffreq1: $('input.awg.ch1[name="iffreq"]').val(),
        ifvoltag1: $('input.awg.ch1[name="ifvoltag"]').val(),
        ifoffset1: $('input.awg.ch1[name="ifoffset"]').val(),
        outputch1: $('select.awg.ch1[name="outputch"]').val(),
        oupfiltr1: $('select.awg.ch1[name="oupfiltr"]').val(),
        oupconfig1: $('select.awg.ch1[name="oupconfig"]').val(),
        iffunction2: $('select.awg.ch2[name="iffunction"]').val(),
        ifdesign2: $('input.awg.ch2[name="ifdesign"]').val(),
        iffreq2: $('input.awg.ch2[name="iffreq"]').val(),
        ifvoltag2: $('input.awg.ch2[name="ifvoltag"]').val(),
        ifoffset2: $('input.awg.ch2[name="ifoffset"]').val(),
        outputch2: $('select.awg.ch2[name="outputch"]').val(),
        oupfiltr2: $('select.awg.ch2[name="oupfiltr"]').val(),
        oupconfig2: $('select.awg.ch2[name="oupconfig"]').val()
    }, 
    function(data) {
        logdebug(data);
        console.log("setting awg-ifwave: " + data.message);
        console.log(data.wavefom);
    }); 
};

// main -> ifwave
$(function () {
    $('input.awg#set-main').bind('click', function () {
        $('div.awgcontent#settings-main').hide();
        $('div.awgcontent#settings-ifwave').show(); }); 
    return false;
});

// Adjust input based on different function type:
$(function () {
    $('select.awg.ch1#settings[name="iffunction"]').on('change', function () {
        $('input.awg.ch1').parent().hide();
        if ($('select.awg.ch1#settings[name="iffunction"]').val()=="arb") {
            $('input.awg.ch1.arb').parent().show();
        } else if ($('select.awg.ch1#settings[name="iffunction"]').val()=="cos") {
            $('input.awg.ch1.cosin').parent().show();
        } else if ($('select.awg.ch1#settings[name="iffunction"]').val()=="sin") {
            $('input.awg.ch1.cosin').parent().show();
        };
        return false;
    });
});
$(function () {
    $('select.awg.ch2#settings[name="iffunction"]').on('change', function () {
        $('input.awg.ch2').parent().hide();
        if ($('select.awg.ch2#settings[name="iffunction"]').val()=="arb") {
            $('input.awg.ch2.arb').parent().show();
        } else if ($('select.awg.ch2#settings[name="iffunction"]').val()=="cos") {
            $('input.awg.ch2.cosin').parent().show();
        } else if ($('select.awg.ch2#settings[name="iffunction"]').val()=="sin") {
            $('input.awg.ch2.cosin').parent().show();
        };
        return false;
    });
});

// settings: execution
$(function () {
    $('input.awg#set-main').bind('click', function () {
        console.log("set-up main");
        awgmain(); return false; }); });
$(function () {
    $('input.awg#set-ifwave').bind('click', function () {
        console.log("set-up if-wave");
        awgifwave(); return false; }); });

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
            console.log(data.message);
            if (data.gstatus == 0){
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