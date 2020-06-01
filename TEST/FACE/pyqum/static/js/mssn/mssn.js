//when page is loading:
$(document).ready(function(){
    $('button#all-tab').toggleClass('active');
});

function mssnencrpytonian() {
    return '/' + 'ghhgjad';
};

function openTab(evt, Name) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the link that opened the tab
    document.getElementById(Name).style.display = "block";
    evt.currentTarget.className += " active";
} 

function Normalize_Dip(Z) {
    var Zrow = [];
    var zmin = Math.min.apply(Math, Z);
    var zmax = Math.max.apply(Math, Z);
    $.each(Z, function(i, z) {
        var znml = (z-zmax)/(zmax-zmin);
        Zrow.push(znml);
    });
    return Zrow;
}

function Normalize_Peak(Z) {
    var Zrow = [];
    var zmin = Math.min.apply(Math, Z);
    var zmax = Math.max.apply(Math, Z);
    $.each(Z, function(i, z) {
        var znml = (z-zmin)/(zmax-zmin);
        Zrow.push(znml);
    });
    return Zrow;
}

function VdBm_Conversion(Y, selector) {
    Y_Conv = [];
    ytitle = '<b>Signal(' + $(selector).val() + ')</b>';
    if ($(selector).val() == 'V') {
        $.each(Y, function(i, val) {Y_Conv.push(val);});
    } else if ($(selector).val() == 'dBm') {
        $.each(Y, function(i, val) {
            var val = 10*Math.log10(val**2/50*1000);
            Y_Conv.push(val);
        });
    };
    return {'y3': Y_Conv, 'ytitle': ytitle}; 
}