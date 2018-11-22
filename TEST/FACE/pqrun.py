from pyqum import create_app

app = create_app()

# for local access
# app.run(host='127.0.0.1', port=5200, debug=False, use_reloader=False)

# for web access across internet, off reloader if go official
app.run(host='0.0.0.0', port=5200, debug=True, use_reloader=True)
