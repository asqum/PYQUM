import visa
from pyqum.instrument.logger import address, set_status
ESGrs = address("ESG")

def control(switch, frequency=3, power=-5):
    info = dict()
    rm = visa.ResourceManager()
    esg = rm.open_resource(ESGrs) #establishing connection using GPIB# with the machine
    esg.write('*CLS') #Clear buffer memory
    esg.write('*RST')
    esg.read_termination = '\n' #omit termination tag from output 
    esg.timeout = 15000 #set timeout in ms
    info['Identity'] = esg.query('*IDN?')  #inquiring machine identity: "who r u?"

    if switch is True:
        fa, powa = frequency, power

        # esg.write(':SOUR:FREQ %sMHZ' %fa)
        stat = esg.write(':SOUR:FREQ:FIX %sMHZ' %fa)
        print("\nwrite freq:", str(stat[1]))
        print("write freq:", str(stat[1])[-7:])

        # esg.write(':SOUR:FREQ:FIX %sGHZ' %fa)

        # esg.write(':SOUR:POW %sDBM' %powa)
        stat = esg.write(':SOUR:POW:LEV %sDBM' %powa)
        print("write pow:", stat)
        # esg.write(':POWer:LEVel %sDBM' %powa)

        ans = esg.query(':SOUR:FREQ?')
        info['Frequency'] = float(ans)
        ans = esg.query(':SOUR:POW?')
        # ans = esg.query(':SOUR:POW:LEV?')
        info['Power'] = float(ans)
        
        # stat = esg.write('OUTP ON')
        stat = esg.write('OUTP:STAT 1')
        print("ON:", stat)

    elif switch is False:
        esg.write('OUTP OFF')

    info['State'] = esg.query('OUTP?')
    # info['State'] = esg.query(':OUTPut:STATe?')
    if info['State'] == '0':
        esg.close() #close if switched off
        info['State']='OFF'
    elif info['State'] == '1':
        info['State']='ON'
    # else: info['State']='ERROR'

    set_status("ESG", info)
    return info

info = control(True, 2700, -48)
print(info)