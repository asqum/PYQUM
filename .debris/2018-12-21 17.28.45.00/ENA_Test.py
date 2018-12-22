import visa
import numpy

# ena
rm = visa.ResourceManager()
ena = rm.open_resource('GPIB0::16::INSTR') #establishing GPIB connection with ENA E5071C
# ena = rm.open_resource('TCPIP0::169.254.176.142::INSTR') #establishing LAN connection with ENA E5071C

ena.read_termination = '\n' #omit termination tag from output 
ena.timeout = 8000 #set timeout

#Checking Connections & Identities

# print('All connected GPIB Instruments:', rm.list_resources())
print(ena.query('*IDN?'))  #inquiring machine identity: "who r u?"

#Clear buffer memory
ena.write(':SENS:CORR:COLL:CLE') 

# switch on ena
ena.write('OUTP ON')

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

ecal()

# Extract confidence


# switch off ena
ena.write('OUTP OFF')
ena.close()
