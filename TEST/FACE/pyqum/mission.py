# Loading Basics
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from os.path import basename as bs
myname = bs(__file__).split('.')[0] # This py-script's name

import requests
from flask import Flask, request, render_template, Response, redirect, Blueprint, jsonify
from pyqum.instrument.logger import address, get_status, set_status, status_code, output_code
from pyqum.directive.characterize import F_Response

# Scientific Constants
from scipy import constants as cnst


encryp = 'ghhgjad'
bp = Blueprint(myname, __name__, url_prefix='/mssn')

# Main
@bp.route('/')
def show():
    return render_template("blog/msson/mission.html", encryp=encryp)

# ALL
@bp.route('/all', methods=['GET'])
def all(): 
    # Test Bed # All Task # Great Work
    return render_template("blog/msson/all.html")
@bp.route('/all/test', methods=['GET'])
def alltest():
    i = request.args.get('idea')
    print(Back.MAGENTA + 'i: %s'%i)
    return jsonify(i=i)
@bp.route('/all/insertopt', methods=['GET'])
def allinsertopt():
    x = [100, 200, 300, 400, 500, 600, 777]
    return jsonify(x=x)

# CHAR
@bp.route('/char', methods=['GET'])
def char(): 
    return render_template("blog/msson/char.html")
# CHAR -> F-Response
@bp.route('/char/fresp/init', methods=['GET'])
def char_fresp_init(): 
    global M_fresp
    M_fresp = F_Response()
    # ifb = eval(str(request.args.get('ifb')))
    return jsonify(daylist=M_fresp.daylist)
@bp.route('/char/fresp/time', methods=['GET'])
def char_fresp_time():
    wday = int(request.args.get('wday'))
    M_fresp.selectday(wday)
    M_fresp.listime()
    return jsonify(startimes=M_fresp.startimes)



# DATA
@bp.route('/data', methods=['GET'])
def data(): 
    return render_template("blog/msson/data.html")


def test():
    Op = "a"
    M = RTAmp([0,0,1], [-70,-50,3], [0.7e9,18e9,251], [10,10,1], [0,1,2], '', Op)
    if Op.lower() != "n":
        M.selectday(0)
        M.selectmoment(1)
        M.accesstructure()
        M.loadata()
        print(M.selectedata[-1])
        M.buildata()
        print(M.datacontainer)

# test()




print(Back.BLUE + Fore.CYAN + myname + ".bp registered!") # leave 2 lines blank before this
