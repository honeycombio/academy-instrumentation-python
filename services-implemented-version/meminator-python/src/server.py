import os
import subprocess
from flask import Flask, jsonify, send_file, request
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

from download import generate_random_filename, download_image
# from custom_span_processor import CustomSpanProcessor

# Acquire a tracer
tracer = trace.get_tracer("meminator-tracer")

IMAGE_MAX_WIDTH_PX = 1000
IMAGE_MAX_HEIGHT_PX = 1000

app = Flask(__name__)
# Route for health check


@app.route('/health')
def health():
    result = {"message": "I am here", "status_code": 0}
    return jsonify(result)


@app.route('/applyPhraseToPicture', methods=['POST', 'GET'])
def meminate():
    input = request.json or {"phrase": "I got you"}
    request_span = trace.get_current_span()

    phrase = input.get("phrase", "words go here").upper()
    request_span.set_attribute("app.meminate.phrase", phrase)

    imageUrl = input.get("imageUrl", "http://missing.booo/no-url-here.png")
    request_span.set_attribute("app.meminate.imageUrl", imageUrl)

    # Get the absolute path to the PNG file
    input_image_path = download_image(imageUrl)

    # Check if the file exists
    if not os.path.exists(input_image_path):
        request_span.add_event(
            "image_not_found", {
                "input_image_path": input_image_path, "imageUrl": imageUrl})
        request_span.set_status(Status(StatusCode.ERROR))
        return 'downloaded image file not found', 500

    # Define the output image path
    output_image_path = generate_random_filename(input_image_path)

    command = ['convert',
               input_image_path,
               '-resize', f'{IMAGE_MAX_WIDTH_PX}x{IMAGE_MAX_HEIGHT_PX}>',
               '-gravity', 'North',
               '-pointsize', '48',
               '-fill', 'white',
               '-undercolor', '#00000080',
               '-font', 'Angkor-Regular',
               '-annotate', '0', phrase,
               output_image_path]

    request_span.add_event("convert_subprocess_start", {
                           "command": " ".join(command)})

    # Run the command, gracefully catch any errors
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        request_span.add_event("convert_subprocess_end",
                               {"command": " ".join(command),
                                "returncode": result.returncode,
                                "stdout": result.stdout,
                                "stderr": result.stderr})
    except Exception as e:
        request_span.add_event("convert_subprocess_failed",
                               {"command": " ".join(command),
                                "returncode": result.returncode,
                                "stderr": result.stderr,
                                "error": e})
        print("An error occurred:", str(e))
        request_span.set_status(Status(StatusCode.ERROR))
        request_span.record_exception(e)
        return 'An error occurred generating your image, sorry', 500

    # Sub-span version
    # with tracer.start_as_current_span("span-name") as subprocess_span:
        # subprocess_span.set_attribute("app.subprocess.command", " ".join(command))
        # result = subprocess.run(command, capture_output=True, text=True)
        # subprocess_span.set_attribute("app.subprocess.returncode", result.returncode)
        # subprocess_span.set_attribute("app.subprocess.stdout", result.stdout)
        # subprocess_span.set_attribute("app.subprocess.stderr", result.stderr)
        # if result.returncode != 0:
        #     raise Exception("Subprocess failed with return code:", result.returncode)

    # Serve the modified image
    return send_file(
        output_image_path,
        mimetype='image/png'
    )


if __name__ == '__main__':
    app.run(port=10117)
