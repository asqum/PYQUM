import qpu.backend.phychannel as pch
from qutip import sigmax, sigmay, sigmaz, basis, qeye, tensor, Qobj
from qutip_qip.operations import Gate #Measurement in 0.3.X qutip_qip
from qutip_qip.circuit import QubitCircuit
from qutip_qip.compiler import GateCompiler, Instruction
import numpy as np
import qpu.backend.circuit.backendcircuit as bec
import qpu.backend.component as qcp
from pandas import DataFrame
import pulse_signal.common_Mathfunc as ps 

class SQCompiler(GateCompiler):
    """Custom compiler for generating pulses from gates using the base class 
    GateCompiler.

    Args:
        num_qubits (int): The number of qubits in the processor
        params (dict): A dictionary of parameters for gate pulses such as
                       the pulse amplitude.
    """

    def __init__(self, num_qubits, params):
        super().__init__(num_qubits, params=params)
        self.params = params
        self.gate_compiler = {
            "RX": self.rxy_compiler,
            "RY": self.rxy_compiler,
            "RZ": self.rz_compiler,
            "RO": self.measurement_compiler,
            "IDLE": self.idle_compiler,
        }

    def generate_pulse(self, gate, tlist, coeff, phase=0.0):
        """Generates the pulses.

        Args:
            gate (qutip_qip.circuit.Gate): A qutip Gate object.
            tlist (array): A list of times for the evolution.
            coeff (array): An array of coefficients for the gate pulses
            phase (float): The value of the phase for the gate.

        Returns:
            Instruction (qutip_qip.compiler.instruction.Instruction): An instruction
            to implement a gate containing the control pulses.                                               
        """

        new_coeff = np.exp(1j*phase)*coeff
        pulse_info = [
            ("sx" + str(gate.targets[0]), new_coeff.real),
            ("sy" + str(gate.targets[0]), new_coeff.imag),
        ]
        return [Instruction(gate, tlist=tlist, pulse_info=pulse_info)]
    def _concatenate_pulses(
        self, pulse_instructions, scheduled_start_time, num_controls
    ):
        """
        Concatenate compiled pulses coefficients and tlist for each pulse.
        If there is idling time, add zeros properly to prevent wrong spline.
        """
        min_step_size = np.inf
        # Concatenate tlist and coeffs for each control pulses
        compiled_tlist = [[] for tmp in range(num_controls)]
        compiled_coeffs = [[] for tmp in range(num_controls)]
        for pulse_ind in range(num_controls):
            last_pulse_time = 0.0
            for start_time, tlist, coeff in pulse_instructions[pulse_ind]:
                # compute the gate time, step size and coeffs
                # according to different pulse mode
                (
                    gate_tlist,
                    coeffs,
                    step_size,
                    pulse_mode,
                ) = self._process_gate_pulse(start_time, tlist, coeff)
                min_step_size = min(step_size, min_step_size)

                if abs(last_pulse_time) < step_size * 1.0e-6:  # if first pulse
                    compiled_tlist[pulse_ind].append([0.0])
                    if pulse_mode == "continuous":
                        compiled_coeffs[pulse_ind].append([0.0])
                    # for discrete pulse len(coeffs) = len(tlist) - 1

                # If there is idling time between the last pulse and
                # the current one, we need to add zeros in between.
                if np.abs(start_time - last_pulse_time) > step_size * 1.0e-6:
                    idling_tlist = self._process_idling_tlist(
                        pulse_mode, start_time, last_pulse_time, step_size
                    )
                    compiled_tlist[pulse_ind].append(idling_tlist)
                    compiled_coeffs[pulse_ind].append(
                        np.zeros(len(idling_tlist))
                    )

                # Add the gate time and coeffs to the list.
                execution_time = gate_tlist + start_time
                last_pulse_time = execution_time[-1]
                compiled_tlist[pulse_ind].append(execution_time)
                compiled_coeffs[pulse_ind].append(coeffs)

        final_time = np.max([tlist[-1][-1] for tlist in compiled_tlist])
        for pulse_ind in range(num_controls):
            if not compiled_tlist[pulse_ind]:
                continue
            last_pulse_time = compiled_tlist[pulse_ind][-1][-1]
            if np.abs(final_time - last_pulse_time) > min_step_size * 1.0e-6:
                idling_tlist = self._process_idling_tlist(
                    pulse_mode, final_time, last_pulse_time, min_step_size
                )
                compiled_tlist[pulse_ind].append(idling_tlist)
                compiled_coeffs[pulse_ind].append(np.zeros(len(idling_tlist)))

        for i in range(num_controls):
            if not compiled_coeffs[i]:
                compiled_tlist[i] = None
                compiled_coeffs[i] = None
            else:
                compiled_tlist[i] = np.concatenate(compiled_tlist[i])
                compiled_coeffs[i] = np.concatenate(compiled_coeffs[i])
        return compiled_tlist, compiled_coeffs

    def _process_idling_tlist(
        self, pulse_mode, start_time, last_pulse_time, step_size
    ):
        idling_tlist = []
        if pulse_mode == "continuous":
            point_num = int( -((start_time-last_pulse_time) //-step_size) )
            idling_tlist.append(
                np.linspace(
                    last_pulse_time, start_time, point_num, endpoint=False
                )
            )
        elif pulse_mode == "discrete":
            # idling until the start time
            idling_tlist.append([start_time])
        return np.concatenate(idling_tlist)
    def rxy_compiler(self, gate, args):
        """Compiles single-qubit gates to pulses.
        
        Args:
            gate (qutip_qip.circuit.Gate): A qutip Gate object.
        
        Returns:
            Instruction (qutip_qip.compiler.instruction.Instruction): An instruction
            to implement a gate containing the control pulses.
        """
        
        
        pulse_length = self.params["rxy"]["pulse_length"]
        pulse_strength = self.params["rxy"]["pulse_strength"]
        dt = self.params["rxy"]["dt"]
        anharmonicity = self.params["anharmonicity"]

        if self.params["waveform"][0] != "NaN":
            waveform = self.params["waveform"][0]
            a_weight = self.params["waveform"][1]
        else:
            waveform = "DRAGe"
            a_weight = -0.5


        sampling_point = int( -(pulse_length//-dt) )
        tlist = np.linspace(0, pulse_length, sampling_point, endpoint=False)
        if waveform == "DRAGe" :
            shifter = ps.ErfShifter(pulse_length,pulse_length/4)
        else:
            shifter = 0
        coeff = ps.DRAGFunc(tlist, *(1,pulse_length/4.,pulse_length/2., shifter, a_weight/anharmonicity) ) *gate.arg_value/np.pi

        if gate.name == "RX":
            return self.generate_pulse(gate, tlist, coeff, phase=0.0)
        elif gate.name == "RY":
            return self.generate_pulse(gate, tlist, coeff, phase=np.pi / 2)

    def measurement_compiler(self, gate, args):
        """Compiles single-qubit gates to pulses.
        
        Args:
            gate (qutip_qip.circuit.Gate): A qutip Gate object.
        
        Returns:
            Instruction (qutip_qip.compiler.instruction.Instruction): An instruction
            to implement a gate containing the control pulses.
        """
        
        pulse_length = self.params["ro"]["pulse_length"]
        dt = self.params["ro"]["dt"]

        sampling_point = int( -(pulse_length//-dt) )
        tlist = np.linspace(0,pulse_length,sampling_point, endpoint=False)

        coeff = ps.GERPFunc(tlist, *(1,pulse_length,0,30,60/4.) ) 

        pulse_info = [
            ("ro" + str(gate.targets[0]), coeff)
        ]
        return [Instruction(gate, tlist=tlist, pulse_info=pulse_info)]


    def rz_compiler(self, gate, args):
        """Compiles single-qubit gates to pulses.
        
        Args:
            gate (qutip_qip.circuit.Gate): A qutip Gate object.
        
        Returns:
            Instruction (qutip_qip.compiler.instruction.Instruction): An instruction
            to implement a gate containing the control pulses.
        """
        
        sampling_point = gate.arg_value
        tlist = np.linspace(0,sampling_point,sampling_point, endpoint=False)
        coeff = ps.GERPFunc(tlist, *(1,sampling_point,0,15,30/4.) )

        pulse_info = [
            ("sz" + str(gate.targets[0]), coeff)
        ]
        return [Instruction(gate, tlist=tlist, pulse_info=pulse_info)]

    def idle_compiler( self, gate, args ):

        dt = self.params["rxy"]["dt"]
        idle_time = gate.arg_value
        idle_point = int( -(idle_time//-dt) )
        if idle_point>0:
            tlist = np.linspace(0,idle_time,idle_point, endpoint=False)
            coeff = ps.constFunc(tlist, 0 )
            pulse_info = [
                # ("sz" + str(gate.targets[0]), coeff),
                ("sx" + str(gate.targets[0]), coeff),
                ("sy" + str(gate.targets[0]), coeff)
            ]
            return [Instruction(gate, tlist=tlist, pulse_info=pulse_info)]
        else:
            return []

    def to_waveform( self, circuit:QubitCircuit , **kwargs):
        try:
            target_q_idx = kwargs["q_idx"]
        except:
            target_q_idx = 0
        compiled_data = self.compile(circuit.gates, schedule_mode=False)

        tlist_map = compiled_data[0]
        coeffs_map = compiled_data[1]
        waveform_channel = []

        ### TODO because for SQ there should be single Qubit signals output. import target qubit index for qi variable
        
        for qi in [target_q_idx]:#range(circuit.N): '''Ratis debug for Q2 (idx = 1) 10/14 : When target_index is 0 due to the range func,  label_index(1) != target_index(0)'''
            print("Circuit qubit number and this qi: ",circuit.N,qi)
            envelope_rf = control_xy(coeffs_map, qi)
            if type(envelope_rf) != type(None):
                waveform_channel.append( (qi,"xy",envelope_rf) )

            envelope_rf = control_z(coeffs_map, qi)
            if type(envelope_rf) != type(None):
                waveform_channel.append( (qi,"z",envelope_rf) )

            envelope_rf = measurement_ro(coeffs_map, qi)
            if type(envelope_rf) != type(None):
                waveform_channel.append( (qi,"ro_in",envelope_rf) )
        return waveform_channel

def control_xy( coeffs_map, target_index ):
    sx_exist = False
    sy_exist = False
    for label in coeffs_map.keys():
        label_index = int(label[2:])
        label_action = label[:2]
        if label_index == target_index:
            match label_action:
                    case "sx":
                        sx_exist = True
                        sx_coeff = np.array(coeffs_map[label])
                    case "sy": 
                        sy_exist = True
                        sy_coeff = np.array(coeffs_map[label])
                    case _: pass
    if sx_exist and sy_exist:
        rf_envelop = sx_coeff +1j*sy_coeff
        return rf_envelop
    return None   

def measurement_ro( coeffs_map, target_index ):
    ro_exist = False
    for label in coeffs_map.keys():
        label_index = int(label[2:])
        label_action = label[:2]
        if label_index == target_index:
            match label_action:
                    case "ro":
                        ro_exist = True
                        ro_coeff = np.array(coeffs_map[label])
                    case _: pass
    if ro_exist :
        rf_envelop = ro_coeff 
        return rf_envelop
    return None


def control_z( coeffs_map, target_index ):
    z_exist = False
    for label in coeffs_map.keys():
        label_index = int(label[2:])
        label_action = label[:2]
        if label_index == target_index:
            match label_action:
                    case "sz":
                        z_exist = True
                        z_coeff = np.array(coeffs_map[label])
                    case _: pass
    if z_exist :
        rf_envelop = z_coeff 
        return rf_envelop
    return None

def compiler_template(self, gate, args):
        """Compiles single-qubit gates to pulses.
        
        Args:
            gate (qutip_qip.circuit.Gate): A qutip Gate object.
        
        Returns:
            Instruction (qutip_qip.compiler.instruction.Instruction): An instruction
            to implement a gate containing the control pulses.
        """
        
        pulse_length = self.params["ro"]["pulse_length"]
        dt = self.params["ro"]["dt"]

        sampling_point = int( -(pulse_length//-dt) )       

        tlist = np.linspace(0,sampling_point,sampling_point, endpoint=False)

        coeff = ps.GERPFunc(tlist, *(1,sampling_point,0,15,30/4.) )
        pulse_info = [
            # (control label, coeff)
            ("sz" + str(gate.targets[0]), coeff)
        ]
        return [Instruction(gate, tlist=tlist, pulse_info=pulse_info)]