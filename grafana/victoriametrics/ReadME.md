Following Datasource add

Loki
  - url: http://loki2:3200/loki/api/v1/push
  - url: http://loki1:3100/loki/api/v1/push


VM/Prometheus
- victoria-metrics1:8428
- victoria-metrics1:8428


Install OnPremise
- VictoriaMetrics
    - Link: https://docs.victoriametrics.com/single-server-victoriametrics/
    - Release: https://github.com/VictoriaMetrics/VictoriaMetrics/releases/tag/v1.104.0
