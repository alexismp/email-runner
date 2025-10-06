# Product Requirements Document: Image Handling Service

## 1. Introduction

This document outlines the product requirements for a backend service designed to handle image uploads, storage, and email delivery. The primary use case is for a conference booth where attendees can have their picture taken and emailed to them as a souvenir. The service is intended to be a demonstration of modern development practices using Google Cloud, AI Studio, Gemini CLI, and Jules.

## 2. Core Features

### 2.1. Image Upload and Storage

- **Description**: The service must provide an endpoint to accept an image and a filename via a POST request. Upon receipt, the service will store this image in a designated Google Cloud Storage (GCS) bucket.
- **User Story**: As a frontend application, I want to send an image file to the backend so that it can be stored securely and retrieved later.
- **Acceptance Criteria**:
    - The endpoint must accept a JSON payload containing a base64-encoded image string and a filename.
    - The image must be successfully stored in the GCS bucket specified at deploy-time.
    - The service should return a success status upon successful upload.

### 2.2. Email Image as Attachment

- **Description**: The service must provide an endpoint to send a previously uploaded image as an email attachment to a specified recipient.
- **User Story**: As a user, I want to provide my email address and the name of my picture to have it sent to my inbox.
- **Acceptance Criteria**:
    - The endpoint must accept a JSON payload containing a recipient's email address and the filename of the image to be sent.
    - The service must first verify that the requested image exists in the GCS bucket.
    - If the image does not exist, the service should return an appropriate error message.
    - If the image exists, the service should return an immediate success message to the client and then proceed to send the email asynchronously.
    - The email must contain specific predefined text.

### 2.3. Service Health Check

- **Description**: The service must have a simple "heartbeat" endpoint to allow for health monitoring.
- **User Story**: As a system administrator, I want to be able to ping the service to ensure it is running and responsive.
- **Acceptance Criteria**:
    - A GET request to the root URL (`/`) should return a simple `200 OK` response.

### 2.4. Service Status Endpoint

- **Description**: The service must provide an endpoint that gives insight into its operational status, specifically related to the GCS bucket.
- **User Story**: As a system administrator, I want to know how many images are currently stored and where the storage bucket is located.
- **Acceptance Criteria**:
    - A GET request to the `/status` endpoint should return a JSON object.
    - The JSON object must contain the URL to the GCS bucket and the total count of images currently stored in it.

## 3. Non-Functional Requirements

- **Deployment**: The service must be packaged as a Docker container and be deployable to Google Cloud Run.
- **Configuration**: All external service configurations (GCS bucket name, SendGrid API keys, etc.) must be injectable via environment variables at deploy-time. No secrets should be hardcoded in the source code.
- **Scalability**: As a Cloud Run service, it should be able to scale automatically based on incoming request traffic.
- **Security**: The service should not expose any sensitive information in its error messages or status endpoints. Communication with GCS and SendGrid should be secure.

## 4. Email Content Specification

The body of the email sent to the recipient must contain the following text:

**Subject**: Thanks for visiting our booth!

**Body**:
<p>Thank you for visiting Google Cloud's booth at the conference! The entire experience was coded with AI Studio, Gemini CLI and Jules.</p>
<p>We'd love for you to try out these technologies yourself. Get started with free Google Cloud credits (no credit card required) by visiting: <a href="https://trygcp.dev/dvxx-be-25">trygcp.dev/dvxx-be-25</a></p>