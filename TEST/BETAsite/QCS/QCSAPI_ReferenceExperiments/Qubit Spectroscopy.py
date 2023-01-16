# %%

"""
This is a demo designed to show how to:
- Perform qubit spectroscopy to find the 0-1 transition frequency
- Save the transiition frequency as a calibration

The assumed system has:
- Two qubits
- Multiplexed dispersive readout

The demo is designed to work both with real hardware and with the plotting backend
If hardware is used, verify that the configuration matches with two_qubit_system.yaml

"""

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
We define an Experiment in this script for portability,
but for re-use purposes it is easy to create libraries of Experiments
and import them in workflows with:
    
    `from my_experiments import QubitSpectroscopyExperiment`

"""
class QubitSpectroscopyExperiment(Experiment):
    """
    A Experiment that sweeps the frequency of XY control pulses on all qubits,
    plays a single qubit control pulse,
    and performs a measurement.
    """
    sweep = Sweep(
        # spec_frequency=np.linspace(100e6, 500e6, 3),
        spec_frequency=np.linspace(4.1e9, 4.3e9, 3),
    )

    def make_sequence(self, sequence_builder: SequenceBuilder):
        readouts = self.system.get_instances(ReadoutResonator)
        qubits = self.system.get_instances(Qubit)

        # sweep the frequency of all Qubit objects
        for qubit in qubits:
            sequence_builder.assign_cal_param_sweep(
                qubit.xy.frequency,
                self.sweep.spec_frequency,
            )

        # play a pulse on all the qubits
        sequence_builder.append_in_parallel(
            [qubit.xy.play_pulse()
            for qubit in qubits]
        )

        # do a measurement with every Readout object in the systems
        sequence_builder.append_in_parallel(
            [readout.perform_measurement()
            for readout in readouts]
        )


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

"""
Interact with the calibration data.
We can update some system parameters that will make
the readout pulses more applicable to a multiplexing scenario
"""

if use_hardware:
    """
    these ~8 GHz frequencies are synthesized
    using the upconversion feature of the M5300A AWG
    # and then downconverted back to IF with the M5201A Downconverter
    and acquired on the M5200A Digitizer
    """
    #readout_frequencies = [4.3e9, 4.4e9]
    #readout_frequencies = [4.0e9, 4.0e9]
    readout_frequencies = [4.5e9]
else:
    # choose some IF frequencies that render nicely on the plot
    #readout_frequencies = [200e6, 333e6]
    readout_frequencies = [200e6]

# save these values in the cal file
for readout, readout_frequency in zip(
    system.get_instances(ReadoutResonator),
    readout_frequencies,
):
    # set the "logical channel" frequency
    # N.B. both Readout objects are on the same physical channel
    # but their absolute frequencies are independent
    # and will be multiplexed automatically
    readout.drive_channel.frequency.value = readout_frequency
    # also update some pulse parameters
    readout.drive_channel.default_pulse.amplitude.value = 0.2
    readout.drive_channel.default_pulse.sigma.value = 40e-9

# Finally, set the number of shots taken
# for every point in the Sweep
system.syst_cal_container.number_of_averages.value = 100

system.save_calibrations()
"""
At this point one can inspect the file
```two_qubit_system.default_calibrations.yaml```
to see these parameters that have been set
"""


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
Execute the experiment

When use_hardware, the Labber Instrument Server must be open already.
The first execution takes a minute or so to configure the instruments.
Successive runs are much faster.
"""
qubit_spec = QubitSpectroscopyExperiment(system)
results = backend.execute(qubit_spec)

if use_hardware:
    # plot the data
    plot_results_single_sweep(results, sweep_unit='Hz')


# %%
"""
"Perform data analysis"
Here is where a user extracts some meaning from their spectroscopy experiment
e.g. analyzes the data to get the qubit frequency

Then we can feed that into the calibration data, and it will be used in future experiments
"""

# let's say the user found this frequency
# this is artifically low for demonstration purposes
# but can be to 15 GHz
qubit_frequency = 4.2e9

# set the frequency in the calibration data file
qubit = system.get_instances(Qubit)[0]
qubit.xy.frequency.value = qubit_frequency

system.save_calibrations()


