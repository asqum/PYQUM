


$(document).ready(function(){
    // $('div.qestimatecontent').show();
    FD_render_input("fidelity");
    console.log( "Load readout_fidelity" );

    let e_loadButton = document.getElementById("fidelity-button-load");
    e_loadButton.addEventListener("click", FD_load_data);
    let e_fitButton = document.getElementById("fidelity-button-fit");
    e_fitButton.addEventListener("click", FD_fit_data);
    let e_preButton = document.getElementById("fidelity-button-pretrain");
    e_preButton.addEventListener("click", FD_pretrain_data);
    // let e_plot1DButton = document.getElementById("fidelity-plot1D-button");
    // e_plot1DButton.addEventListener("click", get_plot1D);
    // let e_plot2DtButton = document.getElementById("fidelity-plot2D-button");
    // e_plot2DtButton.addEventListener("click", get_plot2D);
    let e_plottButton = document.getElementById("fidelity-button-plot");
    e_plottButton.addEventListener("click", FD_plot_data);
});

function get_fidelity_selectInfo( quantificationType ){

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

            }         
        }



    }
    let analysisIndex={
        valueIndex:valueIndex,
        axisIndex:axisIndex,
        aveInfo:{
            axisIndex:aveAxisIndex,
            aveRange:aveRange
        }
    }


    console.log( "Selection " );
    console.log( analysisIndex );
    $.ajaxSettings.async = true;

    return analysisIndex
}


function FD_render_input ( quantificationType )
{

    $.ajaxSettings.async = false;

    let measureParameters = document.getElementById(quantificationType+"-input");
    console.log(quantificationType+"-input");


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
            DOM_parameterPlotTypeSelector.setAttribute("onchange", "FD_showAveInput(this)");
            DOM_parameterSetting.appendChild(DOM_parameterPlotTypeSelector);

            // Create plot selection
            let plotType = ["single value","x axis - value","y axis - value","average"];
            let plotTypeValue = ["single_value","x_value","y_value","average"];
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
    // FD_creatDOM_FitDataType("all", "fidelity-allParamater");
    $.ajaxSettings.async = true;
}

function FD_showAveInput(selectObject) {
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
function FD_creatDOM_FitDataType( fitFunc, parentID ){
    // Creat select for parameter plot type
    console.log( "FD_creatDOM_FitDataType" );
    let parentDOM = document.getElementById( parentID );

    let DOM_dataTypeSelector = document.createElement("select");
    DOM_dataTypeSelector.id = fitFunc+"-data_type";
    DOM_dataTypeSelector.setAttribute("class", "measureParaSelect plotTypeSelect");
    parentDOM.appendChild(DOM_dataTypeSelector);
    // Create plot selection
    let dataType = ["Amplitude","Phase","IQ plane"];
    let dataTypeValue = ["amplitude","phase","iqPlane"];
    for( ipt=0; ipt<dataType.length; ipt++)
    {
        let DOM_dataType = document.createElement("option");
        DOM_dataType.innerHTML = dataType[ipt];
        DOM_dataType.setAttribute("value", dataTypeValue[ipt]);
        DOM_dataTypeSelector.appendChild(DOM_dataType);
    }
}


function FD_load_data(){
    console.log( "Get data" );

    $.ajaxSettings.async = false;
    let analysisIndex = get_fidelity_selectInfo("fidelity");

    //Send information to python
    $.getJSON( '/benchmark/fidelity/load',
        {   quantificationType: JSON.stringify("fidelity"), 
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

    let plotID_2D = "fidelity-plot2D-rawOverview";
    let plotID_1D_ampPhase = "fidelity-plot1D-ampPhase";
    let plotID_1D_IQ = "fidelity-plot1D-IQ";
    $.ajaxSettings.async = false;
    let htmlInfo=get_htmlInfo_python();


    let plot2D_signalType = document.getElementById("fidelity-plot2D-zSelector").value;
    let plot1D_yAxisType = document.getElementById("fidelity-plot2D-ySelector").value;

    console.log( "plot2D_signalType" );

    console.log( plot2D_signalType );
    let z_data;
    let y_axis=[];
    let x_axis=[];

    //Get 2D data
    $.getJSON( '/benchmark/fidelity/getJson_plot2D',
    {   plot2D_signalType: JSON.stringify(plot2D_signalType), },
        function (data) {
        console.log( "Get 2D data" );
        console.log( data );
        z_data= data;

    });
    //Get x axis
    $.getJSON( '/benchmark/fidelity/getJson_plotAxis',
    {   plot1D_axisType: JSON.stringify('x_value'), },
        function (data) {
        console.log( "Get x axis" );
        x_axis = data;
    });
    //Get y axis
    $.getJSON( '/benchmark/fidelity/getJson_plotAxis',
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

    let plotID_2D = "fidelity-plot2D-rawOverview";
    let plotID_1D_ampPhase = "fidelity-plot1D-ampPhase";
    let plotID_1D_IQ = "fidelity-plot1D-IQ";
    $.ajaxSettings.async = false;
    let htmlInfo=get_htmlInfo_python();

    let selectType = document.getElementById("fidelity-plot2D-ySelector").value;
    let selectValue = document.getElementById("fidelity-plot1D-y_value").value;

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
    $.getJSON( '/benchmark/fidelity/getJson_plotAxis',
    {   plot1D_axisType: JSON.stringify('x_value'), },
        function (data) {
        console.log( "Get x axis" );
        plotData_AmpPhase["raw"]["x"]= data;
    });
    //Get fitted x axis
    $.getJSON( '/benchmark/fidelity/getJson_plotAxis',
    {   plot1D_axisType: JSON.stringify('x_value_fit'), },
        function (data) {
        console.log( "Get x axis" );
        plotData_AmpPhase["fitted"]["x"]= data;
    });
    //Get raw signal
    $.getJSON( '/benchmark/fidelity/getJson_plot1D',
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
    $.getJSON( '/benchmark/fidelity/getJson_plot1D',
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

function FD_fit_data(){

    // Plot fit parameters
    $.getJSON( '/benchmark/fidelity/getJson_fitParaPlot',{ }, function (data) {});
}

function FD_pretrain_data(){

    // Plot fit parameters
    $.getJSON( '/benchmark/fidelity/getJson_Pretrain',{ }, function (data) {});
}

function FD_plot_data(){

    // Plot fit parameters
    $.getJSON( '/benchmark/plot',{ }, function (data) {});
}
