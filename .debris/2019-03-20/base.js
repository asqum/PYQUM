$(document).ready(function(){
    


$("button.home").bind('click', function(){
    window.open("/", '_self');    
    return false;
});

$("button.machine").bind('click', function(){
    window.open("/mach", '_self');    
    return false;
});

$("button.mission").bind('click', function(){
    window.open("/mssn", '_self');    
    return false;
});

$("button.bridge").bind('click', function(){
    window.open("/script", '_self');    
    return false;
});

$("button.guide").bind('click', function(){
    window.open("/guide", '_self');    
    return false;
});

$("button.display").bind('click', function(){
    window.open("/figstatic", '_self');    
    return false;
});



});