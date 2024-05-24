# %%
"""
        FAST FLUX SPECTROSCOPY
"""

from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
from qualang_tools.results import progress_counter, fetching_tool
from qualang_tools.loops import from_array
import matplotlib.pyplot as plt
from configuration_opx import *
import numpy as np

###################
# The QUA program #
###################

qubit_xy = 'q5_xy'
qubit_z = 'q5_z'
rr = "q5_rr"

n_avg = 1000  # The number of averages

if_min = 40e6
if_max = 200e6
if_step = 4e6

ifs = np.arange(if_min, if_max, if_step)

delay_min = 4
delay_max = 20_000//4
delay_step = 50
delays = np.arange(delay_min, delay_max, delay_step)

with program() as fast_flux_spec:
    n = declare(int)  # QUA variable for the averaging loop
    df = declare(int)  # QUA variable for the qubit detuning
    delay = declare(int)  # QUA variable for the idle time
    I = declare(fixed)  # QUA variable for the measured 'I' quadrature
    Q = declare(fixed)  # QUA variable for the measured 'Q' quadrature
    I_st = declare_stream()  # Stream for the 'I' quadrature
    Q_st = declare_stream()  # Stream for the 'Q' quadrature
    n_st = declare_stream()  # Stream for the averaging iteration 'n'
    if_val = declare(int)  # QUA variable for the readout frequency
    delay = declare(int)

    with for_(n, 0, n < n_avg, n + 1):
        save(n, n_st)

        with for_(*from_array(if_val, ifs)):

            update_frequency(qubit_xy, if_val)

            with for_(*from_array(delay, delays)):

                play("unipolar", qubit_z, duration= delay + 250) # 250 stands for at least the length of the xy pulse + xy_z delay

                wait(delay, qubit_xy)
                play("x180", qubit_xy)

                align()
                wait(250)
                # Multiplexed readout, also saves the measurement outcomes
                measure(
                    "readout",
                    rr,
                    None,
                    dual_demod.full("rotated_cos", "out1", "rotated_sin", "out2", I),
                    dual_demod.full("rotated_minus_sin", "out1", "rotated_cos", "out2", Q),
                )                
                # Wait for the qubit to decay to the ground state
                wait(250_000 // 4, rr)
                # Save the 'I' & 'Q' quadratures to their respective streams
                save(I, I_st)
                save(Q, Q_st)

    with stream_processing():
        n_st.save("iteration")
        I_st.buffer(len(delays)).buffer(len(ifs)).average().save("I")
        Q_st.buffer(len(delays)).buffer(len(ifs)).average().save("Q")

# %%
#####################################
#  Open Communication with the QOP  #
#####################################
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name)
qmm.close_all_quantum_machines()
###########################
# Run or Simulate Program #
###########################

simulate = False

if simulate:
    # Simulates the QUA program for the specified duration
    simulation_config = SimulationConfig(duration=40_000)  # In clock cycles = 4ns
    job = qmm.simulate(config, fast_flux_spec, simulation_config)
    job.get_simulated_samples().con1.plot()
    plt.show(block=False)
else:
    # Open a quantum machine to execute the QUA program
    qm = qmm.open_qm(config, close_other_machines=False)
    print("Open QMs: ", qmm.list_open_quantum_machines())
    # Send the QUA program to the OPX, which compiles and executes it
    job = qm.execute(fast_flux_spec)
    fetch_names = ["iteration", "I", "Q"]
    # Tool to easily fetch results from the OPX (results_handle used in it)
    results = fetching_tool(job, fetch_names, mode="live")
    
    # Live plotting
    while results.is_processing():
        # Fetch results
        res = results.fetch_all()
        # Progress bar
        progress_counter(res[0], n_avg, start_time=results.start_time)

    res = results.fetch_all()
    # save res into file

    # Close the quantum machines at the end in order to put all flux biases to 0 so that the fridge doesn't heat-up
    qm.close()
    print("Experiment QM is now closed")
    plt.show(block=False)

# %%
