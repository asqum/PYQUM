var qsystem = $('select.all.mssn.queue').val();
var TASK = {'F_Response': 'fresp', 'CW_Sweep': "cwsweep", 'Single_Qubit': "singleqb"}; //Translation of names between Python and JS

//when page is loading:
$(document).ready(function(){
    $('body.mssn div.tab button.tablinks').hide()
    $('body.mssn div.tab button.tablinks#ALL-tab').show()
    $('body.mssn div.tab button.tablinks#' + qsystem + '-tab').show()
    $('div.all.clock').append($('<h4 style="background-color: lightgreen;"></h4>').text(Date($.now())));
    window.queuejobid = [];

    // Sequencing asynchronous events:
    $.when( qumqueue() ).then(function () { qumjob(); });
    
});

function qumqueue() {
    // $('button.all-qumuser').hide();
    
    $.getJSON(mssnencrpytonian() + '/mssn'+'/all/queue', {
        queue: qsystem,
    }, function (data) {
        $('h3.all-mssn-news').text("Welcome home, " + data.loginuser);
        console.log("user: " + data.loginuser);
        console.log("QUEUE: " + data.QUEUE);
        console.log("User may access active job: " + data.access_active_job); // PENDING: ALSO CHECK IF THERE'S ANY ACTIVE CALIBRATION(S)

        queuejobid.splice(0, queuejobid.length);
        $('table.mssn-QUEUE tbody.all.mssn-queue-update').empty();
        $.each(data.QUEUE, function(i,val){
            queuejobid.push(val.id)
            // QUEUE_userlist.push(val.username);
            if (i==0 && data.access_active_job==true) { // only the first in line has the data under construction:
                var jobidlink = '<div class="buttons"><a class="all-mssn-access btn green" id="jid_' + val.id + '">' + val.id + ' <i class="fa fa-cog fa-spin fa-3x fa-fw" style="font-size:15px;color:green;"></i></a></div>';
                var link = '</td><td><div class="col-100" id="left"><button class="all-queue-out push_button w-95 red" id="jid_' + val.id + '_' + qsystem + '">' + 'STOP</button></div></td>';
            } else {
                var jobidlink = '<div class="buttons"><a class="all-mssn-inspect btn yellow" id="jid_' + val.id + '">' + val.id + ' </a></div>';
                var link = '</td><td><div class="col-100" id="left"><button class="all-queue-out push_button w-95 blue" id="jid_' + val.id + '_' + qsystem + '">' + 'QOUT</button></div></td>';
            };

            var date = new Date(val.startime);
            Startime = date.toLocaleString("en-GB"); // British English uses day-month-year order and 24-hour time without AM/PM
            var comments = new String(val.comment);
            Comments = comments.replaceAll("\\n","; ");
            $('table.mssn-QUEUE tbody.all.mssn-queue-update').append('<tr><td>' + jobidlink + '</td><td>' + val.task + '</td><td>' + Startime + 
                                                    '</td><td>' + val.username + '</td><td>' + val.instrument + '</td><td>' + Comments +  
                                                    link + '</tr>');
        });
    });
    return false;
};
function qumjob() {
    $( "i.all-mssn-queue.fa-cog" ).remove(); //clear previous
    $('button#ALL-tab').prepend("<i class='all-mssn-queue fa fa-cog fa-spin fa-3x fa-fw' style='font-size:15px;color:green;'></i> ");
    $('button.all-qumuser').hide();
    // console.log('queue: ' + $('select.all.mssn.queue').val());
    $.getJSON(mssnencrpytonian() + '/mssn'+'/all/job', {
        queue: qsystem,
    }, function (data) {
        $('div.row.all-job-by-sample').empty().append('<div class="col-20" id="left"><label class="parameter">' + data.update_count + '/' + data.Job_count + '/' + data.maxlist + ' JOB(s) WITH SAMPLE: </label></div>' + 
                                                        '<div class="col-20" id="left"><div class="buttons"><a class="all-mssn btn green">' + data.samplename + '</a></div></div>');
        console.log("user: " + data.loginuser);

        // BUILDING TABLE:
        var day_index = 0; 
        if (typeof data.joblist[0] == "undefined") { var prev_day = ""; } else { var prev_day = data.joblist[0]['dateday']; };
        $('table.mssn-JOB tbody.all.mssn-job-update').empty();
        $.each(data.joblist, function(i,val) {
            // excluding queued job(s):
            if (queuejobid.indexOf(val.id)===-1) {

                // progress segregation:
                if (parseInt(val.progress)===100) {
                    var actionbutton = '</td><td><div class="buttons"><a class="all-mssn-progress btn green" id="jid_' + val.id + '">' + val.progress + '</a></div>';
                } else if (parseInt(val.progress)===0) {
                    var actionbutton = '</td><td><div class="buttons"><a class="all-mssn-progress btn red" id="jid_' + val.id + '">' + val.progress + '</a></div>';
                } else if (val.tag!='') {
                    var actionbutton = '</td><td><div class="buttons"><a class="all-mssn-progress btn blue" id="jid_' + val.id + '">' + val.tag + ': ' + parseInt(val.progress) + '</a></div>';
                } else {
                    var actionbutton = '</td><td><div class="buttons"><a class="all-mssn-progress btn orange" id="jid_' + val.id + '">' + val.progress + '</a></div>';
                };

                // data-status segregation:
                if (val.dateday==null) {
                    var datastatus = '<div class="buttons"><a class="all-mssn-requeue btn red" id="jid_' + val.id + '">' + 'REQUEUE' + '</a></div>';
                } else {
                    var datastatus = '<div class="buttons"><a class="all-mssn-access btn blue" id="jid_' + val.id + '" value="abc">' + 'ACCESS' + '</a></div>';
                };

                // Convert timestamp to local time:
                var date = new Date(val.startime);
                Startime = date.toLocaleString("en-GB"); // British English uses day-month-year order and 24-hour time without AM/PM
                // Startime = date.getDate() + "/" + (date.getMonth() + 1) + "/" + date.getFullYear() + " " + date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds();
                
                // Showing COMMENT or NOTE:
                if ($('table.mssn-JOB tr th select.all_comment_note').val()=='Comment') {
                    var Comment_Note = new String(val.comment).replaceAll("\\n", "; ");
                } else if ($('table.mssn-JOB tr th select.all_comment_note').val()=='Note') {
                    if (val.note==null) { var Comment_Note = "";
                    } else { var Comment_Note = new String(val.note); };
                };

                // Alternate row-background-color with each days:
                if (val.dateday!=prev_day) {
                    prev_day = val.dateday;
                    day_index = day_index + 1;
                };
                if (day_index%2) { alt_BG = ' style="background-color: #f3f3f3;"' }
                else { alt_BG = ' style="background-color: #dddddd;"' };
                // console.log(val.id + ". " + val.dateday + " [" + day_index + "]");

                // Filling the rows:
                $('table.mssn-JOB tbody.all.mssn-job-update').append('<tr' + alt_BG + '><td>' + val.id + '</td><td>' + datastatus + '</td><td>' + val.task + '</td><td>' + Startime +
                '</td><td>' + val.username + '</td><td>' + val.instrument + actionbutton + '</td><td>' + Comment_Note + '</td>' + '</tr>');
                // console.log("Comment: " + val.comment.replace(/(\r\n|\n|\r)/gm,", "));
            };
        });
        $( "i.all-mssn-queue.fa-cog" ).remove(); //clear previous
    });
    return false;
};

// When ALL tab is clicked upon:
$('button.tablinks#ALL-tab').click( function () {
    // setTimeout(() => {qumqueue();}, 371); qumjob();
    $.when( qumqueue() ).done(function () { qumjob(); });
    return false;
});
// When Certain Queue is selected:
$('select.all.mssn.queue').on('change', function() {
    qsystem = $(this).val();
    $('body.mssn div.tab button.tablinks').hide()
    $('body.mssn div.tab button.tablinks#ALL-tab').show()
    $('body.mssn div.tab button.tablinks#' + qsystem + '-tab').show()
    // setTimeout(() => {qumqueue();}, 137); qumjob();
    $.when( qumqueue() ).done(function () { qumjob(); });
    return false;
});
// When STOP / Q-OUT button is pressed inside Q-TABLE: 
// (If the button is inserted after load, then you need to delegate. Below is code to click any button in a cell in the table when the complete table is dynamically inserted)
$(document).on('click', 'table tbody tr td button.all-queue-out', function() { //use this if button is inserted after document has been loaded (dynamic delegation of elements)
    // console.log("hello");
    $.getJSON(mssnencrpytonian() + '/mssn'+'/all/queue/out', {
        queue: qsystem, JID: $(this).attr('id').split('_')[1]
    }, function(data) {
        console.log(data.message);
        $('h3.all-mssn-warning').text("Queue has change: " + data.message);
        // qumqueue(); qumjob();
        $.when( qumqueue() ).done(function () { qumjob(); });
    })
    return false;
});
// IF ACCESS button is pressed inside JOB-TABLE (or currently active JOB inside QUEUE-TABLE):
$(document).on('click', 'div.buttons a.all-mssn-access', function() {
    var jobid = $(this).attr('id').split('_')[1];
    console.log('jobid: ' + jobid);
    $.getJSON(mssnencrpytonian() + '/mssn'+'/all/access/job', {
        jobid: jobid
    }, function(data) {
        console.log('task: ' + TASK[data.tdmpack.task] + ', day: ' + data.tdmpack.dateday + ', moment: ' + data.tdmpack.wmoment + ', queue: ' + data.tdmpack.queue);
        // Click on MSSN-TAB:
        $('.mssn button.tablinks').removeClass('active');
        $('.mssn button.tablinks#' + data.tdmpack.queue + '-tab').addClass('active');
        $('.mssn div.tabcontent').hide();
        $('.mssn div.tabcontent#' + data.tdmpack.queue.replace(/\d+/g, '')).show(); // remove any digits from the string
        // Click on TASK-TAB:
        $('button.access.' + TASK[data.tdmpack.task]).click();
        // Posting Notification:
        $('input.' + TASK[data.tdmpack.task] + '.notification').show().val('JOB #' + jobid + ' > ' + data.tdmpack.dateday + ' > ' + data.tdmpack.wmoment);
        // // Clicking on it:
        // $('input.' + TASK[data.tdmpack.task] + '.notification').trigger('click'); PENDING: Hearing the list-day EVENT before clicking!
    });
    return false;
});
// IF REQUEUE button is pressed inside JOB-TABLE:
$(document).on('click', 'table tbody tr td div.buttons a.all-mssn-requeue', function() {
    var jobid = $(this).attr('id').split('_')[1];
    console.log('jobid: ' + jobid);
    $('button.tablinks#ALL-tab').trigger('click');
    $.getJSON(mssnencrpytonian() + '/mssn'+'/all/requeue/job', {
        jobid: jobid
    }, function(data){
        $('h3.all-mssn-warning').text("Clearance: " + data.clearance + "; Perimeter: " + data.requeue.perimeter);
    });
    return false;
});
// Revert between COMMENT and NOTE:
$(document).on('change', 'table.mssn-JOB tr th select.all_comment_note', function() {
    qumjob();
});
// TO SIMPLE-INSPECT PARAMETER & PERIMETER OF JOB IN QUEUE: (PENDING)
$(document).on('click', 'table tbody tr td div.buttons a.all-mssn-inspect.yellow', function() {
    $('h3.all-mssn-warning').text("CHECK IF YOUR CURRENTLY ACCESSED SAMPLE IS ACTIVE OR THERE IS SOME ACTIVE CALIBRATION(S) GOING ON");
    var jobid = $(this).attr('id').split('_')[1];
    console.log('jobid: ' + jobid);
    $.getJSON(mssnencrpytonian() + '/mssn'+'/all/inspect/job', {

    }, function(data) {
        // ONLY DISPLAY DIRECTLY FROM JOB-TABLE W/O ACCESSING INTO STORED DATA


    });
    return false;
});
// IF UNFINISHED JOB PROGRESS IS CLICK: (Providing Options to dismiss it / close the case)
$(document).on('click', 'table tbody tr td div.buttons a.all-mssn-progress.orange', function() {
    var progressing = parseFloat($(this).text());
    var progress_box = '<div class="buttons"><a class="all-mssn-progress btn orange" id="' + $(this).attr('id') + '">' + progressing + '</a></div>';
    var action = '<div class="buttons"><a class="all-mssn-close btn red" id="' + $(this).attr('id') + '">' + "CLOSE" + '</a></div>';
    $(this).parent().parent().empty().append(progress_box + action);
    return false;
});
// IF CLOSE BUTTON IS CLICK:
$(document).on('click', 'table tbody tr td div.buttons a.all-mssn-close.red', function() {
    $(this).remove();
    var jobid = $(this).attr('id').split('_')[1];
    $.getJSON(mssnencrpytonian() + '/mssn'+'/all/close/job', {
        jobid: jobid, tag: "STOPPED"
    }, function(data) {
        console.log(data.message);
        $('a.all-mssn-progress.orange#jid_'+jobid).removeClass('orange').addClass('rred').text('Press F5');
    });
    return false;
});
// IF TAGGED JOB PROGRESS IS CLICK: (Providing Options to recover it / reopen the case)
$(document).on('click', 'table tbody tr td div.buttons a.all-mssn-progress.blue', function() {
    var tag = $(this).text();
    var progress_box = '<div class="buttons"><a class="all-mssn-progress btn blue" id="' + $(this).attr('id') + '">' + tag + '</a></div>';
    var action = '<div class="buttons"><a class="all-mssn-reopen btn green" id="' + $(this).attr('id') + '">' + "REOPEN" + '</a></div>';
    $(this).parent().parent().empty().append(progress_box + action);
    return false;
});
// IF REOPEN BUTTON IS CLICK:
$(document).on('click', 'table tbody tr td div.buttons a.all-mssn-reopen.green', function() {
    $(this).remove();
    var jobid = $(this).attr('id').split('_')[1];
    $.getJSON(mssnencrpytonian() + '/mssn'+'/all/reopen/job', {
        jobid: jobid
    }, function(data) {
        console.log(data.message);
        $('a.all-mssn-progress.blue#jid_'+jobid).removeClass('blue').addClass('rred').text('Press F5');
    });
    return false;
});





