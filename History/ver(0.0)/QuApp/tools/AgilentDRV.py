# This is a collection of low-level VIs for Agilent Drivers

from QuApp.tools.Callout import Call_VI
# from Callout import Call_VI

# Root-location for the M9392A drivers
LOC01 = "C:\\Program Files (x86)\\Agilent\\M9392\\LabVIEW Driver\\20xx\\Agilent M9392" #VSA
LOC02 = "C:\\Program Files (x86)\\Agilent\\M933x\\LabVIEW Driver\\20xx\\Agilent M933x" #AWG

@Call_VI
def InitializeVSA(Parameters):
    pack = dict()
    pack['VIPath'] = LOC01 + "\\Initialize With Options.vi"
    pack['ParameterNames'] = ["resource string", "option string", "id query (Off)", "reset device (Off)"]
    pack['Parameters'] = Parameters
    pack['Indicators'] = ["instrument handle out", "error out"]
    return pack

@Call_VI
def CloseVSA(handle):
    pack = dict()
    pack['VIPath'] = LOC01 + "\\Close.vi"
    pack['ParameterNames'] = ["instrument handle"]
    pack['Parameters'] = handle
    pack['Indicators'] = ["error out"]
    return pack

@Call_VI
def InitializeAWG(Parameters):
    pack = dict()
    pack['VIPath'] = LOC02 + "\\Initialize With Options.vi"
    pack['ParameterNames'] = ["resource string", "option string", "id query (Off)", "reset device (Off)"]
    pack['Parameters'] = Parameters
    pack['Indicators'] = ["instrument handle out", "error out"]
    return pack

@Call_VI
def CloseAWG(handle):
    pack = dict()
    pack['VIPath'] = LOC02 + "\\Close.vi"
    pack['ParameterNames'] = ["instrument handle"]
    pack['Parameters'] = handle
    pack['Indicators'] = ["error out"]
    return pack

# @Call_VI
# def ConfigAcquisVSA(Parameters):
#     pack = dict()
#     pack['VIPath'] = LOC01 + "\\Public\\Configure\\Configure Acquisition.vi"
#     pack['ParameterNames'] = ["instrument handle"]
#     pack['Parameters'] = Parameters
#     pack['Indicators'] = ["error out"]
#     return pack

