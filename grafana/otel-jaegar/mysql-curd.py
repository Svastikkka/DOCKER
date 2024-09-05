import mysql.connector
from mysql.connector import Error
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# Define the service name
resource = Resource.create({"service.name": "mysql-curd"})

# Configure the TracerProvider with the service name
trace.set_tracer_provider(TracerProvider(resource=resource))
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")
trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

# Create a tracer
tracer = trace.get_tracer(__name__)

# MySQL connection configuration
mysql_config = {
    'host': 'localhost',
    'port': 13306,
    'database': 'mydb',
    'user': 'mysqluser',
    'password': 'mysqlpw'
}

def connect_db():
    try:
        connection = mysql.connector.connect(**mysql_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                salary DECIMAL(10, 2) NOT NULL
            )
        """)
        connection.commit()
        print("Table created successfully.")
    except Error as e:
        print(f"Error: {e}")
        connection.rollback()

def insert_employee(connection, name, salary):
    with tracer.start_as_current_span("insert_employee") as span:
        span.set_attribute("employee.name", name)
        span.set_attribute("employee.salary", salary)
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO employees (name, salary) VALUES (%s, %s)", (name, salary))
            connection.commit()
            print("Employee inserted successfully.")
        except Error as e:
            print(f"Error: {e}")
            connection.rollback()

def read_employees(connection):
    with tracer.start_as_current_span("read_employees") as span:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM employees")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except Error as e:
            print(f"Error: {e}")

def update_employee_salary(connection, employee_id, salary):
    with tracer.start_as_current_span("update_employee_salary") as span:
        span.set_attribute("employee.id", employee_id)
        span.set_attribute("employee.new_salary", salary)
        try:
            cursor = connection.cursor()
            cursor.execute("UPDATE employees SET salary = %s WHERE id = %s", (salary, employee_id))
            connection.commit()
            print("Employee salary updated successfully.")
        except Error as e:
            print(f"Error: {e}")
            connection.rollback()

def delete_employee(connection, employee_id):
    with tracer.start_as_current_span("delete_employee") as span:
        span.set_attribute("employee.id", employee_id)
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
            connection.commit()
            print("Employee deleted successfully.")
        except Error as e:
            print(f"Error: {e}")
            connection.rollback()

def main():
    connection = connect_db()
    if connection:
        create_table(connection)
        insert_employee(connection, 'John Doe', 50000)
        read_employees(connection)
        update_employee_salary(connection, 1, 55000)
        delete_employee(connection, 1)
        connection.close()

if __name__ == "__main__":
    main()
