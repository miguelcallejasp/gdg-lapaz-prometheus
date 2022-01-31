from flask import Flask
from flask import render_template, url_for, request, redirect
from prometheus_client import Gauge, Counter
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app
import uuid
import random
from time import sleep
import datetime
import pymongo
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG,
                    format="%(asctime)-15s %(name)s - %(levelname)s - %(message)s")

app = Flask(__name__)

# prometheus metrics

# App Level monitoring
ACTIVE_CASES = Gauge('gdg_active_cases', 'Casos activos')
NEW_CASES = Counter('gdg_new_cases', 'Nuevo caso')
NEW_RECOVERY = Counter('gdg_new_recovery', 'Nuevo recuperado')

# Infrastructure Level monitoring
API_REQUESTS = Counter('api_requests', 'API Requests')
INSERT_LATENCY = Gauge('insert_latency', 'Insert Latency', ['type'])

# Value calculator

active = 0

mongo_client = pymongo.MongoClient("mongodb://mongo:27017")
dbclient = mongo_client.get_database("covid")


# Prometheus Support Functions

def metric_active_up(value):
    global ACTIVE_CASES
    global active
    logging.debug("Agregando caso activo")
    active = active + value
    logging.debug("Gauging set: " + str(active))
    ACTIVE_CASES.set(active)


def metric_active_down(value):
    global ACTIVE_CASES
    global active
    logging.debug("Reduciendo caso activo")
    active = active - value
    ACTIVE_CASES.set(active)


def metric_case():
    global NEW_CASES
    logging.debug("Nuevo caso registrado")
    NEW_CASES.inc()
    NEW_RECOVERY.inc(0)


def metric_recovery():
    global NEW_RECOVERY
    logging.debug("Nuevo recuperado")
    NEW_RECOVERY.inc()
    NEW_CASES.inc(0)


def metric_insert(latency, type):
    global INSERT_LATENCY
    logging.debug("Latency to MongoDB")
    INSERT_LATENCY.labels(type=type).set(latency)



# Flask Apps


def insert_database(case_id_unique, collection_name):
    global dbclient
    # Insert random delay between 0.1 and 2 sec
    sleep(random.random()*2)
    collection = dbclient.get_collection(collection_name)
    collection.insert_one({
        "id_case": str(case_id_unique)
    })


def new_active_case(path):
    # Creating a UUID for the database
    case_id = uuid.uuid1()
    logging.info("Creating UUID for the database: {}".format(case_id))
    # Database Insert Record
    init_timestamp = datetime.datetime.now()
    insert_database(case_id, "new_cases")
    finish_timestamp = datetime.datetime.now()
    delta = finish_timestamp - init_timestamp
    logging.debug("Latency in MongoDB: {}".format(delta))

    metric_insert(delta.total_seconds() * 1000, "new_cases")  # Sending milliseconds precision to metric
    metric_case()
    metric_active_up(1)


def new_recovered_case(path):
    case_id = uuid.uuid1()
    # Database Insert Record
    init_timestamp = datetime.datetime.now()
    insert_database(case_id, "recovered_Cases")
    finish_timestamp = datetime.datetime.now()
    delta = finish_timestamp - init_timestamp
    logging.debug("Latency in MongoDB: {}".format(delta))
    metric_insert(delta.total_seconds() * 1000, "recovered_cases")
    metric_recovery()
    metric_active_down(1)


app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})


@app.route('/api/v1/covid', methods=["POST", "OPTIONS", "GET"])
def contact():
    path = request.path
    if request.method == 'POST':
        if request.form['submit_button'] == 'nuevo_caso':
            logging.debug("Boton de nuevo caso")
            new_active_case(path)
            return render_template('index.html')
        elif request.form['submit_button'] == 'recuperado':
            logging.debug("Boton de recuperado")
            new_recovered_case(path)
            return render_template('index.html')
        else:
            pass  # unknown
    elif request.method == 'GET':
        return render_template('index.html')


@app.route('/api/v2/covid', methods=["POST", "OPTIONS", "GET"])
def contact_v2():
    path = request.path
    if request.method == 'POST':
        if request.form['submit_button'] == 'nuevo_caso':
            logging.debug("Boton de nuevo caso")
            new_active_case(path)
            return render_template('index.html')
        elif request.form['submit_button'] == 'recuperado':
            logging.debug("Boton de recuperado")
            new_recovered_case(path)
            return render_template('index.html')
        else:
            pass  # unknown
    elif request.method == 'GET':
        return render_template('index.html')


if __name__ == '__main__':
    print("GDG Go on!")
    app.run(host='0.0.0.0', port=8080, debug=True)
