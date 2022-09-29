'''For Arrangements of Authorizations & Clearances'''

# Loading Basics
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from os.path import basename as bs
myname = bs(__file__).split('.')[0] # This py-script's name

# from json import loads
import functools
# from datetime import timedelta
# from keyboard import press

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from pyqum import get_db, close_db
from pyqum.instrument.logger import lisample, set_status, get_status, which_queue_system, acting
from pyqum.instrument.reader import inst_designate

bp = Blueprint(myname, __name__, url_prefix='/auth')


#from qpu.backend.circuit.api import to_deviceManager

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """
    If a user id is stored in the session, load the user object from
    the database into ``g.user``.
    This will be executed EVERYTIME a ROUTE (app-instance) is called upon!
    NOTE: ONLY attributes subjected to highly dynamic change will be defined here in order to be efficient!
    """
    # 0. DR-specific parameters:
    g.DR_platform = int(get_status("WEB")['port']) - 5300
    navbar_colors = ['#ffba26', '#ff2626'] # hex-color-sequence for each DR
    try: g.base_color = "rgb(%s, %s, %s)" %tuple([int(navbar_colors[g.DR_platform-1].lstrip('#')[i:i+2], 16) for i in (0, 2, 4)]) # convert hex- to rgb-color
    except: g.base_color = "rgb(%s, %s, %s)" %(0, 0, 0) # Black for Virtual Environment
    
    if session.get('DR_platform') is None: 
        user_id = None
    elif session['DR_platform'] == int(get_status("WEB")['port']) - 5300: 
        user_id = session.get('user_id')
    else: 
        session.clear()
        user_id = None
        return("<h3>DEFLECTED-LOGIN DETECTED</h3><h3>PLEASE REFRESH & RE-LOGIN</h3><h3 style='color:blue;'>Courtesy from HoDoR</h3>")
    
    if user_id is None:
        g.user = None
    else:
        # 1. logged-in user's profile:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        close_db()

        # 2. Latest sample-loading date: (to prevent measuring old samples)
        try: 
            g.latest_date = get_db().execute('SELECT s.registered FROM sample s ORDER BY registered DESC').fetchone()[0].strftime("%Y-%m-%d")
        except: 
            g.latest_date = 0
            print(Fore.BLUE + "No samples yet to be found in the database")
        close_db()
        
        # 3. logged-in user's samples' details:
        # PENDING: allow Admin to access all samples
        g.samples = get_db().execute(
            'SELECT s.id, author_id, samplename, specifications, location, level, description, registered'
            ' FROM sample s JOIN user u ON s.author_id = u.id' # join tables to link (id in user) and (author_id in post) to get username
            ' WHERE u.id = ?'
            ' ORDER BY registered DESC',
            (g.user['id'],)
        ).fetchall()
        close_db()
        g.samples = [dict(s) for s in g.samples]

        # 4. logged-in user's co-authored samples' details:
        g.cosamples = get_db().execute(
            'SELECT s.id, author_id, samplename, specifications, location, level, description, registered'
            ' FROM sample s JOIN user u ON s.author_id = u.id' # join tables to link (id in user) and (author_id in post) to get username
            ' WHERE s.co_authors LIKE ?'
            ' ORDER BY registered DESC',
            ('%%%s%%' %g.user['username'],)
        ).fetchall()
        close_db()
        g.cosamples = [dict(x) for x in g.cosamples]

        # 5. Instrument list & details for each DR (PyQUM) platform:
        g.machlist = get_db().execute(
            '''
            SELECT m.codename, connected, category, sequence, system, note, u.username
            FROM machine m
            INNER JOIN user u ON m.user_id = u.id
            WHERE m.BDR = ?
            ORDER BY m.id DESC
            ''',
            (g.DR_platform,)
        ).fetchall()
        close_db()
        g.machlist = [dict(x) for x in g.machlist]
        g.instlist = [x['codename'].replace('_','-') for x in g.machlist]
        g.machspecs = dict()
        for x in g.machlist: g.machspecs[x['codename']] = x['note']

        # 6. Appointed sample in each measurement system:
        g.CHAR0_sample = get_db().execute("SELECT q.samplename FROM queue q WHERE q.system='CHAR0'").fetchone()[0]
        close_db()
        g.CHAR1_sample = get_db().execute("SELECT q.samplename FROM queue q WHERE q.system='CHAR1'").fetchone()[0]
        close_db()
        g.QPC0_sample = get_db().execute("SELECT q.samplename FROM queue q WHERE q.system='QPC0'").fetchone()[0]
        close_db()
        g.QPC1_sample = get_db().execute("SELECT q.samplename FROM queue q WHERE q.system='QPC1'").fetchone()[0]
        close_db()
        # print(Fore.GREEN + "CHAR0_sample: %s" %g.CHAR0_sample)


        # press('enter') # simulate press-enter-key in cmd to clear the possible clog!


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        affiliation = request.form['affiliation']
        email = request.form['email']
        userstatus = 'pending'
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {0} is already registered.'.format(username)

        if error is None:
            # the name is available, store it in the database and go to the login page
            db.execute(
                'INSERT INTO user (username, password, status, fullname, affiliation, email) VALUES (?, ?, ?, ?, ?, ?)',
                (username, generate_password_hash(password), userstatus, fullname, affiliation, email,)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        close_db()
        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        elif user['status'].upper() != 'APPROVED':
            error = 'Awaiting Approval...'

        # Entering the system after being vetted:
        if error is None:
            # store the user's credentials in a new SESSION (Cookies) and return to the index
            session.clear()
            session['DR_platform'] = int(get_status("WEB")['port']) - 5300
            session['user_id'] = user['id']
            session['user_name'] = user['username']
            session['user_status'] = user['status']
            session['user_measurement'] = user['measurement']
            session['user_instrument'] = user['instrument']
            session['user_analysis'] = user['analysis']
            # measurement related:
            session['c_fresp_structure'] = []
            session['run_clearance'] = False
            session['int_clearance'] = False
            session['bdr_clearance'] = False
            session['people'] = None
            print("%s has logged-in Successfully!" %session['user_name'] )

            g.approved_user_list = None
            if user['management'] == "oversee":
                # ALL approved users' credentials:
                g.approved_user_list = db.execute(
                    'SELECT u.id, username, measurement, instrument, analysis'
                    ' FROM user u WHERE u.status = ?'
                    ' ORDER BY id DESC',
                    ('approved',)
                ).fetchall()
                g.approved_user_list = [dict(x) for x in g.approved_user_list]
            print(Fore.RED + Back.WHITE + "ALL APPROVED USER CREDENTIALS: %s" %g.approved_user_list)

            return redirect(url_for('index'))

        close_db()
        print(error)
        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for('index'))

@bp.route('/user')
def user():
    """Load User Profile and Sample Database"""
    return render_template('auth/user.html')
@bp.route('/user/profile')
def userprofile():

    return render_template('auth/profile.html')
@bp.route('/user/data_indexing')
def userdata_indexing():
    usr_name = session['user_name']
    print("Indexing %s's Data into Database" %usr_name)

    return jsonify(usr_name=usr_name)

# Sample Database Handling:
@bp.route('/user/samples')
def usersamples():
    # Main samples:
    samples = [s['samplename'] for s in g.samples]
    # Shared samples (co-authored):
    cosamples = [s['samplename'] for s in g.cosamples]
    # Current sample:
    try: selected_sample = get_status("MSSN")[session['user_name']]['sample']
    except: selected_sample = 0 # For first-time user to pick a sample to begin with
    # QPC list:
    qpclist = [x['system'] for x in get_db().execute('SELECT system FROM queue').fetchall() if "QPC" in str(x['system']).upper()]
    return render_template('auth/samples.html', samples=samples, cosamples=cosamples, selected_sample=selected_sample, qpclist=qpclist)
@bp.route('/user/samples/register')
def usersamples_register():
    sname = request.args.get('sname')
    loc = request.args.get('loc')
    level = request.args.get('level')
    description = request.args.get('description')
    db = get_db()
    try:
        db.execute(
            'INSERT INTO sample (author_id, samplename, location, level, description)'
            ' VALUES (?, ?, ?, ?, ?)',
            (g.user['id'], sname, loc, level, description,)
        )
        db.commit()
        message = "Sample %s added to the database!" %(sname)
    except Exception as e:
        message = "Abort: %s" %e
    close_db()
    return jsonify(message=message)
@bp.route('/user/samples/access')
def usersamples_access():
    '''Create people session (cookie) here
    '''
    sname = request.args.get('sname')
    db = get_db()
    try:
        sample_cv = db.execute(
            'SELECT s.id, author_id, samplename, specifications, location, level, description, registered, co_authors, history'
            ' FROM sample s JOIN user u ON s.author_id = u.id'
            ' WHERE s.samplename = ?',
            (sname,)
        ).fetchone()
        sample_cv = dict(sample_cv) # convert sqlite3.row into dictionary for this select format

        sample_owner = db.execute(
            'SELECT u.id, username FROM sample s JOIN user u ON s.author_id = u.id WHERE s.samplename = ?',(sname,)
        ).fetchone()['username']
        saved = bool(sname in lisample(sample_owner)) # saved?

        message = "Accessing Sample %s owned by %s" %(sname,sample_owner)
    except:
        raise # NOTE: please run first measurement test to create USRLOG directory!
        sample_cv = []
        message = "Consult ABC"
    close_db()

    system = which_queue_system(sname)
    return jsonify(sample_cv=sample_cv, message=message, saved=saved, system=system)
@bp.route('/user/samples/update')
def usersamples_update():
    sname = request.args.get('sname')
    loc = request.args.get('loc')
    specs = request.args.get('specs')
    description = request.args.get('description')
    coauthors = request.args.get('coauthors')
    level = request.args.get('level')
    history = request.args.get('history')
    
    db = get_db()
    try:
        sample_owner = db.execute('SELECT u.id, username FROM sample s JOIN user u ON s.author_id = u.id WHERE s.samplename = ?',(sname,)).fetchone()['username']
        if (int(g.user['management'])>=7) or (session['user_name']==sample_owner):
            db.execute(
                'UPDATE sample SET location = ?, specifications = ?, description = ?, co_authors = ?, level = ?, history = ? WHERE samplename = ?',
                (loc, specs, description, coauthors, level, history, sname,)
            )
            db.commit()
            message = "Sample %s has been successfully updated!" %(sname)
            acting("UPDATING SAMPLE: %s" %(sname))
        else:
            message = 'CLEARANCE NOT MATCHED: Only Admin / Owner allowed to update samples'
    except:
        message = "Check sample parameters"
    close_db()

    print(message)
    return jsonify(message=message)
@bp.route('/user/samples/meal', methods=['GET'])
def usersamples_meal():
    '''Double Log which USER is using which SAMPLE:'''
    sname = request.args.get('sname')
    print(Fore.BLUE + "TAKING MEAL OF THE SAMPLE %s" %(sname))
    # SESSION (Current Sample):
    session['user_current_sample'] = sname
    # SESSION (Sample's OWNER):
    try: 
        session['people'] = get_db().execute('SELECT u.id, username FROM sample s JOIN user u ON s.author_id = u.id WHERE s.samplename = ?',(sname,)).fetchone()['username']
        close_db()
        print(Fore.YELLOW + "%s is managed (owned) by %s" %(sname, session['people']))
    except: 
        session['people'] = None
    # LOGGED INTO JSON: (PENDING: Align the other MSSN set_status as well with time-stamp)
    try: 
        set_status("MSSN", {session['user_name']: dict(sample=sname, queue=get_status("MSSN")[session['user_name']]['queue'], time=0)})
        acting("MEALING SAMPLE: %s" %(sname))
    except: 
        set_status("MSSN", {session['user_name']: dict(sample=sname, queue='', time=0)})
    return jsonify(sname=get_status("MSSN")[session['user_name']]['sample'])

import qpu.backend.circuit.backendcircuit as bec
import qpu.backend.phychannel as pch
import qpu.backend.component as qcp
from pandas import DataFrame

@bp.route('/user/samplesloc/update/qpc_wiring', methods=['GET'])
def usersamplesloc_update_qpc_wiring():
    peach = request.args.get('peach')
    qpc_selected = request.args.get('qpc_selected')
    print(qpc_selected)
    # Translate Peach to QPC:

    mybec = bec.BackendCircuit()
    wiring_info = peach.split("===")
    print(wiring_info)
    dict_list = eval(wiring_info[0])
    channels = []
    for ch in dict_list:
        #print(ch)
        channels.append( pch.from_dict( ch ) )

    mybec._channels = channels

    
    #mybec._qComps = read_qComp()
    mybec.qc_relation = DataFrame.from_dict(eval(wiring_info[1]))
    mybec.q_reg = eval(wiring_info[2])
    qpc_dict = mybec.to_qpc()
    instr_organized = {}
    dict_str = ["CH","ROLE"]
    for cate, val in qpc_dict.items():
        if cate in dict_str:
            destination = str(val).replace("'",'"')
        else:
            destination = ",".join(val)
        instr_organized[cate]=destination


    instr_organized["ADC"] = "DIG"
    # Update QPC-wiring database:
    try:
        if int(g.user['management'])>=3:
            for key, val in instr_organized.items(): 
                inst_designate(qpc_selected, key, val)
            message = "%s's instrument assignment has been set successfully" %qpc_selected
            acting(message)
        else: message = "Clearance not enough"
    except:
        raise
        #message = "database error"

    return jsonify(message=message)

# Sample Job-History:



print(Back.BLUE + Fore.CYAN + myname + ".bp registered!") # leave 2 lines blank before this

