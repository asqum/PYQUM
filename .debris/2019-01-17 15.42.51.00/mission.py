# Loading Basics
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from os.path import basename as bs
myname = bs(__file__).split('.')[0] # This py-script's name

import requests
from flask import Flask, request, render_template, Response, redirect, Blueprint, jsonify
from pyqum.instrument.logger import address, get_status, set_status, status_code, output_code

# Scientific Constants
from scipy import constants as cnst

# This will run at server startup
# Modulars first, only then Benchtops (if and only if we use render_template)
from pyqum.instrument.modular import AWG, VSA
# AWG.test(False) #seems like AWG's working-instance works differently than VSA's
# awgsess = AWG.InitWithOptions()
# vsasess = VSA.InitWithOptions()
from pyqum.instrument.benchtop import MXG, ESG, DSO, PNA
# esgbench = ESG.Initiate()
# mxgbench = MXG.Initiate()
# dsobench = DSO.Initiate()

encryp = 'ghhgjad'
bp = Blueprint(myname, __name__, url_prefix='/mssn')

# Main
@bp.route('/')
def show():
    return render_template("blog/msson/mission.html", encryp=encryp)

# ALL
@bp.route('/all', methods=['POST', 'GET'])
def all(): 
    # Test Bed # All Task # Great Work
    return render_template("blog/msson/all.html")







print(Back.BLUE + Fore.CYAN + myname + ".bp registered!") # leave 2 lines blank before this
