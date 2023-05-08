# Adding Telemetry to OpenAI's ChatCompletion

```python
# Instrument the OpenAI API
OpenAICompletionInstrumentor().instrument()

# Use the OpenAI API
def call(prompt):
    # get the current span 
    span = trace.get_current_span()
    span.set_attribute("openai.prompt", prompt)
    response = openai.ChatCompletion.create(
        model= "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=500,
        temperature=0.5,
    )
    span.set_attribute("openai.response", response["choices"][0]["message"]["content"])
    


with trace.get_tracer_provider().get_tracer(__name__).start_as_current_span("main"):
    call("What is the meaning of life in a short sentence?")
    call("What is the meaning of death in a long paragraph?")
```

We get some data that looks like this:

```json
{
    "name": "HTTP POST",
    "context": {
        "trace_id": "0x4f30f3348f14cca1c9473b5a2ea813de",
        "span_id": "0xa7c761add82b78c4",
        "trace_state": "[]"
    },
    "kind": "SpanKind.CLIENT",
    "parent_id": "0x236e1b0054104fe2",
    "start_time": "2023-05-07T02:06:41.472934Z",
    "end_time": "2023-05-07T02:06:42.522350Z",
    "status": {
        "status_code": "UNSET"
    },
    "attributes": {
        "http.method": "POST",
        "http.url": "https://api.openai.com/v1/chat/completions",
        "http.status_code": 200
    },
    "events": [],
    "links": [],
    "resource": {
        "attributes": {
            "telemetry.sdk.language": "python",
            "telemetry.sdk.name": "opentelemetry",
            "telemetry.sdk.version": "1.17.0",
            "service.name": "unknown_service"
        },
        "schema_url": ""
    }
}
{
    "name": "openai.ChatCompletion.create",
    "context": {
        "trace_id": "0x4f30f3348f14cca1c9473b5a2ea813de",
        "span_id": "0x236e1b0054104fe2",
        "trace_state": "[]"
    },
    "kind": "SpanKind.CLIENT",
    "parent_id": "0x104c76efec92b98b",
    "start_time": "2023-05-07T02:06:41.438489Z",
    "end_time": "2023-05-07T02:06:42.524253Z",
    "status": {
        "status_code": "UNSET"
    },
    "attributes": {
        "openai.create.model": "gpt-3.5-turbo",
        "openai.create.max_tokens": 500,
        "openai.create.temperature": 0.5,
        "openai.response.id": "chatcmpl-7DO5Jns0IVgSxWRjTaBUHL0VWPtyK",
        "openai.response.created": 1683425201,
        "openai.usage.prompt_tokens": 30,
        "openai.usage.completion_tokens": 13,
        "openai.usage.total_tokens": 43
    },
    "events": [],
    "links": [],
    "resource": {
        "attributes": {
            "telemetry.sdk.language": "python",
            "telemetry.sdk.name": "opentelemetry",
            "telemetry.sdk.version": "1.17.0",
            "service.name": "unknown_service"
        },
        "schema_url": ""
    }
}
{
    "name": "HTTP POST",
    "context": {
        "trace_id": "0x4f30f3348f14cca1c9473b5a2ea813de",
        "span_id": "0xbc74d9bcf2b194c2",
        "trace_state": "[]"
    },
    "kind": "SpanKind.CLIENT",
    "parent_id": "0xa33fc3e93fb9f06d",
    "start_time": "2023-05-07T02:06:42.526738Z",
    "end_time": "2023-05-07T02:06:52.524112Z",
    "status": {
        "status_code": "UNSET"
    },
    "attributes": {
        "http.method": "POST",
        "http.url": "https://api.openai.com/v1/chat/completions",
        "http.status_code": 200
    },
    "events": [],
    "links": [],
    "resource": {
        "attributes": {
            "telemetry.sdk.language": "python",
            "telemetry.sdk.name": "opentelemetry",
            "telemetry.sdk.version": "1.17.0",
            "service.name": "unknown_service"
        },
        "schema_url": ""
    }
}
{
    "name": "openai.ChatCompletion.create",
    "context": {
        "trace_id": "0x4f30f3348f14cca1c9473b5a2ea813de",
        "span_id": "0xa33fc3e93fb9f06d",
        "trace_state": "[]"
    },
    "kind": "SpanKind.CLIENT",
    "parent_id": "0x104c76efec92b98b",
    "start_time": "2023-05-07T02:06:42.524772Z",
    "end_time": "2023-05-07T02:06:52.524828Z",
    "status": {
        "status_code": "UNSET"
    },
    "attributes": {
        "openai.create.model": "gpt-3.5-turbo",
        "openai.create.max_tokens": 500,
        "openai.create.temperature": 0.5,
        "openai.response.id": "chatcmpl-7DO5K8rhgWHrHEpsLizRdNa9QkzkG",
        "openai.response.created": 1683425202,
        "openai.usage.prompt_tokens": 30,
        "openai.usage.completion_tokens": 175,
        "openai.usage.total_tokens": 205
    },
    "events": [],
    "links": [],
    "resource": {
        "attributes": {
            "telemetry.sdk.language": "python",
            "telemetry.sdk.name": "opentelemetry",
            "telemetry.sdk.version": "1.17.0",
            "service.name": "unknown_service"
        },
        "schema_url": ""
    }
}
{
    "name": "main",
    "context": {
        "trace_id": "0x4f30f3348f14cca1c9473b5a2ea813de",
        "span_id": "0x104c76efec92b98b",
        "trace_state": "[]"
    },
    "kind": "SpanKind.INTERNAL",
    "parent_id": null,
    "start_time": "2023-05-07T02:06:41.438400Z",
    "end_time": "2023-05-07T02:06:52.525255Z",
    "status": {
        "status_code": "UNSET"
    },
    "attributes": {
        "openai.prompt": "What is the meaning of death in a long paragraph?",
        "openai.response": "Death is the cessation of life. It is the final stage of life where the physical body ceases to function. Death is a natural process that occurs to all living beings, and it is an inevitable part of life. The meaning of death can vary depending on one's beliefs and cultural background. Some view death as a transition to an afterlife, while others see it as the end of existence. Death can also be seen as a release from suffering and pain, or as a tragedy that leaves loved ones behind. The meaning of death can be complex and emotional, and it is often accompanied by grief and mourning. It is a reminder of the fragility of life and the importance of cherishing the time we have with loved ones. Ultimately, the meaning of death is subjective and personal, and it is up to each individual to make sense of it in their own way."
    },
    "events": [],
    "links": [],
    "resource": {
        "attributes": {
            "telemetry.sdk.language": "python",
            "telemetry.sdk.name": "opentelemetry",
            "telemetry.sdk.version": "1.17.0",
            "service.name": "unknown_service"
        },
        "schema_url": ""
    }
}
```