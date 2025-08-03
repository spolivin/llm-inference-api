# Monitoring system

## Metrics

The state of the system is configured to be monitored via numerous *Prometheus* metrics in [*Grafana* dashboard](../dashboard.json). Such metrics include:

1. Number of successful generations (Code 200 OK)

2. Number of successful downloads of generated files (Code 200 OK)

3. Number of unsuccessful generations (Code 4xx)

4. Number of unsuccessful generations (Code 5xx)

5. Number of unsuccessful downloads (Code 4xx)

6. RAM Usage by API

7. CPU Usage by API

8. Change in HTTP request duration (generation)

9. Change in HTTP request duration (metrics scrapping)

## Loading the dashboard to *Grafana*

Dashboard saved in [`dashboard.json`](../dashboard.json) already includes the implementation of the above metrics for easy re-use during first launch. One needs to do the following steps after services launch:

1. Go to Grafana Web UI and get authorized using new configured username and password from `.env`.
2. Specify *Prometheus* in *Data sources* with `http://prometheus:9090` address.
3. Run `python fix_datasource_uid.py` from the root directory in order to change the UID for the current Grafana session and loading the dashboard.
4. Go to *Dashboards* in Grafana and go to *New -> Import*. One now needs to simply copy and paste the contents of [`dashboard.json`](../dashboard.json) and entering *Load*.
