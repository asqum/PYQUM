import visa
import numpy
from time import sleep

# ena
rm = visa.ResourceManager()
# ena = rm.open_resource('GPIB0::16::INSTR') #establishing GPIB connection with ENA E5071C
ena = rm.open_resource('TCPIP0::169.254.176.142::INSTR') #establishing LAN connection with ENA E5071C

ena.read_termination = '\n' #omit termination tag from output 
ena.timeout = 8000 #set timeout

#Checking Connections & Identities

# print('All connected GPIB Instruments:', rm.list_resources())
print(ena.query('*IDN?'))  #inquiring machine identity: "who r u?"

#Clear buffer memory
ena.write(':SENS:CORR:COLL:CLE') 

# set trace#
def setrace():
    ena.write('CALC1:PAR:COUN 2')
    # trace_num = ena.query_ascii_values('CALC1:PAR:COUN?', container=numpy.array)
    trace_num = ena.query('CALC1:PAR:COUN?')
    print('we have', int(trace_num), 'trace(s)')
    trace_info = ''
    for i in range(int(trace_num)):
        trace_info+=('trace#%s: ' %(i+1) + ena.query('CALC1:PAR%s:DEF?' %(i+1)) +'\n')
    print(trace_info)
    return int(trace_num)

## CALIBRATION
# checking connection between vna & ecal
def checkecalports():
    connected_vnaports = []
    vna_port_num = 4
    ecal_ports = ['0', 'A', 'B', 'C', 'D']

    for i in range(vna_port_num):
        ecal_port_id = ena.query(':SENS1:CORR:COLL:ECAL:PATH? %s' %(i+1))
        if (int(ecal_port_id)==0):
            print('VNA port %s is not connected' %(i+1))
        else:
            connected_vnaports.append(i+1)
            print('VNA port %s is connected to ECAL port %s' %(i+1, ecal_ports[int(ecal_port_id)]))

    # print(connected_vnaports)
    return connected_vnaports
# checking ecal ports
connected_vnaports = checkecalports()

def ecal():
    # ena.write(':SENS1:CORR:COLL:ECAL:SOLT2 1,2') #FDP (for debugging purposes)
    # select calibration type
    def TwoPorts():
        ena.write(':SENS1:CORR:COLL:ECAL:SOLT2 %s,%s' %(connected_vnaports[0], connected_vnaports[1]))
    def Thru():
        ena.write(':SENS1:CORR:COLL:ECAL:THRU %s,%s' %(connected_vnaports[0], connected_vnaports[1]))
    options = {2 : TwoPorts,
            1 : Thru 
            }
    while True:
        try:
            option_id = int(input('Calibration type? (1:Through, 2:Two-Ports)'))
            if option_id in (1, 2):
                break
            else:
                print('There is no such type!') #prevent int other than (1,2)
        except:
            print('Not a valid type!') #prevent run-error
    options[option_id]() #run func from dict
# ecal()

# START TRANSLATION FROM LABVIEW
status = ena.write("FORMat:DATA ASCii,0")
print("Format data: %s" %[x for x in status])
trace_num = setrace()
status = ena.query("SENS:SWE:TYPE?")
print("Sweeping Type: %s" %status)
status = ena.query("SENSe:SWEep:POINts?")
print("Sweeping Points#: %s" %status)
sweeptime = ena.query("SENS:SWE:TIME?")
print("Sweeping Time: %s" %sweeptime)

status = ena.query("SENSe:FREQuency:STARt?")
print("Start Frequency(Hz): %s" %status)
status = ena.query("SENSe:FREQuency:STOP?")
print("Stop Frequency(Hz): %s" %status)

status = ena.query("SENSe:BANDwidth?") #IF Freq
print("Bandwidth (Hz): %s" %status)
status = ena.query("SOURce:POWer?")
print("Power (dBm): %s" %status)

status = ena.write("SENSe:AVER ON") #OFF
print("Set Average ON: %s" %[x for x in status])
Ave_num = 5
status = ena.write("SENSe:AVER:COUN %s" %Ave_num)
print("Set Average Number=%s: %s" %(Ave_num, [x for x in status]))
status = ena.write("SENSe:AVER:CLE")
print("Clear Average: %s" %[x for x in status])
status = ena.write("TRIG:SOUR INT;INIT:CONT ON") #INIT:CONT OFF;INIT:IMM
print("Set Continuous: %s" %[x for x in status])

# switch on ena
ena.write('OUTP ON')

# Waiting while sweeping
waitime = 180 #sec
# sleep(Ave_num*float(sweeptime) + waitime)

# for i in range(trace_num):
#     status = ena.write("CALC:PAR%d:SEL"%(i+1))


i = 1
data = ena.query("CALC:TRAC%d:DATA:FDATA?"%i)
print([x for x in data])



# switch off ena
ena.write('OUTP OFF')
ena.close()
