from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm.simulate.credentials import create_credentials
from qm import SimulationConfig
from configuration import *
from qm.simulate import LoopbackInterface
import matplotlib.pyplot as plt
from qualang_tools.units import unit
from qualang_tools.loops import from_array

qmm = QuantumMachinesManager(host=qop_ip, port=80)
qm = qmm.open_qm(config)

# rr2
freqs = np.arange(-135e6, -128e6, 0.05e6)

## rr1
# freqs = np.arange(47e6, 51e6, 0.05e6)

with program() as res_spec:

    n = declare(int)
    f = declare(int) # Hz int 32 up to 2^32
    I = declare(fixed) # signed 4.28 [-8, 8)
    Q = declare(fixed)
    I_st = declare_stream()
    Q_st = declare_stream()
    
    with for_(n, 0, n < 10000, n+1):
        with for_(*from_array(f, freqs)):
            update_frequency("rr2", f)
            wait(250, "rr2")
            measure("readout", "rr2", None, dual_demod.full("cos", "out1", "sin", "out2", I),
                    dual_demod.full("minus_sin", "out1", "cos", "out2", Q))
            # measure("readout", "rr1", None, dual_demod.full("cos", "out1", "minus_sin", "out2", I),
            #         dual_demod.full("sin", "out1", "cos", "out2", Q)) #rr1
            save(I, I_st)
            save(Q, Q_st)

    with stream_processing():
        I_st.buffer(len(freqs)).average().save("I")
        Q_st.buffer(len(freqs)).average().save("Q")

job = qm.execute(res_spec)

res_handles = job.result_handles
res_handles.wait_for_all_values()
I = res_handles.get("I").fetch_all()
Q = res_handles.get("Q").fetch_all()

s = I + 1j*Q
u = unit()
LO = resonator_LO/u.MHz

plt.plot(LO - freqs/u.MHz, np.abs(s)) # for rr2
# plt.plot(LO + freqs/u.MHz, np.abs(s)) # for rr1
idx = np.argmin(np.abs(s))
print("IF freq at resonance: {}".format(freqs[idx]))
plt.title('rr2')
plt.show()

