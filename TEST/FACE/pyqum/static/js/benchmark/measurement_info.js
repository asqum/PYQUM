

$(document).ready(function(){
    // $('div.qestimatecontent').show();
    console.log( "MEASUREMENTINFO JS" );
    render_measurementInfo();
});


function render_measurementInfo ()
{

    $.ajaxSettings.async = false;

    let measureParameters = document.getElementById("info-parameters");



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

        // Create parameter name
        let DOM_parameterName = document.createElement("label");
        DOM_parameterName.innerHTML = parameterName;
        DOM_parameterName.setAttribute("class", "measureParaSelect");
        DOM_parameterSetting.appendChild(DOM_parameterName);

        // Create parameters information and plot selection

        let DOM_parameterCOrder = document.createElement("p");
        DOM_parameterCOrder.innerHTML = htmlInfo[i]["c_order"];
        DOM_parameterCOrder.setAttribute("class", "measureCOrder");

        DOM_parameterSetting.appendChild(DOM_parameterCOrder);


    }

    $.ajaxSettings.async = true;


}


