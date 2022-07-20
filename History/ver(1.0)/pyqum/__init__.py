# Main Engine for the whole APP
import os, sqlite3, click
from flask import Flask, current_app, g
from flask.cli import with_appcontext

from colorama import init, Back, Fore
init(autoreset=True) #to convert termcolor to wins color

from pathlib import Path
pyfilename = Path(__file__).resolve() # current pyscript filename (usually with path)
DB_PATH = Path(pyfilename).parents[6] / "HODOR" / "CONFIG"

# For Database
def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    # print("Accessing Database from:\n %s" %current_app.config['DATABASE'])
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Clear existing data and create new tables."""
    db = get_db()
    with current_app.open_resource('authschema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


# For Streaming
def stream_template(template_name, **context):
    app = Flask(__name__, instance_relative_config=True)
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    # rv.enable_buffering(2)
    return rv


# equivalent to app.py
def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True,instance_path=DB_PATH)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='good',
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, 'pyqum.sqlite'),
    )
    
    if test_config is None:
            # load the instance config, if it exists, when not testing
            app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path) #leave it as empty instance
    # except OSError:
    #     pass

    # register the database commands
    init_app(app)

    # Register Blueprints
    print(Back.WHITE + Fore.BLACK + "Registering Blueprints...")
    from pyqum import auth, blog, display, bridge, machine, guide, mission
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(display.bp)
    app.register_blueprint(bridge.bp)
    app.register_blueprint(machine.bp)
    app.register_blueprint(mission.bp)
    app.register_blueprint(guide.bp)

    # Manage Program exit
    from atexit import register
    def cleaRAM():
        import gc
        gc.collect()
        return
    register(cleaRAM)

    # make url_for('index') == url_for('blog.index')
    app.add_url_rule('/', endpoint='index')

    print(Back.GREEN + Fore.LIGHTYELLOW_EX + "Starting PYQUM:")
    
    # open default browser on startup
    import webbrowser
    # webbrowser.open("http://127.0.0.1:5200/", new=2)

    # disable process log
    # import logging
    # log = logging.getLogger('werkzeug')
    # log.disabled = True
    # app.logger.disabled = True

    return app
