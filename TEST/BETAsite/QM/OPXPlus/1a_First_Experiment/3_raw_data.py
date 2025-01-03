from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm.simulate.credentials import create_credentials
from qm import SimulationConfig
from configuration import config, qop_ip
from qm.simulate import LoopbackInterface
import matplotlib.pyplot as plt
from qualang_tools import units

qmm = QuantumMachinesManager(host=qop_ip, port=80)
qm = qmm.open_qm(config)

u = units.unit()

n_avg = 100  # Number of averaging loops

###################
# The QUA program #
###################
with program() as raw_trace_prog:
    n = declare(int)
    adc_st = declare_stream(adc_trace=True)

    with for_(n, 0, n < n_avg, n + 1):
        reset_phase("rr1")
        measure("readout", "rr1", adc_st)
        wait(7000, "rr1")

    with stream_processing():
        # Will save average:
        adc_st.input1().average().save("adc1")
        adc_st.input2().average().save("adc2")
        # # Will save only last run:
        adc_st.input1().save("adc1_single_run")
        adc_st.input2().save("adc2_single_run")

#####################################
#  Open Communication with the QOP  #
#####################################
qm = qmm.open_qm(config)
job = qm.execute(raw_trace_prog)
res_handles = job.result_handles
res_handles.wait_for_all_values()
adc1 = u.raw2volts(res_handles.get("adc1").fetch_all())
adc2 = u.raw2volts(res_handles.get("adc2").fetch_all())
adc1_single_run = u.raw2volts(res_handles.get("adc1_single_run").fetch_all())
adc2_single_run = u.raw2volts(res_handles.get("adc2_single_run").fetch_all())

plt.figure()
plt.subplot(121)
plt.title("Single run")
plt.plot(adc1_single_run, label="Input 1")
plt.plot(adc2_single_run, label="Input 2")
plt.xlabel("Time [ns]")
plt.ylabel("Signal amplitude [V]")
plt.legend()

plt.subplot(122)
plt.title("Averaged run")
plt.plot(adc1, label="Input 1")
plt.plot(adc2, label="Input 2")
plt.xlabel("Time [ns]")
plt.legend()
plt.tight_layout()

print(f"\nInput1 mean: {np.mean(adc1)} V\n" f"Input2 mean: {np.mean(adc2)} V")
plt.show()