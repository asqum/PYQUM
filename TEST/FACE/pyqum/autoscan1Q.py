from sys import setprofile
from pyqum.benchmark import AutoScan1Q,Load_From_pyqum
from flask import Blueprint, request, session,render_template, abort, g
from pyqum.instrument.logger import  get_status
from sqlite3 import connect
from pandas import read_sql_query
import json
from numpy import ndarray,mean,array,arange
from colorama import init, Fore, Back, Style
import ast
import ctypes
# Error handling
from contextlib import suppress

from os.path import basename as bs
myname = bs(__file__).split('.')[0] # This py-script's name
encryp = 'ghhgjadz'
bp = Blueprint(myname, __name__, url_prefix='/autoscan1Q')

@bp.route('/')
def show():
	with suppress(KeyError):
		print(Fore.LIGHTBLUE_EX + "USER " + Fore.YELLOW + "%s "%session['user_name'] + Fore.LIGHTBLUE_EX + "has just logged in as Guest #%s!"%session['user_id'])
		# Security implementation:
		# if not g.user['instrument']:
		# 	abort(404)
		#quantificationType = benchmarkDict[session['user_name']].quantificationType
		return render_template("blog/autoscan1Q/autoscan1Q.html")
	return("<h3>WHO ARE YOU?</h3><h3>Please Kindly Login!</h3><h3>Courtesy from <a href='http://qum.phys.sinica.edu.tw:%s/auth/login'>HoDoR</a></h3>" %get_status("WEB")["port"])





sql_path = r'C:\Users\ASQUM\HODOR\CONFIG\pyqum.sqlite'
## Common function
class NumpyEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, ndarray):
			return obj.tolist()
			
		return json.JSONEncoder.default(self, obj)




#----------------main-----------------------
@bp.route('/initialize-CS',methods=['POST','GET'])
def CS_initialize():
    port = json.loads(request.args.get('inout_port'))
    designed_num = json.loads(request.args.get('designed'))
    permission = json.loads(request.args.get('access'))
    mode = json.loads(request.args.get('mode'))
    
    specifications = {"mode":mode,"CPW":designed_num,"I/O":port,"results":{"CavitySearch":{},"PowerDepend":{},"FluxDepend":{},"QubitSearch":{}},"JOBIDs":{"CavitySearch":{},"PowerDepend":{},"FluxDepend":{},"QubitSearch":{}},"step":"0"}

    routine = AutoScan1Q(sparam=port,dcsweepch ="",designed=designed_num)
    old_spec,_ = routine.read_specification()
    if permission == "Enforce" or old_spec == {} :    #history == "" :   #將強制執行量測將結果寫入資料庫（覆蓋）
        print("CavitySearch start:\n")
        routine.cavitysearch(jobid_check="")
        specifications["results"]["CavitySearch"]["answer"] = routine.total_cavity_list   #["1234 MHz",...]
        specifications["results"]["CavitySearch"]["region"] = routine.cavity_list 
        specifications["JOBIDs"]["CavitySearch"] = routine.CS_jobid
        specifications["step"]="1-1"
        routine.write_specification(specifications)

    specifications,_ = routine.read_specification()
    return json.dumps({"answer":specifications["results"]["CavitySearch"]["answer"],"jobid":specifications["JOBIDs"]["CavitySearch"]}, cls=NumpyEncoder)


@bp.route('/MeasureByCavity',methods=['POST','GET'])
def measure_procedure():
    x =  AutoScan1Q(sparam="",dcsweepch = "",designed="")
    speci,history = x.read_specification() #讀取資料庫,必有cavity_region
    scan_mode = speci["mode"]
    part = history[0] # if "1" cavitysearch finished, "2" powerdepend finished, ....
    first_run = 0

    dc_ch = json.loads(request.args.get('dc_chennel'))
    permission = json.loads(request.args.get('access'))
    target_cav = json.loads(request.args.get('target'))
    if scan_mode == "Qubits":
        cavitys = [target_cav.split("-")[0]]
        c_numbers = [target_cav.split("-")[1]]
    else:
        cavitys = speci["results"]["CavitySearch"]["answer"]
        c_numbers = arange(1,len(cavitys)+1,1)

    for i in range(len(cavitys)):
        routine = AutoScan1Q(sparam="",dcsweepch = dc_ch,designed="")
        specifications,history = routine.read_specification()
        # power dep. part
        if permission == "Enforce" or (part == "1" and first_run == 0) or first_run != 0:   #history == "" or specifications["results"]["PD"] == {}
            print("PowerDependent start @ C-%d :\n"%int(c_numbers[i]))

            routine.powerdepend(cavitys[i],"")
            specifications["results"]["PowerDepend"][cavitys[i]] = {} 
            specifications["results"]["PowerDepend"][cavitys[i]]["dress_power(dBm)"]= routine.low_power
            specifications["JOBIDs"]["PowerDepend"][cavitys[i]] = routine.jobid_dict["PowerDepend"]
            specifications["step"] = "2-"+str(c_numbers[i])
            routine.write_specification(specifications)

            first_run = 1

        if scan_mode == "Qubits":
            
            # flux dep. part
            if permission == "Enforce" or (part == "2" and first_run == 0) or first_run != 0:
                print("FluxDependent start @ C-%d :\n"%c_numbers[i])
                specifications,_ = routine.read_specification() #讀取資料庫
                routine.low_power = specifications["results"]["PowerDepend"][cavitys[i]]["low_power"]   #若從這開始，routine中沒有low_power的變數
                
                routine.fluxdepend(cavitys[i],float(cavitys[i].split(" ")[0]),"")  
                specifications["results"]["FluxDepend"][cavitys[i]] = {}
                specifications["results"]["FluxDepend"][cavitys[i]]["f_bare"] = routine.wave["f_bare"]
                specifications["results"]["FluxDepend"][cavitys[i]]["f_dress"] = routine.wave["f_dress"]
                specifications["results"]["FluxDepend"][cavitys[i]]["offset"] = routine.wave["offset"]
                specifications["JOBIDs"]["FluxDepend"][cavitys[i]] = routine.jobid_dict["FluxDepend"]
                specifications["step"] = "3-"+str(c_numbers[i])
                routine.write_specification(specifications)

                first_run = 1
            
            # 2tone part
            if permission == "Enforce" or (part == "3" and first_run == 0) or first_run != 0:
                print("CWsweep start @ C-%d :\n"%c_numbers[i])
                specifications,_ = routine.read_specification() #讀取資料庫
                #補充可能沒有的參數（以此開始時）
                routine.low_power = specifications["results"]["PowerDepend"][cavitys[i]]["low_power"]
                routine.wave = {"f_bare":specifications["results"]["FluxDepend"][cavitys[i]]["f_bare"],"f_dress":specifications["results"]["FluxDepend"][cavitys[i]]["f_dress"],"offset":specifications["results"]["FluxDepend"][cavitys[i]]["offset"]}
                
                routine.qubitsearch(cavitys[i],"")
                specifications["results"]["QubitSearch"][cavitys[i]]["qubit"] = routine.qubit_info['Fq_avg']
                specifications["results"]["QubitSearch"][cavitys[i]]["Ec"] = routine.qubit_info['Ec_avg']
                specifications["results"]["QubitSearch"][cavitys[i]]["acStark"] = routine.qubit_info['acStark_power']
                specifications["JOBIDs"]["QubitSearch"][cavitys[i]] = routine.jobid_dict["QubitSearch"]
                specifications["step"] = "4-"+str(c_numbers[i])
                routine.write_specification(specifications)

                first_run = 1
    
    specifications,_ = routine.read_specification()
    return json.dumps({"results":specifications["results"],"jobids":specifications["JOBIDs"]}, cls=NumpyEncoder)



'''
@bp.route('/measurement',methods=['POST','GET'])
def auto_measurement():  # measurement do not plot

    dc_ch = json.loads(request.args.get('dc_channel'))
    port = json.loads(request.args.get('inout_port'))
    designed_num = json.loads(request.args.get('designed'))
    print('port check: ',port)
    print("Automatic measurement gogogo\n")
    # search(self.quantificationObj)
    routine = AutoScan1Q(sparam=port,dcsweepch = dc_ch,designed=designed_num)
    print("CavitySearch start:\n")
    routine.cavitysearch("")
    CS = {'answer':routine.total_cavity_list}  #['5487 MHz',...]
    print('CS answer: ',CS)
    PD, FD, CW = {}, {}, {}
    JOBIDs = {'CavitySearch':routine.CS_jobid,'PowerDepend':{},'FluxDepend':{},'QubitSearch':{}}
    c_number = 0
    for i in routine.total_cavity_list:
        init(autoreset=True)
        print("PowerDependent start @ C-%d :\n"%(c_number+1))
        print(Back.RED+"Check XY-gate ISO port !")
        routine.powerdepend(i,"")
        f_bare = float(i.split(" ")[0])
        PD[i]={'low_power':routine.readout_para[i]["low_power"],'high_power':routine.readout_para[i]["high_power"]} #need to check
        JOBIDs['PowerDepend'][i] = routine.jobid_dict['PowerDepend']

        print("FluxDependent start @ C-%d :\n"%(c_number+1))
        routine.fluxdepend(i,f_bare,"")
        FD[i]={'flux_offset':routine.readout_para[i]["offset"],'f_bare':routine.readout_para[i]["f_bare"],'f_dress':routine.readout_para[i]["f_dress"]}  #need to check
        JOBIDs['FluxDepend'][i] = routine.jobid_dict['FluxDepend']

        print("CWsweep start @ C-%d :\n"%(c_number+1))
        routine.qubitsearch(i,"")
        CW[i]={'q_freq':routine.readout_para[i]["qubit"],'Ec':routine.readout_para[i]["Ec"],'acStark':routine.readout_para[i]["acStark"]} #AutoScan1Q_classfile.py has not complete this part  
        JOBIDs['QubitSearch'][i] = routine.jobid_dict['QubitSearch']
    
        c_number += 1

    #jobid = {'CavitySearch':2051,'5487 MHz':{"PowerDepend":1000,"FluxDepend":1001,"QubitSearch":1002},...}
    print("Measurement Finish")
    measure_result = {"CS":CS,"PD":PD,"FD":FD,"CW":CW}   #<- this will be saved in sql and show in sameple description
    specifications  = {"result": measure_result,"JOBID":JOBIDs}
    db = connect(sql_path)
    samplename = get_status("MSSN")[session['user_name']]['sample']
    # samplename = "2QAS-19-3"
    db.execute('UPDATE sample SET specifications = ? WHERE samplename = ?', (specifications,samplename))
    db.commit()
    db.close()
    return json.dumps(measure_result, cls=NumpyEncoder)

'''

# developing.... try to put the paras in dictionary with corresponding key
@bp.route('/measurement_paras',methods=['POST','GET'])
def get_paras():
    id = json.loads(request.args.get('this_jobid'))
    connection = connect(sql_path)
    job = read_sql_query("SELECT*FROM job",connection)
    paras = job[job['id']==int(id)]['parameter'].iloc[0]    # <- this is a string with F-response: {'Flux-Bias':fluxbias, 'S-Parameter':sparam, 'IF-Bandwidth':ifb, 'Power':powa, 'Frequency':freq}
    
    return json.dumps(ast.literal_eval(paras), cls=NumpyEncoder)                                 # with CWsweep: {'Flux-Bias':fluxbias, 'XY-Frequency':xyfreq, 'XY-Power':xypowa, 'S-Parameter':sparam, 'IF-Bandwidth':ifb, 'Frequency':freq, 'Power':powa}

# get the specific jobid in the sample description
# set a search button for jobid
# the position in sql is unknown
@bp.route('/get_jobid',methods=['POST','GET'])
def get_jobid():
    connection = connect(sql_path)
    sample = read_sql_query("SELECT * FROM sample", connection)
    samplename = get_status("MSSN")[session['user_name']]['sample']
    # samplename = "2QAS-19-3"
    specifications = sample[sample['samplename']==samplename]['specifications'].iloc[0]

    return json.dumps(ast.literal_eval(specifications)["JOBIDs"], cls=NumpyEncoder)     # contains {'CavitySearch':2051,'PowerDepend':{'5487 MHz':2052,...},'FluxDepend':{'5487 MHz':2053,...},'QubitSearch':{'5487 MHz':2054,...}}


@bp.route('/get_results',methods=['POST','GET'])
def get_results():
    connection = connect(sql_path)
    sample = read_sql_query("SELECT * FROM sample", connection)
    samplename = get_status("MSSN")[session['user_name']]['sample']
    # samplename = "2QAS-19-3"
    specifications = sample[sample['samplename']==samplename]['specifications'].iloc[0]

    return json.dumps(ast.literal_eval(specifications)["results"], cls=NumpyEncoder)  


# haven't update yet
# not for measurement but for plot with a specific jobid
@bp.route('/plot_result',methods=['POST','GET'])
def plot_after_jobid():
    specific_id = json.loads(request.args.get('specific_jobid'))
    if specific_id != "":
        specific_id = int(specific_id)
    designed = json.loads(request.args.get('designed'))
    where_plot = json.loads(request.args.get('measurement_catagories'))
    PD, FD, CW = {}, {}, {}
    print("Construct plot items:\n")
    # search(self.quantificationObj)
    routine = AutoScan1Q(sparam="",dcsweepch = "",designed=designed)
    if where_plot == "CS":
        print("CavitySearch start:\n")
        routine.cavitysearch(specific_id)
        CS = {'plot_items':routine.CS_plot_items,'overview':routine.CS_overview}  #{'5487 MHz':{'Frequency':[...],'Amplitude':[...],'UPhase':[...]},'~ MHz':{...},...}
                                                                                  #{'Frequency':[...],'Amplitude':[...],'UPhase':[...]}
        print("Construction Finish")
        return json.dumps(CS, cls=NumpyEncoder)
    elif where_plot == "PD":
        if specific_id != "":
            cavity = "0000 MHz"
        else:
            cavity = json.loads(request.args.get('target_cavity'))
        print("PowerDependent start:\n")
        routine.powerdepend(cavity,specific_id)
        f_bare = float(cavity.split(" ")[0])
        PD[cavity] = routine.PD_plot_items   # {"3D_axis":{"Frequency":[],"Power":[],"Amplitude":[]},"scatter":{'Power':[],'Fr':[]}}

        print("Construction Finish")
        return json.dumps(PD, cls=NumpyEncoder)
    elif where_plot == "FD":
        if specific_id != "":
            cavity = "0000 MHz"
        else:
            cavity = json.loads(request.args.get('target_cavity'))
        f_bare = float(cavity.split(" ")[0])
        print("FluxDependent start:\n")
        routine.fluxdepend(cavity,f_bare,specific_id)
        FD[cavity] = routine.FD_plot_items       # {"3D_axis":{"Frequency":[],"Flux":[],"Amplitude":[]},"scatter":{'Flux':[],'Fr':[]}}

        print("Construction Finish")
        return json.dumps(FD, cls=NumpyEncoder)
    else:
        if specific_id != "":
            cavity = "0000 MHz"
        else:
            cavity = json.loads(request.args.get('target_cavity'))
        print("QubitSearch start:\n")
        routine.qubitsearch(cavity,specific_id)
        CW = routine.CW_plot_items      #{'xy_power1':{'Targets_value':[],'Targets_Freq':[],'Sub_Frequency':[],'Substrate_value':[]},'xy_power2':{...},...}

        print("Construction Finish")
        return json.dumps(CW, cls=NumpyEncoder)


@bp.route('/get_xypower',methods=['POST','GET'])
def get_xypower():
    specific_id = int(json.loads(request.args.get('specific_jobid')))
    dataframe = Load_From_pyqum(specific_id).load()
    xy_powa = dataframe['XY-Power'].unique() #['-10','-20',...]

    return json.dumps({'xy_power':xy_powa}, cls=NumpyEncoder)

#----------------------------test-------------------------------------------------  

@bp.route('/get_cavity_status',methods=['POST','GET'])
def get_measure_status():
    routine = AutoScan1Q(sparam="",dcsweepch = "",designed="")
    specifications,history = routine.read_specification()
    if len(history) != 0:
        part = history[0]
        cav_number = history[-1]
        if part == "1":
            step = "CavitySearch "
        elif part == "2":
            step = "PowerDependence "
        elif part == "3":
            step = "FluxDependence "
        else:
            step = "2Tone "
        
        return json.dumps({"status":step+"completed @ C-"+cav_number,"cavity_list":specifications["results"]["CavitySearch"]["region"]}, cls=NumpyEncoder)
    else:
        return json.dumps({"status":"New chip!","cavity_list":{}}, cls=NumpyEncoder)


# when change darkmode the result area change too, give the infomation already write in the database
@bp.route('/give_done_info',methods=['POST','GET'])
def give_done_info():
    routine = AutoScan1Q(sparam="",dcsweepch = "",designed="")
    specifications,history = routine.read_specification()
    objects = specifications["results"]["CavitySearch"]["answer"]  #list ['1234 MHz', ...]
    parts = specifications["results"].keys()    #list ["CavitySearch","PowerDepend","FluxDepend","QubitSearch"]

    done_info_dict = {}
    for cav in objects:
        done_info_dict[cav] = {}
        for part in parts:
            if part != "CavitySearch":
                if cav in specifications["results"][part].keys():
                    done_info_dict[cav][part] = specifications["results"][part][cav]
                else:
                    done_info_dict[cav][part] = {}
    
    return json.dumps(done_info_dict, cls=NumpyEncoder)
                    


