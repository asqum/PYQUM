# This is a template for calling out other programming platforms other than Python itself
# from ctypes import *

# calling VI using its activeX methods & properties
def Call_VI(VI_name): #None = []

    import platform
    platinfo = platform.system()

    if platinfo is "Windows":

        import comtypes.client
            
        # Path to type library.
        TypeLibPath = "C:/Program Files (x86)/National Instruments for 8/LabVIEW 2011/resource/labview.tlb"
        comtypes.client.GetModule(TypeLibPath)

        def wrapper(ctrl_params): # VIPath, ParameterNames, Parameters, Indicators=None
            comtypes.CoInitialize()
            unpack = VI_name(ctrl_params)
            VIPath = unpack['VIPath']
            ParameterNames = unpack['ParameterNames']
            Parameters = unpack['Parameters']
            Indicators = unpack['Indicators']
            try:
                Application = comtypes.client.CreateObject("LabVIEW.Application.8",...and
                None, None, comtypes.gen.LabVIEW._Application)
                #Get VI Reference (Application methods)
                VirtualInstrument = Application.GetVIReference(VIPath)
                #Open VI front panel in hidden mode (VI methods)
                VirtualInstrument.OpenFrontPanel(True, 1)  # 0 (Invalid), 1 (Standard: Background), 2 (Closed), 3 (Hidden), 4 (Minimized), and 5 (Maximized).
                #Call VI
                VirtualInstrument.Call(ParameterNames, Parameters) #Classic Control is not supported!
                # VirtualInstrument.CloseFrontPanel()
                
                if not Indicators:
                    data = []
                else:
                    data = [VirtualInstrument.GetControlValue(i) for i in Indicators] # indexed (serialized) data

            except:
                VirtualInstrument = None
                Application = None
                raise  # rethrow the exception to get the full trace on the console

            return data
        
        VirtualInstrument = None
        Application = None

        return wrapper

    else: pass

