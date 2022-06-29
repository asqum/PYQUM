from pyqum import create_app
from flaskext.noextref import NoExtRef
import sys

app = create_app()
# Pending: Hiding certain URLs?
noext = NoExtRef(app, safe_domains=['http://qum.phys.sinica.edu.tw:5300/'])

Port, DeBuG, RLD = 5300, True, True
# Port, DeBuG, RLD = 5300, False, False

def server(mode):
	app.secret_key = "bcsjfhksP_*$3#bcjahfqaOgvGFGhnNg"
	if mode == "local":
		# for local access
		app.run(host='127.0.0.1', port=Port, debug=DeBuG, use_reloader=RLD) #http://localhost:<port#>
	elif mode == "web":
		# for web access across internet, off reloader if go official
		app.run(host='0.0.0.0', port=Port, debug=DeBuG, use_reloader=RLD) #, ssl_context='adhoc') #http://<Public IP>:<port#>
	
if __name__ == "__main__":
	server(sys.argv[1])

