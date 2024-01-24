from qutip_qip.operations import Gate #Measurement in 0.3.X qutip_qip
from qutip_qip.circuit import QubitCircuit
import numpy as np
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm.qua import *
from qm import SimulationConfig
from configuration import *
import matplotlib.pyplot as plt
import numpy as np
from TQRB.RBResult import RBResult
from TQRB.TQClifford import get_TQcircuit_random_clifford
from TQCompiler import *
import warnings

mycompiler = TQCompile( 2, q1_frame_update= 0.64, q2_frame_update= 0.86, params={}, cz_type='eerp' )

circuit_depths = [0,1,2,3]
circuit_repeats = 3
n_avg = 2000
circuit = [[[] for _ in range(circuit_repeats)] for _ in range(len(circuit_depths))]
result = [[[] for _ in range(circuit_repeats)] for _ in range(len(circuit_depths))]

for i in circuit_depths:
    for j in tqdm(range(circuit_repeats), desc="Processing", unit="step"):
        circuit[i][j] = get_TQcircuit_random_clifford(control=2, target=3, num_gates=i, mode='ONE') 
print('Entering QUA program')

for j in tqdm(range(circuit_repeats), desc="Processing", unit="step"):
    for i in circuit_depths:    
        with program() as prog:
            n = declare(int)
            n_st = declare_stream()  
            state = declare(int)
            state_os = declare_stream()
            with for_(n, 0, n < n_avg, n + 1):   
                wait(thermalization_time)
                compiled_data = mycompiler.compile(circuit[i][j],schedule_mode='ASAP')
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
            result[i][j] = job.result_handles.get("state").fetch_all()
    qm.close()
rbresult = RBResult(
    circuit_depths=circuit_depths,
    num_repeats=circuit_repeats,
    num_averages=n_avg,
    state=result,
)
rbresult.plot_hist()
plt.show()

rbresult.plot_fidelity()
plt.show()
print(rbresult)
print(rbresult.value)