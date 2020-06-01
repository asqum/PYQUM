//when page is loading:
$(document).ready(function(){
    console.log("user is ready");
    $('select#sample').empty();
    $('select#sample').append('<option value="-select-">-select-</option>');
    $.getJSON('/auth/user/samples', {
    }, function (data) {
        console.log(data.samples);
        $.each(data.samples, function(i,value) {
            $('select#samples').append('<option value="'+value+'">'+(i+1)+'. '+value+'</option>');
        });
    });
});

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
    var sname = $('select.samples#samples[name="' + usertype + '"]').val();
    $.getJSON('/auth/user/samples/meal', {
        sname: sname
    }, function (data){
        console.log("Loaded Sample: " + data.sname);
    });
    window.location.href=mssnencrpytonian()+'/mssn';
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
$('select.samples#samples').on('change', function(){
    console.log($('select#samples').val());
    window.usertype = this.name;
    console.log('User-type: ' + usertype);
    $.getJSON('/auth/user/samples/access', {
        // access sample based on main or shared selected:
        sname: $('select.samples#samples[name="' + this.name + '"]').val()
    }, function(data){
        console.log(data.message);
        $('input.user-samples#update[name="dob"]').val(data.sample_cv['fabricated']);
        $('input.user-samples#update[name="loc"]').val(data.sample_cv['location']);
        $('input.user-samples#update[name="coauthors"]').val(data.sample_cv['co_authors']);
        $('input.user-samples#update[name="prev"]').val(data.sample_cv['previously']);
        $('textarea.user-samples#update[name="description"]').val(data.sample_cv['description']);
        $('textarea.user-samples#update[name="history"]').val(data.sample_cv['history']);
        $('.samples > label#registered').empty().append($('<h4 style="color: red;"></h4>').text("Since " + data.sample_cv['registered'].replace('\n',' ')));
    });
    return false;
})

// Update samples:
$('input.user.samples.confirm-update#samples-confirm').on('click', function(e) {
    e.preventDefault();
    console.log($('select#samples').val());
    $.getJSON('/auth/user/samples/update', {
        sname: $('select#samples').val(),
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


