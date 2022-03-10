


$(document).ready(function(){
    // $('div.qestimatecontent').show();
    PD_render_input("populationDistribution");
    console.log( "Load popuplation" );

    let e_loadButton = document.getElementById("populationDistribution-button-load");
    e_loadButton.addEventListener("click", PD_load_data);
    let e_fitButton = document.getElementById("populationDistribution-projection-button");
    e_fitButton.addEventListener("click", plot_projectionLine);
    let e_plot1DButton = document.getElementById("populationDistribution-analysis-button");
    e_plot1DButton.addEventListener("click", plot_distribution);
    // let e_plot2DtButton = document.getElementById("populationDistribution-plot2D-button");
    // e_plot2DtButton.addEventListener("click", get_PD_plot2D);
});

function get_PD_selectInfo( quantificationType ){

    $.ajaxSettings.async = false;

    let htmlInfo = get_htmlInfo_python();
    let axisIndex=new Array(1);
    let valueIndex=new Array(htmlInfo.length);

    let aveAxisIndex=[];
    let aveRange;

    let oneShotAxisIndex=[];

    
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
                    console.log(htmlName +" for y-axis");
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

                case "one_shot":
                    console.log(htmlName +" select one_shot");
                    valueIndex[i] = 0;
                    oneShotAxisIndex.push(structurePosition);
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
        }
    }


    console.log( "Selection " );
    console.log( analysisIndex );
    $.ajaxSettings.async = true;

    return analysisIndex
}


function PD_render_input ( quantificationType )
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
            DOM_parameterPlotTypeSelector.setAttribute("onchange", "PD_showAveInput(this)");
            DOM_parameterSetting.appendChild(DOM_parameterPlotTypeSelector);

            // Create plot selection
            let plotType = ["single value","x axis - value","average","one shot"];
            let plotTypeValue = ["single_value","x_value","average","one_shot"];
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
    // PD_creatDOM_FitDataType("all", "populationDistribution-allParamater");
    $.ajaxSettings.async = true;
}

function PD_showAveInput(selectObject) {
    let DOM_parameterSetting=selectObject.parentElement;
    console.log("showAveInput trigger by "+selectObject.id)
    let DOM_parameterAve = DOM_parameterSetting.getElementsByClassName("ave_value")[0];
    DOM_parameterAve.style.display = "none";

    let DOM_parameterValueSelect = DOM_parameterSetting.getElementsByClassName("select_value")[0];
    DOM_parameterValueSelect.style.display = "none";

    let DOM_parameterValueInput = DOM_parameterSetting.getElementsByClassName("input_value")[0];
    DOM_parameterValueInput.style.display = "none";


    switch(selectObject.value){
        case "one_shot":
            console.log("select "+selectObject.value)
            break;
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

function PD_creatDOM_pString( newID, parentID, string  ){
    // Creat select for parameter plot type
    console.log( "CF_creatDOM_FitDataType" );
    let parentDOM = document.getElementById( parentID );

    let DOM_p = document.createElement("p");
    DOM_p.id = parentID+newID;
    DOM_p.innerHTML = string;
    parentDOM.appendChild(DOM_p);
}

function PD_load_data(){
    console.log( "Get data" );

    $.ajaxSettings.async = false;
    let analysisIndex = get_PD_selectInfo("populationDistribution");

    //Send information to python
    $.getJSON( '/benchmark/populationDistribution/load',
        {   quantificationType: JSON.stringify("populationDistribution"), 
            analysisIndex: JSON.stringify(analysisIndex), 
        },
        function (data) {
        console.log( "load data" );
    });
    if ( analysisIndex.axisIndex.length == 2 ){
        get_PD_plot2D();
    }else{
        plot_projectionLine();
    }    
    $.ajaxSettings.async = true;
}

function get_PD_plot2D(){
    console.log( "Plot data" );

    let plotID_2D = "populationDistribution-plot2D-rawOverview";
    let plotID_1D_ampPhase = "populationDistribution-plot1D-ampPhase";
    let plotID_1D_IQ = "populationDistribution-plot1D-IQ";
    $.ajaxSettings.async = false;
    let htmlInfo=get_htmlInfo_python();


    let plot2D_signalType = document.getElementById("populationDistribution-plot2D-zSelector").value;
    let plot1D_yAxisType = document.getElementById("populationDistribution-plot2D-ySelector").value;

    console.log( "plot2D_signalType" );

    console.log( plot2D_signalType );
    let z_data;
    let y_axis=[];
    let x_axis=[];

    //Get 2D data
    $.getJSON( '/benchmark/populationDistribution/getJson_plot2D',
    {   plot2D_signalType: JSON.stringify(plot2D_signalType), },
        function (data) {
        console.log( "Get 2D data" );
        console.log( data );
        z_data= data;

    });
    //Get x axis
    $.getJSON( '/benchmark/populationDistribution/getJson_plotAxis',
    {   plot1D_axisType: JSON.stringify('x_value'), },
        function (data) {
        console.log( "Get x axis" );
        x_axis = data;
    });
    //Get y axis
    $.getJSON( '/benchmark/populationDistribution/getJson_plotAxis',
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


function plot_projectionLine(){
    $.ajaxSettings.async = false;

    let plotID_1D_IQ = "populationDistribution-plot1D-IQ";
    let accInd = document.getElementById("populationDistribution-plot1D-accumulate").value;
    
    console.log( "fit_projectionLine" );
    let projectionLine = {
        accumulationIndex:accInd,
    }
    
    console.log(projectionLine);
    let plotData_IQ = {};

    let axisKeys_fitResult= {};
    // get accumulated data for projection line
    $.getJSON( '/benchmark/populationDistribution/getJson_plotProjection',{ 
        process: JSON.stringify("raw"),
        projectionLine: JSON.stringify(projectionLine),
    }, function (data) {
        console.log("fitResult");
        console.log(data);
        plotData_IQ["rawI"]= data["I"];
        plotData_IQ["rawQ"]= data["Q"];

    });
    // get projection line data and parameters
    let DOM_printCenter = document.getElementById("populationDistribution-clusterCenter-data" )
    $.getJSON( '/benchmark/populationDistribution/getJson_plotProjection',
    {   process: JSON.stringify("fitted"),
        projectionLine: JSON.stringify(projectionLine),
    }, function (data) {
        console.log("fitted");
        console.log(data);
        plotData_IQ["fittedI"]= data["I"];
        plotData_IQ["fittedQ"]= data["Q"];

    }).done(function(data) {
        DOM_printCenter.innerHTML(data["I"].toString());
    }).fail(function(jqxhr, textStatus, error){
        DOM_printCenter.innerHTML("Oops.. Something went wrong!");
    });

    let iqKeys = {
        x: ["rawI","fittedI"],
        y: ["rawQ","fittedQ"],
        yErr: [],
    }

    console.log("fitResult plot");
    console.log(axisKeys_fitResult);

    plot1D(plotData_IQ, iqKeys, plotID_1D_IQ);
    document.getElementById(plotID_1D_IQ).style.display = "block";
    
    $.ajaxSettings.async = true;

}

function plot_distribution(){
    $.ajaxSettings.async = false;

    let plotID_1D_dist = "populationDistribution-plot1D-distribution";
    
    console.log( "plot_distribution" );

    
    let plotData_dist = {};

    let axisKeys_fitResult= {};
    // get accumulated data for projection line
    $.getJSON( '/benchmark/populationDistribution/getJson_plotDistribution',{ 
        process: JSON.stringify("raw"),
    }, function (data) {
        console.log("fitResult");
        console.log(data);
        plotData_dist["x"]= data["x"];
        plotData_dist["data"]= data["data"];
        plotData_dist["fit"]= data["fit"];

    });
 

    let distKeys = {
        x: ["x"],
        y: ["data","fit"],
        yErr: [],
    }

    console.log("fitResult plot");
    console.log(axisKeys_fitResult);

    plot1D(plotData_dist, distKeys, plotID_1D_dist);
    document.getElementById(plotID_1D_dist).style.display = "block";
    
    $.ajaxSettings.async = true;

}

