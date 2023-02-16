$(document).ready(function(){
    // DR-specific navigation-bar color:
    $.getJSON('/basecolor', { }, function(data) {
        console.log("Same color: " + Boolean($("div.navbar").css("background-color")==data.base_color));
        console.log("Previous color: " + $("div.navbar").css("background-color"));
        if ($("div.navbar").css("background-color")!=data.base_color) {
            $("div.navbar").css("background-color", data.base_color);
        };
        console.log("Current color: " + $("div.navbar").css("background-color"));
    });
    
    // Highlight Tab (maybe wouldn't work here)
    // $('button.mission').hide();
    // console if only for debugging purposes:
    // console.log($(location).attr("href"));

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

    if (window.location.pathname == "/guide"){
        // can't find path for this case
        console.log("Path:");
        console.log(window.location.pathname); 
        // Thus we embedded the script in guide.html
    };

    if (window.location.pathname == "/dsply"){
        // can't find path for this case
        console.log("Path:");
        console.log(window.location.pathname); 
        // Thus we embedded the script in display.html
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

// Encryption:
function guidencrpytonian() {
    return '/' + 'hgdfhghfle7';
};

// Loading pages:
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
        window.open(guidencrpytonian() + "/guide", '_self');    
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

// Iterate through select options with button click for a certain row:
// Column 0
$(document).on('click', 'button.minusButton', function() {
    var select_element = $(this).closest('.row').find(".zoomSelect");
    var selIndex = select_element.prop('selectedIndex');
    if (selIndex != 0) { select_element.val(select_element.children('option').eq(selIndex - 1).val()); };
    select_element.trigger("change");
    console.log("Going BACK");
});
$(document).on('click', 'button.plusButton', function() {
    var select_element = $(this).closest('.row').find(".zoomSelect");
    var selIndex = select_element.prop('selectedIndex');
    if (selIndex != select_element.children('option').length - 1) { select_element.val(select_element.children('option').eq(selIndex + 1).val()); };
    select_element.trigger("change");
    console.log("Going FORWARD");
});
// Column 1 (Use this if there's already another same feature on that same row!)
$(document).on('click', 'button.minusButton-1', function() {
    var select_element = $(this).closest('.row').find(".zoomSelect-1");
    var selIndex = select_element.prop('selectedIndex');
    if (selIndex != 0) { select_element.val(select_element.children('option').eq(selIndex - 1).val()); };
    select_element.trigger("change");
    console.log("Going BACK");
});
$(document).on('click', 'button.plusButton-1', function() {
    var select_element = $(this).closest('.row').find(".zoomSelect-1");
    var selIndex = select_element.prop('selectedIndex');
    if (selIndex != select_element.children('option').length - 1) { select_element.val(select_element.children('option').eq(selIndex + 1).val()); };
    select_element.trigger("change");
    console.log("Going FORWARD");
});
// Inter-row (Use this for inter-row manipulation of zoomSelect)
$(document).on('click', 'button.minusButton-interow', function() {
    var select_element = $('.interow').find(".zoomSelect-interow");
    var selIndex = select_element.prop('selectedIndex');
    if (selIndex != 0) { select_element.val(select_element.children('option').eq(selIndex - 1).val()); };
    select_element.trigger("change");
    console.log("Going BACK");
});
$(document).on('click', 'button.plusButton-interow', function() {
    var select_element = $('.interow').find(".zoomSelect-interow");
    var selIndex = select_element.prop('selectedIndex');
    if (selIndex != select_element.children('option').length - 1) { select_element.val(select_element.children('option').eq(selIndex + 1).val()); };
    select_element.trigger("change");
    console.log("Going FORWARD");
});

// Customized up-down selection of multiple parameters on the Missions:
$(document).on('click', 'button.up_select', function() {
    var select_element = $( 'select.char.cwsweep.parameter#c-' + $('select.char.cwsweep.parameter#cwsweep-parameters').val() );
    var selIndex = select_element.prop('selectedIndex');
    if (selIndex != 0) { select_element.val(select_element.children('option').eq(selIndex - 1).val()); };
    select_element.trigger("change");
});
$(document).on('click', 'button.down_select', function() {
    var select_element = $( 'select.char.cwsweep.parameter#c-' + $('select.char.cwsweep.parameter#cwsweep-parameters').val() );
    var selIndex = select_element.prop('selectedIndex');
    if (selIndex != select_element.children('option').length - 1) { select_element.val(select_element.children('option').eq(selIndex + 1).val()); };
    select_element.trigger("change");
});
