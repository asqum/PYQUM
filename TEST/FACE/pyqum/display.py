# Loading Basics
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from os.path import basename as bs
myname = bs(__file__).split('.')[0] # This py-script's name

from flask import Blueprint, render_template, request, redirect, Response, stream_with_context
import random, json, glob, time
import numpy as np

from pyqum import stream_template

bp = Blueprint(myname, __name__, url_prefix='/dsply')

@bp.route('/', methods=['POST', 'GET'])
def show():
    
    return render_template('blog/dsply/display.html')

# Static
@bp.route('/figstatic', methods=['POST', 'GET'])
def figstatic():
    def fetch():
        datas = [0, 10, 5, 2, 20, 30, 45]
        return datas
    return render_template('blog/dsply/figstatic.html', datas=fetch()) #this is where it really goes

# Static
@bp.route('/fastream')
def fastream():
    return render_template('blog/dsply/fastream.html')

# Setting shared variables
x = np.arange(0, 12, 0.1)
lx = len(x)
yr = np.random.ranf(lx) - np.random.ranf(lx)
yr2 = np.random.ranf(lx) - np.random.ranf(lx)
ys = np.sin(3*x)
yc = np.cos(3 * x)
    
# Streaming
@bp.route('/dynamic', methods=['POST', 'GET'])
def dynamic(): # one of the method called by base/layout
    datagen, data = {}, {}
    data['x'] = [x for x in x]
    data['y'] = [y for y in yr]

    if request.method == 'POST':
        
        if request.form.get('analysis'):
            def gen(): 
                i = 1
                while True:
                    data['y'][1:lx] = data['y'][0:lx - 1]
                    data['y'][0] = random.uniform(-1, 1)
                    yield i, data
                    time.sleep(0.03)
                    i += 1

            datagen = gen()

    # return Response(gen()) #Blank page with just data print
    # return Response(stream_with_context(gen())) #SAME AS ABOVE
    # return Response(stream_template('blog/analysis.html', data=rows)) #BLANK!!! WHY???
    return Response(stream_with_context(stream_template('blog/dsply/figdynamic.html', data=datagen)))
    # return render_template('blog/analysis.html', data=data) #NORMAL Display, No streaming!

@bp.route('/stream', methods=['POST', 'GET'])
def stream():
    datad = []
    def gen():
        # datad = [] # only if += is used
        for i in range(371):
            a = np.sin(i * np.pi / 25 + 0.25 * np.pi) + 0.07 * random.uniform(-1, 1)
            b = np.cos(i * np.pi / 25 + 0.25 * np.pi) + 0.13 * random.uniform(-1, 1)
            book = dict(x=a, y=b)
            datad.append(book)
            # datad += [book] # equivalent to append but need to declare it inside def
            yield i, datad
            time.sleep(0.1)
    data = gen()
      
    return Response(stream_with_context(stream_template('blog/dsply/figstream.html', data=data)))

@bp.route('/concurrent', methods=['POST', 'GET'])
def concurrent():  # one of the method called by base/layout
    datad, data, chartop, chartopt = {}, {}, "", ""
    data['x'] = [x for x in x]
    data['yS'] = [y for y in ys]
    data['yR'] = [y for y in yr]
    data['yC'] = [y for y in yc]
    data['xud'], data['yup'], data['ydn'] = [], [], []
    # chartopt = request.form.get("chartopt")
    if 'run' in request.form:
        chartopt = request.form.get("chartopt") # selection picked for chart#1
        chartop = request.form.get("chartop") # selection picked for chart#2
        def gen():
            for i in range(lx):
                data['xud'].append(data['x'][i])
                    
                if str(chartopt) == "sinusoid":
                    data['yup'].append(data['yS'][i])
                if str(chartopt) == "random":
                    data['yup'].append(data['yR'][i])
                if str(chartopt) == "cosine":
                    data['yup'].append(data['yC'][i])       
                
                if str(chartop) == "0":
                    data['ydn'].append(data['yS'][i])
                if str(chartop) == "1":
                    data['ydn'].append(data['yR'][i])
                if str(chartop) == "2":
                    data['ydn'].append(data['yC'][i])

                yield [data['xud'], data['yup'], data['ydn']]
                time.sleep(0.03)
        datad = gen()

    return Response(stream_with_context(stream_template('blog/dsply/figconcurrent.html', datad=datad, chartopt=str(chartopt), chartop=str(chartop))))
    # return render_template('blog/analysis.html', data=data) #NORMAL Display, No streaming!

@bp.route('/game01', methods=['POST', 'GET'])
def game01():
    
    return render_template('blog/dsply/game01.html')

print(Back.BLUE + Fore.CYAN + myname + ".bp registered!") # leave 2 lines blank before this
