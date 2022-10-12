from typing import List, Tuple
import sys
from pulse_signal.digital_mixer import upConversion_IQ, upconversion_LO
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

    def used_instr( self )->dict:
        instr = {}
        for k, devices_info in self.devices.items():
            instr[k] = []
            for di in devices_info:
                if di[0] not in instr[k]: instr[k].append(di[0])
        return instr
            
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

        dac_info = self.devices["DAC"][0]

        dac_out = {}
        dac_out[dac_info] = signal

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
        instr_dict = self.used_instr()
        for d_category in self.devices.keys():
            qpc_dict["CH"][d_category] = []
            qpc_dict["ROLE"][d_category] = []

        for device_info in self.devices["DAC"]:
            used_ch = device_info[1]
            qpc_dict["CH"]["DAC"].append(used_ch)   
            qpc_dict["ROLE"]["DAC"].append(self.name)  
        qpc_dict.update(instr_dict)
        return qpc_dict

class UpConversionChannel( WaveformChannel ):
    def __init__( self, name:str, dt:float=1. ):
        super().__init__( name, dt )
        self.devices = {
            "DAC":[None,None],
            "SG":[None],
        }
        self.paras = {
            "offset_I": 0,
            "offset_Q": 0,
            "amp_balance": 1,
            "phase_balance": 90,

            "freq_IF" : 0.08,
            "power_LO" : 10
        } 
        
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

        IQMixer = (self.paras["amp_balance"],self.paras["phase_balance"],self.paras["offset_I"],self.paras["offset_Q"])
        freq_IF = self.paras["freq_IF"]
        if type(signalRF) != type(None):
            signal_I, signal_Q = upConversion_IQ( signalRF, freq_IF, IQMixer, suppress_leakage=True )
        else:
            signal_I = None
            signal_Q = None
        dac_info = self.devices["DAC"] 

        dac_out = {}
        dac_out[dac_info[0]] = signal_I
        dac_out[dac_info[1]] = signal_Q

        return dac_out

    
    def devices_setting( self, signalRF:ndarray, freq_carrier:float )->dict:

        sg_name = self.devices["SG"][0]
        sg_out = {
            sg_name:{
                "freq": upconversion_LO( freq_carrier, self.paras["freq_IF"] ),
                "power": self.paras["power_LO"]
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
            
            for device_info in self.devices["DAC"]:
                instr_name = device_info[0]
                used_ch = int(device_info[1])
                if len(qpc_dict["DAC"]) == 0:
                    qpc_dict["DAC"].append(instr_name)
                    qpc_dict["ROLE"]["DAC"].append(f"{self.name}_I") 
                else:
                    qpc_dict["ROLE"]["DAC"].append(f"{self.name}_Q") 
                qpc_dict["CH"]["DAC"].append(used_ch)   
                

            for device_info in self.devices["SG"]:
                instr_name = device_info[0]
                used_ch = int(device_info[1])
                qpc_dict["SG"].append(instr_name)   
                qpc_dict["CH"]["SG"].append(used_ch)  
                qpc_dict["ROLE"]["SG"].append(self.name) 

            return qpc_dict

class DownConversionChannel( PhysicalChannel ):
    def __init__( self, name:str ):
        super().__init__( name )
        self.devices = {
            "ADC":[None],
        }
        self.paras = {
            "offset_I": 0,
            "offset_Q": 0,
            "amp_balance": 1,
            "phase_balance": 90,

            "freq_IF" : 0.08,
            "power_LO" : 10
        } 

    
    def devices_setting( self, points:float, repeat:float )->dict:

        adc_name = self.devices["ADC"][0]
        adc_out = {
            adc_name:{
                "point": points,
                "repeat": repeat
            }
        }

        device_setting = {
            "ADC": adc_out,
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
            
            for device_info in self.devices["ADC"]:
                instr_name = device_info[0]
                used_ch = int(device_info[1])
                qpc_dict["ADC"].append(instr_name)   
                qpc_dict["CH"]["ADC"].append(used_ch)  
                qpc_dict["ROLE"]["ADC"].append(self.name) 
                

            return qpc_dict



class PumpingLine( PhysicalChannel ):
    def __init__( self, name:str ):
        super().__init__( name )
        self.devices = {
            "DC":[None],
            "SG":[None],
        }
        self.paras={
            "freq": 4,
            "power": 0,            
        }

    
    def devices_setting( self )->dict:

        dc_name = self.devices["DC"][0]
        dc_out = {
            dc_name:{
                "sweep": self.paras["volt_bias"],
            }
        }
        sg_name = self.devices["SG"][0]
        sg_out = {
            sg_name:{
                "freq": self.paras["freq_pump"],
                "power": self.paras["power_pump"],
            }
        }
        device_setting = {
            "DC": dc_out,
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
            
            for device_info in self.devices["DC"]:
                instr_name = device_info[0]
                used_ch = int(device_info[1])
                qpc_dict["DC"].append(instr_name)   
                qpc_dict["CH"]["DC"].append(used_ch)  
                qpc_dict["ROLE"]["DC"].append(self.name) 
                

            for device_info in self.devices["SG"]:
                instr_name = device_info[0]
                used_ch = int(device_info[1])
                qpc_dict["SG"].append(instr_name)   
                qpc_dict["CH"]["SG"].append(used_ch)  
                qpc_dict["ROLE"]["SG"].append(self.name) 

            return qpc_dict

