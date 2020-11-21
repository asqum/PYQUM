var qsystem = $('select.all.mssn.queue').val();

//when page is loading:
$(document).ready(function(){
    $('div.all.clock').append($('<h4 style="background-color: lightgreen;"></h4>').text(Date($.now())));
    qumqueue();
    qumjob();
});

function qumqueue() {
    // $('button.all-qumuser').hide();
    
    $.getJSON(mssnencrpytonian() + '/mssn'+'/all/queue', {
        queue: qsystem,
    }, function (data) {
        $('h3.all-mssn-news').text("Welcome home, " + data.loginuser);
        console.log("user: " + data.loginuser);
        console.log("QUEUE: " + data.QUEUE);

        window.queuejobid = [];
        // var QUEUE_userlist = [];
        $('table.mssn-QUEUE tbody.all.mssn-queue-update').empty();
        $.each(data.QUEUE, function(i,val){
            queuejobid.push(val.id)
            // QUEUE_userlist.push(val.username);
            if (i==0) { // only the first in line has the data under construction:
                var link = '</td><td><div class="buttons"><a class="all-mssn btn green" id="jid_' + val.id + '">' + "RUNNING " +
                "<i class='fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:green;'></i>" + '</a></div></td>';
            } else {
                var link = '</td><td><button class="all-queue-out push_button w-95 red" id="jid_' + val.id + '_' + qsystem + '">' + 'Q-OUT</button></td>';
            };
            $('table.mssn-QUEUE tbody.all.mssn-queue-update').append('<tr><td>' + val.id + '</td><td>' + val.task + '</td><td>' + val.startime + '</td><td>' + val.samplename +
                                                    '</td><td>' + val.location + '</td><td>' + val.username + '</td><td>' + val.instrument + 
                                                    link + '</tr>');
        });
        // console.log(QUEUE_userlist.indexOf(data.loginuser));
        // if (QUEUE_userlist.indexOf(data.loginuser) === -1 || QUEUE_userlist.length === 0) {
        //     $('div > button.all-qumuser#dive').show();
        // } else {
        //     $('div > button.all-qumuser#yield').show();
        // };
    });
    return false;
};

function qumjob() {
    $( "i.all-mssn-queue.fa-cog" ).remove(); //clear previous
    $('button#all-tab').prepend("<i class='all-mssn-queue fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:green;'></i> ");
    $('button.all-qumuser').hide();
    // console.log('queue: ' + $('select.all.mssn.queue').val());
    $.getJSON(mssnencrpytonian() + '/mssn'+'/all/job', {
        queue: qsystem,
    }, function (data) {
        $('div.row.all-job-by-sample').empty().append('<div class="col-15" id="left"><label class="parameter">ALL JOB WITH SAMPLE: </label></div>' + 
                                                        '<div class="col-10" id="left"><div class="buttons"><a class="all-mssn btn green">' + data.samplename + '</a></div></div>');
        console.log("user: " + data.loginuser);
        console.log("JOB: " + data.joblist);

        $('table.mssn-JOB tbody.all.mssn-job-update').empty();
        $.each(data.joblist, function(i,val) {
            if (queuejobid.indexOf(val.id)===-1) {
                if (parseInt(val.progress)%100===0) {
                    var actionbutton = '</td><td><div class="buttons"><a class="all-mssn btn green" id="jid_' + val.id + '">' + val.progress + '</a></div></td>';
                } else {
                    var actionbutton = '</td><td><div class="buttons"><a class="all-mssn btn orange" id="jid_' + val.id + '">' + val.progress + '</a></div></td>';
                };
                $('table.mssn-JOB tbody.all.mssn-job-update').append('<tr><td>' + val.id + '</td><td>' + val.task + '</td><td>' + val.startime +
                                                    '</td><td>' + val.instrument + actionbutton + '</td><td>' + String(val.comment.replace('\\n',', ')) + '</td>' + '</tr>');
                console.log("Comment: " + val.comment.replace("\\n",", "));
            };
        });
        $( "i.all-mssn-queue.fa-cog" ).remove(); //clear previous
    });
    return false;
};

// When Certain Queue is selected:
$('select.all.mssn.queue').on('change', function() {
    qsystem = $(this).val();
    qumqueue();
    qumjob();
    return false;
});
// When Q-OUT button is pressed: (If the button is inserted after load, then you need to delegate. Below is code to click any button in a cell in the table when the complete table is dynamically inserted)
$(document).on('click', 'table tbody tr td button.all-queue-out', function() { //use this if button is inserted after document has been loaded (dynamic delegation of elements)
    console.log("hello");
    $.getJSON(mssnencrpytonian() + '/mssn'+'/all/queue/out', {
        queue: qsystem, JID: $(this).attr('id').split('_')[1]
    }, function(data) {
        console.log(data.message);
        qumqueue();
        qumjob();
    })
    return false;
});

// Diving in
// $('button.all-qumuser#dive').on('click', function(){
//     $.getJSON(mssnencrpytonian() + '/mssn'+'/all/queue/in', {
//         queue: $('select.all.mssn.queue').val(),
//     }, function (data) {
//         console.log(data.message);
//         qumqueue();
//     });
//     return false;
// });
// Yielding out
// $('button.all-qumuser#yield').on('click', function(){
//     $.getJSON(mssnencrpytonian() + '/mssn'+'/all/queue/out', {
//         queue: $('select.all.mssn.queue').val(),
//     }, function (data) {
//         console.log(data.message);
//         qumqueue();
//     });
//     return false;
// });

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

