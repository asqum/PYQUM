import sys
 
sys.path.insert(0, 'C:/Users/ASQUM/Documents/GitHub/PYQUM/TEST/FACE')
 
from pyqum.apache import server as application

# PENDING: 
If a factory function is used in a __init__.py file, then the function should be imported:

from yourapplication import create_app
application = create_app()
???
##