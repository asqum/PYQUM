//when page is loading:
$(document).ready(function(){
    console.log("index is ready");
    $('p.posts').empty();
    $.getJSON('/posts', {
    }, function (data) {
        console.log(data.posts);
        $.each(data.posts, function(i,value) {
            $('div.posts').append(
                "<div class='container-post'>" +
                    "<div class='row'>" +
                        "<div class='title'>" + value['title'] + "</div>" +
                    "</div>" +
                    "<div class='row'>" +
                        "<div class='about' id=" + i + ">" +
                            "by " + value['username'] + " on " + value['created'] + 
                        "</div>" +
                    "</div>" +
                    "<div class='row'>" +
                        // "<div class='col-10' id='left'></div>" +
                        "<div class='body' id='b" + i + "'>" + "</div>" +
                    "</div>" +
                "</div>"
            );
            if (data.guserid == value['author_id']) { $('div.about#'+i).append(" <a href='/" + value['id'] + "/update'>[Edit]</a>"); };
            var pbody = value['body'].split('\n');
            $.each(pbody, function(x,prow) {
                $('div.body#b'+i).append("<h6 class='body'>" + prow + "</h6>"); //id must be unique!
            });
            console.log(value['body']);
        });
    });
});