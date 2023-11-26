#%% Qiskit imports
from qiskit import QuantumCircuit
from qiskit.providers import Backend, Job, JobStatus
from qiskit.qobj import QobjExperimentHeader
from qiskit.result import Result
from qiskit.result.models import ExperimentResult, ExperimentResultData
from qiskit_experiments.framework import ExperimentData
from qiskit_experiments.library import StateTomography
from qiskit_experiments.library.tomography.basis import PauliMeasurementBasis
from qiskit.visualization import plot_state_city, plot_state_hinton, plot_state_paulivec, plot_state_qsphere
#%% QM imports
from qm.qua import *
from configuration import *
from qm.QuantumMachinesManager import QuantumMachinesManager
from macros import qua_declaration, multiplexed_readout
from qualang_tools.results import fetching_tool
#%% Parameters
shots = 10_000
qp_iter = ['q1', 'q2'] #names of qubits
qubit_number = len(qp_iter)

# %% QUA program
with program() as prog:
            I, I_st, Q, Q_st, n, n_st = qua_declaration(nb_of_qubits=qubit_number)
            align()
            bases = {}
            basis_qua_var = {}
            for q in qp_iter:
                 basis_qua_var[f'basis_{q}'] = declare(int)
                 bases[f'mbasis_{q}'] =  np.array([0, 1, 2])

            tomo_amp1 = {q: declare(fixed) for q in qp_iter}
            tomo_amp2 = {q: declare(fixed) for q in qp_iter}
            tomo_amp3 = {q: declare(fixed) for q in qp_iter}
            tomo_amp4 = {q: declare(fixed) for q in qp_iter}

            state1 = declare(bool)
            state2 = declare(bool)
            state = declare(int)
            state_st = declare_stream()
            with for_(n, 0, n < shots, n+1):
                save(n,n_st)
                # to generalize the for_each_ loops have to be iterated. not sure how to do it
                with for_each_(basis_qua_var['basis_q1'],bases['mbasis_q1']):
                    with for_each_(basis_qua_var['basis_q2'],bases['mbasis_q2']):
                        for q, basis in zip(qp_iter, [basis_qua_var['basis_q1'], basis_qua_var['basis_q2']]):
                            with switch_(basis, unsafe=True):
                                with case_(0):  # Z basis
                                    assign(tomo_amp1[q], 0.0)
                                    assign(tomo_amp2[q], 0.0)
                                    assign(tomo_amp3[q], 0.0)
                                    assign(tomo_amp4[q], 0.0)
                                with case_(1):  # X basis
                                    assign(tomo_amp1[q], 0.0)
                                    assign(tomo_amp2[q], -0.5)
                                    assign(tomo_amp3[q], 0.5)
                                    assign(tomo_amp4[q], 0.0)
                                with case_(2):  # Y basis
                                    assign(tomo_amp1[q], 0.5)
                                    assign(tomo_amp2[q], 0.0)
                                    assign(tomo_amp3[q], 0.0)
                                    assign(tomo_amp4[q], 0.5)
                        ######################
                        # example circuit
                        # align()
                        # play('x180', 'q1_xy')
                        # play('x180', 'q1_xy')
                        # play tomography pulse
                        for q in qp_iter:
                            play('x180'*amp(tomo_amp1[q], tomo_amp2[q], tomo_amp3[q], tomo_amp4[q]), f'{q}_xy')
                            wait(20, f'{q}_xy')
                        align()
                        # readout
                        multiplexed_readout(I, None, Q, None, resonators=[1, 2], weights="rotated_")
                        align()
                        assign(state1, (I[0] > ge_threshold_q1))
                        assign(state2, (I[1] > ge_threshold_q2))
                        assign(state, (Cast.unsafe_cast_int(state1)+(Cast.unsafe_cast_int(state2)<<1)))
                        save(state, state_st)
                        wait(100, )
                        # implement active reset on both qubits and remove wait
                        # wait(10*qubit_T1)
            with stream_processing():
                state_st.buffer(shots, len(bases['mbasis_q1']), len(bases['mbasis_q1'])).save("statequbit0_qubit1")
                n_st.save("shot")
# %% Calibrate
qmm = QuantumMachinesManager(host='127.0.0.1', port=8080)#, octave=octave_config)
qm = qmm.open_qm(config)
job = qm.execute(prog)
results = fetching_tool(job, ['shot', 'statequbit0_qubit1' ], mode="wait_for_all")
n , data = results.fetch_all()
#%%
data_vars = {'state': (['qp','shots', 'mbasis_q1', 'mbasis_q2'], [data])}
coords = {'qp':['qubit0_qubit1'],'shots': np.arange(0,shots,1),
          'mbasis_q1': np.array([0, 1, 2]),  'mbasis_q2': np.array([0, 1, 2]),
          'mbasis': np.reshape(np.stack(np.meshgrid(np.array([0, 1, 2]),np.array([0, 1, 2]))).T,(9,2))}
histogram_data = np.apply_along_axis(lambda x: np.bincount(x, minlength=1), axis =0, arr=data)
# reshape histogram data to represent bases (0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)
# corresponding to (00,00), (00,01), etc. 
histogram_data_reshaped = []
test = []
for i in histogram_data:
    histogram_data_reshaped.append(i.flatten())
histogram_data_reshaped= np.array(histogram_data_reshaped).T
#%%
#################Convert data into qiskit object##############################################
#%% create a job class, that has qiskit structure
class QuaJob(Job):
    def __init__(self, result: Result):
        self._job_id = 0
        self._backend = Backend()
        super().__init__()
        self._result = result
        self._status = JobStatus.DONE

    def result(self):
        """Return job result."""
        return self._result

    def job_id(self):
        return self._job_id

    def backend(self):
        return self._backend

    def status(self):
        return self._status

# function to add measurement data to job object and then to a qiskit state tomo experiment
def histogram_data_to_qiskit_StateTomography(data, basis, qubit_names: list[str]) -> Result:
    """
    This funtion takes an numpy array "data" (histogram: 9 bases x 4 states) and converts it to a qiskit object,
    in order to use the qiskit analysis tool.
    For this, an ExperimentData class has to be constructed and updated with the results stored in the "data".
    numpy array "data" -> ExperimentResultData ->   ExperimentResult -> job             -> \\
                                                                                            analyzable qiskit object
                                                    StateTomography  -> ExperimentData  -> //
    Requirements on 'data' and 'basis:
    - 'basis' - this is the measurement basis, values should be [0, 1, 2] ^ (the number of qubits),
      where 0 is the Z basis, 1 is the X basis and 2 is the Y basis, e.g, for 2 qubits, the values should be
      [0, 0],[0, 1],[0, 2],[1, 0],[1, 1],[1, 2],[2, 0],[2, 1],[2, 2] which correspond to [ZZ, ZX, ZY, XZ, XX, XY, YZ, YX, YY]
    - 'data': histogram data where the first dimension represent the measurment basis and the second dimension the
      state of the qubits in the measurement basis,
      e.g. for 2 qubits and measurement basis 'ZZ' there are entries data[0][x]
      with x = 0, 1, 2, 3  where 0 is the state |00>, 1 is |01>, 2 is |10> and 3 is |11>
    """

    num_qubits = len(qubit_names)
    results = []
    for dat, mb in zip(data,basis):
        header = QobjExperimentHeader(creg_sizes=[['c_tomo', num_qubits]],
                                      memory_slots=num_qubits,
                                      n_qubits=num_qubits,
                                      qreg_sizes=[['q', num_qubits]],
                                      name=f'StateTomography_' +
                                      str(tuple(mb)),
                                      metadata={
                                                'clbits': list(range(num_qubits)),
                                                'cond_clbits': None,
                                                'm_idx': list(mb)}
        )
        shots = dat.sum()
        hist = dat
        results.append(ExperimentResult(shots=shots,
                                        success=True,
                                        data=ExperimentResultData(
                                            {hex(i): hist[i] for i in range(len(hist))}),
                                        meas_level=2, #for discriminated data
                                        header=header
                                        ))
    """
    results is a list of ExperimentResults, which is a qiskit class filled with the result values and parameters.
    But it does not know how to treat the data, thus we construct a StateTomography experiment and parse the results
    by adding the job and running the analysis.
    """

    job = QuaJob(Result('name', 0, 0, 0, True, results=results))

    experiment = StateTomography(QuantumCircuit(num_qubits), measurement_qubits=list(range(num_qubits)),
                                 measurement_basis=PauliMeasurementBasis(), physical_qubits=list(range(num_qubits)))

    expdat = ExperimentData(experiment)
    expdat.add_jobs(job)
    expdat = experiment.analysis.run(expdat)
    return expdat

#%%
qiskit_tomo_res = histogram_data_to_qiskit_StateTomography(histogram_data_reshaped,coords['mbasis'], ['q1', 'q2'])
#%%
# try several different visualization methods

plot_state_city(qiskit_tomo_res.analysis_results('state').value,
                title='prepare --, run on KIT', figsize=(10, 10))
# %%
plot_state_hinton(qiskit_tomo_res.analysis_results(
    'state').value, title='prepare --, run on KIT', figsize=(10, 10))
# %%
plot_state_paulivec(qiskit_tomo_res.analysis_results(
    'state').value, title='prepare --, run on KIT', figsize=(10, 10))

# %%
plot_state_qsphere(qiskit_tomo_res.analysis_results(
    'state').value)

