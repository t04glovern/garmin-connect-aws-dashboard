FROM grafana/grafana:10.1.4

ADD ./grafana.ini /etc/grafana
ADD ./dashboards /var/lib/grafana/dashboards
ADD ./provisioning /etc/grafana/provisioning

ENTRYPOINT [ "/run.sh" ]