#!/usr/bin/env python3

import os
from flask import Flask
import openai
from opentelemetry import trace, baggage
from opentelemetry.launcher import configure_opentelemetry

from llamatry import OpenAICompletionInstrumentor

PORT = 8000
app = Flask(__name__)

configure_opentelemetry(
    service_version="0.1.0",
    log_level="DEBUG",  # optional
    propagators="baggage,tracecontext",
)

openai.api_key = os.environ["OPENAI_API_KEY"]


@app.route("/")
def hello():
    prompt = "What is the meaning of life in a short sentence?"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=50,
        temperature=0.5,
    )
    # add attributes to the span to capture the prompt and response
    # this will be exported to the console but one can imagine this doing into
    # a database or other storage for search or review later
    span = trace.get_current_span()
    span.set_attribute("openai.prompt", prompt)
    span.set_attribute("openai.response", response["choices"][0]["message"]["content"])
    return {"content": response["choices"][0]["message"]["content"]}

OpenAICompletionInstrumentor().instrument()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
