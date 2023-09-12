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
        The waveform types:["DRAG","DRAGe","DRAGt","DRAGh","GAUSS"]
        
        Args:
            gate (qutip_qip.circuit.Gate): A qutip Gate object.
        
        Returns:
            Instruction (qutip_qip.compiler.instruction.Instruction): An instruction
            to implement a gate containing the control pulses.
        """

        pulse_length = self.params[str(gate.targets[0])]["rxy"]["pulse_length"]
        dt = self.params[str(gate.targets[0])]["rxy"]["dt"]
        anharmonicity = self.params[str(gate.targets[0])]["anharmonicity"]

        if self.params[str(gate.targets[0])]["waveform"][0] != "NaN":
            waveform = self.params[str(gate.targets[0])]["waveform"][0]
            a_weight = self.params[str(gate.targets[0])]["waveform"][1]
            sFactor = self.params[str(gate.targets[0])]["waveform"][2]
        else:
            waveform = "DRAG"
            a_weight = 0
            sFactor = 4.

        sampling_point = int( -(pulse_length//-dt) )
        tlist = np.linspace(0, pulse_length, sampling_point, endpoint=False)
        
        match waveform.lower():
            case "dragh": coeff = ps.DRAGFunc_Hermite(
                    tlist, *(1,2,4,pulse_length/2.,a_weight/anharmonicity) ) *gate.arg_value/np.pi
            case "drage":
                shifter = ps.ErfShifter(pulse_length,pulse_length/sFactor)
                coeff = ps.DRAGFunc(
                    tlist, *(1,pulse_length/sFactor,pulse_length/2.,shifter,a_weight/anharmonicity) 
                    ) *gate.arg_value/np.pi 
            case "dragt": coeff = ps.DRAGFunc_Tangential(
                    tlist, *(1,pulse_length/sFactor,pulse_length/2.,a_weight/anharmonicity) 
                    ) *gate.arg_value/np.pi
            case "gauss": coeff = ps.GaussianFamily(
                    tlist,*(1,pulse_length/sFactor,pulse_length/2.,0))*gate.arg_value/np.pi
            case "drag": coeff = ps.DRAGFunc(
                    tlist, *(1,pulse_length/sFactor,pulse_length/2.,0,a_weight/anharmonicity) 
                    ) *gate.arg_value/np.pi
            case _:
                raise NameError('No such fucntion')
            
        if gate.name == "RX":
            return self.generate_pulse(gate, tlist, coeff, phase=0.0)
        elif gate.name == "RY":
            return self.generate_pulse(gate, tlist, coeff, phase=np.pi / 2)
    
    def idle_compiler( self, gate, args ):
        '''
        The time length of idle gate is same as X gate 
        '''
        dt = self.params[str(gate.targets[0])]["rxy"]["dt"]
        idle_time = self.params[str(gate.targets[0])]["rxy"]["pulse_length"]
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
        '''
        Here we give a restriction that the compensate z pulse lengths of two qubits should be the same.
        The waveform types:["CONST","GERP","ERRF"] 
        '''
        targets_label = ''.join(str(target) for target in gate.targets)
        pulse_info = []
        for label in targets_label:   
            if self.params[label]["iswap"]["waveform"][0] != "NaN":
                waveform = self.params[label]["iswap"]["waveform"][0]
                edge = self.params[label]["iswap"]["waveform"][1]
                sFactor = self.params[label]["iswap"]["waveform"][2]
            else:
                waveform = "Const"

            pulse_length = self.params[label]["iswap"]["pulse_length"]
            dt = self.params[label]["iswap"]["dt"]
            dz = self.params[label]["iswap"]["dz"]  
            sampling_point = int( -(pulse_length//-dt) )    
            tlist = np.linspace(0, pulse_length, sampling_point, endpoint=False)

            match waveform.lower(): 
                case "const": coeff = ps.constFunc(tlist, dz )     
                case "gerp": coeff = ps.GERPFunc(tlist, *(dz,pulse_length,0,edge,2*edge/sFactor))
                case "eerp": coeff = ps.EERP(tlist, *(dz,edge/2,edge/sFactor,pulse_length,0))
                case _: raise NameError('No such function') 

            # c_Z for compensate rotation    
            if self.params[label]["iswap"]["c_waveform"][0] != "NaN":
                c_waveform = self.params[label]["iswap"]["c_waveform"][0]
                c_edge = self.params[label]["iswap"]["c_waveform"][1]
                c_sFactor = self.params[label]["iswap"]["c_waveform"][2]

            else: c_waveform = "Const"              
                               
            c_pulse_length = self.params[label]["iswap"]["c_ZW"]
            c_dz = self.params[label]["iswap"]["c_Z"]
            c_sampling_point = int( -(c_pulse_length//-dt) )

            if c_pulse_length != 0:
                c_tlist = np.linspace(
                    pulse_length, pulse_length + c_pulse_length, c_sampling_point, endpoint=False
                    )  
                match c_waveform.lower(): 
                    case "const": c_coeff = ps.constFunc(c_tlist, c_dz )     
                    case "gerp": c_coeff = ps.GERPFunc(
                        c_tlist, *(c_dz,c_pulse_length,c_tlist[0],c_edge,2*c_edge/c_sFactor) ) 
                    case "eerp": c_coeff = ps.EERP(
                        c_tlist, *(c_dz,c_edge/2,c_edge/c_sFactor,c_pulse_length,c_tlist[0]))
                    case _: raise NameError('No such function')  
                tlist = np.append(tlist,c_tlist)
                coeff = np.append(coeff,c_coeff) 
            pulse_info.append(("sz" + label, coeff))
        return [Instruction(gate, tlist=tlist, pulse_info=pulse_info)]
    
    def cz_compiler(self, gate, args):
        '''
        Here we give a restriction that the compensate z pulse lengths of two qubits should be the same. 
        The waveform types:["CONST","GERP"]
        '''
        targets_label = ''.join(str(target) for target in gate.targets)
        pulse_info = []        
        for qi in range(2):
            pulse_length = self.params[str(qi)]["cz"]["pulse_length"]
            dt = self.params[str(qi)]["cz"]["dt"]
            dz = self.params[str(qi)]["cz"]["dz"]
            sampling_point = int( -(pulse_length//-dt) )
            tlist = np.linspace(0, pulse_length, sampling_point, endpoint=False)

            if self.params[str(qi)]["cz"]["waveform"][0] != "NaN":
                waveform = self.params[str(qi)]["cz"]["waveform"][0]
                edge = self.params[str(qi)]["cz"]["waveform"][1]
                sFactor = self.params[str(qi)]["cz"]["waveform"][2]
            else:
                waveform = "Const"

            match waveform.lower(): 
                case "const": coeff = ps.constFunc(tlist, dz )     
                case "gerp": coeff = ps.GERPFunc(tlist, *(dz,pulse_length,0,edge,2*edge/sFactor))
                case "eerp": coeff = ps.EERP(tlist, *(dz,edge/2,edge/sFactor,pulse_length,0)) 
                case _: raise NameError('No such function') 

            # c_Z for compensate rotation
            c_pulse_length = self.params[str(qi)]["cz"]["c_ZW"]
            c_dz = self.params[str(qi)]["cz"]["c_Z"]
            c_sampling_point = int( -(c_pulse_length//-dt) )

            if self.params[str(qi)]["cz"]["c_waveform"][0] != "NaN":
                c_waveform = self.params[str(qi)]["cz"]["c_waveform"][0]
                c_edge = self.params[str(qi)]["cz"]["c_waveform"][1]
                c_sFactor = self.params[str(qi)]["cz"]["c_waveform"][2]

            if c_pulse_length != 0:
                c_tlist = np.linspace(
                    pulse_length, pulse_length + c_pulse_length, c_sampling_point, endpoint=False
                    )
                match c_waveform.lower(): 
                    case "const": c_coeff = ps.constFunc(c_tlist, c_dz )     
                    case "gerp": c_coeff = ps.GERPFunc(
                        c_tlist, *(c_dz,c_pulse_length,c_tlist[0],c_edge,2*c_edge/c_sFactor) )
                    case "eerp": c_coeff = ps.EERP(
                        c_tlist, *(c_dz,c_edge/2,c_edge/c_sFactor,c_pulse_length,c_tlist[0]))           
                tlist = np.append(tlist,c_tlist)
                coeff = np.append(coeff,c_coeff) 
            pulse_info.append(
                ("sz" + str(qi), coeff)
            )

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
        pulse_info = []
        for label in targets_label:
            pulse_info.append(("ro" + label, coeff))
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
    
    def to_waveform( self, circuit:QubitCircuit, schedule_mode=None ):
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
    
    def _process_idling_tlist(
        self, pulse_mode, start_time, last_pulse_time, step_size
    ):
        '''
        This function in Gatecompiler does not meet our need, here we give some finetune to our need.
        '''
        idling_tlist = []
        if pulse_mode == "continuous":
            # We add sufficient number of zeros at the beginning
            # and the end of the idling to prevent wrong cubic spline.
            # if start_time - last_pulse_time > 3 * step_size:
            #     idling_tlist1 = np.linspace(
            #         last_pulse_time + step_size / 5,
            #         last_pulse_time + step_size,
            #         10,
            #     )
            #     idling_tlist2 = np.linspace(
            #         start_time - step_size, start_time, 10
            #     )
            #     idling_tlist.extend([idling_tlist1, idling_tlist2])
            # else:
            idling_tlist.append(
                    np.arange(
                    last_pulse_time + step_size, start_time, step_size
                )
            )
        elif pulse_mode == "discrete":
            # idling until the start time
            idling_tlist.append([start_time])
        return np.concatenate(idling_tlist)
    
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
        if str(target_index) == label_index:
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

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    compiler = TQCompile(2, params={})
    iswap = Gate("ISWAP", [0,1])
    cz = Gate("CZ", 0, 1)
    rg_x0 = Gate("RX", 0, arg_value= np.pi)
    
    for i in range(2):
        compiler.params[str(i)] = {}
        compiler.params[str(i)]["cz"] = {}
        compiler.params[str(i)]["cz"]["dt"] = 0.5
        compiler.params[str(i)]["cz"]["pulse_length"] = 20
        compiler.params[str(i)]["cz"]["dz"] = -0.5
        compiler.params[str(i)]["cz"]["c_ZW"] = 10
        compiler.params[str(i)]["cz"]["c_Z"] = 0.3
        compiler.params[str(i)]["cz"]["waveform"] = ["EERP",5,4]
        compiler.params[str(i)]["cz"]["c_waveform"] = ["EERP",2,4]
        compiler.params[str(i)]["iswap"] = {}
        compiler.params[str(i)]["iswap"]["dt"] = 0.5
        compiler.params[str(i)]["iswap"]["pulse_length"] = 40
        compiler.params[str(i)]["iswap"]["dz"] = 0.5
        compiler.params[str(i)]["iswap"]["c_Z"] = -0.2
        compiler.params[str(i)]["iswap"]["c_ZW"] = 40 
        compiler.params[str(i)]["iswap"]["waveform"] = ["EERP",10,4]
        compiler.params[str(i)]["iswap"]["c_waveform"] = ["EERP",10,4]
        compiler.params[str(i)]["waveform"] = ["GAUSS",-0.5,4]
    gateseq = [cz,iswap]

    circuit = QubitCircuit(2)

    for gate in gateseq:
        circuit.add_gate(gate)
        compiled_data = compiler.compile(circuit,schedule_mode='ASAP')
    print(compiled_data[1])
    plt.plot(compiled_data[1]['sz0'])
    plt.show()
