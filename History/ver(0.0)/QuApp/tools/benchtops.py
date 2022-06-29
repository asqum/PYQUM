import visa

def ESG(switch, frequency=3, power=-5):
    display = dict()
    rm = visa.ResourceManager()
    esg = rm.open_resource('GPIB0::27::INSTR') #establishing connection using GPIB# with the machine
    esg.write('*CLS') #Clear buffer memory
    esg.write('*RST')
    esg.read_termination = '\n' #omit termination tag from output 
    esg.timeout = 15000 #set timeout in ms

    display['Identity'] = esg.query('*IDN?')  #inquiring machine identity: "who r u?"

    if switch is True:
        # setting params
        fa = frequency
        powa = power
        esg.write(':SOUR:FREQ:FIX %sGHZ' %fa)
        esg.write(':POWer:LEVel %sDBM' %powa)
        display['Frequency'] = esg.query(':SOUR:FREQ?')
        display['Power'] = esg.query(':SOUR:POW:LEV?')
        
        esg.write('OUTP ON')

    elif switch is False:
        esg.write('OUTP OFF')

    display['STATE'] = esg.query(':OUTPut:STATe?')
    if display['STATE'] is 0: esg.close()

    return display

# for DEBUGGING
# status = ESG(True)
# print(status)