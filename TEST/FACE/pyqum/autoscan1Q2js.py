from benchmark import AutoScan1Q
from flask import Blueprint, request
from sqlite3 import connect
from pandas import read_sql_query
import json
from numpy import ndarray,mean,array
from colorama import init, Fore, Back, Style

from os.path import basename as bs
myname = bs(__file__).split('.')[0] # This py-script's name
bp = Blueprint(myname, __name__, url_prefix='/autoscan1Q2js')

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
    print("Automatic measurement gogogo\n")
    # search(self.quantificationObj)
    routine = AutoScan1Q(sparam=port,dcsweepch = dc_ch)
    print("CavitySearch start:\n")
    routine.cavitysearch(jobid="")
    CS = {'answer':routine.cavity_list}  #{'5487 MHz':{'Frequency':[...],'Amplitude':[...],'UPhase':[...]},'~ MHz':{...},...}
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

    #return json.dumps(measure_result, cls=NumpyEncoder)

# developing.... try to put the paras in dictionary with corresponding key
@bp.route('/measurement_paras',methods=['POST','GET'])
def get_paras():
    id = json.loads(request.args.get('this_jobid'))

    path='pyqum.sqlite'
    connection = connect(path)
    job = read_sql_query("SELECT*FROM job",connection)
    paras = job[job['id']==id]['parameter'].iloc[0]    # <- this is a dictionary with F-response: {'Flux-Bias':fluxbias, 'S-Parameter':sparam, 'IF-Bandwidth':ifb, 'Power':powa, 'Frequency':freq}
    return json.dumps(paras, cls=NumpyEncoder)                                 # with CWsweep: {'Flux-Bias':fluxbias, 'XY-Frequency':xyfreq, 'XY-Power':xypowa, 'S-Parameter':sparam, 'IF-Bandwidth':ifb, 'Frequency':freq, 'Power':powa}

# get the specific jobid in the sample description
# set a search button for jobid
@bp.route('/get_jobid',methods=['POST','GET'])
def get_jobid():
    JOBIDs = json.loads(request.args.get('jobid_dict'))
    return json.dumps(JOBIDs, cls=NumpyEncoder)     # contains {'CavitySearch':2051,'PowerDepend':{'5487 MHz':2052,...},'FluxDepend':{'5487 MHz':2053,...},'QubitSearch':{'5487 MHz':2054,...}}


# not for measurement but for plot with a specific jobid
@bp.route('/plot_result',methods=['POST','GET'])
def plot_after_jobid():
    specific_id = json.loads(request.args.get('specific_jobid'))
    cavity = json.loads(request.args.get('target_cavity'))
    where_plot = json.loads(request.args.get('measurement_catagories'))
    PD, FD, CW = {}, {}, {}
    print("Construct plot items:\n")
    # search(self.quantificationObj)
    routine = AutoScan1Q(sparam="",dcsweepch = "")
    if where_plot == "CS":
        print("CavitySearch start:\n")
        routine.cavitysearch(jobid=specific_id)
        CS = {'plot_items':routine.CS_plot_items,'overview':routine.CS_overview}  #{'5487 MHz':{'Frequency':[...],'Amplitude':[...],'UPhase':[...]},'~ MHz':{...},...}
        
        print("Construction Finish")
        return json.dumps(CS, cls=NumpyEncoder)
    elif where_plot == "PD":
        print("CavitySearch start:\n")
        routine.cavitysearch(jobid=specific_id)
        print("PowerDependent start:\n")
        routine.powerdepend(cavity,jobid=specific_id)
        f_bare = float(cavity.split(" ")[0])
        PD[cavity]={routine.PD_plot_items} #need to check

        print("Construction Finish")
        return json.dumps(PD, cls=NumpyEncoder)
    elif where_plot == "FD":
        print("CavitySearch start:\n")
        routine.cavitysearch(jobid=specific_id)
        print("PowerDependent start:\n")
        routine.powerdepend(cavity,jobid=specific_id)
        f_bare = float(cavity.split(" ")[0])
        print("FluxDependent start:\n")
        routine.fluxdepend(cavity,f_bare,jobid=specific_id)
        FD[cavity] = routine.FD_plot_items  #need to check

        print("Construction Finish")
        return json.dumps(FD, cls=NumpyEncoder)
    else:
        print("CavitySearch start:\n")
        routine.cavitysearch(jobid=specific_id)
        print("PowerDependent start:\n")
        routine.powerdepend(cavity,jobid=specific_id)
        f_bare = float(cavity.split(" ")[0])
        print("FluxDependent start:\n")
        routine.fluxdepend(cavity,f_bare,jobid=specific_id)
        print("CWsweep start:\n")
        routine.qubitsearch(cavity,jobid=specific_id)
        CW[cavity] = routine.CW_plot_items

        print("Construction Finish")
        return json.dumps(CW, cls=NumpyEncoder)
    