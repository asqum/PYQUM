import os, sqlite3, json

from pathlib import Path
pyfilename = Path(__file__).resolve() # current pyscript filename (usually with path)
CONFIG_PATH = Path(pyfilename).parents[5] / "HODOR" / "CONFIG" # "BETAsite" is 1 floor higher than "pyqum", path_parents+2 in directive
DR_SETTINGS = os.path.join(CONFIG_PATH, 'DR_settings.sqlite')
print("DR_SETTINGS DATABASE location: %s" %DR_SETTINGS)

db = sqlite3.connect(DR_SETTINGS, detect_types=sqlite3.PARSE_DECLTYPES)
db.row_factory = sqlite3.Row

# Instrument-Pack for certain queue:
inst_pack = db.execute(
    '''
    SELECT i.id, designation, configuration FROM instrument i WHERE i.category = ? AND i.queue = ? ORDER BY id DESC
    '''
    ,('DC','CHAR0',)
).fetchall()
inst_pack = [dict(x) for x in inst_pack]
print(inst_pack)
print("DC Sweep Channel: %s" %json.loads(inst_pack[0]['configuration'].replace("'",'"'))['dcsweepch'])

db.close()
