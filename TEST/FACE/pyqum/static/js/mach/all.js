//when page is loading:
$(document).ready(function(){
    updatemachlist();
});

function digitalclock(){
    $('div.all.clock').empty();
    $('div.all.clock').append($('<h4 style="background-color: yellow;"></h4>').text(Date($.now())));   
};

function updatemachlist() {
    var statecolor = ['green', 'red'];
    $('table.mach tbody.all.machine-update').empty();
    $.getJSON('/mach/all/machine', { }, function (data) {
        $.each(data.machlist, function(i,val) {
            $('table.mach tbody.all.machine-update').append('<tr></tr>')
                                                    .append('<td>' + val.codename + '</td><td style="background-color: ' + 
                                                    statecolor[parseInt(val.connected)] + ';"> </td><td>' + val.username + 
                                                    '</td><td>' + val.category + '</td><td>' + val.sequence + '</td><td>' + val.system + '</td>');
        });
    });
};


$('button.mach.all.machine-update').click(function() {
    updatemachlist();
    console.log('Machine list updated!');
    return false;
})

