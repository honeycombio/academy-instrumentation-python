In this module, you'll learn how to add custom spans and start new traces.

Custom spans can be used to capture details about a specific function or method, or to measure the performance of a specific operation within a function or method.

Starting a new trace is useful when you want to capture details about operations that span multiple functions or methods.

### Prerequisites

This module assumes that you've completed the previous module on context.

### Steps:

1. Add the following code to the `create_picture` method at the start of the method:

```python
# Create a new span with the name 'create_picture' and set attributes
with tracer.start_as_current_span("custom_span_name") as span:
    # Fetch data from phrase-picker and image-picker services asynchronously
    phrase_response = fetch_from_service('phrase-picker')
```

This code creates a new span with the name `custom_span_name` and sets it as the current span. The span is closed when the `with` block exits.

2. Let's set some span attributes. Update the `create_picture` method with the following code:

```python
image_result = image_response.json() if phrase_response and image_response.ok else {"imageUrl": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Banana-Single.jpg/1360px-Banana-Single.jpg"}
span.set_attribute("phrase_result", phrase_result.get("phrase"))
span.set_attribute("image_result", image_result.get("imageUrl"))
```

3. Navigate back to the project root and build the app

```shell
cd ..
./run
```

Look at the added custom span in Honeycomb.

4. Next, let's start a new trace. Update the `create_picture` method with the following code:

```python
# Create a new span with an empty context to start a new trace
with tracer.start_as_current_span("new_trace", context=context.Context()) as new_trace:
    # Make a request to the meminator service
    body = {**phrase_result, **image_result}
    # Start a new span for the meminator fetch operation
    new_trace_span = tracer.start_span("meminator_fetch", context=context.get_current())
    meminator_response = fetch_from_service('meminator', method="POST", body=body)
    new_trace_span.end()
    time.sleep(3)
    new_trace_span.set_attribute("meminator_response_status", meminator_response.status_code)
```

5. Navigate back to the project root and build the app

```shell
cd ..
./run
```

Look at the new trace and the new span in Honeycomb.
