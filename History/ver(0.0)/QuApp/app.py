from flask import Flask
from QuApp.views.index import bp as index_bp
from QuApp.views.characterizations import bp as characterization_bp
from QuApp.views.experiments import bp as experiments_bp
from QuApp.views.calibration import bp as calib_bp
from QuApp.views.schemes import bp as schemes_bp

app = Flask(__name__)

app.register_blueprint(index_bp)
app.register_blueprint(characterization_bp)
app.register_blueprint(experiments_bp)
app.register_blueprint(calib_bp)
app.register_blueprint(schemes_bp)

