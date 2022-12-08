'''
This is for adapting to customized FPGA
'''

import sys
sys.path.append('C:/program Files(x86)/Keysight/SD1/Libraries/Python')
import keysightSD1 
import time

# ALL FPGA PATH:
from pyqum.instrument.reader import device_port
from pathlib import Path
FPGA_FOLDER = Path(device_port("FPGA"))
M3102_PATH = FPGA_FOLDER / "M3102A.k7z"
FPGA_PATH = FPGA_FOLDER / "M3102A_AVE.k7z"

class SD_AINAVE(keysightSD1.SD_AIN):
    def __init__(self):
        super(SD_AINAVE, self).__init__()
        self.FPGA = False
    
    def loadAVEBitFile(self, FPGA_LEVEL=0):
        '''
        FPGA LEVEL:
        0: Revert FPGA mode to False and Load default BitFile/Firmware
        1: Waveform Average
        2: 
        '''
        if int(FPGA_LEVEL)==0:
            self.FPGA = False
            try: self.FPGAload(str(M3102_PATH))
            except(RuntimeError): print("Required Firmware version of 02.03")
            except(FileNotFoundError): print("Original bitfile load error: M3102A.k7z not found in %s" %str(M3102_PATH))
            return

        if int(FPGA_LEVEL)==1:
            error = self.FPGAload(str(FPGA_PATH))
            if error !=0: raise FileNotFoundError("FPGA bitfile load error")   

        # Checking Sandbox:
        # self.FPGAreset(keysightSD1.SD_ResetMode.PULSE)
        self.regClear = self.FPGAgetSandBoxRegister("Mem_Clear")
        if not isinstance(self.regClear,keysightSD1.SD_SandBoxRegister):
            raise TypeError("can't find regClear register") 
        self.regNumOfPoint = self.FPGAgetSandBoxRegister("Mem_NumOfPoint")
        if not isinstance(self.regNumOfPoint,keysightSD1.SD_SandBoxRegister):
            raise TypeError("can't find regNumOfPoint register") 
        self.regNumOfShot = self.FPGAgetSandBoxRegister("Mem_NumOfShot")
        if not isinstance(self.regNumOfShot,keysightSD1.SD_SandBoxRegister):
            raise TypeError("can't find regNumOfShot register") 
        self.regStatus0 = self.FPGAgetSandBoxRegister("Mem_State_0")
        if not isinstance(self.regStatus0,keysightSD1.SD_SandBoxRegister):
            raise TypeError("can't find regStatus0 register") 
        self.regStatus1 = self.FPGAgetSandBoxRegister("Mem_State_1")
        if not isinstance(self.regStatus1,keysightSD1.SD_SandBoxRegister):
            raise TypeError("can't find regStatus1 register") 
        self.FPGA = True 
        
    def DAQconfigAVE(self,CH, pointsPerCycle, nCycles, triggerDelay, triggerMode):
        if self.FPGA:
            if pointsPerCycle % 10 != 0:
                raise ValueError("pt_per_shot should be multiple of 10")  
            if pointsPerCycle >65530:
                raise ValueError("pt_per_shot can't exceed 65530")
            if nCycles > 1000000:
                raise ValueError("total shots can't exceed 65535")
            error = self.DAQconfig(CH, pointsPerCycle, 1, triggerDelay, triggerMode)
            if error != 0:
                raise ValueError("DAQ configure error in channel ",CH)
            self.regNumOfPoint.writeRegisterInt32(pointsPerCycle)
            self.regNumOfShot.writeRegisterInt32(nCycles)
        else:
            self.DAQconfig(CH, pointsPerCycle, nCycles, triggerDelay, triggerMode)
    
    def aveMemoryClear(self):
        if self.FPGA:
            self.regClear.writeRegisterInt32(1)

    def checkFinished(self, timeout_in_s=1):
        if self.FPGA:
            status0 = self.regStatus0.readRegisterInt32()
            status1 = self.regStatus1.readRegisterInt32()
            tstart = time.time()
            tcheck = 0
            while(tcheck < timeout_in_s and (status0 !=26 or status1 != 26)):
                status0 = self.regStatus0.readRegisterInt32()
                status1 = self.regStatus1.readRegisterInt32()
                tcheck = time.time()-tstart
            if tcheck >=timeout_in_s:
                info = self.getDebugInfo()
                raise RuntimeError("AVE process timeout, check trigger timing or incease timeout time setting. Register info:"+info)

    def getDebugInfo(self):
        TrigCnt0 = self.FPGAgetSandBoxRegister("Mem_TriggerCnt0")
        TrigCnt1 = self.FPGAgetSandBoxRegister("Mem_TriggerCnt1")
        regNumOfShot = self.FPGAgetSandBoxRegister("Mem_NumOfShot")
        tn0 = TrigCnt0.readRegisterInt32()
        tn1 = TrigCnt1.readRegisterInt32()
        shots = regNumOfShot.readRegisterInt32()
        info = "tn0 = "+str(tn0)+", tn1 = "+str(tn1)+", shots="+str(shots)
        return info





    


