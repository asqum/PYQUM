'''
This is for adapting to customized FPGA
'''

import sys
sys.path.append('C:/program Files(x86)/Keysight/SD1/Libraries/Python')
import keysightSD1 
import time
import numpy as np 

# ALL FPGA PATH:
from pyqum.instrument.reader import device_port
from pathlib import Path
FPGA_FOLDER = Path(device_port("FPGA"))
print("FPGA Bitfile stored in " + str(FPGA_FOLDER))
# M3102_PATH = FPGA_FOLDER / "M3102A.k7z"
# FPGA_PATH = FPGA_FOLDER / "M3102A_AVE.k7z"

def unsignedToSigned(usInput, maxbit):
	mask = 2**(maxbit)-1
	signedMax = 2**(maxbit -1)-1
	if usInput > signedMax:
		usInput = ((~(usInput-1))&mask)
		usInput = usInput*(-1)
	return usInput

def dataUnpack(data, unpack_no):
        dataOut = np.empty(0)
        for i in range(0, len(data),unpack_no):
            temp = (int(data[i])&0xFFFF)+((int(data[i+1])&0xFFFF)<<16)+((int(data[i+2])&0xFFFF)<<32)+((int(data[i+3])&0xFFFF)<<48)
            temp = unsignedToSigned(temp, 64)
            dataOut= np.append(dataOut, temp)
        return dataOut
    
class SD_FPGA(keysightSD1.SD_AIN):
    def __init__(self):
        super(SD_FPGA, self).__init__()
        self._bitModeDefine()
        self._FPGA = self.bitMode_Keysight

    def assignCard(self, cardName:str):
        """ select different digitizeer by setting the model name of digitizer
            Args:
                cardName: the model name of the digitizer, currently only M3102A is available
        """
        if cardName == "M3102A":
            self._assignM3102A()    
        else:
            raise TypeError(cardName +"is not defined") 
      
    def loadFPGABitFile(self, bitFileMode:int):
        """
        load different bitfile by setting different bitFileMode
        Args:
        bitFileMode: use the mode setting constant defined in bitModeDefine
        """
        if bitFileMode == self.bitMode_Keysight:
            self._loadBitFile(self.bitPath_Keysight)
            self._FPGA = self.bitMode_Keysight
        elif bitFileMode == self.bitMode_AVE:
            self._loadBitFile(self.bitPath_AVE)
            self._FPGA = self.bitMode_AVE 
        elif bitFileMode == self.bitMode_SingleDDC:
            self._loadBitFile(self.bitPath_SingleDDC)
            self._FPGA=self.bitMode_SingleDDC
        elif bitFileMode == self.bitMode_SingleDDC_Int:
            self._loadBitFile(self.bitPath_SingleDDC_Int)
            self._FPGA = self.bitMode_SingleDDC_Int
        elif bitFileMode == self.bitMode_SingleDDC_Spt:
            self._loadBitFile(self.bitPath_SingleDDC_Spt)
            self._FPGA = self.bitMode_SingleDDC_Spt
        elif bitFileMode == self.bitMode_DualDDC:
            self._loadBitFile(self.bitPath_DualDDC)
            self._FPGA = self.bitMode_DualDDC
        elif bitFileMode == self.bitMode_DualDDC_Int:
            self._loadBitFile(self.bitPath_DualDDC_Int)
            self._FPGA = self.bitMode_DualDDC_Int
        elif bitFileMode == self.bitMode_DualDDC_Spt:
            self._loadBitFile(self.bitPath_DualDDC_Spt)
            self._FPGA = self.bitMode_DualDDC_Spt 
        elif bitFileMode == self.bitMode_AVE_SingleDDC:
            self._loadBitFile(self.bitPath_AVE_SingleDDC)
            self._FPGA = self.bitMode_AVE_SingleDDC
        elif bitFileMode == self.bitMode_AVE_SingleDDC_Int:
            self._loadBitFile(self.bitPath_AVE_SingleDDC_Int)
            self._FPGA = self.bitMode_AVE_SingleDDC_Int
        elif bitFileMode == self.bitMode_AVE_DualDDC:
            self._loadBitFile(self.bitPath_AVE_DualDDC)
            self._FPGA = self.bitMode_AVE_DualDDC
        elif bitFileMode == self.bitMode_AVE_DualDDC_Int:
            self._loadBitFile(self.bitPath_AVE_DualDDC_Int)
            self._FPGA = self.bitMode_AVE_DualDDC_Int
        else:
            raise ValueError("bit Mode assign Error")
        self._getOffsetReg()
        self._getAveReg()
        self._getDDCReg()
            
    def adjustOffset(self, CH:int, offset:int):
        """ set the input offset value
            Args:
            CH: input channel, only 1,2,3,4 is valid
            offset: offset value of each channel, the unit is digit
        """
        if offset < -8192 or offset > 8191:
            raise ValueError("the offset value is out of range")
        if self._FPGA == self.bitMode_Keysight:
            return 
        if self._FPGA & self.bitMode_Dual:
            if CH == 1:
                self.regCh1Offset.writeRegisterInt32(offset)
            elif CH ==2:
                self.regCh2Offset.writeRegisterInt32(offset)
            elif CH ==3:
                self.regCh3Offset.writeRegisterInt32(offset)
            elif CH ==4:
                self.regCh4Offset.writeRegisterInt32(offset)
            else:
                raise ValueError("CH number setting error")
        else:
            if CH == 1:
                self.regCh1Offset.writeRegisterInt32(offset)
            elif CH ==2:
                self.regCh2Offset.writeRegisterInt32(offset)
            else:
                raise ValueError("CH number setting error")       
    
    def setDDCFreq(self, CH, frequency):
        """ Args:
            CH: input channel number only 1 or 3 is valid
            frequency: the local oscillator frequency. the unit is Hz
        """
        if not self._FPGA & self.bitMode_DDC:
            return 
        temp_a_b = ((frequency*self.superSampling)*(2**25))/(self.samplingRate*self.Lo_T)
        A = int(temp_a_b)
        B = round((temp_a_b -A)*(5**10))
        if CH == 1:
            self.regCh1LoA.writeRegisterInt32(A)
            self.regCh1LoB.writeRegisterInt32(B)
            self.regCh1SetFreq.writeRegisterInt32(1)
            self.regCh1SetFreq.writeRegisterInt32(0)
            
        elif CH ==2:
            self.regCh2LoA.writeRegisterInt32(A)
            self.regCh2LoB.writeRegisterInt32(B)
            self.regCh2SetFreq.writeRegisterInt32(1)
            self.regCh2SetFreq.writeRegisterInt32(0)
               
    def DAQconfigFPGA(self, CH, pt_per_shot, shots, trig_delay, trigger_mode):
        """
        replace the original DAQconfig function. the parameter is the same
        """
        if self._FPGA & self.bitMode_AVE:
            print("config AVE")
            self._DAQconfigAVE(CH, pt_per_shot, shots, trig_delay, trigger_mode)
        elif self._FPGA & self.bitMode_DDC:
            print("config DDC")
            self._DAQconfigDDC(CH, pt_per_shot, shots, trig_delay, trigger_mode)
        else:
            error = self.DAQconfig(CH, pt_per_shot, shots, trig_delay, trigger_mode)
            if error != 0:
                raise ValueError("DAQ configure error in channel ",CH)

    def aveMemoryClear(self):
        if self._FPGA & self.bitMode_AVE or self._FPGA & self.bitMode_Spt:
            print("clear memory")
            self.regCh1Clear.writeRegisterInt32(1)
            self.regCh2Clear.writeRegisterInt32(1)

    
    def checkFinished(self, Channel, pt_per_shot, shots, timeout_in_s =1):
        tstart = time.time()
        if self._FPGA & self.bitMode_AVE or self._FPGA & self.bitMode_Spt:
            self._checkStatus(Channel, tstart, timeout_in_s)
        elif self._FPGA == self.bitMode_Keysight or self._FPGA & self.bitMode_Int:
            self._checkDataCount(Channel, pt_per_shot*shots, tstart, timeout_in_s)
        elif self._FPGA == self.bitMode_DualDDC or self._FPGA == self.bitMode_SingleDDC :
           self._checkDataCount(Channel, int(pt_per_shot*shots/5), tstart, timeout_in_s)

    def _checkDataCount(self, Channel, totolPts, tstart, timeout_in_s):
        """Arg:
            Channel: DAQ channel for 1 to 4
            totalPts: the data points expect to read back
            tstart: starting timestamp of timeout 
        """
        counter = 0
        tcheck = 0
        while(tcheck < timeout_in_s and counter != totolPts):
            counter = self.DAQcounterRead(Channel)
            tcheck = time.time()-tstart
        if tcheck >=timeout_in_s:
            raise RuntimeError("time out in Reading data points from Channel:"+str(Channel)+" datacount="+str(counter))

    def _checkStatus(self, Channel, tstart, timeout_in_s):
        """
        check the status for AVE function:
        Args:
        Channel: DAQ channel for 1 to 4
        tstart: starting timestamp of timeout 
        """
        status = 0
        tcheck = 0
        while(tcheck < timeout_in_s and status != 26):
            if Channel == 1:
                status = self.regCh1State.readRegisterInt32()
            elif Channel == 2:
                status = self.regCh2State.readRegisterInt32()
                print("ch2 status:", status)
            elif Channel ==3:
                status = self.regCh3State.readRegisterInt32()
            elif Channel == 4:
                status = self.regCh4State.readRegisterInt32()
            else:
                raise ValueError(" incorrect channel settikng")
            tcheck = time.time()-tstart
        if tcheck >= timeout_in_s:
            raise RuntimeError("AVE status runtime error in channel:"+str(Channel))


    def getAVEDebugInfo(self, enable_ch12= True):
        if not (self._FPGA & self.bitMode_AVE or self._FPGA & self.bitMode_Spt):
            return
        if enable_ch12:
            regCh1TriggerCnt = self.FPGAgetSandBoxRegister("Mem_Ch1_TriggerCnt")
            regCh2TriggerCnt = self.FPGAgetSandBoxRegister("Mem_Ch2_TriggerCnt")
            tn0 = regCh1TriggerCnt.readRegisterInt32()
            tn1 = regCh2TriggerCnt.readRegisterInt32()
            shots1 = self.regCh1Shot.readRegisterInt32()
            shots2 = self.regCh2Shot.readRegisterInt32()
            info = "tn0 = "+str(tn0)+", tn1 = "+str(tn1)+", shots1="+str(shots1)+ ",shots2="+str(shots2)
        else: 
            regCh3TriggerCnt = self.FPGAgetSandBoxRegister("Mem_Ch3_TriggerCnt")
            regCh4TriggerCnt = self.FPGAgetSandBoxRegister("Mem_Ch4_TriggerCnt")
            tn0 = regCh3TriggerCnt.readRegisterInt32()
            tn1 = regCh4TriggerCnt.readRegisterInt32()
            shots= self.regCh2Shot.readRegisterInt32()
            info = "tn3 = "+str(tn0)+", tn4 = "+str(tn1)+",shots2="+str(shots)
        return info

    def DAQreadFPGA(self, CH, timeout):
        datacounter = self.DAQcounterRead(CH)
        print("datacount of CH", CH, "=", datacounter)
        
        if datacounter == 0:
            raise ValueError(" There is no output data in the acquired channel")
        if datacounter % 10:
            datacounter = int(datacounter/10)*10   
        data = self.DAQread(CH, datacounter, timeout)
        
        if self._FPGA & self.bitMode_Int or self._FPGA == self.bitMode_AVE:
            data = dataUnpack(data, self.superSampling)

        return data
        
    def _assignM3102A(self):
        self.samplingRate =5e8
        self.superSampling = 5
        self.Lo_T = 8
        self.bitPath_Keysight = str(FPGA_FOLDER  / "M3102A.k7z")
        self.bitPath_SingleDDC = str(FPGA_FOLDER  / "M3102A_SingleDDC.k7z")
        self.bitPath_SingleDDC_Int = str(FPGA_FOLDER  / "M3102A_SingleDDC_Int.k7z")
        self.bitPath_SingleDDC_Spt = str(FPGA_FOLDER  / "M3102A_SingleDDC_Spt.k7z")
        self.bitPath_DualDDC = str(FPGA_FOLDER  / "M3102A_DualDDC.k7z")
        self.bitPath_DualDDC_Int = str(FPGA_FOLDER  / "M3102A_DualDDC_Int.k7z")
        self.bitPath_DualDDC_Spt = str(FPGA_FOLDER  / "M3102A_DualDDC_Spt.k7z")
        self.bitPath_AVE = str(FPGA_FOLDER  / "M3102A_AVE.k7z")
        self.bitPath_AVE_SingleDDC = str(FPGA_FOLDER  / "M3102A_AVE_SingleDDC.k7z")
        self.bitPath_AVE_SingleDDC_Int = str(FPGA_FOLDER  / "M3102A_AVE_SingleDDC_Int.k7z")
        self.bitPath_AVE_DualDDC = str(FPGA_FOLDER  / "M3102A_AVE_DualDDC.k7z")
        self.bitPath_AVE_DualDDC_Int = str(FPGA_FOLDER  / "M3102A_AVE_DualDDC_Int.k7z")

    def _bitModeDefine(self):
        """ Define the bitMode constant
            0x01: AVE
            0x02: DDC
            0x04: Single DDC
            0x08: Dual DDC
            0x10: Integration
            0x20: Single Point 
        """
        self.bitMode_Keysight = 0x00
        self.bitMode_AVE = 0x01
        self.bitMode_DDC = 0x02 
        self.bitMode_Single = 0x04
        self.bitMode_Dual = 0x08
        self.bitMode_Int = 0x10
        self.bitMode_Spt = 0x20
        # DDC COMBO:
        self.bitMode_SingleDDC = self.bitMode_DDC|self.bitMode_Single # 6
        self.bitMode_SingleDDC_Int =self.bitMode_SingleDDC|self.bitMode_Int # 22
        self.bitMode_SingleDDC_Spt =self.bitMode_SingleDDC_Int|self.bitMode_Spt # 54
        self.bitMode_DualDDC = self.bitMode_DDC|self.bitMode_Dual # 10
        self.bitMode_DualDDC_Int = self.bitMode_DualDDC|self.bitMode_Int # 26
        self.bitMode_DualDDC_Spt = self.bitMode_DualDDC_Int|self.bitMode_Spt # 58
        self.bitMode_AVE_SingleDDC = self.bitMode_AVE|self.bitMode_SingleDDC # 7
        self.bitMode_AVE_SingleDDC_Int = self.bitMode_AVE_SingleDDC|self.bitMode_Int # 23
        self.bitMode_AVE_DualDDC = self.bitMode_AVE|self.bitMode_DualDDC # 11
        self.bitMode_AVE_DualDDC_Int = self.bitMode_AVE_DualDDC| self.bitMode_Int # 27
    
    def _getAveReg(self):
        if not (self._FPGA & self.bitMode_AVE or self._FPGA & self.bitMode_Spt):
            return 
        if self._FPGA & self.bitMode_Spt or (self._FPGA & self.bitMode_Dual and self._FPGA & self.bitMode_AVE):
            self.regCh1State = self.FPGAgetSandBoxRegister("Mem_Ch1_State_I")
            self.regCh2State = self.FPGAgetSandBoxRegister("Mem_Ch1_State_Q")
            self.regCh3State = self.FPGAgetSandBoxRegister("Mem_Ch2_State_I")
            self.regCh4State = self.FPGAgetSandBoxRegister("Mem_Ch2_State_Q")
        else:
            self.regCh1State = self.FPGAgetSandBoxRegister("Mem_Ch1_State")
            self.regCh2State = self.FPGAgetSandBoxRegister("Mem_Ch2_State")
        self.regCh1Point = self.FPGAgetSandBoxRegister("Mem_Ch1_Point")
        self.regCh1Shot = self.FPGAgetSandBoxRegister("Mem_Ch1_Shot")
        self.regCh1Clear = self.FPGAgetSandBoxRegister("Mem_Ch1_Clear")
        self.regCh2Point = self.FPGAgetSandBoxRegister("Mem_Ch2_Point")
        self.regCh2Shot = self.FPGAgetSandBoxRegister("Mem_Ch2_Shot")
        self.regCh2Clear = self.FPGAgetSandBoxRegister("Mem_Ch2_Clear")
    
    def _getOffsetReg(self):
        if self._FPGA == self.bitMode_Keysight:
            return 
        if self._FPGA& self.bitMode_Dual:
            self.regCh1Offset = self.FPGAgetSandBoxRegister("Mem_Ch1_Offset_I")
            self.regCh2Offset = self.FPGAgetSandBoxRegister("Mem_Ch1_Offset_Q")
            self.regCh3Offset = self.FPGAgetSandBoxRegister("Mem_Ch2_Offset_I")
            self.regCh4Offset = self.FPGAgetSandBoxRegister("Mem_Ch2_Offset_Q") 
        else :
            self.regCh1Offset = self.FPGAgetSandBoxRegister("Mem_Ch1_Offset")
            self.regCh2Offset = self.FPGAgetSandBoxRegister("Mem_Ch2_Offset")

    def _getDDCReg(self):
        if self._FPGA& self.bitMode_DDC:
            self.regCh1SetFreq = self.FPGAgetSandBoxRegister("Mem_Ch1_SetFreq")
            # self.regCh1PhaseReset = self.FPGAgetSandBoxRegister("Mem_Ch1_phRst")
            self.regCh1LoA = self.FPGAgetSandBoxRegister("Mem_Ch1_LoA")
            self.regCh1LoB = self.FPGAgetSandBoxRegister("Mem_Ch1_LoB")
            self.regCh2SetFreq = self.FPGAgetSandBoxRegister("Mem_Ch2_SetFreq")
            # self.regCh2PhaseReset = self.FPGAgetSandBoxRegister("Mem_Ch2_phRst")
            self.regCh2LoA = self.FPGAgetSandBoxRegister("Mem_Ch2_LoA")
            self.regCh2LoB = self.FPGAgetSandBoxRegister("Mem_Ch2_LoB")
        
    def _loadBitFile(self, filepath):
        error = self.FPGAload(filepath)
        if error !=0:
            raise FileExistsError("can't load bitFile"+str(filepath))   
    
    def _DAQconfigAVE(self,CH, pt_per_shot, shots, trig_delay, trigger_mode):
        if self._FPGA & self.bitMode_AVE:
            if pt_per_shot % 10 != 0:
                raise ValueError("pt_per_shot should be multiple of 10")  
            if pt_per_shot >65530:
                raise ValueError("pt_per_shot can't exceed 65530")
            if self._FPGA & self.bitMode_DDC:
                self._DAQconfigDDC(CH, pt_per_shot, 1, trig_delay, trigger_mode)
            elif (self._FPGA == self.bitMode_AVE):
                error = self.DAQconfig(CH, pt_per_shot*5, 1, trig_delay*5, trigger_mode)
                if error:
                    raise ValueError("DAQ configure error in channel ",CH)
            else:
                error = self.DAQconfig(CH, pt_per_shot*5, 1, trig_delay, trigger_mode)
                if error:
                    raise ValueError("DAQ configure error in channel ",CH)
            pt_per_shot = round(pt_per_shot/5)-1
            if CH == 1:
                self.regCh1Point.writeRegisterInt32(pt_per_shot)
                self.regCh1Shot.writeRegisterInt32(shots)
            elif CH ==2:
                self.regCh2Point.writeRegisterInt32(pt_per_shot)
                self.regCh2Shot.writeRegisterInt32(shots)
            else:
                pass
                # raise ValueError("in Fpga mode, CH value only can be configure CH=1 or CH=2")

    def _DAQconfigDDC(self, CH, pt_per_shot, shots, trig_delay, trigger_mode):
        if self._FPGA & self.bitMode_DDC:
            if pt_per_shot % 10 !=0:
                raise ValueError(" pt_per_shot should be multiples of 10")
            if pt_per_shot > 65535:
                raise ValueError(" pt_per_shot can't exceed 65530")
            if self._FPGA & self.bitMode_Spt:
                if CH ==1:
                    self.regCh1Point.writeRegisterInt32(round(pt_per_shot/5)-1)
                    self.regCh1Shot.writeRegisterInt32(shots)
                elif CH ==2 or CH==3:
                    self.regCh2Point.writeRegisterInt32(round(pt_per_shot/5)-1)
                    self.regCh2Shot.writeRegisterInt32(shots)

            if self._FPGA & self.bitMode_Int==0:
                pt_per_shot = round(pt_per_shot/5)
            if self._FPGA & self.bitMode_Spt:
                shots = 1
            print("pt_per_shot=", pt_per_shot, "shots=", shots)
            if CH == 1:
                error = self.DAQconfig(1, pt_per_shot, shots, trig_delay, trigger_mode)
                error = self.DAQconfig(2, pt_per_shot, shots, trig_delay, trigger_mode)
                if error != 0:
                    raise ValueError("DAQ configure error in channel ",CH)
            elif CH ==2 or CH==3:
                print("configure 3, 4 for DDC")
                error = self.DAQconfig(3, pt_per_shot, shots, trig_delay, trigger_mode)
                error = self.DAQconfig(4, pt_per_shot, shots, trig_delay, trigger_mode)

        else: 
            raise ValueError("DAQconfigDDC only can be used in DDC mode")

    
    
    





    


