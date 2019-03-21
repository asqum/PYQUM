import visa


try:
    address = "visa://192.168.1.23:7777/ASRL3::INSTR"

    rm = visa.ResourceManager()
    bench = rm.open_resource(address) #, baud_rate=57600, data_bits=7)
    print(bench)
    bench.baud_rate, bench.data_bits = 57600, 7
    bench.parity = visa.constants.Parity(1)
    bench.stop_bits = visa.constants.StopBits(10)
    bench.timeout = 7000
    bench.read_termination = '\r\n'

    interface = str(bench.interface_type).split('.')[1].upper()
    print("INTERFACE: %s" %interface)
    print("INTERFACE is SERIAL: %s" %(interface == 'ASRL'))

    model = bench.query('*IDN?')
    print("MODEL: %s" %model)

    print('\nTemperature:')
    T1 = bench.query('RDGK? 1')
    print("T1: %sK" %str(T1))
    T2 = bench.query('RDGK? 2')
    print("T2: %sK" %T2)
    T5 = bench.query('RDGK? 5')
    print("T5: %sK" %T5)

    print('\nResistance:')
    R1 = bench.query('RDGR? 1')
    print("R1: %sOhm" %R1)
    R2 = bench.query('RDGR? 2')
    print("R2: %sOhm" %R2)
    R5 = bench.query('RDGR? 5')
    print("R5: %sOhm" %R5)

    print('\nPower:')
    P1 = bench.query('RDGPWR? 1')
    print("P1: %sW" %P1)
    P2 = bench.query('RDGPWR? 2')
    print("P2: %sW" %P2)
    P5 = bench.query('RDGPWR? 5')
    print("P5: %sW" %P5)

    print("Display setting: %s" %bench.query("display?"))
    bench.write("display 2,2,2")
    # bench.write("display 2,1,2")
    # bench.write("display 1,2,1")

except:
    print(rm.last_status)
    if rm.last_status == visa.constants.StatusCode.error_resource_not_found:
        print("Please make sure the address is correct or the instrument is turned on")
    elif rm.last_status == visa.constants.StatusCode.error_resource_busy:
        print("The instrument is still busy with another session")
    