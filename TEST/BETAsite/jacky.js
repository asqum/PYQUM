let plotData_IQ = {};
let iqKeys = {
    x: ["rawI","fittedI"],
    y: ["rawQ","fittedQ"],
    yErr: [],
}
let plotData_AmpPhase = {
    raw: {},
    fitted: {},
};
let ampPhaseKeys = {
    x: [ ["x"], ["x"] ] ,
    y: [ ["Amplitude"],["Phase"] ],
    yErr: [ [],[] ],
}
//Get x axis
$.getJSON( '/benchmark/common_fitting/getJson_plotAxis',
{   plot1D_axisType: JSON.stringify('x_value'), },
    function (data) {
    console.log( "Get x axis" );
    plotData_AmpPhase["raw"]["x"]= data;
});
//Get fitted x axis
$.getJSON( '/benchmark/common_fitting/getJson_plotAxis',
{   plot1D_axisType: JSON.stringify('x_value_fit'), },
    function (data) {
    console.log( "Get x axis" );
    plotData_AmpPhase["fitted"]["x"]= data;
});
//Get raw signal
$.getJSON( '/benchmark/common_fitting/getJson_plot1D',
{   process: JSON.stringify("raw"), 
    plotInfo: JSON.stringify(plotInfo), },
    function (data) {
    console.log( "Get raw data" );
    plotData_IQ["rawI"]= data["I"];
    plotData_IQ["rawQ"]= data["Q"];

    plotData_AmpPhase["raw"]["Amplitude"]= data["Amplitude"];
    plotData_AmpPhase["raw"]["Phase"]= data["Phase"];
});

//Get fitted signal
$.getJSON( '/benchmark/common_fitting/getJson_plot1D',
{   process: JSON.stringify("fitted"), 
    plotInfo: JSON.stringify(plotInfo), },
    function (data) {
    console.log( "Get fitted data" );
    plotData_IQ["fittedI"]= data["I"];
    plotData_IQ["fittedQ"]= data["Q"];

    plotData_AmpPhase["fitted"]["Amplitude"]= data["Amplitude"];
    plotData_AmpPhase["fitted"]["Phase"]= data["Phase"];
});    
console.log( "Plot data" );

console.log( plotData_AmpPhase );
console.log( plotData_IQ );

plot1D_2subplot_shareX(plotData_AmpPhase, ampPhaseKeys, plotID_1D_ampPhase);
document.getElementById(plotID_1D_ampPhase).style.display = "block";

plot1D(plotData_IQ, iqKeys, plotID_1D_IQ);
document.getElementById(plotID_1D_IQ).style.display = "block";
document.getElementById(plotID_2D).style.display = "none";

$.ajaxSettings.async = true;