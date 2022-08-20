//--------------------Global functions-------------------------
// 開關深色模式
var dark = document.getElementById("dmbutton");
dark.addEventListener('click' , darkMode);
// Dark Mode
function darkMode() {
    let element = document.body;
    element.classList.toggle("dark-mode");
    if(document.getElementById('dmbutton').value=='0'){
        document.getElementById('dmbutton').setAttribute('value','1');
        //按鍵變為深色模式
        let but = document.getElementsByClassName('content-button');
        for(let i=0;i<but.length;i++){
            but[i].style.color = 'rgb(0,255,0)';
        };

    }else{
        document.getElementById('dmbutton').setAttribute('value','0');
        let but = document.getElementsByClassName('content-button');
        for(let i=0;i<but.length;i++){
            but[i].style.color = 'rgb(0,0,0)';
        };
    };
    dark_plot();
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
function reset_paras(){
    document.getElementById('Freqrange').innerHTML = '';
    document.getElementById('Powrange').innerHTML = '';
    document.getElementById('Fluxrange').innerHTML = '';
    document.getElementById('IFBW').innerHTML = '';
    document.getElementById('XYFreqrange').innerHTML = '';
    document.getElementById('XYPowrange').innerHTML = '';
    document.getElementById('Repeattime').innerHTML = '';
};

function reset_address(){
    history.pushState("", document.title, window.location.pathname);
    history.go(0);
};

//-----------------Measurement settings-------------------
//start auto measurement
var MS_process = document.getElementById("Start-measure-but");
MS_process.addEventListener('click' , start_measure);
//hash to the MS window
var showcontent_MS = document.getElementById("showcontent-MS");
showcontent_MS.addEventListener('click' , show_content_MS);
//refresh all the html
var refresh= document.getElementById("refresh");
refresh.addEventListener('click' , reset_address);

// results container
var cavities = {};
var cavity_keys = [];
var cavities_array = [];
var powers = {};
var pd_array = {};
var flux = {};
var fd_array = {};
var q_freq = {};
var q_array = {};

// measurement settings
var designed_num = '0';
var dc_ch = '1';
var port = 'S21,';

function start_measure(){
    designed_num = document.getElementById('CPw-num-inp').value;
    dc_ch = document.getElementById('dc-channel-inp').value;
    port = document.getElementById('port-inp').value;

    console.log(designed_num)
    if(designed_num=='' || designed_num=='0'){
        alert("Your Designed cavity number is 0 or empty !");
    };

    // connect to autoscan1Q2js.py
    console.log("Start Measurement by Bot ")
    $.getJSON( '/autoscan1Q2js/measurement',{  
        designed: JSON.stringify(designed_num),
        dc_channel: JSON.stringify(dc_ch),
        inout_port: JSON.stringify(port), 

    }, function (datas) {   //need to check this is correct or not
        console.log( "Searching Finished " );
        cavities = datas["CS"]['answer'];
        cavities_array = datas["CS"]['arrays']; // above two are sets {}
        cavity_keys = Object.keys(cavities); // 'CS-','PD-',... + ['4.566',...] *1000 is the options value
        for (let i=0;i<cavity_keys.length;i++){
            powers[cavity_keys[i]] = datas["PD"][cavity_keys[i]]['power'] // a number
            pd_array[cavity_keys[i]] = datas["PD"][cavity_keys[i]]['arrays'] // a dataframe

            flux[cavity_keys[i]] = datas["FD"][cavity_keys[i]]['flux']   // a number
            fd_array[cavity_keys[i]] = datas["FD"][cavity_keys[i]]['arrays']  // a dataframe

            q_freq[cavity_keys[i]] = datas["CW"][cavity_keys[i]]['q_freq']   
            q_array[cavity_keys[i]] = datas["CW"][cavity_keys[i]]['arrays']  
        };
        
    });
    // ToSolve: How to show the results on the html?
    console.log("Print out the results");
    show_results();
};



function show_results(){
    let resultsBycavity = {};
    for(let i=0;i<cavity_keys.length;i++){
        let target_cav = cavity_keys[i];  //'4.599'...
        resultsBycavity[String(Math.floor(Number(target_cav)*1000))+" MHz"] = ["Power: "+String(powers[target_cav])+" dBm","Flux: "+String(flux[target_cav])+" µA","Qubit @ "+String(Math.floor(Number(q_freq[target_cav])*1000))+" MHz"];
    };
    document.getElementById('result').innerHTML = resultsBycavity;
};

function show_content_MS(){
    window.location.hash = "#MS-content";
};

//-----------------CavitySearch---------------------------
// 畫出baseline
var fig_CS = document.getElementById("CS-search");
fig_CS.addEventListener('click' , get_plot1D_CS);
//根據選項畫出cavities
var cavities_CS = document.getElementById("looks-CS");
cavities_CS.addEventListener('click' , show_cavities);
// 顯示量測參數
var showpara_CS = document.getElementById("sp-CS");
showpara_CS.addEventListener('click' , showparas_CS);

//顯示內文
var showcontent_CS = document.getElementById("showcontent-CS");
showcontent_CS.addEventListener('click' , function(){show_content("showcontent-CS","CS-content");});


// generate the options in the select id
function generate_options(id,data,cata){
    // get the selector in the body
      let CavitySelect = document.getElementById(id); 
      let result_keys =  Object.keys(data)
      const opt_num = Object.keys(data).length

    // generate the options in the select
      for(let ipt=0; ipt<opt_num; ipt++){
          let option = document.createElement("option");
          option.innerHTML = String(Math.floor(Number(result_keys[ipt])*1000))+' MHz';
          option.setAttribute('value',cata+String(Math.floor(Number(result_keys[ipt])*1000)));//String(Number(result_keys[ipt])*1000)+' MHz'
          CavitySelect.appendChild(option);
        };
};

// 顯示目前量測參數
function showparas_CS(){
    let paranum = document.getElementById('sp-CS').value;
    if(paranum=='1'){
        document.getElementById('Freqrange-CS').innerHTML = '';
        document.getElementById('Powrange-CS').innerHTML = '';
        document.getElementById('IFBW-CS').innerHTML = '';
        document.getElementById('sp-CS').setAttribute('value','0');
    }else{
        //Show parameters
        document.getElementById('Freqrange-CS').innerHTML = '•Frequence Range : 0 ~ 5 GHz';
        document.getElementById('Powrange-CS').innerHTML = '•Power : -20 dBm';
        document.getElementById('IFBW-CS').innerHTML = '•IF Bandwidth : 200';
        document.getElementById('sp-CS').setAttribute('value','1');
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
        const result = Object.keys(data);
        document.getElementById('resultId-CS').innerHTML = 'Cavity @ (GHz): '+result;
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


function get_plot1D_CS(){
    let modenum = document.getElementById('dmbutton').value;  // get darkmode or not
    
    const location_id = "CavitySearch-result-plot";
    let ampPhaseKeys = {
        x: [ ["Frequency"], ["Frequency"] ] ,
        y: [ ["Amplitude"],["UPhase"] ],
    };

    genopt (cavities);
    let baseline = [1,2,3,4,5,6,7,8,9,10];
    plot1D_2y_CS(baseline, ampPhaseKeys, location_id,modenum);
    document.getElementById(location_id).style.display = "block";
    document.getElementById('CS-search').setAttribute('value','1');
};


// jump to cavities plot html
function show_cavities(){
    let modenum = document.getElementById('dmbutton').value;
    let option_num = document.getElementById('cavity-select-CS').length;
    let cavity = document.getElementById('cavity-select-CS').value.slice(3);
    let ampPhaseKeys = {
        x: [ ["Frequency"], ["Frequency"] ] ,
        y: [ ["Amplitude"],["UPhase"] ]
    };
    let plot_array = {};
    for(let i=0;i<option_num;i++){
        if(Number(cavity)==Math.floor(Number(Object.keys(cavities)[i])*1000)){
            plot_array = cavities_array[i];  //cavities_array is a list without key
        };
    };
    plot1D_2y_CS(plot_array, ampPhaseKeys, "CavitySearch-result-plot",modenum);
    document.getElementById("CavitySearch-result-plot").style.display = "block";
    document.getElementById('CS-search').setAttribute('value','2');
};

//------------------PowerDependence-----------------------------------
// 畫出baseline
var fig_PD = document.getElementById("PD-search");
fig_PD.addEventListener('click' , get_plot2D_PD);
var showpara_PD = document.getElementById("sp-PD");
showpara_PD.addEventListener('click' , showparas_PD);
var showcontent_PD = document.getElementById("showcontent-PD");
showcontent_PD.addEventListener('click' , function(){show_content("showcontent-PD","FD-content");});


// 顯示目前量測參數
function showparas_PD(){
    let paranum = document.getElementById('sp-PD').value;
    if(paranum=='1'){
        //Show parameters
        document.getElementById('Freqrange-PD').innerHTML = '';
        document.getElementById('Powrange-PD').innerHTML = '';
        document.getElementById('IFBW-PD').innerHTML = '';
        document.getElementById('sp-PD').setAttribute('value','0');
    }else{
        //Show parameters
        document.getElementById('Freqrange-PD').innerHTML = '•Frequence : '+ document.getElementById('cavity-select-PD').value.slice(3)+' MHz';
        document.getElementById('Powrange-PD').innerHTML = '•Power : -20 ~ 20 dBm';
        document.getElementById('IFBW-PD').innerHTML = '•IF Bandwidth : 200';
        document.getElementById('sp-PD').setAttribute('value','1');
    };
};

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
        z: data[axisKeys.z], 
        x: data[axisKeys.x], 
        y: data[axisKeys.y], 
        zsmooth: 'best',
        mode: 'lines', 
        type: 'heatmap',
        width: 2.5,
        colorbar:{
            tickfont:{color:color_z,size:25},
            title:{
                text:'Amplitude (dBm)',
                side:'right',
                font:{size:30,color:color_z}
            }
        },
    };
    var layout = {
        paper_bgcolor:paper,
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
        },
        yaxis: {
            title: {
                text:'Frequency (GHz)',
                font:{size:25},  
            },
            tickfont:{size:25},
            color: color_y
        },
        showlegend: true,
        hoverlabel:{font:{size:26}}
    };
    var Trace = [trace]
    Plotly.newPlot(plotId, Trace,layout);
};




function get_plot2D_PD(){
    let modenum = document.getElementById('dmbutton').value;  //darkmode or not
    const location_id = "PowerDep-result-plot";
    // check the column name of the dataframe
    let PDKeys = {
        x: [ "Power" ] ,
        y: [ "Frequency" ],
        z: [ "Amplitude" ]
    };

    //make up the quantification output
    let option_num = document.getElementById('cavity-select-PD').length;
    let cavity = document.getElementById('cavity-select-PD').value.slice(3);

    let plot_array = {};
    for(let i=0;i<option_num;i++){
        let target = Object.keys(pd_array)[i];
        if(Number(cavity)==Math.floor(Number(target)*1000)){
            plot_array = pd_array[target];
        };
    };

    plot2D_PD(plot_array, PDKeys, location_id,modenum);
    document.getElementById(location_id).style.display = "block";
    document.getElementById('PD-search').setAttribute('value','1');

};

//-------------------FluxDependence---------------------------------
// 畫出baseline
var fig_FD = document.getElementById("FD-search");
fig_FD.addEventListener('click' , get_plot2D_FD);
var showpara_FD = document.getElementById("sp-FD");
showpara_FD.addEventListener('click' , showparas_FD);
var showcontent_FD = document.getElementById("showcontent-FD");
showcontent_FD.addEventListener('click' , function(){show_content("showcontent-FD","FD-content");});


// 顯示目前量測參數
function showparas_FD(){
    let paranum = document.getElementById('sp-FD').value;
    if(paranum=='1'){
        //Show parameters
        document.getElementById('Freqrange-FD').innerHTML = '';
        document.getElementById('Powrange-FD').innerHTML = '';
        document.getElementById('IFBW-FD').innerHTML = '';
        document.getElementById('Fluxrange-FD').innerHTML = '';
        document.getElementById('sp-FD').setAttribute('value','0');
    }else{
        //Show parameters
        document.getElementById('Freqrange-FD').innerHTML = '•Frequence : '+ document.getElementById('cavity-select-FD').value.slice(3)+' MHz';
        document.getElementById('Powrange-FD').innerHTML = '•Power : -10 dBm';
        document.getElementById('IFBW-FD').innerHTML = '•IF Bandwidth : 200';
        document.getElementById('Fluxrange-FD').innerHTML = '•Flux: -300 ~ 300 µA';
        document.getElementById('sp-FD').setAttribute('value','1');
    };
};

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
        z: data[axisKeys.z], 
        x: data[axisKeys.x], 
        y: data[axisKeys.y], 
        zsmooth: 'best',
        mode: 'lines', 
        type: 'heatmap',
        width: 2.5,
        colorbar:{
            tickfont:{color:color_z,size:25},
            title:{
                text:'Amplitude (dBm)',
                side:'right',
                font:{size:30,color:color_z}
            }
        },
    };
    var layout = {
        paper_bgcolor:paper,
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
        },
        yaxis: {
            title: {
                text:'Frequency (GHz)',
                font:{size:25},  
            },
            tickfont:{size:25},
            color: color_y
        },
        showlegend: true,
        hoverlabel:{font:{size:26}}
    };
    var Trace = [trace]
    Plotly.newPlot(plotId, Trace,layout);
};




function get_plot2D_FD(){
    let modenum = document.getElementById('dmbutton').value;  //darkmode or not
    const location_id = "FluxDep-result-plot";
    
    let FDKeys = {
        x: [ "Flux" ] ,
        y: [ "Frequency" ],
        z: [ "Amplitude" ]
    };

    //make up the quantification output
    let cavity = document.getElementById('cavity-select-FD').value.slice(3);
    let option_num = document.getElementById('cavity-select-FD').length;

    let plot_array = {};
    for(let i=0;i<option_num;i++){
        let target = Object.keys(fd_array)[i];
        if(Number(cavity)==Math.floor(Number(target)*1000)){
            plot_array = fd_array[target];
        };
    };
    plot2D_FD(plot_array, FDKeys, location_id,modenum);
    document.getElementById(location_id).style.display = "block";
    document.getElementById('FD-search').setAttribute('value','1');

};


//-------------------------CWsweep-------------------------------------------
var fig_cw = document.getElementById("CW-search");
fig_cw.addEventListener('click' , get_plot1D_CW);
var showpara_CW = document.getElementById("sp-CW");
showpara_CW.addEventListener('click' , showparas_CW);
//顯示內文
var showcontent_CW = document.getElementById("showcontent-CW");
showcontent_CW.addEventListener('click' , function(){show_content("showcontent-CW","CW-content");});



// 顯示目前量測參數
function showparas_CW(){
    let paranum = document.getElementById('sp-CW').value;
    if(paranum=='1'){
        document.getElementById('Freqrange-CW').innerHTML = '';
        document.getElementById('Powrange-CW').innerHTML = '';
        document.getElementById('Fluxrange-CW').innerHTML = '';
        document.getElementById('IFBW-CW').innerHTML = '';
        document.getElementById('XYFreqrange-CW').innerHTML = '';
        document.getElementById('XYPowrange-CW').innerHTML = '';
        document.getElementById('Repeattime-CW').innerHTML = '';
        document.getElementById('sp-CW').setAttribute('value','0');
    }else{
        //Show parameters
        document.getElementById('Freqrange-CW').innerHTML = '•Frequence : '+ document.getElementById('cavity-select-CW').value.slice(3)+' MHz';
        document.getElementById('Powrange-CW').innerHTML = '•Power : -20 dBm';
        document.getElementById('Fluxrange-CW').innerHTML = '•Flux : -65 µA';
        document.getElementById('IFBW-CW').innerHTML = '•IF Bandwidth : 200';
        document.getElementById('XYFreqrange-CW').innerHTML = '•XY-Frequency Range : 0 ~ 9 GHz';
        document.getElementById('XYPowrange-CW').innerHTML = '•XY-Power : -20 dBm';
        document.getElementById('Repeattime-CW').innerHTML = '•Repeat times : 10';
        document.getElementById('sp-CW').setAttribute('value','1');
    };
};

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

function get_plot1D_CW(){
    let modenum = document.getElementById('dmbutton').value;  //darkmode or not
    const location_id = "CWsweep-result-plot";
    
    let CWKeys = {
        x: [ ["Sub_Frequency"], ["Targets_Freq"] ] ,
        y: [ ["Substrate"],["Targets"] ]
    };

    //make up the quantification output
    let cavity = document.getElementById('cavity-select-CW').value.slice(3)
    let option_num = document.getElementById('cavity-select-CW').length;

    let plot_array = {};
    for(let i=0;i<option_num;i++){
        let target = Object.keys(q_array)[i];
        if(Number(cavity)==Math.floor(Number(target)*1000)){
            plot_array = q_array[target];
        };
    };

    plot1D_2y_CW(plot_array, CWKeys, location_id,modenum);
    document.getElementById(location_id).style.display = "block";
    document.getElementById('CW-search').setAttribute('value','1');
    

};


//---------------------------------------------------------------------------mission complete
