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

class TQCompile(GateCompiler):
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
            "ISWAP": self.iswap_compiler,
            "CZ": self.cz_compiler,
            "IDLE": self.idle_compiler,
            "RO": self.measurement_compiler,
        }

    def rxy_compiler(self, gate, args):
        """Compiles single-qubit gates to pulses.
        
        Args:
            gate (qutip_qip.circuit.Gate): A qutip Gate object.
        
        Returns:
            Instruction (qutip_qip.compiler.instruction.Instruction): An instruction
            to implement a gate containing the control pulses.
        """

        pulse_length = self.params[str(gate.targets)]["rxy"]["pulse_length"]
        dt = self.params[str(gate.targets)]["rxy"]["dt"]
        anharmonicity = self.params[str(gate.targets)]["anharmonicity"]
        a_weight = self.params["a_weight"]
        img_ratio = self.params["img_ratio"]
        sampling_point = int( -(pulse_length//-dt) )
        tlist = np.linspace(0, pulse_length, sampling_point, endpoint=False)
        coeff = ps.DRAGFunc(tlist, *(1,pulse_length/4.,pulse_length/2., a_weight/anharmonicity, img_ratio) ) *gate.arg_value/np.pi

        if gate.name == "RX":
            return self.generate_pulse(gate, tlist, coeff, phase=0.0)
        elif gate.name == "RY":
            return self.generate_pulse(gate, tlist, coeff, phase=np.pi / 2)
    
    def idle_compiler( self, gate, args ):
        # The time length of idle gate is same as X gate 

        dt = self.params[str(gate.targets)]["rxy"]["dt"]
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
    
    def iswap_compiler( self, gate, args):

        pulse_length = self.params["iswap"]["pulse_length"]
        dt = self.params["iswap"]["dt"]
        dz = self.params["iswap"]["dz"]
        sampling_point = int( -(pulse_length//-dt) )
        tlist = np.linspace(0, pulse_length, sampling_point, endpoint=False)
        coeff = ps.constFunc(tlist, dz )
        targets_label = ''.join(str(target) for target in gate.targets)
        pulse_info = [
        ("sz" + targets_label, coeff)
        ]
        return [Instruction(gate, tlist=tlist, pulse_info=pulse_info)]
    
    def cz_compiler(self, gate, args):

        pulse_length = self.params["cz"]["pulse_length"]
        dt = self.params["cz"]["dt"]
        dz = self.params["cz"]["dz"]
        sampling_point = int( -(pulse_length//-dt) )
        tlist = np.linspace(0, pulse_length, sampling_point, endpoint=False)
        coeff = ps.constFunc(tlist, dz )
        targets_label = ''.join(str(target) for target in gate.targets)
        pulse_info = [
        ("sz" + targets_label, coeff)
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
        # The edge with we give 15 sampling points. 
        coeff = ps.GERPFunc(tlist, *(1,pulse_length,0,15,30/4.) ) 
        targets_label = ''.join(str(target) for target in gate.targets)
        pulse_info = [
            ("ro" + targets_label, coeff)
        ]
        return [Instruction(gate, tlist=tlist, pulse_info=pulse_info)]
    
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
    
    def to_waveform( self, circuit:QubitCircuit, schedule_mode ):
        # It translates the gate.compile to waveform_channel:(qi,type,envelope_rf).
        compiled_data = self.compile(circuit.gates, schedule_mode)
        tlist_map = compiled_data[0]
        coeffs_map = compiled_data[1]
        waveform_channel = []
        # N is the number of the qubits
        for qi in range(circuit.N):
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
    # It first checks corresponding targets and xy ports, then returns RF with coeff. sx + i*sy. 
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
        label_index = label[2:]
        label_action = label[:2]
        if str(target_index) in label_index:
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