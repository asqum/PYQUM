$(function () {
    $('a#mod').bind('click', function () { // id become #
        $.getJSON('/model', {

        }, function (data) {
            $('#mod').text(data.message); // id become #
        });
        return false;
    });
}); 

$(function () {
    $('a#gemarker').bind('click', function () { // id become #
        $.getJSON('/getmarker', {

        }, function (dat) {
            $('#gemarker').text(dat.message); // id become #
        });
        return false;
    });
}); 

$(function () {
    $('a#gedelay').bind('click', function () { // id become #
        $.getJSON('/getdelay', {

        }, function (dat) {
            $('#gedelay').text(dat.message); // id become #
        });
        return false;
    });
});