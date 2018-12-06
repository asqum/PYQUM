//when page is loading:
$(document).ready(function(){
    $('div.jobcontent').hide();
});

//show basic's page
$(function() {
    $('button.job#basic').bind('click', function() {
        $('div.jobcontent').hide();
        $('div.jobcontent#basic').show();
        $('button.job').removeClass('selected');
        $('button.job#basic').addClass('selected');
        return false;
    });
});

//basic: squarewave submit
$(function () {
    $('input.job#submitsettings').bind('click', function () {
         //indicate it is still running:
         $( "i.job" ).remove(); //clear previous
         $('button.job#basic').prepend("<i class='job fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:purple;'></i> ");
        $.getJSON('/mach/job/basic', {
            // input value here:
            seg1: $('input.job[name="seg1"]').val(),
            seg2: $('input.job[name="seg2"]').val()
        }, function (data) {
            $( "i.job" ).remove(); //clear previous
        });
        return false;
    });
});