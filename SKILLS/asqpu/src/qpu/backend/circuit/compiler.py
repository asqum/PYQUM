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
            "RX": self.single_qubit_gate_compiler,
            "RY": self.single_qubit_gate_compiler,
            "RZ": self.rz_compiler,
            "RO": self.single_qubit_measurement_compiler,
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
            # (control label, coeff)
            ("sx" + str(gate.targets[0]), new_coeff.real),
            ("sy" + str(gate.targets[0]), new_coeff.imag),
        ]
        #print(tlist)
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

            idling_tlist.append(
                np.linspace(
                    last_pulse_time, start_time, int(start_time-last_pulse_time), endpoint=False
                )
            )
        elif pulse_mode == "discrete":
            # idling until the start time
            idling_tlist.append([start_time])
        return np.concatenate(idling_tlist)
    def single_qubit_gate_compiler(self, gate, args):
        """Compiles single-qubit gates to pulses.
        
        Args:
            gate (qutip_qip.circuit.Gate): A qutip Gate object.
        
        Returns:
            Instruction (qutip_qip.compiler.instruction.Instruction): An instruction
            to implement a gate containing the control pulses.
        """
        
        
        # gate.arg_value is the rotation angle
        sampling_point = 30
        tlist = np.linspace(0,sampling_point,sampling_point, endpoint=False)
        # gate.arg_value is the rotation angle
        coeff = ps.DRAGFunc(tlist, *(1,sampling_point/4.,sampling_point/2., 1) ) *gate.arg_value/np.pi
        # tlist = np.abs(gate.arg_value) / self.params["pulse_amplitude"]
        #print("compile measurement ",gate.name, tlist)
        #coeff *= self.params["pulse_amplitude"] *gate.arg_value/np.pi
        if gate.name == "RX":
            return self.generate_pulse(gate, tlist, coeff, phase=0.0)
        elif gate.name == "RY":
            return self.generate_pulse(gate, tlist, coeff, phase=np.pi / 2)

    def single_qubit_measurement_compiler(self, gate, args):
            """Compiles single-qubit gates to pulses.
            
            Args:
                gate (qutip_qip.circuit.Gate): A qutip Gate object.
            
            Returns:
                Instruction (qutip_qip.compiler.instruction.Instruction): An instruction
                to implement a gate containing the control pulses.
            """
            
            sampling_point = 300
            tlist = np.linspace(0,sampling_point,sampling_point, endpoint=False)
            # gate.arg_value is the rotation angle
            coeff = ps.GERPFunc(tlist, *(1,300,0,15,30/4.) ) 
            # tlist = np.abs(gate.arg_value) / self.params["pulse_amplitude"]
            #coeff *= self.params["pulse_amplitude"] *gate.arg_value/np.pi
            pulse_info = [
                # (control label, coeff)
                ("ro" + str(gate.targets[0]), coeff)
            ]
            #print("compile measurement ",gate.name, tlist)
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
            # gate.arg_value is the rotation angle
            coeff = ps.GERPFunc(tlist, *(1,sampling_point,0,15,30/4.) )
            # tlist = np.abs(gate.arg_value) / self.params["pulse_amplitude"]
            #coeff *= self.params["pulse_amplitude"] *gate.arg_value/np.pi
            pulse_info = [
                # (control label, coeff)
                ("sz" + str(gate.targets[0]), coeff)
            ]
            #print("compile measurement ",gate.name, tlist)
            return [Instruction(gate, tlist=tlist, pulse_info=pulse_info)]