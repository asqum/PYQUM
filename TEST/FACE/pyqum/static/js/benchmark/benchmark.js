//when page is loading:

$(document).ready(function(){
    console.log( "BENCHMARK JS" );
    //compensating what base.js cannot do
    $('.navbar button').removeClass('active');
    $('.navbar button.benchmark').addClass('active');
    $('button#measurement_info-tab').toggleClass('active'); // default show-up of 'qestimate' content is set by benchmark.css
});

function benchmark_encryption() {
    return '/' +'ghhgjadz';
};

function openTab(evt, Name) {
    // Declare all variables
    console.log('Tab: ' + Name );

    var i, tabcontent, tablinks;



    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }


    // Show the current tab, and add an "active" class to the link that opened the tab
    document.getElementById(Name).style.display = "block";
    evt.currentTarget.className += " active";
    register_Quantification(Name);
} 
function get_htmlInfo_python(){
    let htmlInfo;
    $.getJSON( '/benchmark/get_parametersID', 
    {},
        function (data) {
            htmlInfo = data;
    });
    return htmlInfo
}

function register_Quantification(quantificationType){
    $.getJSON( '/benchmark/register_Quantification', 
    {
        quantificationType: JSON.stringify(quantificationType),
    },
        function (data) {
            console.log( "quantification register " +data );
    });
    return quantificationType
}

function get_selectInfo( quantificationType ){

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
            if ( plotType == "y_value" )
            {
                console.log(htmlName +" for y-axis ");
                axisIndex[axisIndex.length] = structurePosition ;
                valueIndex[i]=document.getElementById(quantificationType+"-select_value-"+htmlName).selectedIndex;
                
            }
            if( plotType == "x_value" ){
                console.log(htmlName +" for x-axis ");
                axisIndex[0] = structurePosition ;
                valueIndex[i]=0;
            }
            if( plotType == "single_value" ){
                console.log(htmlName +" select single value ");
                valueIndex[i]=document.getElementById(quantificationType+"-select_value-"+htmlName).selectedIndex;
            }

            if( plotType == "average" ){
                console.log(htmlName +" select average");
                valueIndex[i] = 0;
                aveAxisIndex.push(structurePosition);
                aveRange = document.getElementById(quantificationType+"-ave_value-"+htmlName).value;
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

function render_selection ( quantificationType )
{

    $.ajaxSettings.async = false;

    let measureParameters = document.getElementById(quantificationType+"-parameters");



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



        // Create parameters information and plot selection
        if (htmlInfo[i]["length"] > 1) // The parameter only have one value
        {

            // Create parameter name
            let DOM_parameterName = document.createElement("label");
            DOM_parameterName.innerHTML = parameterName;
            DOM_parameterName.setAttribute("class", "measureParaSelect");
            DOM_parameterSetting.appendChild(DOM_parameterName);

            // Create c-order string
            let DOM_parameterCOrder = document.createElement("p");
            DOM_parameterCOrder.innerHTML = htmlInfo[i]["c_order"];
            DOM_parameterCOrder.setAttribute("class", "measureCOrder");

            DOM_parameterSetting.appendChild(DOM_parameterCOrder);


            let DOM_parameterPlotTypeSelector = document.createElement("select");
            DOM_parameterPlotTypeSelector.id = quantificationType+"-plot_type-"+parameterName;
            DOM_parameterPlotTypeSelector.setAttribute("class", "measureParaSelect");
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


            // Create parameter selection
            if ( htmlInfo[i]["length"]<500 ){
                let DOM_parameterValueSelector = document.createElement("select");
                DOM_parameterValueSelector.id = quantificationType+"-select_value-"+parameterName;
                DOM_parameterValueSelector.setAttribute("class", "measureParaSelect");
                //DOM_parameterValueSelector.setAttribute("onchange", "myFunction()");
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

            // Create average input
            let DOM_parameterAve = document.createElement("input");
            DOM_parameterAve.id = quantificationType+"-ave_value-"+parameterName;
            DOM_parameterAve.setAttribute("class", "measureParaSelect");
            DOM_parameterSetting.appendChild(DOM_parameterAve);
            
        }


    }

    $.ajaxSettings.async = true;


}


function plot1D ( data, axisKeys, plotId ){
    console.log("Plotting 1D");
    let traceNumber = axisKeys.y.length;
    console.log(axisKeys.x);
    console.log(axisKeys.y);
    console.log(axisKeys.yrr);
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
    console.log( "x axis: " +axisKeys.x );

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