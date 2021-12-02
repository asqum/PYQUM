


$(document).ready(function(){
    // $('div.qestimatecontent').show();
    render_common_fitting("common_fitting");
    console.log( "Load qEstimation" );

});

function render_common_fitting ( quantificationType )
{

    $.ajaxSettings.async = false;

    let measureParameters = document.getElementById(quantificationType+"-input");



    let htmlInfo = [];
    $.getJSON( '/benchmark/get_parametersID', 
    {},
        function (data) {
            htmlInfo = data;
    });
    console.log( htmlInfo );
    for(i = 0; i < htmlInfo.length; i++) {


        // Create parameters information and plot selection
        if (htmlInfo[i]["length"] > 1) // The parameter only have one value
        {   
            // get parameter name    
            let parameterName = htmlInfo[i]["name"]
            console.log(i, parameterName);

            // div for parameter infomation
            let DOM_parameterInfo = document.createElement("div");
            DOM_parameterInfo.id = quantificationType+"-info-"+parameterName;
            DOM_parameterInfo.setAttribute("class", "measurePara");
            measureParameters.appendChild(DOM_parameterInfo);

            // Create element for parameter name
            let DOM_parameterName = document.createElement("label");
            DOM_parameterName.innerHTML = parameterName;
            DOM_parameterName.setAttribute("class", "name");
            DOM_parameterInfo.appendChild(DOM_parameterName);

            // Create element for c-order string
            let DOM_parameterCOrder = document.createElement("p");
            DOM_parameterCOrder.innerHTML = htmlInfo[i]["c_order"];
            DOM_parameterCOrder.setAttribute("class", "c_order");
            DOM_parameterInfo.appendChild(DOM_parameterCOrder);


            // Creat div for parameter setting
            let DOM_parameterSetting = document.createElement("div");
            DOM_parameterSetting.id = quantificationType+"-setting-"+parameterName;
            DOM_parameterSetting.setAttribute("class", "measurePara");
            measureParameters.appendChild(DOM_parameterSetting);

            // Creat select for parameter plot type 
            let DOM_parameterPlotTypeSelector = document.createElement("select");
            DOM_parameterPlotTypeSelector.id = quantificationType+"-plot_type-"+parameterName;
            DOM_parameterPlotTypeSelector.setAttribute("class", "measureParaSelect plotTypeSelect");
            DOM_parameterPlotTypeSelector.setAttribute("onchange", "showAveInput(this)");
            DOM_parameterSetting.appendChild(DOM_parameterPlotTypeSelector);

            // Create plot selection
            let plotType = ["single value","x axis - value","y axis - value","y axis - count","average"];
            let plotTypeValue = ["single_value","x_value","y_value","y_count","average"];
            for( ipt=0; ipt<plotType.length; ipt++)
            {
                let DOM_parameterPlotType = document.createElement("option");
                DOM_parameterPlotType.innerHTML = plotType[ipt];
                DOM_parameterPlotType.setAttribute("value", plotTypeValue[ipt]);
                DOM_parameterPlotTypeSelector.appendChild(DOM_parameterPlotType);
            }


            // Create parameter value selection
            let DOM_parameterValueSelector = document.createElement("select");
            DOM_parameterValueSelector.id = quantificationType+"-select_value-"+parameterName;
            DOM_parameterValueSelector.setAttribute("class", "measureParaSelect select_value");
            //DOM_parameterValueSelector.style.display = "none";
            DOM_parameterSetting.appendChild(DOM_parameterValueSelector);
            let parameterValue;
            console.log(parameterName, " Selector ");
            $.getJSON( '/benchmark/get_parameterValue',
            {   parameterKey: parameterName,},
                function (data) {
                parameterValue=data;
            });
            let selectLen = parameterValue.length;
            if ( htmlInfo[i]["length"]>50 ){ selectLen = 50;}
            for ( iv=0; iv<selectLen; iv++)
            {
                let DOM_parameterValue = document.createElement("option");
                DOM_parameterValue.innerHTML = parameterValue[iv];
                DOM_parameterValueSelector.appendChild(DOM_parameterValue);
            }
            
            // Create parameter value input
            let DOM_parameterValueInput = document.createElement("input");
            DOM_parameterValueInput.id = quantificationType+"-input_value-"+parameterName;
            DOM_parameterValueInput.setAttribute("class", "measureParaSelect input_value");
            //DOM_parameterValueInput.style.display = "none";
            DOM_parameterSetting.appendChild(DOM_parameterValueInput);

            

            // Create average input
            let DOM_parameterAve = document.createElement("input");
            DOM_parameterAve.id = quantificationType+"-ave_value-"+parameterName;
            DOM_parameterAve.setAttribute("class", "measureParaSelect ave_value");
            DOM_parameterAve.style.display = "none";
            DOM_parameterSetting.appendChild(DOM_parameterAve);


            // Create x axis fitting input
            let DOM_parameterFit = document.createElement("input");
            DOM_parameterFit.id = quantificationType+"-fitting_input-"+parameterName;
            DOM_parameterFit.setAttribute("class", "measureParaSelect fitting_input");
            DOM_parameterFit.setAttribute("value", parameterValue[0]+","+parameterValue[parameterValue.length-1]);
            DOM_parameterFit.style.display = "none";
            DOM_parameterSetting.appendChild(DOM_parameterFit);
            
        }


    }

    $.ajaxSettings.async = true;
}

$(function () {

    // saving exported mat-data to client's PC:
    $('#qFactor-Download-button').on('click', function () {
        console.log("SAVING CSV FILE");
    

        $.getJSON( '/benchmark/common_fitting/exportMat_fitPara', {
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


    // plot
    $('#qFactor-plot-button').on('click', function () {
        let plotID_2D = "qFactor-plot2D-rawOverview";
        let plotID_1D_ampPhase = "qFactor-plot1D-ampPhase";
        let plotID_1D_IQ = "qFactor-plot1D-IQ";
        console.log( "plot!!" );
        $.ajaxSettings.async = false;
        let htmlInfo=get_htmlInfo_python();
        let analysisIndex = get_selectInfo("qEstimation");
        if ( analysisIndex.axisIndex.length == 2 ){
            $.getJSON( '/benchmark/common_fitting/getJson_plot',
            {   quantificationType: JSON.stringify("qEstimation"), 
                analysisIndex: JSON.stringify(analysisIndex), 
                plotType: JSON.stringify("2D_amp"), },
                function (data) {
                console.log( "2D plot" );
                console.log( data );
                let axisKeys = {
                    x: htmlInfo[analysisIndex.axisIndex[0]]["name"],
                    y: htmlInfo[analysisIndex.axisIndex[1]]["name"],
                    z: "amplitude",
                }
                console.log( data );
                
                document.getElementById(plotID_2D).style.display = "block";
                plot2D(data, axisKeys, plotID_2D);
            });
        }else{
            document.getElementById(plotID_2D).style.display = "none";
        }


        $.getJSON( '/benchmark/common_fitting/getJson_plot',
        {   quantificationType: JSON.stringify("qEstimation"), 
            analysisIndex: JSON.stringify(analysisIndex),
            plotType: JSON.stringify("1D_all"), },
            function (data) {
            console.log( "1D plot test Q" );
            console.log( data );
            let ampPhaseKeys = {
                x: [ [htmlInfo[analysisIndex.axisIndex[0]]["name"]], [htmlInfo[analysisIndex.axisIndex[0]]["name"]] ] ,
                y: [ ["Amplitude"],["Phase"] ],
                yErr: [ [],[] ],
            }
            plot1D_2subplot_shareX(data, ampPhaseKeys, plotID_1D_ampPhase);
            let iqKeys = {
                x: [["I"]],
                y: [["Q"]],
                yErr: [[]],
            }
            plot1D_2y(data, iqKeys, plotID_1D_IQ);
        });
        $.ajaxSettings.async = true;

    });
    //Test fit data
    $('#qFactor-fit-button').on('click', function () {

        $.ajaxSettings.async = false;
        let htmlInfo=get_htmlInfo_python();
        let analysisIndex = get_selectInfo("qEstimation");

        console.log( "Fit plot" );
        console.log( analysisIndex );

        let xAxisKey = htmlInfo[analysisIndex["axisIndex"][0]]["name"];
        let fitRange = document.getElementById("qEstimation"+"-fitting_input-"+xAxisKey).value;

        let baseline_correction = document.getElementById("qFactor-fit-baseline-correct").checked;
        let baseline_smoothness = document.getElementById("qFactor-fit-baseline-smoothness").value;
        let baseline_asymmetry = document.getElementById("qFactor-fit-baseline-asymmetry").value;
        let gain = document.getElementById("qFactor-fit-gain").value;

        let fitParameters = {
            interval: {
                input: fitRange,
            },
            baseline:{
                correction: baseline_correction,
                smoothness: baseline_smoothness,
                asymmetry: baseline_asymmetry,
            },
            gain:gain,
            
        }
        
        console.log(fitParameters);

        // Plot fit parameters
        $.getJSON( '/benchmark/common_fitting/getJson_fitParaPlot',{  
            fitParameters: JSON.stringify(fitParameters),
            analysisIndex: JSON.stringify(analysisIndex), 
        }, function (data) {
            console.log("fitResult");
            console.log(data);
            let fitResultxAxisKey = "Single_plot";

            if (analysisIndex.axisIndex.length == 2) { fitResultxAxisKey = htmlInfo[analysisIndex["axisIndex"][1]]["name"] }
            // if ( fitResultxAxisKey == "Power" ) { fitResultxAxisKey = "power_corr" }

            console.log("xAxisKey: "+fitResultxAxisKey);

            let axisKeys_fitResult = {
                x: [fitResultxAxisKey],
                y: ["Qi_dia_corr","Qi_no_corr","absQc","Qc_dia_corr","Ql","fr","theta0","phi0","single_photon_limit", "photons_in_resonator"],
                yErr: ["Qi_dia_corr_err", "Qi_no_corr_err", "absQc_err", "absQc_err", "Ql_err", "fr_err", "", "phi0_err","",""],
            }
            let plotdata = Object.assign({}, data["extendResults"], data["results"], data["errors"] );
            plotdata[fitResultxAxisKey] = data[fitResultxAxisKey]
            plot1D( plotdata, axisKeys_fitResult, "qFactor-plot-fittingParameters");

        });


        $.ajaxSettings.async = true;

    });

});

