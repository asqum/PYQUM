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
              //$('div.dsocontent#about').append("<a href=#display>image</a>");
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
// $(function () {
//     $('input.dso#settings').keypress(function(e) {
//         var key = e.which;
//         if (key == 13) { $('input.dso#settings').trigger('click'); } }); });
$(function () {
    $('input.dso#submitsettings').bind('click', function () {
         //indicate it is still running:
         $( "i.dso" ).remove(); //clear previous
         $('button.dso#display').prepend("<i class='dso fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        $.getJSON('/mach/dso/settings', {
            // input value here:
            rnge: $('input.dso[name="rnge"]').val(),
            scal: $('input.dso[name="scal"]').val(),
            ofset: $('input.dso[name="ofset"]').val(),
            rnge2: $('input.dso[name="rnge2"]').val(),
            scal2: $('input.dso[name="scal2"]').val(),
            ofset2: $('input.dso[name="ofset2"]').val(),
            trnge: $('input.dso[name="trnge"]').val(),
            tdelay: $('input.dso[name="tdelay"]').val(),
            tscal: $('input.dso[name="tscal"]').val(),
            avenum: $('input.dso[name="avenum"]').val()
        }, function (data) {
            $('div.dsocontent#debug').append($('<h4 style="background-color: lightgreen;"></h4>').text(Date($.now())));
            $.each(data.message, function(index, value) {
                $('div.dsocontent#debug').append($('<h4 style="color: black;"></h4>').text(Number(index+1) + ". " + value));
              });
            //click on about
            $('button.dso#about').trigger('click'); //or: .click();
            //update display-button:
            $('button.dso#display').addClass('newupdate');
            $( "i.dso" ).remove(); //clear previous
            $('button.dso#display').prepend("<i class='dso fa fa-file-photo-o faa-ring animated fa-4x' style='font-size:15px;color:blue;'></i> ");
        });
        return false;
    });
});

//autoscale on submit
$('input.dso#autoscale').bind('click', function () {
    $( "i.dso" ).remove(); //clear previous
    $('button.dso#settings').prepend("<i class='dso fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
    $.getJSON('/mach/dso/autoscale', {
    }, function (data) {
        $( "i.dso" ).remove(); //clear previous
        $('input.dso[name="rnge"]').val(data.yrange);
        $('input.dso[name="scal"]').val(data.yscale);
        $('input.dso[name="ofset"]').val(data.yoffset);
        $('input.dso[name="rnge2"]').val(data.yrange2);
        $('input.dso[name="scal2"]').val(data.yscale2);
        $('input.dso[name="ofset2"]').val(data.yoffset2);
        $('input.dso[name="trnge"]').val(data.trange);
        $('input.dso[name="tdelay"]').val(data.tdelay);
        $('input.dso[name="tscal"]').val(data.tscale);
    });
    return false;
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

//show display's page
$(function() {
    $('button.dso#display').bind('click', function() {
        $('div.dsocontent').hide();
        $('div.dsocontent#display').show();
        $( "i.dso" ).remove();
        $('button.dso').removeClass('selected');
        $('button.dso#display').removeClass('newupdate');
        $('button.dso#display').addClass('selected');
        //refresh image-cache:
        jQuery('img').each(function(){
            jQuery(this).attr('src',jQuery(this).attr('src')+ '?' + (new Date()).getTime());
            });
        return false;
    });
});