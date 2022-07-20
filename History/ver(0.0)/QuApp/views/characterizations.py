from flask import Blueprint, render_template, request, redirect
import random, json, glob
from pathlib import Path

bp = Blueprint(__name__, __name__, template_folder='templates')

def random_string(length=16):
    final_string = ''
    chars = "abcdefghijklmnopqrstuvwxyz0123456789"
    for i in range (0, length):
        final_string += chars[random.randint(0, len(chars)-1)]
    
    return final_string

from QuApp.tools.AgilentDRV import InitializeVSA, CloseVSA
from QuApp.tools.benchtops import ESG
from QuApp.tools.NIModules import *

INPATH = "E:/NCHUQ/INSTATUS/"

@bp.route('/characterizations', methods=['POST', 'GET']) #this will appear as the web address
def show():
    vsastatus = Path(INPATH) / "VSAstatus.pyqum"
    esgstatus = Path(INPATH) / "esgstatus.pyqum"
    dataram = dict() #or {}

    if request.method == 'POST':
        VSArs = "PXI24::12::0::INSTR;PXI24::14::0::INSTR;PXI24::8::0::INSTR;PXI24::9::0::INSTR;PXI29::0::0::INSTR"
        AWGrs = "PXI0::CHASSIS1::SLOT3::FUNC0::INSTR"

        if request.form.get('closevsa'):
            with open(vsastatus) as jfile:
                contents = json.load(jfile)

            if 'STATE:' not in contents:
                handle = [contents['handle']]
                CloseVSA(handle)
                dataram['STATE:'] = "OFF"
                contents.update(dataram) #update dict and overwrite file
                with open(vsastatus, 'w') as file:
                    json.dump(contents, file)

                return redirect('/')

        if request.form.get('initiatevsa'):
            respons = InitializeVSA([VSArs, "", False, False])
            if respons[1][1] is 0:
                dataram['Initialize'] = "ON: No Errors"
            else: dataram['Initialize'] = "Errors: " + respons[1][2]
            dataram['handle'] = respons[0]

            with open(vsastatus, 'w') as file:
                json.dump(dataram, file)
            
            return redirect('/')

        if request.form.get('esgon'):
            freq = request.form.get('frequency')
            powa = request.form.get('power')
            status = ESG(True, freq, powa)
            dataram.update(status)
            
            with open(esgstatus, 'w') as file:
                json.dump(dataram, file)
            
            return redirect('/')

        if request.form.get('esgoff'):
            status = ESG(False)
            dataram.update(status)
            
            with open(esgstatus, 'w') as file:
                json.dump(dataram, file)
            
            return redirect('/')

    return render_template('characterizations.html') #this is where it really goes
