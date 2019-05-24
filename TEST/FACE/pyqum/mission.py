# Loading Basics
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from os.path import basename as bs
myname = bs(__file__).split('.')[0] # This py-script's name

import requests
from flask import Flask, request, render_template, Response, redirect, Blueprint, jsonify
from pyqum.instrument.logger import address, get_status, set_status, status_code, output_code
from pyqum.directive.characterize import TESTC

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
# CHAR -> FLEM
@bp.route('/char/rtamp/init', methods=['GET'])
def charrtampinit(): 
    ampstate = [int(request.args.get('ampstate'))]*2 + [1]
    powr = eval(str(request.args.get('powr')))
    freq = eval(str(request.args.get('freq')))
    ifb = eval(str(request.args.get('ifb')))
    comment = str(request.args.get('comment'))
    try:
        global rtamp_operation
        rtamp_operation = str(request.args.get('operation'))
        global M_rtamp
        M_rtamp = RTAmp(ampstate, powr, freq, ifb, [0,1,2], comment, rtamp_operation)
        if rtamp_operation.lower() == 'n':
            dayslot = [M_rtamp.day]
        else: dayslot = M_rtamp.daylist
    except: dayslot = ["pick a day"]
    return jsonify(status="Initiated", dayslot=dayslot)
@bp.route('/char/rtamp/time', methods=['GET'])
def charrtamptime(): 
    try:
        wday = int(request.args.get('wday'))
        print("wday: %s" %wday)
        M_rtamp.selectday(wday)
        if rtamp_operation.lower() == 'n':
            timeslot = [M_rtamp.moment]
        else: 
            M_rtamp.accesstimeline()
            timeslot = M_rtamp.startimes
    except: timeslot = ["pick a time"]
    return jsonify(timeslot=timeslot)
@bp.route('/char/rtamp/run', methods=['GET'])
def charrtamprun(): 
    try:
        wmoment = int(request.args.get('wmoment'))
        M_rtamp.selectmoment(wmoment)
        M_rtamp.accesstructure()
        M_rtamp.loadata()
        Idata = M_rtamp.selectedata[::2]
        Qdata = M_rtamp.selectedata[1::2]
    except:
        M_rtamp.datacontainer = {}
        Idata = []
        Qdata = []
    return jsonify(datacontainer=M_rtamp.datacontainer, Idata=Idata, Qdata=Qdata)

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
