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
def auto_measurement():  # designed is the cavity number should exist

    dc_ch = json.loads(request.args.get('dc_channel'))
    port = json.loads(request.args.get('inout_port'))
    print("Automatic measurement gogogo\n")
    # search(self.quantificationObj)
    routine = AutoScan1Q(sparam=port,dcsweepch = dc_ch)
    print("CavitySearch start:\n")
    routine.cavitysearch()
    CS = {'answer':routine.cavity_list,'plot_items':routine.CS_plot_items,'overview':routine.CS_overview}  #{'5487 MHz':{'Frequency':[...],'Amplitude':[...],'UPhase':[...]},'~ MHz':{...},...}
    PD, FD, CW = {}, {}, {}
    jobid = {'CavitySearch':routine.CS_jobid}
    for i in routine.total_cavity_list:
        print("PowerDependent start:\n")
        power_df = routine.powerdepend(i)
        f_bare = mean(routine.cavity_list[str(i)])
        PD[i]={'power':routine.select_power,'arrays':power_df} #need to check

        print("FluxDependent start:\n")
        flux_df = routine.fluxdepend(i,f_bare)
        FD[i]={'flux':routine.wave,'arrays':flux_df}  #need to check

        print("CWsweep start:\n")
        routine.qubitsearch(i)
        CW[i]={'q_freq':routine.readout_para[i]["qubit"],'Ec':routine.readout_para[i]["Ec"],'acStark':routine.readout_para[i]["acStark"],'plot_items':routine.CW_plot_items} #AutoScan1Q_classfile.py has not complete this part  
        
        jobid[i] = routine.jobid_dict       
        break
    #jobid = {'CavitySearch':2051,'5487 MHz':{"PowerDepend":1000,"FluxDepend":1001,"QubitSearch":1002},...}
    print("Measurement Finish")
    measure_result = {"CS":CS,"PD":PD,"FD":FD,"CW":CW,"JOBID":jobid}
    return json.dumps(measure_result, cls=NumpyEncoder)

# developing.... try to put the paras in dictionary with corresponding key
@bp.route('/measurement_paras',methods=['POST','GET'])
def get_paras():
    path='pyqum.sqlite'
    connection = connect(path)
    job = read_sql_query("SELECT*FROM job",connection)
    id = json.loads(request.args.get('this_jobid'))
    paras = job[job['id']==id]['parameter'].iloc[0]
    para_dict = {paras}     # <- trying...
    return json.dumps(para_dict, cls=NumpyEncoder)

