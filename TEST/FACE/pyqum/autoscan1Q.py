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
    routine.cavitysearch(jobid="")
    CS = {'answer':routine.total_cavity_list}  #['5487 MHz',...]
    print('CS answer: ',CS)
    PD, FD, CW = {}, {}, {}
    JOBIDs = {'CavitySearch':routine.CS_jobid,'PowerDepend':{},'FluxDepend':{},'QubitSearch':{}}
    for i in routine.total_cavity_list:
        print("PowerDependent start:\n")
        routine.powerdepend(i,jobid='')
        f_bare = float(i.split(" ")[0])
        PD[i]={'low_power':routine.readout_para[i]["low_power"],'high_power':routine.readout_para[i]["high_power"]} #need to check
        JOBIDs['PowerDepend'][i] = routine.jobid_dict['PowerDepend']

        print("FluxDependent start:\n")
        routine.fluxdepend(i,f_bare,jobid='')
        FD[i]={'flux_offset':routine.readout_para[i]["offset"],'f_bare':routine.readout_para[i]["f_bare"],'f_dress':routine.readout_para[i]["f_dress"]}  #need to check
        JOBIDs['FluxDepend'][i] = routine.jobid_dict['FluxDepend']

        print("CWsweep start:\n")
        routine.qubitsearch(i,jobid="")
        CW[i]={'q_freq':routine.readout_para[i]["qubit"],'Ec':routine.readout_para[i]["Ec"],'acStark':routine.readout_para[i]["acStark"]} #AutoScan1Q_classfile.py has not complete this part  
        JOBIDs['QubitSearch'][i] = routine.jobid_dict['QubitSearch']

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

    return json.dumps(ast.literal_eval(specifications)["JOBID"], cls=NumpyEncoder)     # contains {'CavitySearch':2051,'PowerDepend':{'5487 MHz':2052,...},'FluxDepend':{'5487 MHz':2053,...},'QubitSearch':{'5487 MHz':2054,...}}


@bp.route('/get_results',methods=['POST','GET'])
def get_results():
    connection = connect(sql_path)
    sample = read_sql_query("SELECT * FROM sample", connection)
    samplename = get_status("MSSN")[session['user_name']]['sample']
    # samplename = "2QAS-19-3"
    specifications = sample[sample['samplename']==samplename]['specifications'].iloc[0]

    return json.dumps(ast.literal_eval(specifications)["result"], cls=NumpyEncoder)  


global progress
# not for measurement but for plot with a specific jobid
@bp.route('/plot_result',methods=['POST','GET'])
def plot_after_jobid():
    specific_id = int(json.loads(request.args.get('specific_jobid')))
    where_plot = json.loads(request.args.get('measurement_catagories'))
    PD, FD, CW = {}, {}, {}
    print("Construct plot items:\n")
    # search(self.quantificationObj)
    routine = AutoScan1Q(sparam="",dcsweepch = "")
    if where_plot == "CS":
        print("CavitySearch start:\n")
        global progress
        progress = routine.id
        routine.cavitysearch(jobid=specific_id)
        CS = {'plot_items':routine.CS_plot_items,'overview':routine.CS_overview}  #{'5487 MHz':{'Frequency':[...],'Amplitude':[...],'UPhase':[...]},'~ MHz':{...},...}
                                                                                  #{'Frequency':[...],'Amplitude':[...],'UPhase':[...]}
        print("Construction Finish")
        return json.dumps(CS, cls=NumpyEncoder)
    elif where_plot == "PD":
        cavity = json.loads(request.args.get('target_cavity'))
        print("PowerDependent start:\n")
        routine.powerdepend(cavity,jobid=specific_id)
        f_bare = float(cavity.split(" ")[0])
        PD[cavity] = routine.PD_plot_items   # {"3D_axis":{"Frequency":[],"Power":[],"Amplitude":[]},"scatter":{'Power':[],'Fr':[]}}

        print("Construction Finish")
        return json.dumps(PD, cls=NumpyEncoder)
    elif where_plot == "FD":
        cavity = json.loads(request.args.get('target_cavity'))
        f_bare = float(cavity.split(" ")[0])
        print("FluxDependent start:\n")
        routine.fluxdepend(cavity,f_bare,jobid=specific_id)
        FD[cavity] = routine.FD_plot_items       # {"3D_axis":{"Frequency":[],"Flux":[],"Amplitude":[]},"scatter":{'Flux':[],'Fr':[]}}

        print("Construction Finish")
        return json.dumps(FD, cls=NumpyEncoder)
    else:
        cavity = json.loads(request.args.get('target_cavity'))
        print("QubitSearch start:\n")
        routine.qubitsearch(cavity,jobid=specific_id)
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
@bp.route('/get_test',methods=['POST','GET'])
def get_test():
    print("check here: ",progress)
    print('read address:',ctypes.cast(progress, ctypes.py_object).value)
    return json.dumps({'now':ctypes.cast(progress, ctypes.py_object).value}, cls=NumpyEncoder)