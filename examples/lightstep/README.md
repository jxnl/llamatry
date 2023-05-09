# Lightstep Example

Here's an improved example on how to set up and run an example app using Lightstep with OpenTelemetry in Python. For more detailed documentation, visit the Lightstep blog.

## Installation

```bash
pip install -r requirements.txt
opentelemetry-bootstrap -a install
```

Set up your environment variables:

```bash
export FLASK_ENV=development
export LS_SERVICE_NAME=hello-server
export LS_ACCESS_TOKEN=<YOUR_ACCESS_TOKEN>
```

Replace <YOUR_ACCESS_TOKEN> with your actual Lightstep access token.

## Running the Application

Instrument your Python app with OpenTelemetry:

```bash
opentelemetry-instrument python server.py
```

Your application should now be running, and you can view the traces in your Lightstep dashboard.