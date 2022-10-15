from sys import setprofile
from pyqum.benchmark import AutoScan1Q,Load_From_pyqum
from flask import Blueprint, request, session,render_template, abort, g
from pyqum.instrument.logger import  get_status
from sqlite3 import connect
from pandas import read_sql_query
import json
from numpy import ndarray,mean,array
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
    dc_ch = json.loads(request.args.get('dc_channel'))
    port = json.loads(request.args.get('inout_port'))
    designed_num = json.loads(request.args.get('designed'))
    permission = json.loads(request.args.get('access'))
    
    specifications = {"CPW":designed_num,"wiring":{"I/O":port,"dc_chennel":dc_ch},"results":{"CavitySearch":{},"PowerDepend":{},"FluxDepend":{},"QubitSearch":{}},"JOBIDs":{"CavitySearch":{},"PowerDepend":{},"FluxDepend":{},"QubitSearch":{}},"step":"0"}

    routine = AutoScan1Q(sparam=port,dcsweepch = dc_ch,designed=designed_num,target_cav="")
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
    return json.dumps(specifications["results"]["CavitySearch"]["answer"], cls=NumpyEncoder)


@bp.route('/MeasureByCavity',methods=['POST','GET'])
def measure_procedure():

    permission = json.loads(request.args.get('access'))
    scan_mode = json.loads(request.args.get('scan_mode'))
    target_cav = json.loads(request.args.get('target'))
    cavity = target_cav.split("-")[0]
    c_number = target_cav.split("-")[1]
    routine = AutoScan1Q(sparam="",dcsweepch = "",designed="",target_cav=cavity)



    # power dep. part
    specifications,history = routine.read_specification() #讀取資料庫,必有cavity_region
    part = history[0] # if "1" cavitysearch finished, "2" powerdepend finished, ....
    first_run = 0

    if permission == "Enforce" or (part == "1" and first_run == 0) or first_run != 0:   #history == "" or specifications["results"]["PD"] == {}
        print("PowerDependent start @ C-%d :\n"%c_number)

        routine.powerdepend(cavity,"")
        specifications["results"]["PowerDepend"][cavity]["low_power"] = routine.low_power
        specifications["JOBIDs"]["PowerDepend"][cavity] = routine.jobid_dict["PowerDepend"]
        specifications["step"] = "2-"+str(c_number)
        routine.write_specification(specifications)

        first_run = 1

    if scan_mode == "Qubits":
        
        # flux dep. part
        if permission == "Enforce" or (part == "2" and first_run == 0) or first_run != 0:
            print("FluxDependent start @ C-%d :\n"%c_number)
            specifications,_ = routine.read_specification() #讀取資料庫
            routine.low_power = specifications["results"]["PowerDepend"][cavity]["low_power"]   #若從這開始，routine中沒有low_power的變數
            
            routine.fluxdepend(cavity,float(cavity.split(" ")[0]),"")  
            specifications["results"]["FluxDepend"][cavity]["f_bare"] = routine.wave["f_bare"]
            specifications["results"]["FluxDepend"][cavity]["f_dress"] = routine.wave["f_dress"]
            specifications["results"]["FluxDepend"][cavity]["offset"] = routine.wave["offset"]
            specifications["JOBIDs"]["FluxDepend"][cavity] = routine.jobid_dict["FluxDepend"]
            specifications["step"] = "3-"+str(c_number)
            routine.write_specification(specifications)

            first_run = 1
        
        # 2tone part
        if permission == "Enforce" or (part == "3" and first_run == 0) or first_run != 0:
            print("CWsweep start @ C-%d :\n"%c_number)
            specifications,_ = routine.read_specification() #讀取資料庫
            #補充可能沒有的參數（以此開始時）
            routine.low_power = specifications["results"]["PowerDepend"][cavity]["low_power"]
            routine.wave = {"f_bare":specifications["results"]["FluxDepend"][cavity]["f_bare"],"f_dress":specifications["results"]["FluxDepend"][cavity]["f_dress"],"offset":specifications["results"]["FluxDepend"][cavity]["offset"]}
            
            routine.qubitsearch(cavity,"")
            specifications["results"]["QubitSearch"][cavity]["qubit"] = routine.qubit_info['Fq_avg']
            specifications["results"]["QubitSearch"][cavity]["Ec"] = routine.qubit_info['Ec_avg']
            specifications["results"]["QubitSearch"][cavity]["acStark"] = routine.qubit_info['acStark_power']
            specifications["JOBIDs"]["QubitSearch"][cavity] = routine.jobid_dict["QubitSearch"]
            specifications["step"] = "4-"+str(c_number)
            routine.write_specification(specifications)

            first_run = 1
    
    specifications,_ = routine.read_specification()
    return json.dumps(specifications["results"], cls=NumpyEncoder)



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

