# Loading Basics
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from os.path import basename as bs
myname = bs(__file__).split('.')[0] # This py-script's name

from flask import Blueprint, render_template, request, redirect, jsonify, g, session
import random, json, ctypes, requests
from pathlib import Path

# from pyqum.instrument.modular import VSA, AWG
# from pyqum.instrument.benchtop import ESG

bp = Blueprint(myname, __name__)

cache = {}

@bp.route('/script', methods=['POST', 'GET']) #this will appear as the web address
def show():

    return render_template('blog/bridg/script.html')


print(Back.BLUE + Fore.CYAN + myname + ".bp registered!") # leave 2 lines blank before this
