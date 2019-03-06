import visa


address = "visa://192.168.1.23:7777/ASRL3::INSTR"

rm = visa.ResourceManager()
bench = rm.open_resource(address, baud_rate=57600, data_bits=7)
bench.parity = visa.constants.Parity(1)
bench.stop_bits = visa.constants.StopBits(10)


bench.timeout = 7000
bench.read_termination = '\n'

model = bench.query('*IDN?')
print(model)

T1 = bench.query('RDGK? 1')
print("T1: %s" %T1)
T2 = bench.query('RDGK? 2')
print("T5: %s" %T2)
T5 = bench.query('RDGK? 5')
print("T5: %s" %T5)

bench.write("display 2,2,1")
# bench.write("display 1,2,1")