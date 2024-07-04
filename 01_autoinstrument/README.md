## Module 1: Autoinstrumentation

### Prerequisites:

> 🔖 This step assumes that you have a Honeycomb API Key. If you don't have one, you can sign up for a free account at [Honeycomb](https://ui.honeycomb.io/signup) and follow the directions [here](https://docs.honeycomb.io/get-started/configure/environments/manage-api-keys/#create-api-key) to get an API key.

In the project root directory, copy the `example.env` file to a new file called `.env` and update the following:

```shell
HONEYCOMB_API_KEY=<ADD_YOUR_API_KEY>
OTEL_TRACES_EXPORTER=otlp
OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf
SERVICE_PATH="services"
```

We are going to add autoinstrumentation for the backend-for-frontend-python service for the Meminator app.

### Steps:

To add autoinstrumentation follow the steps below:

1. Spin up and activate a python virtualenv: `python3 -m venv .venv && source ./.venv/bin/activate`
2. Install the required packages: `pip install -r requirements.txt`
3. Install the packages required for Opentelemetry:

```shell
pip install opentelemetry-distro \
 opentelemetry-exporter-otlp-proto-http

# Install instrumentation libraries specific to our application
opentelemetry-bootstrap -a install

# Add the requirements to the requirements.txt file
pip freeze -l > requirements.txt
```

4. Modify `server.py` to include the following import:

```python
from opentelemetry.instrumentation.flask import FlaskInstrumentor
```

Then add the instrumentor to the app after instantiating the WSGI app:

```python
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
```

5. Modify the command to run the app in the Dockerfile:

```Dockerfile
CMD ["opentelemetry-instrument", "flask", "run", "-p 10114", "--host=0.0.0.0"]
```

6. Navigate back to the project root and build the app

```shell
cd ..
./run
```
