//when page is loading:
$(document).ready(function(){

    if (window.location.pathname == "/dsply/figstatic"){
        console.log(window.location.pathname);
        $('.navbar button').removeClass('active');
        $('.navbar button#static-tab').addClass('active'); 
    };
});

// $(function () {
//     $("button#static-tab").bind('click', function(){
//         window.open("/dsply/figstatic", '_self');
//         return false;
//     });
// });

