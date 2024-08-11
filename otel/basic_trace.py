from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Define the service name
resource = Resource.create({"service.name": "basic_trace"})

# Configure the TracerProvider with the service name
trace.set_tracer_provider(TracerProvider(resource=resource))
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

# Create a tracer
tracer = trace.get_tracer(__name__)

# Start a span
with tracer.start_as_current_span("foo") as roll_span:
    roll_span.set_attribute("roll.value", "Hello world!")
    print("Hello world!")
