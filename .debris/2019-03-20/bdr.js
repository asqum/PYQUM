//when page is loading:
$(document).ready(function(){
    $('div.bdrcontent').hide();
});

//show log's page
$(function () {
    $('button#bdr').bind('click', function () {
        $.getJSON('/mach/bdr/log', {
        }, function (data) {
            $('div.instrlog#bdr').empty();
            $('div.instrlog#bdr').append($('<p style="margin-top:32px;"></p>'));
            $.each(data.log, function(index, value) {
                $('div.instrlog#bdr').append($('<h4 style="color: white;"></h4>').text(index + ": ").
                append($('<span style="color: yellow;"></span>').text(value)));
              });
              $('div.instrlog#bdr').slideToggle('fast');
              $('button#bdr').toggleClass('active');
        });
        return false;
    });
});


//show temperature's page
$(function() {
    $('button.bdr#temperature').bind('click', function() {
        $('div.bdrcontent').hide();
        $('div.bdrcontent#temperature').show();
        $('button.bdr').removeClass('selected');
        $('button.bdr#temperature').addClass('selected');
        return false;
    });
});

//setting on key-press
// $(function () {
//     $('input.bdr#settings').keypress(function(e) {
//         var key = e.which;
//         if (key == 13) { $('input.bdr#settings').trigger('click'); } }); });
$(function () {
    $('input.bdr#submitsettings').bind('click', function () {
         //indicate it is still running:
         $( "i.bdr" ).remove(); //clear previous
         $('button.bdr#display').prepend("<i class='bdr fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        $.getJSON('/mach/bdr/settings', {
            // input value here:
            rnge: $('input.bdr[name="rnge"]').val(),
            scal: $('input.bdr[name="scal"]').val(),
            ofset: $('input.bdr[name="ofset"]').val(),
            rnge2: $('input.bdr[name="rnge2"]').val(),
            scal2: $('input.bdr[name="scal2"]').val(),
            ofset2: $('input.bdr[name="ofset2"]').val(),
            trnge: $('input.bdr[name="trnge"]').val(),
            tdelay: $('input.bdr[name="tdelay"]').val(),
            tscal: $('input.bdr[name="tscal"]').val(),
            avenum: $('input.bdr[name="avenum"]').val()
        }, function (data) {
            $('div.bdrcontent#debug').append($('<h4 style="background-color: lightgreen;"></h4>').text(Date($.now())));
            $.each(data.message, function(index, value) {
                $('div.bdrcontent#debug').append($('<h4 style="color: black;"></h4>').text(Number(index+1) + ". " + value));
              });
            //click on about
            $('button.bdr#display').trigger('click'); //or: .click();
            //update display-button:
            $('button.bdr#about').addClass('newupdate');
            $( "i.bdr" ).remove(); //clear previous
            $('button.bdr#about').prepend("<i class='bdr fa fa-file-text-o faa-ring animated fa-4x' style='font-size:15px;color:blue;'></i> ");
        });
        return false;
    });
});

//autoscale on submit
$('input.bdr#autoscale').bind('click', function () {
    $( "i.bdr" ).remove(); //clear previous
    $('button.bdr#settings').prepend("<i class='bdr fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
    $.getJSON('/mach'+'/bdr/autoscale', {
    }, function (data) {
        $( "i.bdr" ).remove(); //clear previous
        $('input.bdr[name="rnge"]').val(data.yrange);
        $('input.bdr[name="scal"]').val(data.yscale);
        $('input.bdr[name="ofset"]').val(data.yoffset);
        $('input.bdr[name="rnge2"]').val(data.yrange2);
        $('input.bdr[name="scal2"]').val(data.yscale2);
        $('input.bdr[name="ofset2"]').val(data.yoffset2);
        $('input.bdr[name="trnge"]').val(data.trange);
        $('input.bdr[name="tdelay"]').val(data.tdelay);
        $('input.bdr[name="tscal"]').val(data.tscale);
    });
    return false;
});





//show display's page
$(function() {
    $('button.bdr#display').bind('click', function() {
        $('div.bdrcontent').hide();
        $('div.bdrcontent#display').show();
        $('button.bdr').removeClass('selected');
        $('button.bdr#display').addClass('selected');
        //refresh image-cache:
        jQuery('img').each(function(){
            jQuery(this).attr('src',jQuery(this).attr('src')+ '?' + (new Date()).getTime());
            });
        return false;
    });
});

