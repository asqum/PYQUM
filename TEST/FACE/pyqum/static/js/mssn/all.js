function qumqueue() {
    $('button.all-qumuser').hide();
    $.getJSON(mssnencrpytonian() + '/mssn'+'/all/measurequm', {
    }, function (data) {
        console.log(data.loginuser);
        console.log(data.CHAR0_queue);
        var CHAR0_queue_userlist = [];
        $('table.mssn tbody.all.mssn-queue-update').empty();
        $.each(data.CHAR0_queue, function(i,val){
            CHAR0_queue_userlist.push(val.username);
            $('table.mssn tbody.all.mssn-queue-update').append('<tr></tr>')
                                                    .append('<td>' + val.task + '</td><td>' + val.startime + '</td><td>' + val.samplename +
                                                    '</td><td>' + val.location + '</td><td>' + val.username + '</td><td>' + val.instrument + 
                                                    '</td><td><button class="all-char-0 push_button w-95 red">YIELD</button></td>');
        });
        console.log(CHAR0_queue_userlist.indexOf(data.loginuser));
        if (CHAR0_queue_userlist.indexOf(data.loginuser) === -1 || CHAR0_queue_userlist.length === 0) {
            $('div > button.all-qumuser#dive').show();
        } else {
            $('div > button.all-qumuser#yield').show();
        };
    });
    return false;
};


//when page is loading:
$(document).ready(function(){
    $('div.all.clock').append($('<h4 style="background-color: lightgreen;"></h4>').text(Date($.now())));
    qumqueue();
});

// Diving in
$('button.all-qumuser#dive').on('click', function(){
    $.getJSON(mssnencrpytonian() + '/mssn'+'/all/measurequm/in', {
    }, function (data) {
        console.log(data.message);
        qumqueue();
    });
    return false;
});

// Yielding out
$('button.all-qumuser#yield').on('click', function(){
    $.getJSON(mssnencrpytonian() + '/mssn'+'/all/measurequm/out', {
    }, function (data) {
        console.log(data.message);
        qumqueue();
    });
    return false;
});

// Refresh the list with:
// live update
$(function () {
    $('input.all-mssn#live-update').click(function () { 
        var livestat = $('input.all-mssn#live-update').is(':checked'); //use css to respond to click / touch
        if (livestat == true) {
            qumqueue();
            var liveloop = setInterval(qumqueue, 1200);
            $('input.all-mssn#live-update').click(function () {
                clearInterval(liveloop); 
                $( "i.all-mssn" ).remove(); //clear previous
            });
        };
    });
});

