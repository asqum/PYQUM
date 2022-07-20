function Instrument_status(id, value) {
    var x = document.getElementById(id);
    var i = x.selectedIndex;
    document.getElementById("demo").innerHTML = x.options[i].text;
    document.getElementById("fruit").innerHTML = "Fruit #" + value + ":";
}