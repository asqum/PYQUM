import visa

address = "visa://192.168.1.23:7777/ASRL3::INSTR"

rm = visa.ResourceManager()
bench = rm.open_resource(address, baud_rate=57600, data_bits=7)
bench.parity = visa.constants.Parity(1)
bench.stop_bits = visa.constants.StopBits(10)
print("INTERFACE: %s" %str(bench.interface_type).split('.')[1].upper())

bench.timeout = 7000
# bench.read_termination = '\n'

model = bench.query('*IDN?')
print(model)

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

bench.write("display 2,2,1")
# bench.write("display 1,2,1")