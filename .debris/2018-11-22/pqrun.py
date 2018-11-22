from pyqum import create_app

app = create_app()
# app.run(host='127.0.0.1', port=5200, debug=False, use_reloader=False)
app.run(host='0.0.0.0', port=5200, debug=True, use_reloader=False)
