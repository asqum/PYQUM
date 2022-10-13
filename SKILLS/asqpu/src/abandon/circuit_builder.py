from qpu.backend.component.qubit.transmon import Transmon
from qpu.backend.action.basic_action import PhysicalAction, Idle
import abc
from typing import List, Tuple, Dict
from qpu.backend.circuit.backendcircuit import BackendCircuit
from pulse_signal.pulse import Pulse, Waveform
from pulse_signal.common_Mathfunc import DRAGFunc
from copy import deepcopy
from numpy import ndarray, pi

from qpu.backend.phychannel.physical_channel import UpConversionChannel, DACChannel
## TODO might replace by qutip
class CircuitBuilder():
    """
    組建微波脈衝序列
    
    """
    def __init__( self, base_circuit:BackendCircuit ):
        self._base_circuit = base_circuit

        
        self._channel_output = dict.fromkeys(base_circuit.get_IDs_channel())

        for a in self._channel_output:
            self._channel_output[a] = []
            #print(id(self._channel_output[a]))
        self._t0_element = 0
    @property
    def base_circuit( self ):
        return self._base_circuit

    @property
    def t0_element( self )->float:
        return self._t0_element

    @property
    def channel_output( self )->Dict[str,List[Pulse]]:
        return self._channel_output
    @channel_output.setter
    def channel_output( self, value:Dict[str,List[Pulse]] ):
        self._channel_output = value
    

    def add_element( self, qubit_id:str, action_id:str, pars:List ):

        base_circuit = self.base_circuit

        qubit = base_circuit.get_qComp(qubit_id)
        action = base_circuit.get_action(action_id)
        action.pars = pars
        action.t0 = self.t0_element
        new_pulse = action.to_pulse(qubit)
        port = base_circuit.get_port(action_id)
        channel_id = base_circuit.get_channel_qPort(qubit_id,port).id
        if action!=None:
            for channel in base_circuit.channels:
                #print(qubit_id, chid, action.id, self.t0_element)
                if channel == channel_id:
                    channel.pulse_sequence.append(new_pulse)
                    #print("Add",qubit_id, chid, action.id, self.t0_element)
                    
                else:
                    idle_operation = Idle("i",[0])
                    idle_operation.duration = new_pulse.duration
                    idle_operation.t0 = self.t0_element
                    idle_pulse = idle_operation.to_pulse()
                    channel.pulse_sequence.append(idle_pulse)

            self._t0_element += new_pulse.duration

    def to_waveform_channel( self, dt:float )->Dict[str,Waveform]:
        """
        輸出每個channel的波形, 自訂義dt
        """
        channel_waveform = dict.fromkeys(self.base_circuit.get_IDs_channel())
        base_circuit = self.base_circuit

        for channel in base_circuit.channels:
            channel_waveform[channel.id]=channel.to_waveform_channel( dt )
        return channel_waveform

    def to_waveform_dac( self )->Dict[str,Waveform]:
        """
        輸出每個DAC的波形
        """
        base_circuit = self.base_circuit
        dac_waveform = {}
        for channel in base_circuit.channels:
            dac_waveform.update( channel.to_waveform_dac() )

        return dac_waveform 



#if __name__ == '__main__':
    