[![Actions Status](https://github.com/miguelcallejasp/gdg-lapaz-prometheus/workflows/build/badge.svg)](https://github.com/miguelcallejasp/gdg-lapaz-prometheus/actions)


# Prometheus 101

Repository of the material needed for the Crash Course Prometheus 101.
The app is a simple counter for active and recovered cases for COVID. A single click will add a case and another will decrease the case count.

## Prometheus Metrics
The following metrics are available at the endpoint: `http://localhost:8080/metrics`

|Metric Type|Metric|Description|
|---|---|---|
|`COUNTER`|`new_cases_total`|This is a counter for new cases. It only goes up.|
|`COUNTER`|`new_recovery_total`|This is a counter for a new recovery case. It only goes up.|
|`GAUGE`|`active_cases`| This is a gauge value. It goes up or down depending on the action.|

## Metrics Example
This is how the metrics would look like:

```
# HELP gdg_active_cases Casos activos
# TYPE gdg_active_cases gauge
active_cases 1.0

# HELP gdg_new_cases_total Nuevo caso
# TYPE gdg_new_cases_total counter
new_cases_total 9.0

# HELP gdg_new_recovery_total Nuevo recuperado
# TYPE gdg_new_recovery_total counter
new_recovery_total 8.0

```

### Prometheus Query Examples
The following queries can be done over Prometheus.

|Prometheus Query|Description|
|---|---|
|`rate(new_cases_total{}[1m])`| The rate in which new cases are happening|
|`rate(new_recovery_total{}[1m])`| The rate in which new cases are happening|
|`active_cases`| The total number of active cases.|
|`new_recovery_total{}/new_cases_total{} * 100` | Ratio of incidents|

### Content
The repository has:
- Small Flask application that returns a site with 2 buttons.
- Flask module for Prometheus client.
- Docker container for the app itself.
- Docker container for Prometheus and Grafana.

## Configuration
Create the docker containers to start the application using:

```
docker-compose up -d
```

The command will build a new container with the current code. This will enable a site at `http://localhost:8080/api/covid`.

### Make it public

`ngrok http 8080`

## Examples

![Website Example](https://storage.googleapis.com/mojix-devops-wildfire-bucket/images/prom101_site.png)

![Grafana](https://storage.googleapis.com/mojix-devops-wildfire-bucket/images/grafana_prom101.png)
