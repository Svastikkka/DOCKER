# Requirments
- `opentelemetry-api`: Provides the interfaces for integrating tracing and metrics into your code.
- `opentelemetry-sdk`: Implements the functionality to collect and manage traces and metrics.
- `opentelemetry-exporter-otlp-proto-http`: Sends telemetry data over HTTP in Protobuf format to an OTLP-compatible backend.
- `opentelemetry-exporter-otlp`: Provides flexible OTLP exporting capabilities using various protocols.
- `opentelemetry-instrumentation-flask`: Automatically instruments Flask applications for tracing.
- `flask`: Framework for building web applications.
- `mysql-connector-python`: Connects and interacts with MySQL databases.


# Can be use in following
- DAGs/Basic Scripts
- NodeJS/Flask/Django
- MYSQL
- Kafka

To download dependecies
```bash 
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
```

```bash
conda activate svastikkka
pip3 install -r requirements.txt
```


# Sample scripts
- To test basic script
```bash
python basic_trace.py
```

- To test on flask app
```bash 
flask run -p 8080
```

- To test on mysql curd operations
```bash 
python mysql-curd.py
```

- To test on kafka
```bash 
python producer.py
```

# Reference
- https://medium.com/jaegertracing/introducing-native-support-for-opentelemetry-in-jaeger-eb661be8183c
- [Getting Started](https://opentelemetry.io/docs/languages/python/getting-started/)