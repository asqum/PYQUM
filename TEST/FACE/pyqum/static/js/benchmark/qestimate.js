$(document).ready(function(){
    // $('div.qestimatecontent').show();
    console.log( "QESTIMATE JS" );
    
});
var gAxisIndex = [4];

function get_selectAxis(){
    $.getJSON( '/benchmark/get_parametersID', {

    }, function (htmlIDs) {
        var valueIndex = new Array(htmlIDs.length);
        var axisIndex = [4];
        var isSameAxis = axisIndex == gAxisIndex;
        if ( !isSameAxis ){
            for ( i in htmlIDs) {
                if ( htmlIDs[i] != "Frequency" ){
    
                    valueIndex[i] = document.getElementById("select-"+htmlIDs[i]).selectedIndex
                    if ( document.getElementById("check-"+htmlIDs[i]).checked && axisIndex.length<2 )
                    {
                        axisIndex[axisIndex.length]= i ;
                        console.log( "htmlIDs: " +htmlIDs[i]+" is check "+document.getElementById("check-"+htmlIDs[i]).checked+ axisIndex.length+"i"+i );
                    }
                }else{
                    valueIndex[i]=0
                }
            }
        }
        console.log( "value indeice: " +valueIndex );
        console.log( "dimension: " +axisIndex.length );
        console.log( "axis index: " +axisIndex );
        gAxisIndex = axisIndex;
    });

    return axisIndex != gAxisIndex
}

function plot1D ( data, xKeys, yKeys, plotId ){
    console.log("Plotting 1D");
    var traceNumber = yKeys.length;
    var tracies = new Array(traceNumber);
    var ix;
    for (var i = 0; i < traceNumber; i++){
        if ( xKeys.length != 1 ){
            ix = i
        }else{
            ix = 0
        }
        tracies[i] = {
        x: data[xKeys[ix]],
        y: data[yKeys[i]],
        mode: 'markers',
        type: 'scatter'
        };
    }


    Plotly.newPlot(plotId, tracies, layout, {showSendToCloud: true});
}

function plot2D( data, plotId) {
    console.log("Plotting 2D");
    console.log( "x length: " +data.x.length );

    // Frame assembly:
    var trace = {
        z: data.z, 
        x: data.x, 
        y: data.y, 
        zsmooth: 'best',
        mode: 'lines', 
        type: 'heatmap',
        width: 2.5
    };
    
    console.log("1st z-trace: " + trace.z[0][0]);

    // Plotting the Chart using assembled TRACE:
    var Trace = [trace]
    Plotly.newPlot(plotId, Trace, {showSendToCloud: true});
};


// assemble 2D-data based on c-parameters picked
$(function () {
    $('#qFactor-plot-button').on('click', function () {


            if (axisIndex.length<=2)
            {
                $.getJSON( '/benchmark/qestimate/plot',
                {   valueIndex: JSON.stringify(valueIndex),
                    axisIndex: JSON.stringify(axisIndex) }, 
                    function (data) {
                    console.log( data );

                    plot2D(data, "qFactor-plot-Overview2D");

                    currentData={
                        x: data.x,
                        y: data.z[valueIndex[axisIndex[1]]],
                        xtitle: data.xtitle,
                        ytitle: data.ytitle
                    };

                    plot1D(currentData,["x"],["y"], "qFactor-plot-fittingResult");
                    
                });
            }else{
                console.log( "Too many axis." );
            }
        

    });
    return false;
});
$(function () {
    $('#qFactor-fit-button').on('click', function () {



        var fittingRangeFrom = document.getElementById("qFactor-fittingRange-from").value
        var fittingRangeTo = document.getElementById("qFactor-fittingRange-to").value

        console.log( "fit from " + fittingRangeFrom + " to ",  fittingRangeTo);
        $.getJSON( '/benchmark/qestimate/fitting',{  
            fittingRangeFrom:fittingRangeFrom, fittingRangeTo:fittingRangeTo  
        }, function (data) {
            console.log( Object.keys(data) );
            console.log( data );

            plot1D( data, ["Power"], ["Qc_dia_corr","Qi_dia_corr","fr"], "qFactor-plot-fittingParameters");
        });



    });
    return false;
});

