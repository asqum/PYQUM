# %%

"""
This is a demo designed to show how to:
- Perform a Ramsey timescan to find the T2* coherence time of their qubits
    To do this we apply two pi/2 pulses and scan the time between them
- Add a spin-echo pulse to the experiment to find the T2E coherence time
    This is identical to a Ramsey scan, but with an added pi pulse in the middle

The assumed system has:
- Two qubits
- Multiplexed dispersive readout

The demo is designed to work both with real hardware and with the plotting backend
If hardware is used, verify that the configuration matches with two_qubit_system.yaml

"""

from multiprocessing.sharedctypes import Value
import pathlib

# import required packages
import keysight.qcs as qcs
from keysight.qcs.entities.readouts import ReadoutResonator
from keysight.qcs.entities.qubits import Qubit
from keysight.qcs.experiment import Experiment
from keysight.qcs.sequencing.sequence_builder import SequenceBuilder
from keysight.qcs.sequencing.sweep import Sweep
from keysight.qcs.backends.plotting_backend import PlottingBackend
from keysight.qcs.backends.waveform_backend import WaveformUploadBackend
from keysight.qcs.results import ExperimentResults
import numpy as np
import plotly.graph_objects as pgo

# if you have a custom experiments library, you can also import that (not used here)
# import my_experiments



# %%
"""
Here we define if we are using real hardware
If use_hardware = True, we run the experiment with the waveform upload backend
If use_hardware = False, we plot the waveforms with the plotting backend
"""
use_hardware = True


# %%

"""
Load the system configuration file
to create a System object - the main entry point to 
the calibration data.

This example comes with a configuration file
in the same directory as this script.
"""
example_directory = pathlib.Path(__file__).parent
filename_system_config = example_directory / 'two_qubit_system.yaml'
system = qcs.load_system(str(filename_system_config))

# display names of objects defined in the configuration file
print(list(system.keys()))
# create a calibration file
# populated with default values
# change the below line to system.save_calibrations() to overwrite the saved cal file
system.load_calibrations()

# %%

if use_hardware:
    """
    these ~8 GHz frequencies are synthesized
    using the upconversion feature of the M5300A AWG
    # and then downconverted back to IF with the M5201A Downconverter
    and acquired on the M5200A Digitizer
    """
    #readout_frequencies = [8.1e9, 8.2222e9]
    readout_frequencies = [4.5e9]
else:
    # choose some IF frequencies that render nicely on the plot
    #readout_frequencies = [200e6, 333e6]
    readout_frequencies = [200e6]


# %%
"""Create a Backend that can execute the experiment"""
if use_hardware:
    # to execute on real hardware
    backend = WaveformUploadBackend()
else:
    # preview the control and measurement sequence
    # with the PlottingBackend
    backend = PlottingBackend()

print(backend)


# %%


def plot_results_single_sweep(results: ExperimentResults, sweep_unit: str = None):
    """
    A helper function to visualize saved data

    Creates a single figure, and plots the average digitizer trace
    for each point in the sweep.
    """
    fig = pgo.Figure()
    for readout_name in results.get_readout_names():
        dataset = results.get_record(readout_name).get_dataset()
        raw_data = dataset.get_data()
        average_traces = raw_data.mean(axis=-1)
        # results description metadata
        time_axis = dataset.get_axes()[0].axis_params['Time (s)'].values
        sweep_axis = results.get_sweep_axes()[0]
        sweep_name = list(sweep_axis.axis_params.keys())[0]
        sweep_values = sweep_axis.axis_params[sweep_name].values

        for sweep_value, trace in zip(sweep_values, average_traces):
            trace_label = f'{readout_name}: {sweep_name} = {sweep_value}'
            if sweep_unit is not None:
                trace_label += f' {sweep_unit}'

            fig.add_trace(
                pgo.Scatter(x=time_axis, y=trace, name=trace_label)
            )

    fig.update_layout(title=str(results.filename))
    fig.show()


# %%

"""
-----------------------------------------------------------------------------------------------------------------------------
The above is common to all demo files
"""

class Ramsey(Experiment):
    """
    A Experiment that sweeps the frequency of XY control pulses on all qubits,
    plays a single qubit control pulse,
    and performs a measurement.
    """
    sweep = Sweep(
        delay=np.linspace(0, 100e-9, 3),
    )

    def make_sequence(self, sequence_builder: SequenceBuilder):
        readouts = self.system.get_instances(ReadoutResonator)
        qubits = self.system.get_instances(Qubit)

        # play a pi/2 pulse on all the qubits
        sequence_builder.append_in_parallel(
            [qubit.xy.play_pulse(amplitude_scale = 0.5)
            for qubit in qubits]
        )

        # delay
        sequence_builder.delay(self.sweep.delay)


        # play a pi/2 pulse on all the qubits
        sequence_builder.append_in_parallel(
            [qubit.xy.play_pulse(amplitude_scale = 0.5)  
            for qubit in qubits]
        )

        # do a measurement with every Readout object in the systems
        sequence_builder.append_in_parallel(
            [readout.perform_measurement()
            for readout in readouts]
        )


T2_test = Ramsey(system)
results_T2 = backend.execute(T2_test)

if use_hardware:
    plot_results_single_sweep(results_T2)

"""
Users can process the results of this data as well as their T1 results to calculate T2*
"""

# %%
class SpinEcho(Experiment):
    """
    A Experiment that sweeps the frequency of XY control pulses on all qubits,
    plays a single qubit control pulse,
    and performs a measurement.
    """
    sweep = Sweep(
        delay=np.linspace(0, 50e-9, 3),
    )

    def make_sequence(self, sequence_builder: SequenceBuilder):
        readouts = self.system.get_instances(ReadoutResonator)
        qubits = self.system.get_instances(Qubit)

        # play a pi/2 pulse on all the qubits
        sequence_builder.append_in_parallel(
            [qubit.xy.play_pulse(amplitude_scale = 0.5)
            for qubit in qubits]
        )


        # delay
        sequence_builder.delay(self.sweep.delay)


        # play a pi pulse on all the qubits
        sequence_builder.append_in_parallel(
            [qubit.xy.play_pulse(amplitude_scale = 1.0)  
            for qubit in qubits]
        )


        # delay
        sequence_builder.delay(self.sweep.delay)


        # play a pi/2 pulse on all the qubits
        sequence_builder.append_in_parallel(
            [qubit.xy.play_pulse(amplitude_scale = 0.5)  
            for qubit in qubits]
        )

        # do a measurement with every Readout object in the systems
        sequence_builder.append_in_parallel(
            [readout.perform_measurement()
            for readout in readouts]
        )


T2E_test = SpinEcho(system)
results_T2E = backend.execute(T2E_test)

if use_hardware:
    plot_results_single_sweep(results_T2E)

"""
Now users know enough to calculate T2E
"""
# %%
