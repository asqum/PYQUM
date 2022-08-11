from pyqum import create_app

app = create_app()
Port, DeBuG, RLD = 5300, False, False

def server():
    app.secret_key = "bcsjfhksP_*$3#bcjahfqaOgvGFGhnNg"
    # for web access across internet, off reloader if go official
    app.run(host='0.0.0.0', port=Port, debug=DeBuG, use_reloader=RLD) #, ssl_context='adhoc') #http://<Public IP>:<port#>
    
if __name__ == "__main__":
    server()
