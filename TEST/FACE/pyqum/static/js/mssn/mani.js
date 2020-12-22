//when page is loading:
$(document).ready(function(){
    $('div.manicontent').hide();

    return false;
});

// RETURN to Sample selection page:
$('input.mani.loaded#sample-name').on('click', function() {
    window.location.href='/auth/user';
    return false;
});


 
