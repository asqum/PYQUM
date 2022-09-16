$(document).ready(function(){
    var dark = document.getElementById("dmbutton");
    dark.addEventListener('click' , darkMode);
    //start auto measurement
    var MS_process = document.getElementById("Start-measure-but");
    MS_process.addEventListener('click' , start_measure);
    //hash to the MS window
    var showcontent_MS = document.getElementById("showcontent-MS");
    showcontent_MS.addEventListener('click' , show_content_MS);
    //refresh all the html
    var refresh= document.getElementById("refresh");
    refresh.addEventListener('click' , reset_address);
    var search_process = document.getElementById("search-jobid");
    search_process.addEventListener('click' ,gaussian_fitting );//gaussian_fitting
    // 畫出baseline
    var fig_CS = document.getElementById("CS-search");
    fig_CS.addEventListener('click' , get_plot1D_CS);
    //根據選項畫出cavities
    var cavities_CS = document.getElementById("looks-CS");
    cavities_CS.addEventListener('click' , show_cavities);
    // 顯示量測參數
    var showpara_CS = document.getElementById("sp-CS");
    showpara_CS.addEventListener('click' , function(){show_paras("CS");});

    //顯示內文
    var showcontent_CS = document.getElementById("showcontent-CS");
    showcontent_CS.addEventListener('click' , function(){show_content("showcontent-CS","CS-content");});
    // 畫出baseline
    var fig_PD = document.getElementById("PD-search");
    fig_PD.addEventListener('click' , get_plot2D_PD);
    var showpara_PD = document.getElementById("sp-PD");
    showpara_PD.addEventListener('click' , function(){show_paras("PD");});
    var showcontent_PD = document.getElementById("showcontent-PD");
    showcontent_PD.addEventListener('click' , function(){show_content("showcontent-PD","PD-content");});
    // 畫出baseline
    var fig_FD = document.getElementById("FD-search");
    fig_FD.addEventListener('click' , get_plot2D_FD);
    var showpara_FD = document.getElementById("sp-FD");
    showpara_FD.addEventListener('click' , function(){show_paras("FD");});
    var showcontent_FD = document.getElementById("showcontent-FD");
    showcontent_FD.addEventListener('click' , function(){show_content("showcontent-FD","FD-content");});
    var fig_cw = document.getElementById("CW-search");
    fig_cw.addEventListener('click' , get_plot1D_CW);
    var showpara_CW = document.getElementById("sp-CW");
    showpara_CW.addEventListener('click' , function(){show_paras("CW");});
    //顯示內文
    var showcontent_CW = document.getElementById("showcontent-CW");
    showcontent_CW.addEventListener('click' , function(){show_content("showcontent-CW","CW-content");});
    // 生成初始xypower選項
    var xypowa_generator = document.getElementById("showcontent-CW");
    xypowa_generator.addEventListener('click' , function(){xypowa_options_generator(mode='initialize');});
    // 改變xypower選項
    var xypower_switcher = document.getElementById("cavity-select-CW");
    xypower_switcher.addEventListener('change' , function(){xypowa_options_generator(mode='switch');});
});




//--------------------Global functions-------------------------
function log_print(text){
    var log = document.getElementById("progress_report_block");
    log.innerHTML = text;
}

// generate the spans in results with div tag input a dictionary  (naked check OK)
function generate_result_span(){  
    results = cavities_plot;
  // get the selector in the body
    let dm_mode = document.getElementById("dmbutton").value;
    let cavity = Object.keys(results);     // cavity freq list ['5487 MHz',...];
    let result_block = document.getElementById("result");
    result_block.innerHTML = "";
  // generate the options in the select
    for(let ipt=0; ipt<cavity.length; ipt++){
        let div = document.createElement("div");
        div.innerHTML = cavity[ipt]+": "+final_result_set['PD'][cavity[ipt]]+","+final_result_set['FD'][cavity[ipt]]+","+final_result_set['CW'][cavity[ipt]];
        div.setAttribute('value','result'+cavity[ipt]);//String(Number(result_keys[ipt])*1000)+' MHz'
        result_block.appendChild(div);
    };
    if(dm_mode==0){
      result_block.style.backgroundColor = "rgb(248, 218, 218)";
      result_block.style.color = "#000";
    }else{
      result_block.style.backgroundColor = "rgba(37, 37, 37, 0.369)";
      result_block.style.color = "rgb(225, 255, 0)";
    };
    result_block.style.display="block"
};



// 開關深色模式
// Dark Mode
function darkMode() {
    let element = document.body;
    element.classList.toggle("dark-mode");
    if(document.getElementById('dmbutton').value=='0'){
        document.getElementById('dmbutton').setAttribute('value','1');
    }else{
        document.getElementById('dmbutton').setAttribute('value','0');
    };
    dark_plot();
    if(document.getElementById('search-jobid').value==='1'){
        generate_result_span(cavities_plot); 
    };
};

function dark_plot(){
    const ids=['CS-search','PD-search','FD-search','CW-search'];
    for(let i=0;i<ids.length;i++){
        let plotnum = document.getElementById(ids[i]).value;
        if(plotnum=='1'){
            if(i==0){
                get_plot1D_CS();
            }else if(i==1){
                get_plot2D_PD();
            }else if(i==2){
                get_plot2D_FD();
            }else{
                get_plot1D_CW();
            };
        }else if(plotnum==2){
            show_cavities();
        }else{
        
        }
    };
};

function show_content(but_id,content_id){
    let content_value = document.getElementById(but_id).value;
    if(content_value=="0"){
        document.getElementById(but_id).setAttribute('value',"1");
        document.getElementById(content_id).style.display='block';
        window.location.hash = "#"+content_id;
    }else{
        window.location.hash = "#"+content_id;
    };
};

//重置量測參數
function reset_paras(where){
    document.getElementById('Freqrange-'+where).innerHTML = '';
    document.getElementById('Powrange-'+where).innerHTML = '';
    document.getElementById('Fluxrange-'+where).innerHTML = '';
    document.getElementById('IFBW-'+where).innerHTML = '';
    document.getElementById('XYFreqrange-'+where).innerHTML = '';
    document.getElementById('XYPowrange-'+where).innerHTML = '';
};

function reset_address(){
    history.pushState("", document.title, window.location.pathname);
    history.go(0);
};



//-----------------Measurement settings-------------------


// results container
var final_result_set = {};


// measurement settings
var dc_ch = '1';
var port = 'S21,';
// work independently
function start_measure(){
    
    dc_ch = document.getElementById('dc-channel-inp').value;
    port = document.getElementById('port-inp').value;
    designed = document.getElementById('CPw-num-inp').value;

    // connect to autoscan1Q2js.py
    log_print("Start Measurement by Bot ")
    $.getJSON( '/autoscan1Q/measurement',{  
        dc_channel: JSON.stringify(dc_ch),
        inout_port: JSON.stringify(port), 
        designed: JSON.stringify(designed),
    }, function (measure_result) {   //need to check this is correct or not
        final_result_set = measure_result;
        log_print( "Measurement finish!" );
    });
    // ToSolve: How to show the results on the html?
    //gaussian_fitting();
}


function show_content_MS(){
    window.location.hash = "#MS-content";
}

//---------------------Search JOBID--------------------------
// do first 


var CS_jobid = 0;
var PD_jobids = {}; //{'5487 MHz':5050,...}
var FD_jobids = {}; // smae above
var CW_jobids = {}; // same above


function search_jobids(){
    log_print("JOBIDs Loading...");
    $.getJSON( '/autoscan1Q/get_jobid',{  
    }, function (JOBIDs){
        CS_jobid = JOBIDs['CavitySearch']
        PD_jobids = JOBIDs['PowerDepend']
        FD_jobids = JOBIDs['FluxDepend']
        CW_jobids = JOBIDs['QubitSearch'] 
    });
    log_print("Results Loading...");
    $.getJSON( '/autoscan1Q/get_results',{  
    }, function (results){
        final_result_set = results;
    });
    genopt (PD_jobids);
    document.getElementById('search-jobid').setAttribute('value','1')
};

var cavities_plot = {};
var CS_overview = {};

function gaussian_fitting(specific_jobid=""){
    if (specific_jobid===""){
        search_jobids();
        let spinner = document.getElementById("spinner");
        log_print("Start Gaussian fitting wait plz...");
        let where = "CS";
        spinner.style.visibility = "visible";
        spinner.style.opacity = '1';
        $.getJSON( '/autoscan1Q/plot_result',{  
            measurement_catagories : JSON.stringify(where),
            specific_jobid : JSON.stringify(String(CS_jobid))   //CS_jobid"5108"

        }, function (plot_items) {   //need to check this is correct or not
            cavities_plot = plot_items['plot_items'];
            CS_overview = plot_items['overview'];
            genopt (cavities_plot);
        })
        .done(function(plot_items) {
            spinner.style.visibility = "hidden";
            spinner.style.opacity = '0';
            log_print("Gaussian fitting finish!");
            generate_result_span();
        })
        .fail(function(jqxhr, textStatus, error){
            spinner.style.visibility = "hidden";
            spinner.style.opacity = '0';
            log_print("Somewhere missing...");
            alert("Gaussian fitting mixing!");
        });
    }else{
        let spinner = document.getElementById("spinner");
        log_print("Start Gaussian fitting wait plz...");
        let where = "CS";
        spinner.style.visibility = "visible";
        spinner.style.opacity = '1';
        $.getJSON( '/autoscan1Q/plot_result',{  
            measurement_catagories : JSON.stringify(where),
            specific_jobid : JSON.stringify(String(specific_jobid))   //CS_jobid"5108"

        }, function (plot_items) {   //need to check this is correct or not
            cavities_plot = plot_items['plot_items'];
            CS_overview = plot_items['overview'];
            genopt (cavities_plot);
        })
        .done(function(plot_items) {
            spinner.style.visibility = "hidden";
            spinner.style.opacity = '0';
            log_print("Gaussian fitting finish!");
            generate_result_span();
        })
        .fail(function(jqxhr, textStatus, error){
            spinner.style.visibility = "hidden";
            spinner.style.opacity = '0';
            log_print("Somewhere missing...");
            alert("Gaussian fitting mixing!");
        });
    }
}



//-----------------CavitySearch---------------------------



// generate the options in the select id
function generate_options(id,data,cata){
    // get the selector in the body
      let CavitySelect = document.getElementById(id); 
      let result_keys =  Object.keys(data)
      const opt_num = Object.keys(data).length

    // generate the options in the select
      for(let ipt=0; ipt<opt_num; ipt++){
          let option = document.createElement("option");
          option.innerHTML = result_keys[ipt];
          option.setAttribute('value',cata+result_keys[ipt]);//value = CS-5487 MHz
          CavitySelect.appendChild(option);
        };
};


// after we have the cavities, generate the correspond options in the next steps which needs to select the cavity.
function genopt (data) {
    let selectors = ['cavity-select-CS','cavity-select-PD','cavity-select-FD','cavity-select-CW']
    let catagories = ['CS-','PD-','FD-','CW-']
    const detected_num = Object.keys(data).length;
    if(detected_num>0){
        for(let i=0;i<selectors.length;i++){
            document.getElementById(selectors[i]).options.length = 0; //清除舊options
            generate_options(selectors[i],data,catagories[i]);
        };   
    }else{
        alert("WARNING!!\nNo cavity is detected!");
    };   
};


// plot search result
function plot1D_2y_CS ( data, axisKeys, plotId, modenum ){
   
    let groupNumber = axisKeys.x.length;
    let color_list= []
    let tracies = [];
    let ix;
    let yGroup = ["y","y2"];
    if(modenum=='0'){
        color_list=['#1f77b4','rgb(220 20 60)'];
    }else{
        color_list=['rgb(255,255,0)','rgb(255,0,255)'];
    };

    if(modenum=='0'){
        var layout = {
            plot_bgcolor:"rgb(252, 243, 223)",
            paper_bgcolor:'rgb(252, 243, 223)',
            title:{
                text:'Scan-Results',
                font:{
                    size:30
                }
            },
            xaxis:{
                title: {
                    text:'Frequency (GHz)',
                    font:{size:25}
                },
                tickfont:{size:25},
                zeroline: false,
                color:'rgb(0,0,0)'
            },
            yaxis: {
                title: {
                    text:'Amplitude (dBm)',
                    font:{size:25},  
                },
                zeroline: false,
                color: '#1f77b4'
            },
            yaxis2: {
                title: {
                    text:'UPhase',
                    font:{size:25}
                },
                zeroline: false,
                color: 'rgb(220 20 60)',
                overlaying:'y',
                side: 'right'
            },
            showlegend: true,
            hoverlabel:{font:{size:26}}
        };
    }else{
        var layout = {
            plot_bgcolor:"black",
            paper_bgcolor:'rgb(0,0,0)',
            title:{
                text:'Scan-Results',
                font:{
                    size:30,
                    color:'rgb(0,255,255)'
                }
            },
            xaxis:{
                title: {
                    text:'Frequency (GHz)',
                    font:{size:25}
                },
                zeroline: false,
                tickfont:{size:25},
                color: 'rgb(0,255,0)',
            },
            yaxis: {
                title: {
                    text:'Amplitude (dBm)',
                    font:{size:25},  
                },
                zeroline: false,
                color: 'rgb(255,255,0)',
            },
            yaxis2: {
                title: {
                    text:'UPhase',
                    font:{size:25}
                },
                color: 'rgb(255,0,255)',
                zeroline: false,
                overlaying:'y',
                side: 'right'
            },
            showlegend: true,
            legend:{font:{color:'rgb(0,255,0)'}},
            hoverlabel:{font:{size:26}}

        };
    }; 
    
    for ( gi=0; gi<groupNumber; gi++ ){
        let xKeysInGroup = axisKeys.x[gi];
        let yKeysInGroup = axisKeys.y[gi];

        let yNumberInGroup = yKeysInGroup.length;

        for (let i = 0; i < yNumberInGroup; i++){
            
            if ( xKeysInGroup.length != 1 ){
                ix = i
            }else{
                ix = 0
            };
            let newTrace = {
                x: data[axisKeys.x[gi][ix]],
                y: data[axisKeys.y[gi][i]],
                yaxis: yGroup[gi],
                name:String(yKeysInGroup), 
                mode: 'lines',
                line:{color:color_list[gi]}
            };
                
            tracies.push(newTrace);
        
        };
    };
    Plotly.newPlot(plotId, tracies, layout);
};


// plot the result of whole cavity 
function get_plot1D_CS(){
    log_print("Ploting Cavity baseline...");
    $.ajaxSettings.async = false;
    let specific_jobid = document.getElementById('jobid-CS').value;
    if (specific_jobid!==""){
        let modenum = document.getElementById('dmbutton').value;  // get darkmode or not
        
        const location_id = "CavitySearch-result-plot";
        let ampPhaseKeys = {
            x: [ ["Frequency"], ["Frequency"] ] ,
            y: [ ["Amplitude"],["UPhase"] ],
        };
        plot1D_2y_CS(CS_overview, ampPhaseKeys, location_id,modenum);
        const result = Object.keys(cavities_plot);
        document.getElementById('resultId-CS').innerHTML = 'Cavity @ : '+result;
        document.getElementById(location_id).style.display = "block";
        document.getElementById('CS-search').setAttribute('value','1');
        log_print("Ploting finish!");
    }else{
        gaussian_fitting(specific_jobid);
        let modenum = document.getElementById('dmbutton').value;  // get darkmode or not
        const location_id = "CavitySearch-result-plot";
        let ampPhaseKeys = {
            x: [ ["Frequency"], ["Frequency"] ] ,
            y: [ ["Amplitude"],["UPhase"] ],
        };
        plot1D_2y_CS(CS_overview, ampPhaseKeys, location_id,modenum);
        const result = Object.keys(cavities_plot);
        document.getElementById('resultId-CS').innerHTML = 'Cavity @ : '+result;
        document.getElementById(location_id).style.display = "block";
        document.getElementById('CS-search').setAttribute('value','1');
        log_print("Ploting finish!");
    };
};


// jump to cavities plot html
function show_cavities(){
    log_print("Ploting specific cavity...");
    let modenum = document.getElementById('dmbutton').value;
    let cavity = document.getElementById('cavity-select-CS').value.slice(3);
    let ampPhaseKeys = {
        x: [ ["Frequency"], ["Frequency"] ] ,
        y: [ ["Amplitude"],["UPhase"] ]
    };

    plot1D_2y_CS(cavities_plot[cavity], ampPhaseKeys, "CavitySearch-result-plot", modenum);
    document.getElementById("CavitySearch-result-plot").style.display = "block";
    document.getElementById('CS-search').setAttribute('value','2');
    log_print("Ploting cavity finish!");
};

//------------------PowerDependence-----------------------------------



function plot2D_PD( data, axisKeys, plotId, modenum ) {

    let paper = ''
    let color_x = ''
    let color_y = ''
    let color_z = ''
    let color_t = ''
    if(modenum=='0'){
        paper = "rgb(252, 243, 223)";
        color_x = "rgb(0,0,0)";
        color_y = "rgb(0,0,0)";
        color_z = "rgb(0,0,0)";
        color_t = 'rgb(0,0,0)';
    }else{
        paper = "rgb(0,0,0)";
        color_x = "rgb(0,255,0)";
        color_y = 'rgb(255,255,0)';
        color_z = 'rgb(255,0,255)'
        color_t = 'rgb(0,255,255)';
    };
    // Frame assembly:
    var trace = {
        z: data['heatmap'][axisKeys.z], 
        x: data['heatmap'][axisKeys.x], 
        y: data['heatmap'][axisKeys.y], 
        zsmooth: 'best',
        mode: 'lines', 
        type: 'heatmap',
        width: 2.5,
        colorbar:{
            automargin: true,
            tickfont:{color:color_z,size:25},
            title:{
                text:'Amplitude (dBm)',
                side:'right',
                font:{size:30,color:color_z}
            }
        },
    };
    var trace_scatter = { 
        x: data['scatter'][axisKeys.x], 
        y: data['scatter'][axisKeys.y2],
        mode:'markers',
        name:"Fr",
        line:{color:'#37A22F'}
    };
    var layout = {
        paper_bgcolor:paper,
        plot_bgcolor:paper,
        title:{
            text:'PowerDependence-Results',
            font:{
                size:30,
                color:color_t
            }
        },
        xaxis:{
            title: {
                text:'Power (dBm)',
                font:{size:25}
            },
            zeroline: false,
            color:color_x,
            tickfont:{size:25},
            automargin: true
        },
        yaxis: {
            title: {
                text:'Frequency (GHz)',
                font:{size:25},  
            },
            tickfont:{size:16},
            color: color_y,
            automargin: true
        },
        yaxis2: {
            
        },
        showlegend: false,
        hoverlabel:{font:{size:20}}
    };
    var Trace = [trace,trace_scatter]
    Plotly.newPlot(plotId, Trace,layout);
};




function get_plot2D_PD(){
    log_print("Ploting PowerDependence result...");
    let modenum = document.getElementById('dmbutton').value;  //darkmode or not
    let cavity = document.getElementById('cavity-select-PD').value.slice(3);
    const location_id = "PowerDep-result-plot";
    // check the column name of the dataframe
    let PDKeys = {
        x: [ "Power" ] ,
        y: [ "Frequency" ],
        y2:[ "Fr" ],
        z: [ "Amplitude" ]
    };
    $.ajaxSettings.async = false;
    let pd_plot = {};
    let where = "PD";
    $.getJSON( '/autoscan1Q/plot_result',{  
        measurement_catagories:JSON.stringify(where),
        specific_jobid : JSON.stringify(String(PD_jobids[cavity])),  //PD_jobids[cavity]5097
        target_cavity : JSON.stringify(cavity)
    }, function (plot_items) {   //need to check this is correct or not
        pd_plot = plot_items[cavity];
    });

    //make up the quantification output
    $.ajaxSettings.async = true;

    plot2D_PD(pd_plot, PDKeys, location_id, modenum);
    document.getElementById(location_id).style.display = "block";
    document.getElementById('PD-search').setAttribute('value','1');
    log_print("Ploting finish!");
};

//-------------------FluxDependence---------------------------------




function plot2D_FD( data, axisKeys, plotId, modenum ) {

    let paper = ''
    let color_x = ''
    let color_y = ''
    let color_z = ''
    let color_t = ''
    if(modenum=='0'){
        paper = "rgb(252, 243, 223)";
        color_x = "rgb(0,0,0)";
        color_y = "rgb(0,0,0)";
        color_z = "rgb(0,0,0)";
        color_t = 'rgb(0,0,0)';
    }else{
        paper = "rgb(0,0,0)"; 
        color_x = "rgb(0,255,0)";
        color_y = 'rgb(255,255,0)';
        color_z = 'rgb(255,0,255)'
        color_t = 'rgb(0,255,255)';
    };
    // Frame assembly:
    var trace = {
        z: data['heatmap'][axisKeys.z], 
        x: data['heatmap'][axisKeys.x], 
        y: data['heatmap'][axisKeys.y], 
        zsmooth: 'best',
        mode: 'lines', 
        type: 'heatmap',
        width: 2.5,
        colorbar:{
            tickfont:{color:color_z,size:25},
            automargin: true,
            title:{
                text:'Amplitude (dBm)',
                side:'right',
                font:{size:30,color:color_z}
            }
        },
    };
    var trace_scatter = { 
        x: data['scatter'][axisKeys.x], 
        y: data['scatter'][axisKeys.y2],
        mode:'markers',
        name:"Fr",
        line:{color:'#37A22F'}
    };
    var layout = {
        paper_bgcolor:paper,
        plot_bgcolor:paper,
        title:{
            text:'PowerDependence-Results',
            font:{
                size:30,
                color:color_t
            }
        },
        xaxis:{
            title: {
                text:'Flux (µA)',
                font:{size:25}
            },
            zeroline: false,
            color:color_x,
            tickfont:{size:25},
            automargin: true
        },
        yaxis: {
            title: {
                text:'Frequency (GHz)',
                font:{size:25},  
            },
            tickfont:{size:16},
            color: color_y,
            automargin: true
        },
        yaxis2:{},
        showlegend: false,
        hoverlabel:{font:{size:20}}
    };
    var Trace = [trace,trace_scatter]
    Plotly.newPlot(plotId, Trace,layout);
};




function get_plot2D_FD(){
    log_print("Ploting FluxDependence result...");
    let modenum = document.getElementById('dmbutton').value;  //darkmode or not
    let cavity = document.getElementById('cavity-select-FD').value.slice(3);
    const location_id = "FluxDep-result-plot";
    $.ajaxSettings.async = false;
    let FDKeys = {
        x: [ "Flux" ] ,
        y: [ "Frequency" ],
        y2: [ "Fr" ],
        z: [ "Amplitude" ]
    };
    let fd_plot = {};
    let where = "FD";
    $.getJSON( '/autoscan1Q/plot_result',{  
        measurement_catagories:JSON.stringify(where),
        specific_jobid : JSON.stringify(String(FD_jobids[cavity])),//FD_jobids[cavity]5105
        target_cavity : JSON.stringify(cavity)
    }, function (plot_items) {   //need to check this is correct or not
        fd_plot = plot_items[cavity];
    });
    $.ajaxSettings.async = true;
    plot2D_FD(fd_plot, FDKeys, location_id,modenum);
    document.getElementById(location_id).style.display = "block";
    document.getElementById('FD-search').setAttribute('value','1');
    log_print("Ploting finish!");
};


//-------------------------CWsweep-------------------------------------------



function plot1D_2y_CW ( data, axisKeys, plotId, modenum ){
    let groupNumber = axisKeys.x.length;
    let color_list= []
    let tracies = [];
    let ix;

    if(modenum=='0'){
        color_list=['#1f77b4','rgb(220 20 60)'];
    }else{
        color_list=['rgb(255,0,255)','rgb(255,255,0)'];
    };

    if(modenum=='0'){
        var layout = {
            plot_bgcolor:"rgb(252, 243, 223)",
            paper_bgcolor:'rgb(252, 243, 223)',
            title:{
                text:'CWsweep-Results',
                font:{
                    size:30
                }
            },
            xaxis:{
                title: {
                    text:'XY-Frequency (GHz)',
                    font:{size:25}
                },
                tickfont:{size:25},
                zeroline: false,
                color:'rgb(0,0,0)'
            },
            yaxis: {
                title: {
                    text:'Amplitude-Redefined (dBm)',
                    font:{size:25},  
                },
                color: '#1f77b4'
            },
            showlegend: true,
            hoverlabel:{font:{size:26}}
        };
    }else{
        var layout = {
            title:{
                text:'CWsweep-Results',
                font:{
                    size:30,
                    color:'rgb(0,255,255)'
                }
            },
            plot_bgcolor:"black",
            paper_bgcolor:'rgb(0,0,0)',
            xaxis:{
                title: {
                    text:'XY-Frequency (GHz)',
                    font:{size:25}
                },
                zeroline: false,
                tickfont:{size:25},
                color: 'rgb(0,255,0)',
            },
            yaxis: {
                title: {
                    text:'Amplitude-Redefined (dBm)',
                    font:{size:25},  
                },
                color: 'rgb(255,0,255)',
            },
            showlegend: true,
            legend:{font:{color:'rgb(0,255,0)'}},
            hoverlabel:{font:{size:26}}
        };
    }; 
    
    for ( gi=0; gi<groupNumber; gi++ ){
        let xKeysInGroup = axisKeys.x[gi];
        let yKeysInGroup = axisKeys.y[gi];

        let yNumberInGroup = yKeysInGroup.length;
    
        if(gi == 0){
            for (let i = 0; i < yNumberInGroup; i++){
            
                if ( xKeysInGroup.length != 1 ){
                    ix = i
                }else{
                    ix = 0
                };
                let newTrace = {
                    x: data[axisKeys.x[gi][ix]],
                    y: data[axisKeys.y[gi][i]],
                    name:String(yKeysInGroup), 
                    mode: 'lines',
                    line:{color:color_list[gi]}
                };
                    
                tracies.push(newTrace);
            
            };

        }else{
            for (let i = 0; i < yNumberInGroup; i++){
            
                if ( xKeysInGroup.length != 1 ){
                    ix = i
                }else{
                    ix = 0
                };
                let newTrace = {
                    x: data[axisKeys.x[gi][ix]],
                    y: data[axisKeys.y[gi][i]],
                    name:String(yKeysInGroup), 
                    mode: 'markers',
                    marker:{
                        color:color_list[gi],
                        symbol:'x',
                        size:14
                    }
                };
                    
                tracies.push(newTrace);
            };
        };
    };
    Plotly.newPlot(plotId, tracies, layout);
};

var q_plot = {};
function get_plot1D_CW(){
    log_print("Ploting CWsweep result...");
    let modenum = document.getElementById('dmbutton').value;  //darkmode or not
    const location_id = "CWsweep-result-plot";
    let cavity = document.getElementById('cavity-select-CW').value.slice(3)
    let xy_powa = document.getElementById('power-select-CW').value.slice(8)
    $.ajaxSettings.async = false;
    let CWKeys = {
        x: [ ["Sub_Frequency"], ["Targets_Freq"] ] ,
        y: [ ["Substrate_value"],["Targets_value"] ]
    };

    let where = "CW";
    $.getJSON( '/autoscan1Q/plot_result',{  
        measurement_catagories:JSON.stringify(where),
        specific_jobid : JSON.stringify(String(CW_jobids[cavity])),//CW_jobids[cavity]5141
        target_cavity : JSON.stringify(cavity)

    }, function (plot_items) {   //need to check this is correct or not
        q_plot = plot_items;
    });
    $.ajaxSettings.async = true;
    plot1D_2y_CW(q_plot[xy_powa], CWKeys, location_id,modenum);
    document.getElementById(location_id).style.display = "block";
    document.getElementById('CW-search').setAttribute('value','1');
    log_print("Ploting finish!");
};

function xypowa_options_generator(mode){
    
    // get the selector in the body
    let xyPowaSelect = document.getElementById('power-select-CW'); 
    let cavity = document.getElementById('cavity-select-CW').value.slice(3);
    
    $.ajaxSettings.async = false;
    let xy_options = {}
    
    $.getJSON( '/autoscan1Q/get_xypower',{  
        specific_jobid : JSON.stringify(String(CW_jobids[cavity])),//CW_jobids[cavity]5141

    }, function (xy_powas) {   //need to check this is correct or not
        xy_options = xy_powas['xy_power']; //list
    });
    
    const opt_num = xy_options.length
    if (mode=='initialize'){
        for(let ipt=0; ipt<opt_num; ipt++){
            let option = document.createElement("option");
            option.innerHTML = xy_options[ipt]+" dBm";
            option.setAttribute('value',"xyPower="+xy_options[ipt]);//value = "xyPower=-10"
            xyPowaSelect.appendChild(option);
        };
    }else{
        while (xyPowaSelect.options.length > 0) {
            select.remove(0);
        }
        for(let ipt=0; ipt<opt_num; ipt++){
            let option = document.createElement("option");
            option.innerHTML = xy_options[ipt]+" dBm";
            option.setAttribute('value',"xyPower="+xy_options[ipt]);//value = "xyPower=-10"
            xyPowaSelect.appendChild(option);
        };
    };
    $.ajaxSettings.async = true;
};


//------------------------------ShowParameters----------------------------------------


// 顯示目前量測參數
function paras_layout(where,paras_dict){
    
    $.ajaxSettings.async = false;
    let paranum = document.getElementById('sp-'+where).value;
    if(where != 'CW'){
        paras_dict['XY-Frequency']='OPT,';
        paras_dict['XY-Power']='OPT,';
    };
    
    if(paranum=='1'){
        reset_paras(where);
        document.getElementById('sp-'+where).setAttribute('value','0');
    }else{
        //Show parameters
        if(where=='CS'){
            document.getElementById('Freqrange-'+where).innerHTML = '•Frequence : '+ String(paras_dict['Frequency']);
        }else{
            document.getElementById('Freqrange-'+where).innerHTML = '•Frequence : '+ document.getElementById('cavity-select-'+where).value.slice(3);
        }
        document.getElementById('Powrange-'+where).innerHTML = '•Power (dBm) : '+ String(paras_dict['Power']);
        document.getElementById('Fluxrange-'+where).innerHTML = '•Flux : '+ String(paras_dict['Flux-Bias']);
        document.getElementById('IFBW-'+where).innerHTML = '•IF Bandwidth : '+ String(paras_dict['IF-Bandwidth']);
        document.getElementById('XYFreqrange-'+where).innerHTML = '•XY-Frequency Range (GHz) : '+ String(paras_dict['XY-Frequency']);
        document.getElementById('XYPowrange-'+where).innerHTML = '•XY-Power (dBm) : '+ String(paras_dict['XY-Power']);
        document.getElementById('sp-'+where).setAttribute('value','1');
    };
    $.ajaxSettings.async = true;
};



// show measurement parameters  naked check OK
function show_paras(where){
    log_print("Access measurement parameters...")
    let request_jobid = ''
    if(where == 'CS'){
        request_jobid = String(CS_jobid);//String(CS_jobid);"5108"

    }else if(where == 'PD'){
        let cavity_key = document.getElementById('cavity-select-PD').value.slice(3)
        request_jobid = String(PD_jobids[cavity_key]);//String(PD_jobids[cavity_key]);"5097"
        
    }else if(where == 'FD'){
        let cavity_key = document.getElementById('cavity-select-FD').value.slice(3)
        request_jobid = String(FD_jobids[cavity_key]);//String(FD_jobids[cavity_key]);"5105"

    }else{
        let cavity_key = document.getElementById('cavity-select-CW').value.slice(3)
        request_jobid = String(CW_jobids[cavity_key]);//String(CW_jobids[cavity_key]);"5141"

    };
    $.ajaxSettings.async = false;
    let paras_dict = {};
    
    $.getJSON( '/autoscan1Q/measurement_paras',{  
        this_jobid: JSON.stringify(request_jobid),
    }, function (paras){
        paras_dict = paras;
    });
    $.ajaxSettings.async = true;
    
    paras_layout(where,paras_dict);
    log_print("Parameters showing!");
};


