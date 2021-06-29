



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

    let axisIndex=[]
    let valueIndex=[]


    let AnalysisIndex = {
        axisIndex:axisIndex,
        valueIndex:valueIndex,
      }
    // $.ajax({
    //     dataType: "json",
    //     url: "/benchmark/get_parametersID",
    //     async: false, 
    //     success: function(htmlIDs) {
    //     }
    // });
    let htmlInfo;
    $.getJSON( '/benchmark/get_parametersID', 
    {},
        function (data) {
            htmlInfo = data;
    });


    axisIndex = [];
    valueIndex = new Array(varName.length);

    // Initialize
    if (gAxisIndex.length == 0){ gAxisIndex = []; }
    if (gValueIndex.length == 0){ gValueIndex = new Array(varName.length); }

    // Get select parameter index
    for ( i in htmlInfo.length ) {
        htmlName = htmlInfo[i]["name"];
        varLength = htmlInfo[i]["length"];
        structurePosition = htmlInfo[i]["structurePosition"]
        if ( varLength = 0 ){ valueIndex[i]=0 }
        else{
            valueIndex[i] = document.getElementById("select-"+htmlName).selectedIndex;
            console.log("Select " + valueIndex[i] );
        }
        console.log("valueIndex " + valueIndex );

        let axisDimension = axisIndex.length;
        if ( document.getElementById("check-"+htmlName).checked && axisIndex.length<2 )
        {
            console.log(htmlName +" is checked ");
            axisIndex[axisDimension] = structurePosition ;
        }

    }
    AnalysisIndex.valueIndex = valueIndex;
    AnalysisIndex.axisIndex = axisIndex;

    console.log( AnalysisIndex );
    return plotIndex
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
        tracies[i] = {
        x: data[axisKeys.x[ix]],
        y: data[axisKeys.y[i]],
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
        

        let AnalysisIndex = get_selectInfo();

        if (gAxisIndex.length<=2 )
        {

            console.log( "2D plot" );
            console.log( AnalysisIndex );
            $.getJSON( '/benchmark/qestimate/getJson_2Dplot',
            {   AnalysisIndex: JSON.stringify(AnalysisIndex),}, 
                function (data) {
                console.log( data );
                let axisKeys = {
                    x: "frequency",
                    y: htmlInfo[AnalysisIndex.axisIndex[0]["name"]],
                    z: "amplitude",
                }
                console.log( data );

                plot2D(data, axisKeys, "qFactor-plot-rawOverview2D");
            });

            console.log(  "1D plot" );
            $.getJSON( '/benchmark/qestimate/getJson_1Dplot',
            {   AnalysisIndex: JSON.stringify(AnalysisIndex),}, 
                function (data) {
                console.log( data );
                let axisKeys = {
                    x: ["Data_point_frequency","Fitted_curve_frequency"],
                    y: ["Data_point_amplitude","Fitted_curve_amplitude"],
                }
                //console.log( data.Fitted_curve_amplitude );

                plot1D(data, axisKeys, "qFactor-plot-fittingResult");
            });

            
        }else{
            console.log( "Too many axis." );
        }
        

        $.ajaxSettings.async = true;

    });
    //Test fit data
    $('#qFactor-fit-button').on('click', function () {


        $.ajaxSettings.async = false;
        let htmlInfo=get_htmlInfo_python();


        let AnalysisIndex = get_selectInfo();

        console.log( "Fit plot" );
        console.log( AnalysisIndex );

        let fittingRangeFrom = document.getElementById("qFactor-fittingRange-from").value
        let fittingRangeTo = document.getElementById("qFactor-fittingRange-to").value
        console.log( "fit from " + fittingRangeFrom + " to ",  fittingRangeTo);
        $.getJSON( '/benchmark/qestimate/getJson_fitParaPlot',{  
            fittingRangeFrom:fittingRangeFrom, fittingRangeTo:fittingRangeTo,
            AnalysisIndex: JSON.stringify(AnalysisIndex), 
        }, function (data) {

            let axisKeys_fitResult = {
                x: [htmlInfo[AnalysisIndex.axisIndex[0]]["name"]],
                y: ["Qc_dia_corr", "Qi_dia_corr", "Ql", "fr"],
            }
            plot1D( data, axisKeys_fitResult, "qFactor-plot-fittingParameters");

            

        $.ajaxSettings.async = true;
        });
    });

});

