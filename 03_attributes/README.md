In this module, you'll learn how to add attributes to spans.

Attributes are key-value pairs that provide context to the span. Attributes can be used to filter and group spans in the Honeycomb UI.

### Prerequisites

This module assumes that you've completed the previous module on context.

### Steps:

1. Add the following code to the `create_picture` method after `phrase_result` and `image_result` are created:

```python
span.set_attribute("phrase_result", phrase_result.get("phrase")) # Add an attribute to the span
span.set_attribute("image_result", image_result.get("imageUrl")) # Add another attribute to the span
span.end()
```

2. Navigate back to the project root and build the app

```shell
cd ..
./run
```

Look at the added span attributes in Honeycomb.
