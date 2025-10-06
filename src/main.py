import base64
import logging
import os
from functools import wraps

import magic
from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
from google.cloud import storage
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Attachment,
    Content,
    Disposition,
    FileContent,
    FileName,
    FileType,
    Mail,
)

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://tronify-me-714656958210.us-central1.run.app"}})

PROJECT_ID = os.environ.get("PROJECT_ID")
BUCKET_NAME = os.environ.get("BUCKET_NAME")
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
API_KEY = os.environ.get("API_KEY")

gcs_client = storage.Client()
sendgrid_client = SendGridAPIClient(SENDGRID_API_KEY)


def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.headers.get("X-API-KEY") != API_KEY:
            return "Unauthorized", 401
        return f(*args, **kwargs)

    return decorated_function


@app.route("/", methods=["GET"])
def heartbeat():
    """Heartbeat endpoint to check if the service is alive.""" 
    return "OK", 200


@app.route("/upload", methods=["POST"])
@require_api_key
def upload_picture():
    """
    Handles picture uploads to Google Cloud Storage.

    The request payload should be a JSON object with the following keys:
    - "image": The base64-encoded image content.
    - "name": The name of the image file.
    """
    try:
        data = request.get_json()
        image_content = base64.b64decode(data["image"])
        image_name = data["name"]

        # Check if the file is an image
        mime_type = magic.from_buffer(image_content, mime=True)
        if not mime_type.startswith("image/"):
            return "Invalid file type. Only images are allowed.", 400

        bucket = gcs_client.get_bucket(BUCKET_NAME)
        blob = bucket.blob(image_name)
        blob.upload_from_string(image_content)

        return "Picture uploaded successfully", 201
    except Exception as e:
        logging.error(f"Error uploading picture: {e}")
        return "Error uploading picture", 500


@app.route("/email", methods=["POST"])
@require_api_key
def email_picture():
    """
    Sends an email with a picture attachment.

    The request payload should be a JSON object with the following keys:
    - "email": The recipient's email address.
    - "name": The name of the picture file to attach.
    """
    try:
        data = request.get_json()
        recipient_email = data["email"]
        image_name = data["name"]

        bucket = gcs_client.get_bucket(BUCKET_NAME)
        blob = bucket.blob(image_name)

        if not blob.exists():
            return "Picture not found", 404

        image_content = blob.download_as_bytes()
        encoded_content = base64.b64encode(image_content).decode()

        message = Mail(
            from_email=SENDER_EMAIL,
            to_emails=recipient_email,
            subject="Thanks for visiting our booth!",
            html_content=Content(
                "text/html",
                "<p>Thank you for visiting Google Cloud's booth at the "
                "conference! The entire experience was coded with AI Studio, "
                "Gemini CLI and Jules.</p>"
                "<p>We'd love for you to try out these technologies yourself. "
                "Get started with free Google Cloud credits (no credit card "
                "required) by visiting: "
                '<a href="https://trygcp.dev/dvxx-be-25">'
                "trygcp.dev/dvxx-be-25</a></p>",
            ),
        )
        attachment = Attachment(
            FileContent(encoded_content),
            FileName(image_name),
            FileType("image/jpeg"),
            Disposition("attachment"),
        )
        message.attachment = attachment

        sendgrid_client.send(message)

        return "Email sent successfully", 200
    except Exception as e:
        logging.error(f"Error sending email: {e}")
        return "Error sending email", 500


@app.route("/status", methods=["GET"])
def status():
    """
    Returns the status of the service, including the bucket URL and the
    number of pictures in the bucket.
    """
    try:
        bucket = gcs_client.get_bucket(BUCKET_NAME)
        blobs = list(bucket.list_blobs())
        num_pictures = len(blobs)
        bucket_url = f"https://console.cloud.google.com/storage/browser/{BUCKET_NAME}"

        return {
            "bucket_url": bucket_url,
            "num_pictures": num_pictures,
        }, 200
    except Exception as e:
        logging.error(f"Error getting status: {e}")
        return "Error getting status", 500