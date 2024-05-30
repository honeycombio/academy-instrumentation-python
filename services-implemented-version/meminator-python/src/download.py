
import os
import uuid
import requests
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

tracer = trace.get_tracer("meminator-tracer")

# uncomment this decoration to launch a new child span
# @tracer.start_as_current_span("do_work")


def download_image(url):
    current_span = trace.get_current_span()

    # Send a GET request to the URL
    current_span.add_event("image_download_start", {"url": url, })
    try:
        response = requests.get(url)
        current_span.add_event("image_download_end",
                               {"url": url,
                                "response_statuscode": response.status_code})
    except Exception as e:
        current_span.add_event("image_download_failed",
                               {"url": url,
                                "response_statuscode": response.status_code,
                                "error": e})
        print("An error occurred:", str(e))
        current_span.set_status(Status(StatusCode.ERROR))
        current_span.record_exception(e)
        return os.path.abspath('tmp/BusinessWitch.png')

    # Open the file in binary mode and write the image content
    filename = generate_random_filename(url)

    current_span.add_event("image_file_write_start", {"filename": filename})
    try:
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Image downloaded successfully and saved as {filename}")
        current_span.add_event("image_file_write_end", {"filename": filename})
        return filename
    except Exception as e:
        current_span.add_event("image_file_write_failed",
                               {"filename": filename,
                                "error": e})
        print("An error occurred:", str(e))
        current_span.set_status(Status(StatusCode.ERROR))
        current_span.record_exception(e)
        return os.path.abspath('tmp/BusinessWitch.png')


def generate_random_filename(input_filename):
    # Extract the extension from the input filename
    extension = get_file_extension(input_filename)

    # Generate a UUID and convert it to a string
    random_uuid = uuid.uuid4()
    # Convert UUID to string and remove dashes
    random_filename = str(random_uuid).replace("-", "")

    # Append the extension to the random filename
    random_filename_with_extension = random_filename + extension

    random_filepath = os.path.join("/tmp", random_filename_with_extension)

    return random_filepath


def get_file_extension(url):
    # Split the URL by "." and get the last part
    parts = url.split(".")
    if len(parts) > 1:
        return "." + parts[-1]
    else:
        return ""
