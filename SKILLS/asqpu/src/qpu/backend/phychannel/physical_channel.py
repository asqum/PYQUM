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

    def to_qpc( self ):
        qpc_dict = {}
        qpc_dict["CH"] = {}
        qpc_dict["ROLE"] = {}
        for d_category in self.devices.keys():
            qpc_dict[d_category] = []
            qpc_dict["CH"][d_category] = []
            qpc_dict["ROLE"][d_category] = []

        for name in self.devices["DAC"]:
            device_info = name.split("-")
            instr_name = device_info[0]
            used_ch = int(device_info[1])
            qpc_dict["DAC"].append(instr_name)   
            qpc_dict["CH"]["DAC"].append(used_ch)   
            qpc_dict["ROLE"]["DAC"].append(self.name)   

        return qpc_dict

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


    def to_qpc( self ):
            qpc_dict = {}
            qpc_dict["CH"] = {}
            qpc_dict["ROLE"] = {}
            for d_category in self.devices.keys():
                qpc_dict[d_category] = []
                qpc_dict["CH"][d_category] = []
                qpc_dict["ROLE"][d_category] = []
            
            for name in self.devices["DAC"]:
                device_info = name.split("-")
                print(device_info)
                instr_name = device_info[0]
                used_ch = int(device_info[1])
                if len(qpc_dict["DAC"]) == 0:
                    qpc_dict["DAC"].append(instr_name)
                    qpc_dict["ROLE"]["DAC"].append(f"{self.name}_I") 
                else:
                    qpc_dict["ROLE"]["DAC"].append(f"{self.name}_Q") 
                qpc_dict["CH"]["DAC"].append(used_ch)   
                

            for name in self.devices["SG"]:
                device_info = name.split("-")
                instr_name = device_info[0]
                used_ch = int(device_info[1])
                qpc_dict["SG"].append(instr_name)   
                qpc_dict["CH"]["SG"].append(used_ch)  
                qpc_dict["ROLE"]["SG"].append(self.name) 

            return qpc_dict

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



