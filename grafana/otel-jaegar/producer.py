from confluent_kafka import Producer
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# OpenTelemetry Setup
resource = Resource.create({"service.name": "kafka-producer"})
trace.set_tracer_provider(TracerProvider(resource=resource))
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))
tracer = trace.get_tracer(__name__)

# Kafka configuration
kafka_conf = {
    'bootstrap.servers': 'localhost:19092'  # External listener defined in your Docker setup
}

# Create a Kafka Producer
producer = Producer(**kafka_conf)

# Delivery callback to confirm message delivery
def delivery_callback(err, msg):
    if err:
        print(f"Message failed delivery: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")

# Produce 1000 messages
for i in range(1000):
    message = f"Message number {i + 1}"
    
    # Trace each message production
    with tracer.start_as_current_span(f"produce_message_{i + 1}") as span:
        span.set_attribute("kafka.topic", "testing-kafka")
        span.set_attribute("kafka.message", message)
        
        # Send the message
        producer.produce('testing-kafka', value=message, callback=delivery_callback)

# Wait for all messages to be delivered
producer.flush()

print("1000 messages sent to topic 'testing-kafka'")
