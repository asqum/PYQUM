



$(document).ready(function(){
    // $('div.qestimatecontent').show();
    console.log( "DECOHERENCE JS" );
    render_Decoherence ();
});


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
    let axisIndex=new Array(1);
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

            if ( document.getElementById("plot_type-"+htmlName).value == "y_value" )
            {
                console.log(htmlName +" for y-axis ");
                axisIndex[axisIndex.length] = structurePosition ;
                valueIndex[i]=document.getElementById("select_value-"+htmlName).selectedIndex;
                
            }
            if( document.getElementById("plot_type-"+htmlName).value == "x_value" ){
                console.log(htmlName +" for x-axis ");
                axisIndex[0] = structurePosition ;
                valueIndex[i]=0;

            }
            if( document.getElementById("plot_type-"+htmlName).value == "single_value" ){
                console.log(htmlName +" select single value ");
                valueIndex[i]=document.getElementById("select_value-"+htmlName).selectedIndex;

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

function render_Decoherence ()
{

    $.ajaxSettings.async = false;

    let measureParameters = document.getElementById("qFactor-parameters");



    let htmlInfo = [];
    $.getJSON( '/benchmark/get_parametersID', 
    {},
        function (data) {
            htmlInfo = data;
    });
    console.log( htmlInfo );
    for(i = 0; i < htmlInfo.length; i++) {
        let DOM_parameterSetting = document.createElement("div");
        DOM_parameterSetting.setAttribute("class", "measurePara");
        measureParameters.appendChild(DOM_parameterSetting);


        let parameterName = htmlInfo[i]["name"]
        console.log(i, parameterName);
        let DOM_parameterName = document.createElement("label");
        DOM_parameterName.innerHTML = parameterName;
        DOM_parameterName.setAttribute("class", "measureParaSelect");

        DOM_parameterSetting.appendChild(DOM_parameterName);
        // Create parameters information and plot selection
        if (htmlInfo[i]["length"] == 1) // The parameter only have one value
        {
            let DOM_parameterCOrder = document.createElement("p");
            DOM_parameterCOrder.innerHTML = htmlInfo[i]["c_order"];
            DOM_parameterCOrder.setAttribute("class", "measureCOrder");

            DOM_parameterSetting.appendChild(DOM_parameterCOrder);

        }
        else{ // The parameter number > 1
            let DOM_parameterPlotTypeSelector = document.createElement("select");
            DOM_parameterPlotTypeSelector.id = "plot_type-"+parameterName;
            DOM_parameterPlotTypeSelector.setAttribute("class", "measureParaSelect");
            DOM_parameterSetting.appendChild(DOM_parameterPlotTypeSelector);

            let plotType = ["single value","x axis - value","y axis - value","y axis - count"];
            let plotTypeValue = ["single_value","x_value","y_value","y_count"];

            for( ipt=0; ipt<plotType.length; ipt++)
            {
                let DOM_parameterPlotType = document.createElement("option");
                DOM_parameterPlotType.innerHTML = plotType[ipt];
                DOM_parameterPlotType.setAttribute("value", plotTypeValue[ipt]);
                DOM_parameterPlotTypeSelector.appendChild(DOM_parameterPlotType);
            }



            if ( htmlInfo[i]["length"]<50 ){
                let DOM_parameterValueSelector = document.createElement("select");
                DOM_parameterValueSelector.id = "select_value-"+parameterName;
                DOM_parameterValueSelector.setAttribute("class", "measureParaSelect");
                DOM_parameterSetting.appendChild(DOM_parameterValueSelector);
                let parameterValue;
                console.log(parameterName, " Selector ");

                $.getJSON( '/benchmark/get_parameterValue',
                {   parameterKey: parameterName,},
                    function (data) {
                    parameterValue=data;
                });
                for ( iv=0; iv<parameterValue.length; iv++)
                {
                    let DOM_parameterValue = document.createElement("option");
                    DOM_parameterValue.innerHTML = parameterValue[iv];
                    
                    DOM_parameterValueSelector.appendChild(DOM_parameterValue);
                }
            }else{
                let DOM_parameterValueInput = document.createElement("input");
                DOM_parameterValueInput.setAttribute("class", "measureParaSelect");
                DOM_parameterSetting.appendChild(DOM_parameterValueInput);

            }


        }

    }

    $.ajaxSettings.async = true;


}