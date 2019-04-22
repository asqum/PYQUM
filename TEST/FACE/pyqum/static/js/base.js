$(document).ready(function(){
    // console if only for debugging purposes:
    // console.log($(location).attr("href"));
    // console.log(window.location.pathname);

    if (window.location.pathname == "/"){
        $('.navbar button').removeClass('active');
        $('.navbar button.home').addClass('active'); 
    };
              
    if (window.location.pathname == "/mach"){
        console.log(window.location.pathname); 
    };    
    
    if (window.location.pathname == "/mssn"){
        console.log(window.location.pathname);
    };

    if (window.location.pathname == "/script"){
        $('.navbar button').removeClass('active');
        $('.navbar button.bridge').addClass('active'); 
    };

    if (window.location.pathname == "/gd/guide"){
        $('.navbar button').removeClass('active');
        $('.navbar button.guide').addClass('active'); 
    };

    if (window.location.pathname == "/figstatic"){
        $('.navbar button').removeClass('active');
        $('.navbar button.display').addClass('active'); 
    };

    if (window.location.pathname == "/auth/register"){
        $('.navbar button').removeClass('active');
        $('.navbar button.reg').addClass('active'); 
    };

    if (window.location.pathname == "/auth/login"){
        $('.navbar button').removeClass('active');
        $('.navbar button.login').addClass('active'); 
    };
 
    if (window.location.pathname == "/auth/user"){
        $('.navbar button').removeClass('active');
        $('.navbar button.user').addClass('active'); 
    };

});

$(function () {
    $("button.home").bind('click', function(){
        window.open("/", '_self');  
        return false;
    });
});

$(function () {
    $("button.machine").bind('click', function(){
        window.open("/mach", '_self');   
        return false;
    });
});

$(function () {
    $("button.mission").bind('click', function(){
        window.open("/mssn", '_self');    
        return false;
    });
});

$(function () {
    $("button.bridge").bind('click', function(){
        window.open("/script", '_self');   
        return false;
    });
});

$(function () {
    $("button.guide").bind('click', function(){
        window.open("/gd/guide", '_self');    
        return false;
    });
});

$(function () {
    $("button.display").bind('click', function(){
        window.open("/display", '_self');
        return false;
    });
});

$(function () {
    $("button.reg").bind('click', function(){
        window.open("/auth/register", '_self');
        return false;
    });
});

$(function () {
    $("button.login").bind('click', function(){
        window.open("/auth/login", '_self');
        return false;
    });
});

$(function () {
    $("button.logout").bind('click', function(){
        window.open("/auth/logout", '_self');
        return false;
    });
});

$(function () {
    $("button.user").bind('click', function(){
        window.open("/auth/user", '_self');
        return false;
    });
});

// reset caches on-click
$(function () {
    $('button.reset').bind('click', function() {
        jQuery('link').each(function(){
            jQuery(this).attr('href',jQuery(this).attr('href')+ '?' + (new Date()).getTime());
            console.log("Caches have just been RESET!"); });
        // jQuery('script').each(function(){
        //     jQuery(this).attr('src',jQuery(this).attr('src')+ '?' + (new Date()).getTime());
        //     });
        return false;
    });
});