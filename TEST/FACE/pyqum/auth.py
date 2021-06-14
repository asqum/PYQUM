'''For Arrangements of Authorizations & Clearances'''

# Loading Basics
from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color
from os.path import basename as bs
myname = bs(__file__).split('.')[0] # This py-script's name

import functools
from keyboard import press

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash

from pyqum import get_db
from pyqum.instrument.logger import lisample, set_status, get_status

bp = Blueprint(myname, __name__, url_prefix='/auth')


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
    """
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        # logged-in user's profile:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

        # logged-in user's samples' details:
        g.samples = get_db().execute(
            'SELECT s.id, author_id, samplename, fabricated, location, previously, description'
            ' FROM sample s JOIN user u ON s.author_id = u.id' # join tables to link (id in user) and (author_id in post) to get username
            ' WHERE u.id = ?'
            ' ORDER BY registered DESC',
            (user_id,)
        ).fetchall()
        g.samples = [dict(s) for s in g.samples]

        # logged-in user's co-authored samples' details:
        g.cosamples = get_db().execute(
            'SELECT s.id, author_id, samplename, fabricated, location, previously, description'
            ' FROM sample s JOIN user u ON s.author_id = u.id' # join tables to link (id in user) and (author_id in post) to get username
            ' WHERE s.co_authors LIKE ?'
            ' ORDER BY registered DESC',
            ('%%%s%%' %g.user['username'],)
        ).fetchall()
        g.cosamples = [dict(x) for x in g.cosamples]

        # Instrument list & details for each DR (PyQUM) platform:
        g.machlist = get_db().execute(
            '''
            SELECT m.codename, connected, category, sequence, system, u.username
            FROM machine m
            INNER JOIN user u ON m.user_id = u.id
            ORDER BY m.id DESC
            '''
        ).fetchall()
        g.machlist = [dict(x) for x in g.machlist]
        g.instlist = [x['codename'].replace('_','-') for x in g.machlist]

        # Appointed sample in each measurement system:
        g.CHAR0_sample = get_db().execute("SELECT q.samplename FROM queue q WHERE q.system='CHAR0'").fetchone()[0]
        g.QPC0_sample = get_db().execute("SELECT q.samplename FROM queue q WHERE q.system='QPC0'").fetchone()[0]
        g.QPC1_sample = get_db().execute("SELECT q.samplename FROM queue q WHERE q.system='QPC1'").fetchone()[0]
        # print(Fore.GREEN + "CHAR0_sample: %s" %g.CHAR0_sample)

        # DR-specific parameters:
        g.DR_platform = int(get_status("WEB")['port']) - 5300
        navbar_colors = ['#ffba26', '#ff2626'] # hex-color-sequence for each DR
        g.base_color = "rgb(%s, %s, %s)" %tuple([int(navbar_colors[g.DR_platform-1].lstrip('#')[i:i+2], 16) for i in (0, 2, 4)]) # convert hex- to rgb-color


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
            return redirect(url_for('index'))

            g.userlist = None
            if user['management'] == "oversee":
                # ALL approved users' credentials:
                g.userlist = get_db().execute(
                    'SELECT u.id, username, measurement, instrument, analysis'
                    ' FROM user u WHERE u.status = ?'
                    ' ORDER BY id DESC',
                    ('approved',)
                ).fetchall()
                g.userlist = [dict(x) for x in g.userlist]
            print(Fore.RED + Back.WHITE + "USER CREDENTIALS: %s" %g.userlist)

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
    return render_template('auth/samples.html', samples=samples, cosamples=cosamples, selected_sample=selected_sample)
@bp.route('/user/samples/register')
def usersamples_register():
    sname = request.args.get('sname')
    dob = request.args.get('dob')
    loc = request.args.get('loc')
    prev = request.args.get('prev')
    description = request.args.get('description')
    db = get_db()
    try:
        db.execute(
            'INSERT INTO sample (author_id, samplename, fabricated, location, previously, description)'
            ' VALUES (?, ?, ?, ?, ?, ?)',
            (g.user['id'], sname, dob, loc, prev, description,)
        )
        db.commit()
        message = "Sample %s added to the database!" %(sname)
    except:
        message = "Check sample registration"
    return jsonify(message=message)
@bp.route('/user/samples/access')
def usersamples_access():
    '''Create people session (cookie) here
    '''
    sname = request.args.get('sname')
    db = get_db()
    try:
        sample_cv = db.execute(
            'SELECT s.id, author_id, samplename, fabricated, location, previously, description, registered, co_authors, history'
            ' FROM sample s JOIN user u ON s.author_id = u.id'
            ' WHERE s.samplename = ?',
            (sname,)
        ).fetchone()
        sample_cv = dict(sample_cv) # convert sqlite3.row into dictionary for this select format

        sample_owner = db.execute('SELECT u.id, username FROM sample s JOIN user u ON s.author_id = u.id WHERE s.samplename = ?',(sname,)).fetchone()['username']
        saved = bool(sname in lisample(sample_owner)) # saved?

        message = "Accessing Sample %s owned by %s" %(sname,sample_owner)
    except:
        # raise # NOTE: please run first measurement test to create USRLOG directory!
        sample_cv = []
        message = "Consult ABC"
    # print('sample cv: %s' %sample_cv)
    return jsonify(sample_cv=sample_cv, message=message, saved=saved)
@bp.route('/user/samples/update')
def usersamples_update():
    sname = request.args.get('sname')
    loc = request.args.get('loc')
    dob = request.args.get('dob')
    description = request.args.get('description')
    coauthors = request.args.get('coauthors')
    prev = request.args.get('prev')
    history = request.args.get('history')
    ownerpassword = request.args.get('ownerpassword')
    db = get_db()
    try:
        sample_owner = db.execute('SELECT u.id, username FROM sample s JOIN user u ON s.author_id = u.id WHERE s.samplename = ?',(sname,)).fetchone()['username']
        people = db.execute('SELECT password FROM user WHERE username = ?', (sample_owner,)).fetchone()
        if check_password_hash(people['password'], ownerpassword):
            db.execute(
                'UPDATE sample SET location = ?, fabricated = ?, description = ?, co_authors = ?, previously = ?, history = ? WHERE samplename = ?',
                (loc, dob, description, coauthors, prev, history, sname,)
            )
            db.commit()
            message = "Sample %s has been successfully updated!" %(sname)
        else:
            message = 'PASSWORD NOT VALID'
    except:
        message = "Check sample parameters"
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
        print(Fore.YELLOW + "%s is managed by %s" %(sname, session['people']))
    except: 
        session['people'] = None
    # LOGGED INTO JSON:
    try: set_status("MSSN", {session['user_name']: dict(sample=sname, queue=get_status("MSSN")[session['user_name']]['queue'])})
    except: set_status("MSSN", {session['user_name']: dict(sample=sname, queue='')})
    return jsonify(sname=get_status("MSSN")[session['user_name']]['sample'])


# Experiment Database Handling:



print(Back.BLUE + Fore.CYAN + myname + ".bp registered!") # leave 2 lines blank before this

