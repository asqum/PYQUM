//when page is loading:
$(document).ready(function(){
    // Previous select-values (extracted from rendered-HTML page via POST): 
    var mainsample = $('select.samples[name="main"]').val();
    // console.log("Main: " + mainsample);
    var sharedsample = $('select.samples[name="shared"]').val();
    // console.log("Shared: " + sharedsample);
    const sselection = [mainsample, sharedsample];
    window.selectedsname = sselection.find(s => s != 0); // return the first element that satisfies the predicate
    console.log("Loading:" + selectedsname);
    AccesSample(selectedsname);
});

// Accessing Sample's Details:
function AccesSample(sname) {
    if (typeof sname == 'undefined') {
        $('.samples > label#registered').empty().append($('<h4 style="color: red;"></h4>').text("Pick a Sample"));
    }
    $.getJSON('/auth/user/samples/access', {
        // access sample based on main or shared selected:
        sname: sname, 
    }, function(data){
        console.log(data.message);
        $('input.user-samples#update[name="dob"]').val(data.sample_cv['fabricated']);
        $('input.user-samples#update[name="loc"]').val(data.sample_cv['location']);
        $('input.user-samples#update[name="coauthors"]').val(data.sample_cv['co_authors']);
        $('input.user-samples#update[name="prev"]').val(data.sample_cv['previously']);
        $('textarea.user-samples#update[name="description"]').val(data.sample_cv['description']);
        $('textarea.user-samples#update[name="history"]').val(data.sample_cv['history']);
        $('.samples > label#registered').empty().append($('<h4 style="color: red;"></h4>').text("Since " + data.sample_cv['registered'].replace('\n',' ')));
        if (data.system=="NULL") { $('div#which_queue_system').empty().append($('<h4 style="color: red;"></h4>').text("Please assign the queue-system via MACHINE/BDR/SAMPLES")); }
        else { $('div#which_queue_system').empty().append($('<h4 style="color: blue;"></h4>').text("Assigned to: " + data.system)); };
    });
};
 
// Pending: Loading function from other JS script/module?
function mssnencrpytonian() {
    return '/' + 'ghhgjad';
};

// hiding parameter settings when click outside the modal box:
$('.modal-toggle.samples.add-details').on('click', function(e) {
    e.preventDefault();
    $('.modal.samples.add-details').toggleClass('is-visible');
});
$('.modal-toggle.samples.confirm-update').on('click', function(e) {
    e.preventDefault();
    $('.modal.samples.confirm-update').toggleClass('is-visible');
});

// toggle adding samples modal box:
$('button.user-samples#samples-add').on('click', function(e) {
    e.preventDefault();
    $('.modal.samples.add-details').toggleClass('is-visible');
});
$('button.user-samples#samples-update').on('click', function(e) {
    e.preventDefault();
    $('.modal.samples.confirm-update').toggleClass('is-visible');
});

// MEAL: MEASURE & ANALYZE
$('button.user-samples#samples-meal').on('click', function(e) {
    $.getJSON('/auth/user/samples/meal', {
        sname: selectedsname,
    }, function (data){
        console.log("Loaded Sample: " + data.sname);
        window.location.href=mssnencrpytonian()+'/mssn'; // placing here will prevent this route from being skipped!
    });
    return false;
});

// Registration
$('input.user.samples.add-details#samples-register').on('click', function(e) {
    e.preventDefault();
    if( $("input.user-samples#register[name='sname']").val().length === 0 ||
        $("input.user-samples#register[name='loc']").val().length === 0 ||
        $("textarea.user-samples#register[name='description']").val().length === 0 ) {
            alert('Check name, location and description!');
            console.log('Check name, location and description!');
    } else {
        $.getJSON('/auth/user/samples/register', {
            sname: $('input.user-samples#register[name="sname"]').val(),
            dob: $("input.user-samples#register[name='dob']").val(),
            loc: $("input.user-samples#register[name='loc']").val(),
            prev: $("input.user-samples#register[name='prev']").val(),
            description: $("textarea.user-samples#register[name='description']").val()
        }, function (data) {
            console.log(data.message);
            window.location.href='/auth/user';
        });
    };
});

// Access samples:
$('select.samples').on('change', function(){
    console.log("Selected: " + $('select.samples').val());
    console.log('User-type: ' + this.name);
    selectedsname = $('select.samples[name="' + this.name + '"]').val();
    AccesSample(selectedsname); 
    return false;
})

// Update samples:
$('input.user.samples.confirm-update#samples-confirm').on('click', function(e) {
    e.preventDefault();
    console.log($('select.samples').val());
    $.getJSON('/auth/user/samples/update', {
        sname: $('select.samples#samples').val(), // only main user can update!
        dob: $('input.user-samples#update[name="dob"]').val(),
        loc: $('input.user-samples#update[name="loc"]').val(),
        coauthors: $('input.user-samples#update[name="coauthors"]').val(),
        prev: $('input.user-samples#update[name="prev"]').val(),
        description: $('textarea.user-samples#update[name="description"]').val(),
        history: $('textarea.user-samples#update[name="history"]').val(),
        ownerpassword: $('input.user-samples#ownerpassword').val(),
    }, function (data) {
        $('.samples > label#registered').empty().append($('<h4 style="color: red;"></h4>').text(data.message));
    });
    
});


