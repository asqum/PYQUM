"""
A simple sandbox to showcase different QUA functionalities during the installation.
"""

from qm.qua import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from qm import SimulationConfig
from configuration import *
from qualang_tools.simulator_tools import create_simulator_controller_connections

from macros import multiplexed_readout, cz_gate
import matplotlib.pyplot as plt

###################
# The QUA program #
###################
with program() as hello_qua:
    # Play first X/2
    play("x90", f"q4_xy")
    # Play truncated flux pulse
    align()
    # Wait some time to ensure that the flux pulse will arrive after the x90 pulse
    wait(400 * u.ns)
    # Play the flux pulse only if t is larger than the minimum of 4 clock cycles (16ns)
    
    play("const", f"q4_z", duration=100)
    
    
    wait((600 + 1000) * u.ns, f"q4_xy")
    # wait(400 * u.ns)
    # align()

    
    play("x90", f"q4_xy")
    


#####################################
#  Open Communication with the QOP  #
#####################################
qmm = QuantumMachinesManager(host=qop_ip, port=qop_port, cluster_name=cluster_name, octave=octave_config)

###########################
# Run or Simulate Program #
###########################

simulate = True

if simulate:
    # Simulates the QUA program for the specified duration
    simulation_config = SimulationConfig(duration=3_00)  # In clock cycles = 4ns
    # Simulate blocks python until the simulation is done
    job = qmm.simulate(config, hello_qua, simulation_config)
    # Plot the simulated samples
    job.get_simulated_samples().con1.plot()
    job.get_simulated_samples().con2.plot()
    plt.show()

    # connections = create_simulator_controller_connections(2)
    # job = qmm.simulate(config,hello_qua,SimulationConfig(duration=1000, controller_connections=connections))
    # # get DAC and digital samples (optional).
    # samples = job.get_simulated_samples()
    # # get the waveform report object
    # waveform_report = job.get_simulated_waveform_report()
    # waveform_report.create_plot(samples, plot=True, save_path="./")

else:
    # Open a quantum machine to execute the QUA program
    qm = qmm.open_qm(config)
    # Send the QUA program to the OPX, which compiles and executes it - Execute does not block python!
    job = qm.execute(hello_qua)
