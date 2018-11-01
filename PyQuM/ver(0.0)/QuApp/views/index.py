from flask import Blueprint, render_template
from pathlib import Path
import glob

bp = Blueprint(__name__, __name__, template_folder='templates')

def fetch_data():
    complete_data = []
    # AllPath = Path("E:/NCHUQ/PYQUM/PyQuM/QuApp/database/") / "*.pyqum"
    AllPath = "E:/NCHUQ/PYQUM/PyQuM/QuApp/database/*.pyqum"
    datas = glob.glob(AllPath)
    for data in datas:
        with open(data) as dfile:
            complete_data.append(dfile.read())
    return complete_data

@bp.route('/')
def show():
    return render_template('index.html', datas=fetch_data())
