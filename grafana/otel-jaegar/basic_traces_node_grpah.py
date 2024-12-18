from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Define the service name
resource = Resource.create({"service.name": "node_graph_trace"})

# Configure the TracerProvider with the service name
trace.set_tracer_provider(TracerProvider(resource=resource))
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

# Create a tracer
tracer = trace.get_tracer(__name__)

# Start a root span
with tracer.start_as_current_span("root") as root_span:
    root_span.set_attribute("operation", "root_operation")
    
    # Node A
    with tracer.start_as_current_span("node_a") as span_a:
        span_a.set_attribute("operation", "operation_a")
        
        # Node B (child of Node A)
        with tracer.start_as_current_span("node_b") as span_b:
            span_b.set_attribute("operation", "operation_b")
            print("Node B operation")

        # Node C (child of Node A)
        with tracer.start_as_current_span("node_c") as span_c:
            span_c.set_attribute("operation", "operation_c")
            print("Node C operation")
    
    # Node D (child of root)
    with tracer.start_as_current_span("node_d") as span_d:
        span_d.set_attribute("operation", "operation_d")
        print("Node D operation")

print("Tracing complete!")
