



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

        if ( axisKeys.yErr.length == 0 || axisKeys.yErr[i]=="" ){
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
    $('#qFactor-Download-button').on('click', function () {
        console.log("SAVING CSV FILE");
    
        // in order to trigger href send-file request: (PENDING: FIND OUT THE WEIRD LOGIC BEHIND THIS NECCESITY)
        //$.getJSON(mssnencrpytonian() + '/mssn/char/' + frespcryption + '/access', { wmoment: wmoment }, function (data) {});
    
        $.getJSON( '/benchmark/qestimate/exportMat_fitPara', {
            //ifreq: $('select.char.fresp.parameter[name="c-freq"]').val()
        }, function (data) {
            console.log("STATUS: " + data.status + ", PORT: " + data.qumport);
            $.ajax({
                url: 'http://qum.phys.sinica.edu.tw:' + data.qumport + '/mach/uploads/ANALYSIS/QEstimation[' + data.user_name + '].mat',
                method: 'GET',
                xhrFields: {
                    responseType: 'blob'
                },
                success: function (data) {
                    console.log("USER HAS DOWNLOADED QEstimation DATA from " + String(window.URL));
                    var a = document.createElement('a');
                    var url = window.URL.createObjectURL(data);
                    a.href = url;
                    a.download = 'QEstimation.mat';
                    document.body.append(a);
                    a.click();
                    a.remove();
                    window.URL.revokeObjectURL(url);
                    //$('#qFactor-Download-button').hide();
                }
            });
        });
        return false;
    });


    //Just for test
    $('#qFactor-test-button').on('click', function () {


        $.getJSON( '/benchmark/test',{  
            
        }, function (data) {
            console.log( data )
        });

    });
    // plot
    $('#qFactor-plot-button').on('click', function () {
        console.log( "2D plot" );
        let plotID_2D = "qFactor-plot2D-rawOverview";
        let plotID_1D_ampPhase = "qFactor-plot1D-ampPhase";
        let plotID_1D_IQ = "qFactor-plot1D-IQ";

        $.ajaxSettings.async = false;
        let htmlInfo=get_htmlInfo_python();
        let analysisIndex = get_selectInfo();
        if ( analysisIndex.axisIndex.length == 1 ){
        
        $.getJSON( '/benchmark/qestimate/getJson_plot',
        {   analysisIndex: JSON.stringify(analysisIndex), plotDimension: JSON.stringify(2), plotType: JSON.stringify("2D_amp"), },
            function (data) {
            console.log( "2D plot" );
            console.log( data );
            let axisKeys = {
                x: "frequency",
                y: htmlInfo[analysisIndex.axisIndex[0]]["name"],
                z: "amplitude",
            }
            console.log( data );
            
            document.getElementById(plotID_2D).style.display = "block";
            plot2D(data, axisKeys, plotID_2D);
        });
        }else{
            document.getElementById(plotID_2D).style.display = "none";
        }


        $.getJSON( '/benchmark/qestimate/getJson_plot',
        {   analysisIndex: JSON.stringify(analysisIndex), plotDimension: JSON.stringify(1), plotType: JSON.stringify("1D_amp"), },
            function (data) {
            console.log( "1D amp plot" );
            console.log( data );
            let axisKeys = {
                x: ["Data_point_frequency","Fitted_curve_frequency","Fitted_baseline_frequency","Corr_Data_point_frequency"],
                y: ["Data_point_amplitude","Fitted_curve_amplitude","Fitted_baseline_amplitude","Corr_Data_point_amplitude"],
                yErr: [],
            }
            //console.log( data.Fitted_curve_amplitude );

            plot1D(data, axisKeys, plotID_1D_ampPhase);
        });

        $.getJSON( '/benchmark/qestimate/getJson_plot',
        {   analysisIndex: JSON.stringify(analysisIndex), plotDimension: JSON.stringify(1), plotType: JSON.stringify("1D_IQ"), },
            function (data) {
            console.log( "1D IQ plot" );
            console.log( data );
            let axisKeys = {
                x: ["Data_point_I","Fitted_curve_I","Fitted_baseline_I","Corr_Data_point_I"],
                y: ["Data_point_Q","Fitted_curve_Q","Fitted_baseline_Q","Corr_Data_point_Q"],
                yErr: [],
            }
            //console.log( data.Fitted_curve_amplitude );

            plot1D(data, axisKeys, plotID_1D_IQ);
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

        let rangeFrom = document.getElementById("qFactor-fit-range-from").value;
        let rangeTo = document.getElementById("qFactor-fit-range-to").value;
        let baseline_correction = document.getElementById("qFactor-fit-baseline-correct").checked;
        let baseline_smoothness = document.getElementById("qFactor-fit-baseline-smoothness").value;
        let baseline_asymmetry = document.getElementById("qFactor-fit-baseline-asymmetry").value;

        let fitParameters = {
            range: {
                from: rangeFrom,
                to: rangeTo
            },
            baseline:{
                correction: baseline_correction,
                smoothness: baseline_smoothness,
                asymmetry: baseline_asymmetry,
            }
        }
        console.log(fitParameters);


        // Plot fit parameters
        $.getJSON( '/benchmark/qestimate/getJson_fitParaPlot',{  
            fitParameters: JSON.stringify(fitParameters),
            analysisIndex: JSON.stringify(analysisIndex), 
        }, function (data) {
            let xAxisKey = "Single_plot";
            if (analysisIndex.axisIndex.length == 1) { xAxisKey = htmlInfo[analysisIndex.axisIndex[0]]["name"] }
            let axisKeys_fitResult = {
                x: [xAxisKey],
                y: ["Qc_dia_corr", "Qi_dia_corr", "Ql", "fr", "single_photon_limit", "photons_in_resonator"],
                yErr: ["absQc_err", "Qi_dia_corr_err", "Ql_err", "fr_err", "", ""],
            }
            plot1D( data, axisKeys_fitResult, "qFactor-plot-fittingParameters");

        });


        // Renew 1D plot
        // $.getJSON( '/benchmark/qestimate/getJson_plot',
        // {   analysisIndex: JSON.stringify(analysisIndex), plotDimension: JSON.stringify(1)}, 
        //     function (data) {
        //     console.log( "1D plot" );
        //     console.log( data );
        //     let axisKeys = {
        //         x: ["Data_point_frequency","Fitted_curve_frequency","Fitted_baseline_frequency","Corr_Data_point_frequency"],
        //         y: ["Data_point_amplitude","Fitted_curve_amplitude","Fitted_baseline_amplitude","Corr_Data_point_amplitude"],
        //         yErr: [],
        //     }
        //     //console.log( data.Fitted_curve_amplitude );

        //     plot1D(data, axisKeys, "qFactor-plot-fittingResult");
        // });
        $.ajaxSettings.async = true;

    });

});

