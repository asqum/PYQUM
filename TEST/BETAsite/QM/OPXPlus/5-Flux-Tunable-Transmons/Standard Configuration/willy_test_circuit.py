from qutip_qip.circuit import QubitCircuit
import numpy as np
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
from configuration import *
import matplotlib.pyplot as plt
import numpy as np
from TQRB.CircuitResult import CircuitResult
from TQCompiler import *
import warnings

# cnot:q2_y90,q2_x180,cz,q2_y90,q2_x180
gate_seq = [
    # q4_x90,q_y90,q2_x180,cz,q2_y90,q2_x180
    idle_gate
]
circuit = QubitCircuit(2)
for gate in gate_seq:
    circuit.add_gate(gate)
n_avg = 2000

mycompiler = TQCompile( 2, q1_frame_update= 0.64, q2_frame_update= 0.86, params={}, cz_type='square' )
with program() as prog:
    n = declare(int)
    n_st = declare_stream()  
    state = declare(int)
    state_os = declare_stream()

    ####  TEST GATE
    with for_(n, 0, n < n_avg, n + 1):  
        wait(thermalization_time)
        compiled_data = mycompiler.compile(circuit,schedule_mode='ASAP')
        align()
        wait(flux_settle_time * u.ns)
        out1, out2 = meas()
        assign(state, (Cast.to_int(out2) << 1) + Cast.to_int(out1))
        save(state, state_os)
        save(n, n_st)
    with stream_processing():
        n_st.save("n")
        state_os.buffer(n_avg).save("state") 

simulate = False
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config) 
if simulate:
    simulation_config = SimulationConfig(duration=10_000)  # In clock cycles = 4ns
    job = qmm.simulate(config, prog, simulation_config)
    job.get_simulated_samples().con1.plot()
    # job.get_simulated_samples().con2.plot()
    plt.show()
else:
    qm = qmm.open_qm(config)
    job = qm.execute(prog)
    job.result_handles.wait_for_all_values()
    circuitresult = CircuitResult(
        num_averages=n_avg,
        state=job.result_handles.get("state").fetch_all(),
    ) 
    circuitresult.plot_hist()
    plt.show()
