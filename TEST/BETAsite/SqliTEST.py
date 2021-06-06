import os, sqlite3

from pathlib import Path
pyfilename = Path(__file__).resolve() # current pyscript filename (usually with path)
DB_PATH = Path(pyfilename).parents[5] / "HODOR" / "CONFIG" # "BETAsite" is 1 floor higher than "pyqum"
SETTINGS = os.path.join(DB_PATH, 'settings.sqlite')
print("SETTINGS DATABASE location: %s" %SETTINGS)

from pyqum.instrument.logger import get_status
DR_platform = int(get_status("WEB")['port']) - 5300
print("Current DR: %s" %DR_platform)

db = sqlite3.connect(SETTINGS, detect_types=sqlite3.PARSE_DECLTYPES)
db.row_factory = sqlite3.Row

# Instrument-Pack for certain queue:
inst_pack = db.execute(
    'SELECT i.id, designation, category '
    'FROM instrument i '
    'WHERE i.DR = ? AND i.queue = ? '
    'ORDER BY id DESC',
    (DR_platform,'CHAR0',)
).fetchall()
inst_pack = [dict(x) for x in inst_pack]
print(inst_pack)

db.close()
