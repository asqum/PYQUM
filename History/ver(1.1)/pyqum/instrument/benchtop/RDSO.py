# Communicating with Benchtop RIGOL's Digital Storage Oscilloscope 

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # model's name e.g. ESG, PSG, MXG, AWG, VSA, ADC
debugger = 'debug' + mdlname

import visa
from functools import wraps
from pyqum.instrument.logger import address, set_status, status_code

import matplotlib.pyplot as plt
from numpy import arange, floor, ceil

def debug(state=False):
    exec('%s %s; %s = %s' %('global', debugger, debugger, 'state'), globals(), locals()) # open global and local both-ways channels!
    if state:
        print(Back.RED + '%s: Debugging Mode' %debugger.replace('debug', ''))
    return

debug() # declare the debugger mode here

# INITIALIZATION
def Initiate():
    rs = address(mdlname, reset=eval(debugger)) # Instrument's Address
    rm = visa.ResourceManager()
    try:
        bench = rm.open_resource(rs) #establishing connection using GPIB# with the machine
        stat = bench.write('*CLS') #Clear buffer memory; Load preset
        bench.write(':RUN') #Super-IMPORTANT for RiGoL!
        bench.write(':AUTOSCALE')
        bench.read_termination = '\n' #omit termination tag from output 
        bench.timeout = 150000 #set timeout in ms
        set_status(mdlname, dict(state='connected'))
        print(Fore.GREEN + "%s's connection Initialized: %s" % (mdlname, str(stat[1])[-7:]))
    except: 
        set_status(mdlname, dict(state='DISCONNECTED'))
        print(Fore.RED + "%s's connection NOT FOUND" % mdlname)
        bench = "disconnected"
    return bench

def Attribute(Name):
    @wraps(Name)
    def wrapper(*a, **b):

        global debug
        bench, SCPIcore, action = Name(*a, **b)
        SCPIcore = SCPIcore.split(";")
        headers = SCPIcore[0].split(':')
        parakeys, paravalues, getspecific, command = [headers[-1]] + SCPIcore[1:], [], [], []

        if action[0] == 'Get':
            try:
                for i in range(len(parakeys)):
                    if len(str(action[i+1])) > 0: #special type of query (e.g. commentstate)
                        getspecific.append(" " + str(action[i+1]))
                    else: getspecific.append('')
                    command.append(parakeys[i] + "?" + getspecific[i])

                command = ':'.join(headers[:-1] + [";".join(command)])
                paravalues = bench.query(command).split(';')
                #just in case of the presence of query parameters, which is rare
                paravalues = [paravalues[i] + '(' + str(action[i+1]) + ')' for i in range(len(parakeys))]
                paravalues = [x.replace('()', '') for x in paravalues]

                status = "Success"
            except: # get out of the method with just return-value at exception?
                status = "query unsuccessful"
                ans = None

        if action[0] == 'Set':

            for i in range(len(parakeys)):
                if str(action[i+1]) == '':
                    paravalues.append("NIL") # allow for arbitrary choosing
                else: 
                    paravalues.append(str(action[i+1]))
                    command.append(parakeys[i] + " " + paravalues[i])

            command = ':'.join(headers[:-1] + [";".join(command)])
            status = str(bench.write(command)[1])[-7:]
            
        # formatting return answer
        ans = dict(zip([a.replace('*','') for a in parakeys], paravalues))

        # Logging answer
        if action[0] == 'Get': # No logging for "Set"
            set_status(mdlname, {Name.__name__ : ans})

        # debugging
        if eval(debugger):
            print(Fore.BLUE + "SCPI Command: {%s}" %command)
            if action[0] == 'Get':
                print(Fore.YELLOW + "%s %s's %s: %s <%s>" %(action[0], mdlname, Name.__name__, ans, status))
            if action[0] == 'Set':
                print(Back.YELLOW + Fore.MAGENTA + "%s %s's %s: %s <%s>" %(action[0], mdlname, Name.__name__ , ans, status))

        return status, ans
    return wrapper

@Attribute
def model(bench, action=['Get'] + 10 * ['']):
    SCPIcore = '*IDN'  #inquiring machine identity: "who r u?"
    return bench, SCPIcore, action
@Attribute
def acquiredata(bench, action=['Get'] + 10 * ['']): # ACQUIRING DATA from RDS
    '''1. TYPE: {NORMal|AVERages|PEAK|HRESolution}
       2. AVERages: Set the number of averages and the value should be an integral multiple of 2.
       3. MDEPth: memory depth:
            single channel: <mdep> can be set to AUTO|14000|140000|1400000|1400000|140000000.
            more channels: <mdep> can be set to AUTO|7000|70000|700000|700000|70000000., 
       4. MODE: {RTIMe|ETIMe}
    '''
    SCPIcore = ':ACQUIRE:TYPE;AVERages;MDEPth;MODE'
    return bench, SCPIcore, action

@Attribute
def channel1(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <coupling>, <range>, <scale>, <offset>, <units>, <Display>]'''
    SCPIcore = ':CHANNEL1:COUPLING;RANGE;SCALE;OFFSET;UNITs;Display'
    return bench, SCPIcore, action
@Attribute
def channel2(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <coupling>, <range>, <scale>, <offset>, <units>, <Display>]'''
    SCPIcore = ':CHANNEL1:COUPLING;RANGE;SCALE;OFFSET;UNITs;Display'
    return bench, SCPIcore, action
@Attribute
def timebase(bench, action=['Get'] + 10 * ['']):
    '''action=['Get/Set', <mode>, <range[ns]>, <delay[ns]>, <scale[ns]>]'''
    SCPIcore = ':TIMEBASE:MODE;RANGE;DELAY;SCALE'
    return bench, SCPIcore, action
@Attribute
def waveform(bench, action=['Get'] + 10 * ['']): # SETTING UP WAVEFORM
    '''action=['Get/Set', <POINTS{MAX}>, <SOURCE{CHANNEL#}>, <FORMAT{ASCII}>, <XINCrement?>, <DATA?>]'''
    SCPIcore = ':WAVEFORM:POINTS;SOURCE;FORMAT;XINCrement;DATA'
    return bench, SCPIcore, action
@Attribute
def measure(bench, action=['Get'] + 10 * ['']): # SETTING UP WAVEFORM
    '''action=['Get', <COUNter>, <RISEtime>, <FALLtime>, <PWIDth>, <NWIDth>, <VPP>, <VAMP>, <VRMS>]'''
    SCPIcore = ':MEASure:COUNter;RISEtime;FALLtime;PWIDth;NWIDth;VPP;VAMP;VRMS'
    return bench, SCPIcore, action

def display2D(dx, y, units, channel):
    # setting image path
    from pathlib import Path
    from inspect import getfile, currentframe
    pyfilename = getfile(currentframe()) # current pyscript filename (usually with path)
    INSTR_PATH = Path(pyfilename).parents[2] / "static" / "img" / "rds" # 2 levels up the path
    image_file = "%swaveform(CH%s).png" %(mdlname, channel)
    IMG = Path(INSTR_PATH) / image_file
    # Scaling X
    from math import log10
    x_order = round(log10(dx))
    # Organizing Data
    Y = [float(i) for i in y.split(",")[1:-1]] # to avoid the first and the last string
    X = [x*dx/10**x_order for x in range(len(Y))]  #X = arange(0, len(Y), 1) * dx
    # Plotting
    fig, ax = plt.subplots()
    ax.plot(X, Y)
    ax.set(xlabel=r'$time({\times} 10^{%d}%s)$'%(x_order, units[0]))
    ax.set(ylabel=r'voltage (%s)'%units[1][0])
    ax.set(title="%s's Channel %s"%(mdlname, channel))
    plt.setp(ax.get_xticklabels(), rotation=0, horizontalalignment='right')
    fig.savefig(IMG, format="png")
    if eval(debugger):
        plt.show()

def close(bench, reset=True):
    try:
        if reset:
            bench.write(':STOP') # reset to STOP
            set_status(mdlname, dict(config='reset'))
        else: set_status(mdlname, dict(config='previous'))
        try:
            bench.close() #None means Success?
            status = "Success"
        except: status = "Error"
        set_status(mdlname, dict(state='disconnected'))
        print(Back.WHITE + Fore.BLACK + "%s's connection Closed" %(mdlname))
    except: 
        status = "disconnected per se!!!"
        pass
    return status

# Test Zone
def test(detail=True):
    debug(detail)
    print(Back.WHITE + Fore.MAGENTA + "Debugger mode: %s" %eval(debugger))
    bench = Initiate()
    if bench is "disconnected":
        pass
    else:
        print("This model:")
        model(bench)
        if eval(debugger):
            acquiredata(bench, action=['Set', 'NORMAL','',70000,''])
            acquiredata(bench)

            # status = channel1(bench) # channel 1
            # yrange, yscale, yoffset = status[1]['RANGE'], status[1]['SCALE'], status[1]['OFFSET']
            # channel1(bench, action=['Set', 'DC', yrange, yscale, yoffset, 'Volt', 'OFF'])

            # status = channel2(bench) # channel 2
            # yrange, yscale, yoffset = status[1]['RANGE'], status[1]['SCALE'], status[1]['OFFSET']
            # channel2(bench, action=['Set', 'DC', yrange, yscale, yoffset, 'Volt', 'OFF'])

            # status = timebase(bench) # timebase
            # trange, tdelay, tscale = status[1]['RANGE'], status[1]['DELAY'], status[1]['SCALE']
            # timebase(bench, action=['Set', 'NORMAL', trange, tdelay, tscale])
            # timebase(bench)

            # unitY = list(channel1(bench))[1]["UNITs"]
            # acquiredata(bench, action=['Set', 'average', '100', '7'])
            # status = acquiredata(bench)
            # print(status)

            # waveform(bench, action=['Set', 'max', 'channel1', 'ascii', '?', '?']) # "error: undefined header" will appear #this will light up channel1:display
            # ans = list(waveform(bench))[1]
            # y, dx = ans['DATA'], float(ans['XINCrement'])
            # measure(bench)
            # print(y)
            # display2D(dx, y, units=['s', unitY], channel=1)

            # waveform(bench, action=['Set', 'max', 'channel2', 'ascii', '?', '?']) # "error: undefined header" will appear #this will light up channel1:display
            # ans = list(waveform(bench))[1]
            # y, dx = ans['DATA'], float(ans['XINCrement'])
            # measure(bench)
            # print(y)
            # display2D(dx, y, units=['s', unitY], channel=2)

        else: print(Fore.RED + "Basic IO Test")
    close(bench)
    return


