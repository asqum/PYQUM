//when page is loading:
$(document).ready(function(){
    console.log("user is ready"); 
});

// Registration
$('input.user.profile.data-indexing').on('click', function(e) {
    e.preventDefault();
    $('div.profile#usr_index_status').empty().text("Indexing user database...")
    $.getJSON('/auth/user/data_indexing', {

    }, function(data) {
        $('div.profile#usr_index_status').empty().text(data.usr_name + "'s database has been indexed accordingly");
    });
});

