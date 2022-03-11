


$(document).ready(function(){
    // $('div.qestimatecontent').show();
    CF_render_input("common_fitting");
    console.log( "Load common_fitting" );

    let e_loadButton = document.getElementById("common_fitting-button-load");
    e_loadButton.addEventListener("click", load_data);
    let e_fitButton = document.getElementById("common_fitting-button-fit");
    e_fitButton.addEventListener("click", fit_data);
    let e_plot1DButton = document.getElementById("common_fitting-plot1D-button");
    e_plot1DButton.addEventListener("click", get_plot1D);
    let e_plot2DtButton = document.getElementById("common_fitting-plot2D-button");
    e_plot2DtButton.addEventListener("click", get_plot2D);
});

function get_common_fitting_selectInfo( quantificationType ){

    $.ajaxSettings.async = false;

    let htmlInfo = get_htmlInfo_python();
    let axisIndex=new Array(1);
    let valueIndex=new Array(htmlInfo.length);

    let aveAxisIndex=[];
    let aveRange;

    //let analysisIndex = {};

    
    console.log( "htmlInfo " );
    console.log( htmlInfo.length );
    // Get select parameter index
    for (let i=0; i<htmlInfo.length; i++ ) {
        htmlName = htmlInfo[i]["name"];
        varLength = htmlInfo[i]["length"];
        structurePosition = htmlInfo[i]["structurePosition"]
        if ( varLength == 1 ){ valueIndex[i]=0 }
        else{
            let plotType = document.getElementById(quantificationType+"-plot_type-"+htmlName).value
            console.log( "Plot type " +plotType );
            switch(plotType){
                case "y_value":
                    console.log(htmlName +" for y-axis value");
                    axisIndex[axisIndex.length] = structurePosition ;
                    valueIndex[i]=document.getElementById(quantificationType+"-select_value-"+htmlName).selectedIndex;
                    break;

                case "x_value":
                    console.log(htmlName +" for x-axis ");
                    axisIndex[0] = structurePosition ;
                    valueIndex[i]=0;
                    break;

                case "single_value":
                    console.log(htmlName +" select single value ");
                    valueIndex[i]=document.getElementById(quantificationType+"-select_value-"+htmlName).selectedIndex;
                    break;

                case "average":
                    console.log(htmlName +" select average");
                    valueIndex[i] = 0;
                    aveAxisIndex.push(structurePosition);
                    aveRange = document.getElementById(quantificationType+"-ave_value-"+htmlName).value;
                    break;

                case "oneshot":
                    console.log(htmlName +" select oneshot");
                    valueIndex[i] = 0;
                    oneShotAxisIndex.push(structurePosition);
                    oneShotCenters = document.getElementById(quantificationType+"-ave_value-"+htmlName).value;
                    break;
            }         
        }



    }
    let analysisIndex={
        valueIndex:valueIndex,
        axisIndex:axisIndex,
        aveInfo:{
            axisIndex:aveAxisIndex,
            aveRange:aveRange
        },
        oneShot_Info:{
            axisIndex:oneShotAxisIndex,
            centers:oneShotCenters,
        }
    }


    console.log( "Selection " );
    console.log( analysisIndex );
    $.ajaxSettings.async = true;

    return analysisIndex
}


function CF_render_input ( quantificationType )
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
            DOM_parameterPlotTypeSelector.setAttribute("onchange", "CF_showAveInput(this)");
            DOM_parameterSetting.appendChild(DOM_parameterPlotTypeSelector);

            // Create plot selection
            let plotType = ["single value","x axis - value","y axis - value","average","oneshot"];
            let plotTypeValue = ["single_value","x_value","y_value","average","oneshot"];
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


            
        }


    }
    // CF_creatDOM_FitDataType("all", "common_fitting-allParamater");
    $.ajaxSettings.async = true;
}

function CF_showAveInput(selectObject) {
    let DOM_parameterSetting=selectObject.parentElement;
    console.log("showAveInput trigger by "+selectObject.id)
    let DOM_parameterAve = DOM_parameterSetting.getElementsByClassName("ave_value")[0];
    DOM_parameterAve.style.display = "none";

    let DOM_parameterValueSelect = DOM_parameterSetting.getElementsByClassName("select_value")[0];
    DOM_parameterValueSelect.style.display = "none";

    let DOM_parameterValueInput = DOM_parameterSetting.getElementsByClassName("input_value")[0];
    DOM_parameterValueInput.style.display = "none";


    switch(selectObject.value){
        case "average":
            console.log("select "+selectObject.value)
            DOM_parameterAve.style.display = "block";
            break;
        case "y_value":
            console.log("select "+selectObject.value)
            break;
        case "single_value":
            console.log("select "+selectObject.value)
            DOM_parameterValueInput.style.display = "block";
            DOM_parameterValueSelect.style.display = "block";
            break;
        case "x_value":
            console.log("select "+selectObject.value)
            break;

    }
}


function load_data(){
    console.log( "Get data" );

    $.ajaxSettings.async = false;
    let analysisIndex = get_common_fitting_selectInfo("common_fitting");

    //Send information to python
    $.getJSON( '/benchmark/common_fitting/load',
        {   quantificationType: JSON.stringify("common_fitting"), 
            analysisIndex: JSON.stringify(analysisIndex), 
        },
        function (data) {
        console.log( "load data" );
    });
    if ( analysisIndex.axisIndex.length == 2 ){
        get_plot2D();
    }else{
        get_plot1D();
    }    
    $.ajaxSettings.async = true;
}

function get_plot2D(){
    console.log( "Plot data" );

    let plotID_2D = "common_fitting-plot2D-rawOverview";
    let plotID_1D_ampPhase = "common_fitting-plot1D-ampPhase";
    let plotID_1D_IQ = "common_fitting-plot1D-IQ";
    $.ajaxSettings.async = false;
    let htmlInfo=get_htmlInfo_python();


    let plot2D_signalType = document.getElementById("common_fitting-plot2D-zSelector").value;
    let plot1D_yAxisType = document.getElementById("common_fitting-plot2D-ySelector").value;

    console.log( "plot2D_signalType" );

    console.log( plot2D_signalType );
    let z_data;
    let y_axis=[];
    let x_axis=[];

    //Get 2D data
    $.getJSON( '/benchmark/common_fitting/getJson_plot2D',
    {   plot2D_signalType: JSON.stringify(plot2D_signalType), },
        function (data) {
        console.log( "Get 2D data" );
        console.log( data );
        z_data= data;

    });
    //Get x axis
    $.getJSON( '/benchmark/common_fitting/getJson_plotAxis',
    {   plot1D_axisType: JSON.stringify('x_value'), },
        function (data) {
        console.log( "Get x axis" );
        x_axis = data;
    });
    //Get y axis
    $.getJSON( '/benchmark/common_fitting/getJson_plotAxis',
    {   plot1D_axisType: JSON.stringify(plot1D_yAxisType), },
        function (data) {
        console.log( "Get y axis" );
        y_axis = data;
    });
    let plotData = {
        x:x_axis,
        y:y_axis,
        z:z_data,
    };
    let axisKeys = {
        x: "x",
        y: "y",
        z: "z",
    };
    console.log( "plotData" );
    console.log( plotData );

    plot2D(plotData, axisKeys, plotID_2D);
    document.getElementById(plotID_2D).style.display = "block";
    document.getElementById(plotID_1D_ampPhase).style.display = "none";
    document.getElementById(plotID_1D_IQ).style.display = "none";

    $.ajaxSettings.async = true;
}

function get_plot1D(){
    console.log( "Plot data" );

    let plotID_2D = "common_fitting-plot2D-rawOverview";
    let plotID_1D_ampPhase = "common_fitting-plot1D-ampPhase";
    let plotID_1D_IQ = "common_fitting-plot1D-IQ";
    $.ajaxSettings.async = false;
    let htmlInfo=get_htmlInfo_python();

    let selectType = document.getElementById("common_fitting-plot2D-ySelector").value;
    let selectValue = document.getElementById("common_fitting-plot1D-y_value").value;

    let plotInfo = {
        selectType: selectType,
        selectValue: selectValue,
    };
    console.log( "plotInfo" );
    console.log( plotInfo );
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
}

function fit_data(){

    let plot1D_yAxisType = document.getElementById("common_fitting-plot2D-ySelector").value;
    let analysisIndex = get_common_fitting_selectInfo("common_fitting");

    let fitFunc = document.getElementById("common_fitting-functionSelector").value;
    let signalType = document.getElementById("common_fitting-signalSelector").value;

    let fitRange = document.getElementById("common_fitting-fitRange").value;
    // let initValue = document.getElementById("common_fitting-parameterInitValues").value;

    switch (fitFunc){
        case "NTypeResonator":
            break;
        case "ExpDecay":
            break;
        case "DampOscillation":
            break;
    }
    
    console.log( "Fit plot" );
    console.log( analysisIndex );
    let fitParameters = {
        function: fitFunc,
        signal_type: signalType,
        range: fitRange,
    }
    
    console.log(fitParameters);
    $.ajaxSettings.async = false;
    let plotdata= {};

    $.getJSON( '/benchmark/common_fitting/getJson_plotAxis',
    {   plot1D_axisType: JSON.stringify(plot1D_yAxisType), },
        function (data) {
        console.log( "Get y axis" );
        plotdata["x"]= data;
    });

    let axisKeys_fitResult= {};
    // Plot fit parameters
    $.getJSON( '/benchmark/common_fitting/getJson_fitParaPlot',{  
        fitParameters: JSON.stringify(fitParameters),
        analysisIndex: JSON.stringify(analysisIndex), 
    }, function (data) {
        console.log("fitResult");
        console.log(data);
        let fitResultxAxisKey = "Single_plot";

        // if (analysisIndex.axisIndex.length == 2) { fitResultxAxisKey = htmlInfo[analysisIndex["axisIndex"][1]]["name"] }

        // console.log("xAxisKey: "+fitResultxAxisKey);
        axisKeys_fitResult["x"]= "x";
        axisKeys_fitResult["y"]= data["parKey"]["val"];
        axisKeys_fitResult["yErr"]= data["parKey"]["err"];
        plotdata = Object.assign({},data["data"], plotdata);

    });

    console.log("fitResult plot");
    console.log(axisKeys_fitResult);

    console.log(plotdata);
    plot1D( plotdata, axisKeys_fitResult, "common_fitting-plot-fittingParameters");
    get_plot1D();
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
                url: 'http://qum.phys.sinica.edu.tw:' + data.qumport + '/mach/uploads/ANALYSIS/common_fitting[' + data.user_name + '].mat',
                method: 'GET',
                xhrFields: {
                    responseType: 'blob'
                },
                success: function (data) {
                    console.log("USER HAS DOWNLOADED common_fitting DATA from " + String(window.URL));
                    var a = document.createElement('a');
                    var url = window.URL.createObjectURL(data);
                    a.href = url;
                    a.download = 'common_fitting.mat';
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



});

