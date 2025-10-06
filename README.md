# Image Handling Backend Service

This is a backend service for handling image uploads, storage, and email delivery. It is designed to be deployed as a containerized application on Google Cloud Run.

## Project Overview

The service provides a set of API endpoints to:
- Upload images to a Google Cloud Storage bucket.
- Send an email with a stored image as an attachment.
- Check the health of the service.
- Get the status of the image bucket.

This project was coded with the assistance of AI Studio, Gemini CLI, and Jules.

## Features

- **Image Upload**: Persist images by uploading them to a configurable Google Cloud Storage bucket.
- **Email Delivery**: Send emails with image attachments using the SendGrid API.
- **Heartbeat**: A simple endpoint to verify that the service is running.
- **Status Endpoint**: Provides information about the connected Google Cloud Storage bucket, including its URL and the number of images it contains.
- **Containerized**: Ready for deployment using Docker.

## API Documentation

### `GET /`

A heartbeat endpoint to check if the service is operational.

- **Method**: `GET`
- **Success Response**:
  - **Code**: 200 OK
  - **Content**: `"OK"`

---

### `POST /upload`

Uploads an image to the configured Google Cloud Storage bucket.

- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "image": "<base64_encoded_string>",
    "name": "<your_image_name.jpg>"
  }
  ```
- **Success Response**:
  - **Code**: 201 Created
  - **Content**: `"Picture uploaded successfully"`
- **Error Response**:
  - **Code**: 500 Internal Server Error
  - **Content**: `"Error uploading picture"`

---

### `POST /email`

Sends an email with a specified image from the bucket as an attachment.

- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "email": "<recipient_email@example.com>",
    "name": "<image_name_in_bucket.jpg>"
  }
  ```
- **Success Response**:
  - **Code**: 200 OK
  - **Content**: `"Email sent successfully"`
- **Error Responses**:
  - **Code**: 404 Not Found
    - **Content**: `"Picture not found"`
  - **Code**: 500 Internal Server Error
    - **Content**: `"Error sending email"`

---

### `GET /status`

Retrieves the status of the service, including the bucket URL and the number of pictures.

- **Method**: `GET`
- **Success Response**:
  - **Code**: 200 OK
  - **Content**:
    ```json
    {
      "bucket_url": "https://console.cloud.google.com/storage/browser/<your-bucket-name>",
      "num_pictures": 42
    }
    ```
- **Error Response**:
  - **Code**: 500 Internal Server Error
  - **Content**: `"Error getting status"`

## Setup and Local Execution

### Prerequisites

- Python 3.9+
- `pip`

### Steps

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set environment variables:**
    Create a `.env` file or export the following environment variables:
    ```bash
    export PROJECT_ID="your-gcp-project-id"
    export BUCKET_NAME="your-gcs-bucket-name"
    export SENDGRID_API_KEY="your-sendgrid-api-key"
    export SENDER_EMAIL="your-sender-email@example.com"
    ```

4.  **Run the application:**
    ```bash
    gunicorn --bind 0.0.0.0:8080 main:app --chdir src
    ```
    The service will be available at `http://localhost:8080`.

## Deployment to Google Cloud Run

### Prerequisites

- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (`gcloud`) installed and configured.
- [Docker](https://docs.docker.com/get-docker/) installed.
- A Google Cloud project with the Cloud Run and Cloud Storage APIs enabled.
- A Google Cloud Storage bucket created.
- A SendGrid account and API key.

### Steps

1.  **Build the Docker image:**
    Replace `$PROJECT_ID` with your Google Cloud project ID.
    ```bash
    docker build -t gcr.io/$PROJECT_ID/image-service:v1 .
    ```

2.  **Configure Docker to use `gcloud` as a credential helper:**
    ```bash
    gcloud auth configure-docker
    ```

3.  **Push the image to Google Container Registry (GCR):**
    ```bash
    docker push gcr.io/$PROJECT_ID/image-service:v1
    ```

4.  **Deploy to Cloud Run:**
    Replace the placeholder values with your actual configuration.
    ```bash
    gcloud run deploy image-service \
      --image gcr.io/$PROJECT_ID/image-service:v1 \
      --platform managed \
      --region us-central1 \
      --allow-unauthenticated \
      --set-env-vars "PROJECT_ID=$PROJECT_ID" \
      --set-env-vars "BUCKET_NAME=<your-bucket-name>" \
      --set-env-vars "SENDGRID_API_KEY=<your-sendgrid-key>" \
      --set-env-vars "SENDER_EMAIL=<your-sender-email>"
    ```

After deployment, `gcloud` will provide you with the URL where your service is accessible.