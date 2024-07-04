In this module, you'll learn how to get and change the active span in the context so you can create new branches of spans in your traces.

By the end of this section, you’ll be able to get the active span from the context and make a completely new span in a new context

### Prerequisites

This module assumes that you've completed the previous module on autoinstrumentation.

### Steps:

1. First we’ll start by getting the current context. The current context is stored globally and spans are automatically added to this context by the OpenTelemtry Python API. Add the following import to `server.py`:

```python
from opentelemetry import context
```

2. Next, add the following code to the `create_picture` method:

```python
    # Get the current context
    ctx = context.get_current()
```

If no context is active, the context returned will be empty. This likely means that no spans have been started.

Now that we have a handle on the context, we can use that context to start a new span using that context. This means that the newly created span will be a child of the span in the context ctx:

3. Update the import statement to include the following:

```python
from opentelemetry import context, trace
```

4. Next, start a new span in the current context by adding the following code to the `server.py` file after the FlaskInstrumentor is instantiated:

```python
FlaskInstrumentor().instrument_app(app)
tracer = trace.get_tracer(__name__)
```

Then, in the `create_picture` method, add the following code to start a new span in the current context:

```python
span = tracer.start_span("create_picture", context=ctx)
span.end()
```

5. Next, we'll set a span in the context. This will allow us to pass this context around wherever we have operations that are children of the current span. Add the following code to the `create_picture` method:

```python
ctx2 = trace.set_span_in_context(span, context=ctx) # This method returns a new context
child_span = tracer.start_span("child-span", context=ctx2) # We use the new context to start a new span
child_span.end()
```

6. Navigate back to the project root and build the app

```shell
cd ..
./run
```

This code allows us to see a parent-child relationship created between span and child_span that is propagated through the Context API!

Look at the added spans in Honeycomb.
