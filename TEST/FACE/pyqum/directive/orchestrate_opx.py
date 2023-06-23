'''Orchestrate with QM OPX'''

from colorama import init, Fore, Back
init(autoreset=True) #to convert termcolor to wins color

from os.path import basename as bs
mdlname = bs(__file__).split('.')[0] # instrument-module's name e.g. ENA, PSG, YOKO

from traceback import format_exc
from time import time, sleep
from copy import copy, deepcopy
from json import loads, dumps
from numpy import prod, array, mean, ceil, moveaxis, linspace, outer, ones, divide
from numexpr import evaluate
from flask import session, g

from importlib import import_module as im
from pyqum.instrument.logger import settings, get_status, set_status, jobsinqueue, qout, job_update_perimeter
from pyqum.instrument.toolbox import cdatasearch, waveform, find_in_list



