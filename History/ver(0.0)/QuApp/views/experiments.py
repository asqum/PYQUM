from flask import Blueprint, render_template, request, redirect
import random, json, glob

bp = Blueprint(__name__, __name__, template_folder='templates')

@bp.route('/experiments')
def show():
    def fetch():
        datas = [0, 10, 5, 2, 20, 30, 45]
        return datas
    return render_template('experiments.html', datas=fetch()) #this is where it really goes