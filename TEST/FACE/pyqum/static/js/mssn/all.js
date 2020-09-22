function qumqueue() {
    $('p.all-qumuser#list').empty();
    $('button.all-qumuser').hide();
    $.getJSON(mssnencrpytonian() + '/mssn'+'/all/measurequm', {
    }, function (data) {
        console.log(data.loginuser);
        console.log(data.CHAR0_queue);
        console.log(data.CHAR0_queue.indexOf(data.loginuser));
        if (data.CHAR0_queue.indexOf(data.loginuser) === -1 || data.CHAR0_queue.length === 0) {
            $('div > button.all-qumuser#dive').show();
        } else {
            $('div > button.all-qumuser#yield').show();
        };
        $.each(data.CHAR0_queue, function(i,v){
            console.log('i: ' + i + ', v: ' + v);
            $('p.all-qumuser#list').append("<h3 class='body'>" + v + "</h3>");
        });
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

