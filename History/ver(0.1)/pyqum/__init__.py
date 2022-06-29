# This __init__ represent namespace's main body, which is "pyqum" in this case

import os
from flask import Flask

from colorama import init
init(autoreset=True) #to convert termcolor to wins color

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
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY='dev',
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
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    from pyqum import db
    db.init_app(app)

    # apply the blueprints to the app
    from pyqum import auth, blog, awgonly, combo
    print("Registering Blueprints...")
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(awgonly.bp)
    app.register_blueprint(combo.bp)

    # make url_for('index') == url_for('blog.index')
    app.add_url_rule('/', endpoint='index')

    return app

# TEST GLOBAL
