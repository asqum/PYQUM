#---------------load package of load_data---------------
from os import stat
from numpy import prod,array,ndarray,append, floor, int64, delete, dstack, sqrt
from json import loads
from ast import literal_eval
from re import split
from numpy import linspace, prod
from pandas import DataFrame,concat
from sqlite3 import connect
from pandas import read_sql_query



class waveform:
    '''Guidelines for Command writing:\n
        1. All characters will be converted to lower case.\n
        2. Use comma separated string to represent string list.\n
        3. Inner-Repeat is ONLY used for CW_SWEEP: MUST use EXACTLY ' r ' (in order to differentiate from r inside word-string).\n
        4. waveform.inner_repeat: the repeat-counts indicated after the ' r ' or '^', determining how every .data's element will be repeated.\n
        5. Option to let waveform be 'function-ized' using f: <base/power/log..> at the end of the command/ order:
            a. Base: data points from dense to sparse.
            b. Power: 0-1: same with Log, >1: same with Base, but slower.
            c: Log: data points from sparse to dense.
        NOTE: '^' is equivalent to ' r ' without any spacing restrictions.
    '''
    def __init__(self, command):
        # defaulting to lower case
        command = str(command)
        self.command = command.lower()

        # special treatment to inner-repeat command: (to extract 'inner_repeat' for cwsweep averaging)
        self.inner_repeat = 1
        if ' r ' in self.command:
            self.command, self.inner_repeat = self.command.split(' r ')
            while " " in self.inner_repeat: self.inner_repeat = self.inner_repeat.replace(" ","")
            self.inner_repeat = int(self.inner_repeat)
        if '^' in self.command:
            self.command, self.inner_repeat = self.command.split('^')
            while " " in self.inner_repeat: self.inner_repeat = self.inner_repeat.replace(" ","")
            self.inner_repeat = int(self.inner_repeat)

        # correcting back ("auto-purify") the command-string after having retrieved the repeat-count or not:
        # get rid of multiple spacings
        while " "*2 in self.command:
            self.command = self.command.replace(" "*2," ")
        # get rid of spacing around keywords
        while " *" in self.command or "* " in self.command:
            self.command = self.command.replace(" *","*")
            self.command = self.command.replace("* ","*")
        while " to" in self.command or "to " in self.command:
            self.command = self.command.replace(" to","to")
            self.command = self.command.replace("to ","to")
        while " (" in self.command or "( " in self.command:
            self.command = self.command.replace(" (","(")
            self.command = self.command.replace("( ","(")
        while " )" in self.command or ") " in self.command:
            self.command = self.command.replace(" )",")")
            self.command = self.command.replace(") ",")")
        while " f" in self.command or "f " in self.command:
            self.command = self.command.replace(" f","f")
            self.command = self.command.replace("f ","f")
        while " :" in self.command or ": " in self.command:
            self.command = self.command.replace(" :",":")
            self.command = self.command.replace(": ",":")
        while " /" in self.command or "/ " in self.command:
            self.command = self.command.replace(" /","/")
            self.command = self.command.replace("/ ","/")
        # print(Fore.CYAN + "Command: %s" %self.command)
        
        command = self.command.split(" ") + [""]
        
        # 1. building string list:
        if ("," in command[0]) or ("," in command[1]):
            # remove all sole-commas from string list command:
            command = [x for x in command if x != ',']
            # remove all attached-commas from string list command:
            command = [i for x in command for i in x.split(',') if i != '']
            self.data = command
            self.count = len(command)
        # 2. building number list:
        else:
            command = [x for x in command if x != ""]
            self.data, self.count = [], 0
            for cmd in command:
                self.count += 1
                if "*" in cmd and "to" in cmd:
                    C = [j for i in cmd.split("*") for j in i.split('to')]
                    try:
                        start = float(C[0])
                        steps = range(int(len(C[:-1])/2))
                        for i, target, asterisk in zip(steps,C[1::2],C[2::2]):
                            num = asterisk.split("f:")[0]
                            self.count += int(num)
                            # 2a. Simple linear space / function:
                            self.data += list(linspace(start, float(target), int(num), endpoint=False, dtype=float64))
                            if i==steps[-1]: 
                                self.data += [float(target)] # data assembly complete
                                # 2b. Customized space / function for the WHOLE waveform: base, power, log scales
                                if "f:" in asterisk:
                                    func = asterisk.split("f:")[1]
                                    # print(Fore.CYAN + "Function: %s" %func)
                                    if 'base' in func:
                                        if "e" == func.split('/')[1]: self.data = list(exp(self.data))
                                        else: self.data = list(power(float(func.split('/')[1]), self.data))
                                    elif 'power' in func:
                                        self.data = list(power(self.data, float(func.split('/')[1])))
                                    elif 'log10' in func:
                                        self.data = list(log10(self.data))
                                    elif 'log2' in func:
                                        self.data = list(log2(self.data))
                                    elif 'log' in func:
                                        self.data = list(log(self.data))
                                    else: print("Function NOT defined YET. Please consult developers")
                                    print("scaled %s points" %len(self.data))
                            else: 
                                start = float(target)
                    except: # rooting out the wrong command:
                        # raise
#                         print("Invalid command")
                        pass
                else: self.data.append(float(cmd))     

def variable(i,change_list,corder):
    try:
        tmp = split('[to*]',waveform(corder[change_list[i]]).command)
        out = list(linspace(float(tmp[0]), float(tmp[2]), int(tmp[3])+1))
    except:
        out = split(' ',waveform(corder[change_list[i]]).command)
    return out

def multiply_except_self(where, alist):
    repeat, group = 1,1
    for i in range(len(alist)):
        if i > where:
            repeat*=alist[i]
        elif i < where:
            group*=alist[i]
    return repeat, group

def construct_layer(where,change_list,change_list_len,corder):
    if len(change_list)==1:
        out = variable(where,change_list,corder)
        out.sort()
    else:
        repeat, group = multiply_except_self(where, change_list_len)
        out = variable(where,change_list,corder)*int(repeat)
        out.sort()
        out = out*int(group)
    return out

def repeatable(data,repeatlist,corder):
    repeat_len = waveform(corder[repeatlist[0]]).inner_repeat
    mean_data = data.reshape((-1,repeat_len)).mean(axis=1)
    return mean_data
        
def jobid_search_pyqum(id):
    # --------------Search Path --------------
    path = r'C:\Users\ASQUM\HODOR\CONFIG\pyqum.sqlite'
    conn = connect(path)
    job = read_sql_query("SELECT * FROM job", conn)
    user = read_sql_query("SELECT * FROM user", conn)[['id','username']]
    sample = read_sql_query("SELECT * FROM sample", conn)[['id','samplename','author_id']]
    queue = read_sql_query("SELECT * FROM queue", conn)
    sample_id = job[job['id']==id]['sample_id'].iloc[0]
    queue_name = job[job['id']==id]['queue'].iloc[0]
    dateday = job[job['id']==id]['dateday'].iloc[0]
    task = job[job['id']==id]['task'].iloc[0]
    wmoment  = job[job['id']==id]['wmoment'].iloc[0]
    name_id = sample[sample['id']==sample_id]['author_id'].iloc[0]
    name = user[user['id']==name_id]['username'].iloc[0]
    sample_name = sample[sample['id']==sample_id]['samplename'].iloc[0]
    mission = queue[queue['system']==queue_name]['mission'].iloc[0]
    pyqum_path = r"C:\Users\ASQUM\HODOR\CONFIG\USRLOG\%s\%s\%s\%s\%s.pyqum(%d)"%(name,sample_name,mission,dateday,task,wmoment)
    print("Path : ",pyqum_path)
    return pyqum_path,task

def load_rawdata(pyqum_path):
    # --------------load IQdata --------------
    filesize = stat(pyqum_path).st_size
    with open(pyqum_path, 'rb') as datapie:
    #     print(datapie.read())
        i = 0
        while i < (filesize):
            datapie.seek(i)
            bite = datapie.read(7)
            if bite == b'\x02' + bytes("ACTS", 'utf-8') + b'\x03\x04': # ACTS
                datalocation = i
                break
            else: i += 1
        datapie.seek(datalocation+7)
        writtensize = filesize-datalocation-7
        pie = datapie.read(writtensize)
        datacontainer = bite.decode('utf-8')
    selectdata = ndarray(shape=(writtensize//8,), dtype=">d", buffer=pie) # speed up with numpy ndarray, with the ability to do indexing in it.
    # print("Select Data length: %s" %len(selectdata))
    # print(selectdata)
    # --------------load C-order --------------
    with open(pyqum_path, 'rb') as datapie:
        datapie.seek(17)
    #     print(datapie.read())
        dict_label = datapie.read(datalocation-18)
    dict_str = dict_label.decode("UTF-8")
    file_label = literal_eval(dict_str)
    # print(file_label)
    corder = file_label['c-order']
    print("C-order : \n"+str(corder))
    print("\nComment : \n"+str(file_label['comment']))
    # --------------load Perimeter --------------
    try: perimeter = file_label['perimeter']
    except(KeyError): perimeter = {}
    print("\nperimeter : \n"+str(perimeter))
    try: jobid = perimeter['jobid']
    except(KeyError): jobid = 0
    store_shape = array([waveform(x).count * waveform(x).inner_repeat for x in corder.values()])
    cdatasize = int(prod(store_shape, dtype='uint64')) * file_label['data-density'] #data density of 2 due to IQ
    print("\nC-order Data size: \n%s" %cdatasize)
    print("Select Data length: \n%s" %len(selectdata))   
    # --------------Check data integrity --------------
    if cdatasize == len(selectdata):
        print("\tChecked!\n")
        print("Start load data....")
    else:
        print("examine pyqum data")
    
    return selectdata, corder, jobid, file_label['data-density']

def command_analytic(selectdata,corder,datadensity):
    C_structure = [i for i in corder]
    print("C-order : ",C_structure)
    x,r,parameter,x_len = [],[],[],[]
    for i in corder:
        if waveform(corder[i]).count !=1:
            x = append(x,i)
            x_len = append(x_len,waveform(corder[i]).count)
        elif waveform(corder[i]).inner_repeat !=1:
            r = append(r,i)
        else:
            parameter = append(parameter,i)
    print("Change : ",x)
    print("Repeat : ",r)
    print("Unchange : ",parameter)
    print("\n")
    selectdata_i_data = selectdata[::datadensity]
    selectdata_q_data = selectdata[1::datadensity]
    while len(r)!=0:
        selectdata_i_data = repeatable(selectdata_i_data,r,corder)
        selectdata_q_data = repeatable(selectdata_q_data,r,corder)
        r = delete(r,0)
    if len(x)==1:
        df_label = DataFrame(construct_layer(0,x,x_len,corder), columns = [x[0]])
    else:
        df = DataFrame()
        for i in range(len(x)):
            df1 = DataFrame(construct_layer(i,x,x_len,corder), columns = [x[i]])
            df = concat([df,df1],axis =1)
        df_label = df
    return selectdata_i_data,selectdata_q_data, df_label
def pyqum_load_data(pyqum_path):
    selectdata, corder, jobid, datadensity = load_rawdata(pyqum_path)
    mean_i_data, mean_q_data, df_label = command_analytic(selectdata,corder,datadensity)
    df_i = DataFrame(mean_i_data, columns = ['I'])
    df_q = DataFrame(mean_q_data, columns = ['Q'])
    df_data = concat([df_i,df_q],axis =1)
    tidy_data = concat([df_label,df_data],axis =1)
    df_amp =DataFrame(sqrt(tidy_data['I']**2+tidy_data['Q']**2), columns = ['Amp'])
    amp_data = concat([tidy_data,df_amp],axis =1)
    
    return amp_data,jobid

# if __name__ == "__main__":
#     id = int(input("id? : "))
#     pyqum_path,task = jobid_search_pyqum(id)
#     amp_data,jobid  = pyqum_load_data(pyqum_path)



