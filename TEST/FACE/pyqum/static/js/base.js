$(document).ready(function(){
    // $('button.mission').hide();
    // console if only for debugging purposes:
    // console.log($(location).attr("href"));
    // console.log(window.location.pathname);

    if (window.location.pathname == "/"){
        console.log(window.location.pathname);
        $('.navbar button').removeClass('active');
        $('.navbar button.home').addClass('active');
    };
              
    if (window.location.pathname == "/mach"){
        // can't find path for this case
        console.log("Path:");
        console.log(window.location.pathname); 
        // Thus we embedded the script in machine.html
    };    
    
    if (window.location.pathname == "/mssn"){
        // can't find path for this case
        console.log("Path:");
        console.log(window.location.pathname);
        // Thus we embedded the script in mission.html
    };

    if (window.location.pathname == "/bridge"){
        // can't find path for this case
        console.log("Path:");
        console.log(window.location.pathname); 
        // Thus we embedded the script in bridge.html
    };

    if (window.location.pathname == "/benchmark"){
        // can't find path for this case
        console.log("Path:");
        console.log(window.location.pathname); 
        // Thus we embedded the script in benchmark.html
    };

    if (window.location.pathname == "/gd/guide"){
        console.log(window.location.pathname);
        $('.navbar button').removeClass('active');
        $('.navbar button.guide').addClass('active'); 
    };

    if (window.location.pathname == "/dsply"){
        // can't find path for this case
        console.log("Path:");
        console.log(window.location.pathname); 
        // Thus we embedded the script in machine.html
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

// $(function () {
//     $("button.mission").bind('click', function(){
//         window.open("/mssn", '_self');    
//         return false;
//     });
// });

$(function () {
    $("button.bridge").bind('click', function(){
        window.open("/bridge", '_self');   
        return false;
    });
});

$(function () {
    $("button.benchmark").bind('click', function(){
        window.open("/benchmark", '_self');   
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
        window.open("/dsply", '_self');
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
        // $.getJSON('/reset', {}, function(data){ console.log("RESET: " + data.message)}); // press enter to clear the fog
        return false;
    });
});