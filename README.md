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
- **API Key Authentication**: POST endpoints are secured with an API key.

## API Documentation

### `GET /`

A heartbeat endpoint to check if the service is operational.

- **Method**: `GET`
- **Success Response**:
  - **Code**: 200 OK
  - **Content**: "OK"

---

### `POST /upload`

Uploads an image to the configured Google Cloud Storage bucket.

- **Method**: `POST`
- **Headers**:
  - `X-API-KEY`: Your secret API key.
- **Request Body**:
  ```json
  {
    "image": "<base64_encoded_string>",
    "name": "<your_image_name.jpg>"
  }
  ```
- **Success Response**:
  - **Code**: 201 Created
  - **Content**: "Picture uploaded successfully"
- **Error Response**:
  - **Code**: 401 Unauthorized
  - **Code**: 500 Internal Server Error
  - **Content**: "Error uploading picture"

---

### `POST /email`

Sends an email with a specified image from the bucket as an attachment.

- **Method**: `POST`
- **Headers**:
  - `X-API-KEY`: Your secret API key.
- **Request Body**:
  ```json
  {
    "email": "<recipient_email@example.com>",
    "name": "<image_name_in_bucket.jpg>"
  }
  ```
- **Success Response**:
  - **Code**: 200 OK
  - **Content**: "Email sent successfully"
- **Error Responses**:
  - **Code**: 401 Unauthorized
  - **Code**: 404 Not Found
    - **Content**: "Picture not found"
  - **Code**: 500 Internal Server Error
    - **Content**: "Error sending email"

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
  - **Content**: "Error getting status"

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
    export API_KEY="your-secret-api-key"
    ```

4.  **Run the application:**
    ```bash
    gunicorn --bind 0.0.0.0:8080 main:app --chdir src
    ```
    The service will be available at `http://localhost:8080`.

### Test Client

A test client is provided in `src/test_client.py` to test the `/upload` endpoint.

**Usage:**
```bash
python3 src/test_client.py <path/to/your/file>
```

## Deployment with Cloud Build

This project includes a `cloudbuild.yaml` file to automate deployments to Google Cloud Run.

### Prerequisites

- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) (`gcloud`) installed and configured.
- A Google Cloud project with the Cloud Build, Cloud Run, and Cloud Storage APIs enabled.
- A Google Cloud Storage bucket created.
- A SendGrid account and API key.

### Permissions

Ensure that the Cloud Build service account has the following roles:
- **Cloud Build Service Account** (`roles/cloudbuild.builds.builder`)
- **Cloud Run Admin** (`roles/run.admin`)
- **Service Account User** (`roles/iam.serviceAccountUser`) on the Cloud Run runtime service account.

### Steps

1.  **Submit the build:**
    Replace the placeholder values in the command below with your actual configuration. You can also set these as defaults in the `cloudbuild.yaml` file.
    ```bash
    gcloud builds submit --config cloudbuild.yaml --substitutions=_SERVICE_NAME=email-runner,_REGION=us-central1,_BUCKET_NAME=<your-bucket-name>,_SENDGRID_API_KEY=<your-sendgrid-key>,_SENDER_EMAIL=<your-sender-email>,_API_KEY=<your-secret-api-key>
    ```

This command will trigger a build that:
1.  Builds the Docker image.
2.  Pushes the image to Google Container Registry.
3.  Deploys the new image to your Cloud Run service.