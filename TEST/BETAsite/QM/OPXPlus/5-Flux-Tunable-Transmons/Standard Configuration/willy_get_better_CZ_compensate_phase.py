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
# cnot:q3_y90,q3_x180,cz,q3_y90,q3_x180
gate_seq = [
    q3_x180,q2_y90,q2_x180,cz,q2_y90,q2_x180
    # q2_x180,q3_y90,q3_x180,cz,q3_y90,q3_x180
]
circuit = QubitCircuit(2)
for gate in gate_seq:
    circuit.add_gate(gate)
n_avg = 2000
state_0 =[]
phase_list = []
ticks = 50
state_count_list = [3]
for i in range(ticks):
    phase_list.append(i/ticks)
## q1 0.524, q2 0.373
for phase in phase_list:
    mycompiler = TQCompile( 2, q1_frame_update= phase, q2_frame_update= 0.86, params={}, cz_type='eerp' )
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
        plt.show()
    else:
        qm = qmm.open_qm(config)
        job = qm.execute(prog)
        job.result_handles.wait_for_all_values()
        circuitresult = CircuitResult(
            num_averages=n_avg,
            state=job.result_handles.get("state").fetch_all(),
        ) 
        state_0.append(circuitresult.get_hist_value(count_list=state_count_list))
plt.cla()
plt.plot(phase_list,state_0)
plt.show()