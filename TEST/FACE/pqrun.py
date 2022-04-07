# from flask import g
from pyqum import create_app
#from flaskext.noextref import NoExtRef
from pyqum.instrument.logger import set_status, get_status
import sys

app = create_app()

def server(mode, Port):
	# g.servermode = mode # Working outside of application context.
	set_status("WEB", dict(port=Port, mode=mode), 1)
	app.secret_key = "bcsjfhksP_*$3#bcjahfqaOgvGFGhnNg"
	print(mode)
	if mode == "local":
		# for local access
		set_status("LOCAL",dict(mode=mode))
		app.run(host='127.0.0.1', port=Port, debug=True, use_reloader=True, threaded=True) #http://localhost:<port#>
	elif mode == "development":
		# for web access across internet, off reloader if go official
		set_status("WEB",dict(mode=mode))
		app.run(host='192.168.1.7', port=Port, debug=True, use_reloader=True, threaded=True) #, ssl_context='adhoc') #http://<Public IP>:<port#>
	elif mode == "production":
		# for web access across internet, off reloader if go official
		set_status("WEB",dict(mode=mode))
		app.run(host='0.0.0.0', port=Port, debug=True, use_reloader=False, threaded=True) #, ssl_context='adhoc') #http://<Public IP>:<port#>
	
if __name__ == "__main__":
	server(sys.argv[1], sys.argv[2])

