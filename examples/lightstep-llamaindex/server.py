#!/usr/bin/env python3

import os
from flask import Flask, request
import openai
from opentelemetry.launcher import configure_opentelemetry

from llamatry import Trace, OpenAIInstrumentor

from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader
from llama_index import StorageContext, load_index_from_storage


PORT = 8000
app = Flask(__name__)

configure_opentelemetry(
    service_version="0.1.0",
    log_level="DEBUG",  # optional
    propagators="baggage,tracecontext",
)

openai.api_key = os.environ["OPENAI_API_KEY"]

# rebuild storage context
if os.path.exists("./storage"):
    with Trace.span("StorageContext.from_defaults"):
        storage_context = StorageContext.from_defaults(persist_dir="./storage")
        index = load_index_from_storage(storage_context)
else:
    documents = SimpleDirectoryReader("data").load_data()
    index = GPTVectorStoreIndex.from_documents(documents)
    index.storage_context.persist()

with Trace.span("index.as_query_engine"):
    query_engine = index.as_query_engine()


@app.route("/ask", methods=["POST"])
def ask():
    query = request.get_json()["query"]
    response = query_engine.query(query)
    return {"content": str(response)}


OpenAIInstrumentor().instrument()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
