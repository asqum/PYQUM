from physics_model.complex_system import SingleReadableTransmon
from typing import List, Tuple
import sys
from pulse_signal.digital_mixer import upConversion_IQ, upconversion_LO
from pulse_signal.waveform import Waveform
from abc import ABC, abstractproperty, abstractmethod
from numpy import ndarray






class PhysicalChannel():
    
    #channelTypes = ["PulseRO","PulseCtrl","CWRO","CWCtrl"]
    #deviceTypes = ["DAC","ADC","SG","DC","VNA","SA","IQMixer","DRWiring"]
    

    def __init__( self, name:str ):
        self.name = name
        self.devices = {}
        self.port = None
        #self.pulse_sequence = []

    def __contains__( self )->str:
        return self.name

    def __eq__( self, other )->str:
        if isinstance(other, PhysicalChannel):
            return self.name == other.name
        if isinstance(other, str):
            return self.name == other
        return False
        
    # @property
    # def devices( self )->List[VDevice_abc]:
    #     """
    #     A list include devices that this channel used.
    #     """
    #     return self._devices
    # @devices.setter
    # def devices( self, value:List[VDevice_abc] ):
    #     self._devices = value

    # @property
    # def pulse_sequence( self )->List[Pulse]:
    #     """
    #     The output pulse sequence of this channel.
    #     """
    #     return self._pulse_sequence
    # @pulse_sequence.setter
    # def pulse_sequence( self, value:List[Pulse] ):
    #     self._pulse_sequence = value

    # @property
    # def idle_value( self )->float:
    #     """
    #     The default output value of this channel.
    #     """
    #     return self._idle_value
    # @idle_value.setter
    # def idle_value( self, value:float ):
    #     self._idle_value = value


    def register_device( self, virdtype:str, name:str ):
        """
        Register the device 'name' with virtual device type 'virdtype' in to this physicalChannel\n
        """
        if name not in self.devices[virdtype]:
            self.devices[virdtype].append(name)
        else:
            print(f"Device '{name}' is already registered.")

    
    # def get_devicesID( self, virdtype:str=None )->str:
    #     """
    #     Find the device name
    #     """
    #     IDList = []
    #     for f_type in self.devices.keys():
    #         for d in self.devices[f_type]:
    #             if deviceTypes == None or d.func_type == deviceTypes:
    #                 IDList.append(d.id)
    #         return IDList
    
    
    # def get_dt( self ):
    #     dt = []
    #     for d in self.devices["DAC"]:
    #         if isinstance(d, DAC_abc):
    #             dt.append(d.get_TimeResolution())
    #     if dt.count(dt[0]) == len(dt):
    #         return dt[0]
    #     else:
    #         raise ValueError("dt are not the same.")

    # def to_waveform_channel( self, dt:float )->Waveform:
    #     new_waveform = Waveform( 0, dt )
    #     for p in self.pulse_sequence:
    #         new_t0 = dt*new_waveform.Y.shape[-1]
    #         new_waveform.append( p.generate_signal( new_t0, dt ))

    #     return new_waveform

class WaveformChannel( ABC, PhysicalChannel ):
    def __init__( self, name:str, dt:float=1. ):
        super().__init__( name )
        # self.devices = {
        #     "DAC":[]
        # }
        # self.dt = dt

    @abstractmethod
    def dac_output( self, dt:float=None )->dict:
        pass
         

class DACChannel( WaveformChannel ):
    def __init__( self, name:str, dt:float=1. ):
        super().__init__( name, dt )
        self.devices = {
            "DAC":[]
        }
        self.dt = dt

    def dac_output( self, signal:ndarray )->dict:

        dac_name = self.devices["DAC"][0]
        dac_out = {}
        dac_out[dac_name] = signal
        return dac_out

    def devices_setting( self, signal:ndarray, )->dict:

        device_setting = {
            "DAC": self.dac_output(signal),
        }
        
        return device_setting
class UpConversionChannel( WaveformChannel ):
    def __init__( self, name:str, dt:float=1. ):
        super().__init__( name, dt )
        self.devices = {
            "DAC":[None,None],
            "SG":[None],
        }
        self.comps={
            "IQMixer":{
                "calibration":(1,90,0,0),
            }
        }
        self.freqIF = 0.08
        
    def dac_output( self, signalRF:ndarray )->dict:
        """
        Time dependet DAC output, translate from rf signal
        """
        # if dt == None:
        #     dt = self.dt
        # if freqIF == None: freqIF = self.freqIF
        # else: self.freqIF = freqIF

        # if IQMixer == None: IQMixer = self.comps["IQMixer"]["calibration"]
        # else : IQMixer = self.IQMixer
        IQMixer = self.comps["IQMixer"]["calibration"]

        if type(signalRF) != type(None):
            signal_I, signal_Q = upConversion_IQ( signalRF, self.freqIF, IQMixer, suppress_leakage=False )
        else:
            signal_I = None
            signal_Q = None
        dac_name = self.devices["DAC"]
        dac_out = {}
        dac_out[dac_name[0]] = signal_I
        dac_out[dac_name[1]] = signal_Q

        return dac_out

    def devices_setting( self, signalRF:ndarray, freq_carrier:float )->dict:

        sg_name = self.devices["SG"][0]
        sg_out = {
            sg_name:{
                "freq": upconversion_LO( freq_carrier, self.freqIF ),
            }
        }
        dac_out = self.dac_output(signalRF)
        device_setting = {
            "DAC": dac_out,
            "SG": sg_out
        }
        return device_setting


# class DownConversionChannel( PhysicalChannel ):
#     def __init__( id:str ):
#         super().__init__( id )

#     def get_dt( self ):
#         dt = []
#         for d in self.devices:
#             if isinstance(d, DAC_abc):
#                 dt.append(d.get_TimeResolution())
#         if dt.count(dt[0]) == len(dt):
#             return dt[0]
#         else:
#             raise ValueError("dt are not the same.")



