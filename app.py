from flask import Flask
from flask import render_template, url_for, request, redirect
from prometheus_client import Gauge, Counter
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format="%(asctime)-15s %(name)s - %(levelname)s - %(message)s")

app = Flask(__name__)

# prometheus metrics

ACTIVE_CASES = Gauge('gdg_active_cases', 'Casos activos')
NEW_CASES = Counter('gdg_new_cases', 'Nuevo caso')
NEW_RECOVERY = Counter('gdg_new_recovery', 'Nuevo recuperado')

# Value calculator

active = 0

def active_up(value):
    global ACTIVE_CASES
    global active
    logging.debug("Agregando caso activo")
    active = active + value
    logging.debug("Gauging set: "+str(active))
    ACTIVE_CASES.set(active)

def active_down(value):
    global ACTIVE_CASES
    global active
    logging.debug("Reduciendo caso activo")
    active = active - value
    ACTIVE_CASES.set(active)

def case():
    global NEW_CASES
    logging.debug("Nuevo caso registrado")
    NEW_CASES.inc()
    NEW_RECOVERY.inc(0)

def recovery():
    global NEW_RECOVERY
    logging.debug("Nuevo recuperado")
    NEW_RECOVERY.inc()
    NEW_CASES.inc(0)

app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

@app.route('/api/covid', methods=["POST","OPTIONS","GET"])
def contact():
    if request.method == 'POST':
        if request.form['submit_button'] == 'nuevo_caso':
            logging.debug("Boton de nuevo caso")
            case()
            active_up(1)
            return render_template('index.html')
        elif request.form['submit_button'] == 'recuperado':
            logging.debug("Boton de recuperado")
            recovery()
            active_down(1)
            return render_template('index.html')
        else:
            pass # unknown
    elif request.method == 'GET':
        return render_template('index.html')

if __name__ == '__main__':
    print("GDG Go on!")
    app.run(host='127.0.0.1', port=8080, debug=True)
