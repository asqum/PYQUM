from qpu.backend.component.q_component import QComponent
from qpu.backend.phychannel.physical_channel import PhysicalChannel, UpConversionChannel, DACChannel, PumpingLine
from qpu.backend import phychannel
from qpu.backend import component
from pandas import DataFrame
import abc
from typing import List, Tuple, Union, Dict

from numpy import array, ndarray, zeros, append

class BackendCircuit():
    """
    紀錄元件specification與使用的channel
    """
    def __init__( self ):
        self._qComps = []
        self._channels = []
        #self._actions = []        
        self._devices = []
        self.total_time = 5000
        self.dt = 1
        self.q_reg = None      

    def register_qComp( self, qcomp:QComponent ):
        """
        
        Args:
            qcomp: Quantum component
        """
        if isinstance(qcomp,QComponent):
           self._qComps.append(qcomp)
        else:
            raise TypeError()

    def get_IDs_qComps( self )->List[str]:
        idList = []
        for q in self._qComps:
            idList.append(q.id)
        return idList


    def get_qComp( self, name:str )->QComponent:
        """
        Get Quantum component by its ID.
        """
        for q in self._qComps:
            if q == name:
                return q
        return None


    def register_channel( self, info:Dict ):
        """
        
        Args:
            channel: the type should be "PhysicalChannel"
        """
        # if isinstance(info,PhysicalChannel):
        #    self._channels.append(info)
        if isinstance(info,Dict):
           new_channel = phychannel.from_dict(info)
           self._channels.append(new_channel)
        else:
            raise TypeError()

    # def get_IDs_channel( self )->str:
    #     idList = []
    #     for ch in self.channels:
    #         idList.append(ch.id)
    #     return idList



    def get_channel( self, name:str )->PhysicalChannel:
        """
        Get channel by its name.
        """
        for ch in self.channels:
            if ch == name:
                return ch
        return None



    def get_channel_qPort( self, q_id:str, port:str )->PhysicalChannel:
        """
        Get channel by q_component id and port.
        """
        myfilter = self.qc_relation["q_id"]==q_id

        q_id_channels = self.qc_relation["channel_id"].loc[myfilter].to_list()
        related_channel_id = None
        for channel_id in q_id_channels:
            channel = self._get_channel_id(channel_id)
            
            if channel.port == port:
                related_channel_id = channel_id
        return self._get_channel_id(related_channel_id)

    def get_port( self, action_id:str )->str:
        """ Get port of the action used."""
        myfilter = self.qa_relation["action"] == action_id 
        port_type = self.qa_relation["port_type"].loc[myfilter].to_list()[0]

        return port_type


    def _get_channel_id( self, id:str )->PhysicalChannel:
        """
        Get channel by its ID.
        """
        for ch in self.channels:
            if ch == id:
                return ch
        return None



    
    def translate_channel_output( self, waveform_channel:List ):
        """
        Input a list of tuple (qi, port, envelope_rf), with information of qubit from specification to output RF signal ( envelope, carrier frequency and belonged physical channel name ).
        """
        channel_output = {}
        register_qN = len(self.q_reg["qubit"])



        for qi, port, envelope_rf in waveform_channel:
            if qi >= register_qN:
                print(f"Only {register_qN} qubit are registered")
            else:
                qname = self.q_reg["qubit"][qi]
                qubit = self.get_qComp(qname)
                phyCh = self.get_channel_qPort(qname,port)

                match port:
                    case "xy":
                        freq_carrier = qubit.tempPars["freq_xy"]
                        envelope_rf *= qubit.tempPars["XYL"]
                    case "ro_in":
                        freq_carrier = qubit.tempPars["freq_ro"]
                        envelope_rf *= qubit.tempPars["ROL"]

                    case "z":
                        freq_carrier = 0
                        # envelope_rf += qubit.tempPars["IDLEZ"]

                    case _:
                        freq_carrier = 0

                if phyCh.name not in channel_output.keys():
                    channel_output[phyCh.name] = [(envelope_rf,freq_carrier)]
                else:
                    channel_output[phyCh.name].append( (envelope_rf,freq_carrier) )
        
        for ch_name, q_name in zip(self.qc_relation["channel_id"],self.qc_relation["q_id"]):
            
            phyCh = self.get_channel(ch_name)
            qubit = self.get_qComp(q_name)
            if phyCh.port == "z" and "IDLEZ" in qubit.tempPars.keys(): # shift Z 
                print(ch_name, q_name )
                if ch_name in channel_output.keys():
                    channel_output[ch_name][0] += qubit.tempPars["IDLEZ"]
                else: # If the Z line is not used but reguster in cq_relation
                    channel_output[ch_name] = [(zeros(self.total_point())+qubit.tempPars["IDLEZ"],0)]
        return channel_output


    def devices_setting( self, waveform_channel ):
        """
        Translate different RF signal channel( include carrier freqency complex envelope ) to devices setting.
        
        Args:
            waveform_channel ( ): .
        
        Returns:

        """
        
        devices_setting_all = {
            "DAC":{},
            "SG":{},
            "DC":{},
            "ADC":{},
        }
 

        channel_output = self.translate_channel_output(waveform_channel)

        for phyCh in self.channels:
            print("Get setting from channel",phyCh.name)

                
            if phyCh.name in channel_output.keys():
                print("Qubit control channel")
                phyCh = self.get_channel(phyCh.name)
                
                single_signal = channel_output[phyCh.name][0]

                ## TODO assume all AWG share same output point num
                channel_delay = phyCh.paras["delay"]
                point_delay = int( -(channel_delay//-self.dt) )
                envelope_rf = single_signal[0]
                point_rf = envelope_rf.shape[-1]
                point_buffer = self.total_point() -point_rf -point_delay
                
                if point_buffer>0:
                    envelope_rf = append( zeros(point_buffer), envelope_rf )
                    envelope_rf = append( envelope_rf, zeros(point_delay) )
                else:
                    print("waveform too many points.")
                print(envelope_rf.shape)
                if isinstance(phyCh, UpConversionChannel):
                    freq_carrier = single_signal[1]
                    devices_output =  phyCh.devices_setting( envelope_rf, freq_carrier  )

                if isinstance(phyCh, DACChannel):
                    devices_output =  phyCh.devices_setting( envelope_rf )
            else:
                if isinstance(phyCh, PumpingLine):
                    print("Pumping channel")
                    devices_output =  phyCh.devices_setting()


            for category in devices_setting_all.keys():
                if category in devices_output.keys():
                    for info, setting in devices_output[category].items():
                        instr_name = info[0]
                        channel_idx = info[1]-1
                        if instr_name not in devices_setting_all[category].keys():
                            #TODO Assume All instr only have 4 channel 
                            devices_setting_all[category][instr_name] = [[],[],[],[]]
                        
                        if type(setting) != type(None):
                            devices_setting_all[category][instr_name][channel_idx] = setting
                            


        return devices_setting_all

    def to_qpc( self ):

        qpc_dict = {}
        qpc_dict["CH"] = {}
        qpc_dict["ROLE"] = {}
        ## Init qpc_dict
        categorys = ["SG","DAC","ADC","DC"]
        for c in categorys:
            qpc_dict[c] = []
            qpc_dict["CH"][c] = []
            qpc_dict["ROLE"][c] = []


        for pch in self.channels:
            pch_qpc = pch.to_qpc()
            for c in categorys :
                if c in pch_qpc.keys():
                    for pch_instr in pch_qpc[c]:
                        try:
                            idx_instr = qpc_dict[c].index(pch_instr)
                            qpc_dict["CH"][c][idx_instr].extend(pch_qpc["CH"][c])
                            qpc_dict["ROLE"][c][idx_instr].extend(pch_qpc["ROLE"][c])
                        except:
                            qpc_dict[c].append(pch_instr)
                            qpc_dict["CH"][c].append(pch_qpc["CH"][c])
                            qpc_dict["ROLE"][c].append(pch_qpc["ROLE"][c])

        return qpc_dict

    def total_point( self ):
        return int( -(self.total_time//-self.dt) )


    @property
    def qubits( self )->List[QComponent]:
        return self._qubits
    @qubits.setter
    def qubits( self, value:List[QComponent]):
        self._qubits = value

    @property
    def channels( self )->List[PhysicalChannel]:
        return self._channels
    @channels.setter
    def channels( self, value:List[PhysicalChannel]):
        self._channels = value


    @property
    def qc_relation( self )->DataFrame:
        return self._qc_relation
    @qc_relation.setter
    def qc_relation( self, value:DataFrame):
        self._qc_relation = value









