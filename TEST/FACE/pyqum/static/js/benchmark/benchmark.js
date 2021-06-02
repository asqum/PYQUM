//when page is loading:

$(document).ready(function(){
    console.log( "BENCHMARK JS" );
    //compensating what base.js cannot do
    $('.navbar button').removeClass('active');
    $('.navbar button.benchmark').addClass('active');
    $('button#measurement_info-tab').toggleClass('active'); // default show-up of 'qestimate' content is set by benchmark.css
});

function benchmark_encryption() {
    return '/' +'ghhgjadz';
};

function openTab(evt, Name) {
    // Declare all variables
    console.log('Tab: ' + Name );

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



