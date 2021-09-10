


$(document).ready(function(){
    // $('div.qestimatecontent').show();
    render_selection("qEstimation");
    console.log( "Load qEstimation" );

});


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
        let plotID_2D = "qFactor-plot2D-rawOverview";
        let plotID_1D_ampPhase = "qFactor-plot1D-ampPhase";
        let plotID_1D_IQ = "qFactor-plot1D-IQ";
        console.log( "plot!!" );
        $.ajaxSettings.async = false;
        let htmlInfo=get_htmlInfo_python();
        let analysisIndex = get_selectInfo("qEstimation");
        if ( analysisIndex.axisIndex.length == 2 ){
            $.getJSON( '/benchmark/qestimate/getJson_plot',
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


        $.getJSON( '/benchmark/qestimate/getJson_plot',
        {   quantificationType: JSON.stringify("qEstimation"), 
            analysisIndex: JSON.stringify(analysisIndex), 
            plotType: JSON.stringify("1D_amp"), },
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
        {   quantificationType: JSON.stringify("qEstimation"), 
            analysisIndex: JSON.stringify(analysisIndex),
            plotType: JSON.stringify("1D_IQ"), },
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
        let analysisIndex = get_selectInfo("qEstimation");

        console.log( "Fit plot" );
        console.log( analysisIndex );
        let xAxisKey = htmlInfo[analysisIndex.axisIndex[0]]["name"];
        let fitRange = document.getElementById("qEstimation"+"-fitting_input-"+xAxisKey).value;




        let baseline_correction = document.getElementById("qFactor-fit-baseline-correct").checked;
        let baseline_smoothness = document.getElementById("qFactor-fit-baseline-smoothness").value;
        let baseline_asymmetry = document.getElementById("qFactor-fit-baseline-asymmetry").value;
        let gain = document.getElementById("qFactor-fit-gain").value;

        let fitParameters = {
            range: {
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
        $.getJSON( '/benchmark/qestimate/getJson_fitParaPlot',{  
            fitParameters: JSON.stringify(fitParameters),
            analysisIndex: JSON.stringify(analysisIndex), 
        }, function (data) {
            if (analysisIndex.axisIndex.length == 1) { xAxisKey = "Single_plot" }
            //if ( xAxisKey == "Power" ) { xAxisKey = "power_corr" }
            console.log("fitResult");
            console.log(data);           
            let axisKeys_fitResult = {
                x: [xAxisKey],
                y: ["Qc_dia_corr", "Qi_dia_corr", "Ql", "fr"],
                yErr: ["absQc_err", "Qi_dia_corr_err", "Ql_err", "fr_err"],
            }
            let plotdata = Object.assign({}, data["results"], data["errors"]);

            plot1D( plotdata, axisKeys_fitResult, "qFactor-plot-fittingParameters");

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

