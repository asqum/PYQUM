//when page is loading:
$(document).ready(function(){
    console.log("index is ready");
    $('p.activities').empty();
    $.getJSON('/activities', {
    }, function (data) {
        console.log(data.activities);
        $.each(data.activities, function(i,value) {
            $('div.activities').append(
                "<div class='container-activity'>" +
                    "<div class='row'>" +
                        // "<div class='col-10' id='left'></div>" +
                        "<div class='body' id='b" + i + "'>" + "</div>" +
                    "</div>" +
                "</div>"
            );

            // Convert timestamp to local time:
            var date = new Date(value['startime']);
            Startime = date.toLocaleString("en-GB"); // British English uses day-month-year order and 24-hour time without AM/PM
            $('div.body#b'+i).append("<h7 class='body' style='color: blue;'>" + Startime + ": " + value['username'] +" " + value['log'] + "</h7>"); //id must be unique!
            
            console.log(value['log']);
        });
    });
});