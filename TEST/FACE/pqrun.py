from pyqum import create_app
from flaskext.noextref import NoExtRef
from pyqum.instrument.logger import set_status, get_status
import sys

app = create_app()
# Pending: Hiding certain URLs?
noext = NoExtRef(app, safe_domains=['http://qum.phys.sinica.edu.tw:5300/'])

Port = 5300
# Port, DeBuG, RLD = 5300, False, False

def server(mode):
	app.secret_key = "bcsjfhksP_*$3#bcjahfqaOgvGFGhnNg"
	if mode == "local":
		# for local access
		set_status("LOCAL",dict(mode=mode))
		app.run(host='127.0.0.1', port=Port, debug=True, use_reloader=True) #http://localhost:<port#>
	elif mode == "development":
		# for web access across internet, off reloader if go official
		set_status("WEB",dict(mode=mode))
		app.run(host='0.0.0.0', port=Port, debug=True, use_reloader=True) #, ssl_context='adhoc') #http://<Public IP>:<port#>
	elif mode == "production":
		# for web access across internet, off reloader if go official
		set_status("WEB",dict(mode=mode))
		app.run(host='0.0.0.0', port=Port, debug=True, use_reloader=False) #, ssl_context='adhoc') #http://<Public IP>:<port#>
	
if __name__ == "__main__":
	server(sys.argv[1])

