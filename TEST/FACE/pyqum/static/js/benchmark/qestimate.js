



$(document).ready(function(){
    // $('div.qestimatecontent').show();
    console.log( "QESTIMATE JS" );
});


let gAxisIndex = [];
let gValueIndex = [];

function get_htmlInfo_python(){
    let htmlInfo;
    $.getJSON( '/benchmark/get_parametersID', 
    {},
        function (data) {
            htmlInfo = data;
    });
    return htmlInfo
}

function get_selectInfo(){

    $.ajaxSettings.async = false;


    // $.ajax({
    //     dataType: "json",
    //     url: "/benchmark/get_parametersID",
    //     async: false, 
    //     success: function(htmlIDs) {
    //     }
    // });
    let htmlInfo = get_htmlInfo_python();
    let axisIndex=[];
    let valueIndex=new Array(htmlInfo.length);
    let analysisIndex = {};

    
    console.log( "htmlInfo " );
    console.log( htmlInfo.length );
    // Get select parameter index
    for (let i=0; i<htmlInfo.length; i++ ) {
        htmlName = htmlInfo[i]["name"];
        varLength = htmlInfo[i]["length"];
        structurePosition = htmlInfo[i]["structurePosition"]
        console.log( "htmlInfo i", i, varLength );
        if ( varLength == 1 ){ valueIndex[i]=0 }
        else{
            valueIndex[i] = document.getElementById("select-"+htmlName).selectedIndex;
            console.log("Select " +valueIndex[i] );
            console.log("check " +htmlName );
            let axisDimension = axisIndex.length;
            if ( document.getElementById("check-"+htmlName).checked && axisIndex.length<1 )
            {
                console.log(htmlName +" is checked ");
                axisIndex[axisDimension] = structurePosition ;
            }
        }
        console.log("valueIndex " + valueIndex );



    }
    analysisIndex["valueIndex"] = valueIndex;
    analysisIndex["axisIndex"] = axisIndex;
    console.log( "Selection " );
    console.log( analysisIndex );
    $.ajaxSettings.async = true;

    return analysisIndex
}



function plot1D ( data, axisKeys, plotId ){
    console.log("Plotting 1D");
    let traceNumber = axisKeys.y.length;
    console.log(axisKeys.x[0]);

    let tracies = new Array(traceNumber);
    let ix;
    for (let i = 0; i < traceNumber; i++){
        if ( axisKeys.x.length != 1 ){
            ix = i
        }else{
            ix = 0
        }

        if ( axisKeys.yErr.length == 0 ){
            yErr = {
                type: 'data',
                array: [],
                visible: false
              }
        }else{
            yErr = {
                type: 'data',
                array: data[axisKeys.yErr[i]],
                visible: true
              }
        }
        tracies[i] = {
        x: data[axisKeys.x[ix]],
        y: data[axisKeys.y[i]],
        error_y: yErr,
        name: axisKeys.y[i],
        mode: 'markers',
        type: 'scatter'
        };
    }

    Plotly.newPlot(plotId, tracies, {showSendToCloud: true});
}

function plot2D( data, axisKeys, plotId ) {
    console.log("Plotting 2D");
    console.log( "x length: " +data[axisKeys.x].length );

    // Frame assembly:
    var trace = {
        z: data[axisKeys.z], 
        x: data[axisKeys.x], 
        y: data[axisKeys.y], 
        zsmooth: 'best',
        mode: 'lines', 
        type: 'heatmap',
        width: 2.5
    };
    
    //console.log("1st z-trace: " + trace.z[0][0]);

    // Plotting the Chart using assembled TRACE:
    var Trace = [trace]
    Plotly.newPlot(plotId, Trace, {showSendToCloud: true});
};


$(function () {

    // saving exported mat-data to client's PC:
    $('#qFactor-save-button').on('click', function () {
        console.log("SAVING MAT FILE");
        $.ajaxSettings.async = false;

        let user = "";
        $.getJSON( '/benchmark/get_user', 
        {}, 
            function (name) {
                user = name;
        });
        // in order to trigger href send-file request: (PENDING: FIND OUT THE WEIRD LOGIC BEHIND THIS NECCESITY)
        console.log("STATUS download");
        $.ajax({
            url: 'http://qum.phys.sinica.edu.tw:5301/mach/uploads/ANALYSIS/resonator_fit[' + user + '].mat',
            method: 'GET',
            xhrFields: {
                responseType: 'blob'
            },
            success: function (data) {
                console.log("USER HAS DOWNLOADED resonator_fit from " + String(window.URL));
                var a = document.createElement('a');
                var url = window.URL.createObjectURL(data);
                a.href = url;
                a.download = 'resonator_fit.mat';
                document.body.append(a);
                a.click();
                a.remove();
                window.URL.revokeObjectURL(url);
            }
        });
        $.ajaxSettings.async = true;

        return false;
    });


    //Just for test
    $('#qFactor-test-button').on('click', function () {


        $.getJSON( '/benchmark/test',{  
            
        }, function (data) {
            console.log( data )
        });

    });
    // Test new plot
    $('#qFactor-plot-button').on('click', function () {
        console.log( "2D plot" );
        $.ajaxSettings.async = false;
        let htmlInfo=get_htmlInfo_python();
        let analysisIndex = get_selectInfo();

        console.log( "2D plot" );
        console.log( analysisIndex );

        $.getJSON( '/benchmark/qestimate/getJson_plot',
        {   analysisIndex: JSON.stringify(analysisIndex), plotDimension: JSON.stringify(2)} ,  
            function (data) {
            console.log( data );
            let axisKeys = {
                x: "frequency",
                y: htmlInfo[analysisIndex.axisIndex[0]["name"]],
                z: "amplitude",
            }
            console.log( data );

            plot2D(data, axisKeys, "qFactor-plot-rawOverview2D");
        });

        console.log(  "1D plot" );
        $.getJSON( '/benchmark/qestimate/getJson_plot',
        {   analysisIndex: JSON.stringify(analysisIndex), plotDimension: JSON.stringify(1)}, 
            function (data) {
            console.log( data );
            let axisKeys = {
                x: ["Data_point_frequency","Fitted_curve_frequency"],
                y: ["Data_point_amplitude","Fitted_curve_amplitude"],
                yErr: [],
            }
            //console.log( data.Fitted_curve_amplitude );

            plot1D(data, axisKeys, "qFactor-plot-fittingResult");
        });


        $.ajaxSettings.async = true;

    });
    //Test fit data
    $('#qFactor-fit-button').on('click', function () {


        $.ajaxSettings.async = false;
        let htmlInfo=get_htmlInfo_python();


        let analysisIndex = get_selectInfo();

        console.log( "Fit plot" );
        console.log( analysisIndex );

        let fittingRangeFrom = document.getElementById("qFactor-fittingRange-from").value
        let fittingRangeTo = document.getElementById("qFactor-fittingRange-to").value
        console.log( "fit from " + fittingRangeFrom + " to ",  fittingRangeTo);
        $.getJSON( '/benchmark/qestimate/getJson_fitParaPlot',{  
            fittingRangeFrom:fittingRangeFrom, fittingRangeTo:fittingRangeTo,
            analysisIndex: JSON.stringify(analysisIndex), 
        }, function (data) {

            let axisKeys_fitResult = {
                x: [htmlInfo[analysisIndex.axisIndex[0]]["name"]],
                y: ["Qc_dia_corr", "Qi_dia_corr", "Ql", "fr"],
                yErr: ["absQc_err", "Qi_dia_corr_err", "Ql_err", "fr_err"],
            }
            plot1D( data, axisKeys_fitResult, "qFactor-plot-fittingParameters");

            

        $.ajaxSettings.async = true;
        });
    });

});

