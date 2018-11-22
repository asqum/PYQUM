from pyqum import create_app
import sys

app = create_app()

def server(mode):
    if mode == "local":
        # for local access
        app.run(host='127.0.0.1', port=5200, debug=False, use_reloader=False)
    elif mode == "web":
        # for web access across internet, off reloader if go official
        app.run(host='0.0.0.0', port=5200, debug=True, use_reloader=True)

if __name__ == "__main__":
    server(sys.argv[1])
    