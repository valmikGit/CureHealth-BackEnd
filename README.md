# CureHealth BackEnd

## Introduction

The Synergy_Backend Django project serves as the robust backend for the CureHealth telehealth platform. This project utilizes Django 4.2.6 and incorporates various apps to support features such as user authentication, chat functionality, email sending, and integration with third-party services like Agora for video calls.

## Key Features

### 1. User Authentication

- Utilizes JWT (JSON Web Token) authentication for secure user authentication.
- Configured with customizable token lifetimes and security settings.

### 2. WebSocket Communication

- Implements WebSocket communication using Django Channels for real-time interactions.
- Configured with Redis as the channel layer for handling WebSocket connections.

### 3. Email Sending

- Integrates Django's email backend to send emails for various functionalities.
- Configured to use Gmail SMTP for reliable email delivery.
<!--

### 4. Video Calling (Agora Integration)

- Integrates Agora SDK for seamless video calling functionality.
- Enables direct communication between patients and doctors. -->

<!-- ### 5. Chat Functionality

- Implements chat functionality using Django Channels and Redis.
- Supports real-time communication between users and healthcare professionals. -->

### 4. RESTful API

- Utilizes Django Rest Framework for building a RESTful API.
- Implements various endpoints to support frontend functionalities.

### 5. CORS and Security

- Configures CORS headers to allow cross-origin resource sharing.
- Implements middleware for security measures such as CSRF protection.

### 6. Admin Panel

- Provides a customizable admin panel for easy management of data.
- Allows administrators to monitor and manage the application efficiently.

# API Documentation

This document provides a detailed overview of the core APIs implemented in the project, along with their functionalities.

---

## Patient Management APIs

1. **Get All Patients**

   - **Endpoint:** `/api/patients/`
   - **Method:** GET
   - **Description:** Fetches a list of all registered patients. It validates the data structure and ensures the returned list matches the database.

2. **Get Patient by ID**
   - **Endpoint:** `/api/patients/{id}/`
   - **Method:** GET
   - **Description:** Retrieves details of a specific patient using their ID. It checks the correctness of the response against the database entry.

---

## Doctor Management APIs

1. **Get Doctors by Specialization**

   - **Endpoint:** `/api/doctors/specialization/{specialization}/`
   - **Method:** GET
   - **Description:** Returns a subset of doctors filtered by their specialization. Ensures the correct application of filtering logic.

2. **Post New Doctor**

   - **Endpoint:** `/api/doctors/`
   - **Method:** POST
   - **Description:** Creates a new doctor record with given attributes like specialization and availability. It verifies that the doctor is added to the database with valid inputs.

3. **Update Doctor Details**

   - **Endpoint:** `/api/doctors/{id}/`
   - **Method:** PUT
   - **Description:** Updates the entire profile of an existing doctor. It ensures the old data is replaced with the updated details.

4. **Partial Update Doctor**

   - **Endpoint:** `/api/doctors/{id}/`
   - **Method:** PATCH
   - **Description:** Updates specific attributes of a doctor's profile, such as availability. Validates that only targeted fields are modified without affecting others.

5. **Delete Doctor**
   - **Endpoint:** `/api/doctors/{id}/`
   - **Method:** DELETE
   - **Description:** Deletes a doctor record using their ID. Ensures the record is removed from the database and returns appropriate error messages if the doctor does not exist.

---

## User Management APIs

1. **Get All Users**

   - **Endpoint:** `/api/users/`
   - **Method:** GET
   - **Description:** Fetches a list of all users in the system. It validates the response count and data attributes.

2. **Post New User**

   - **Endpoint:** `/api/users/`
   - **Method:** POST
   - **Description:** Adds a new user to the system. Verifies input validation and the successful creation of user records.

3. **Delete User**
   - **Endpoint:** `/api/users/{id}/`
   - **Method:** DELETE
   - **Description:** Deletes a specific user by ID. Confirms the deletion and checks for proper error handling if the user does not exist.

---

## Appointment Management APIs

1. **Get All Appointments**

   - **Endpoint:** `/api/appointments/`
   - **Method:** GET
   - **Description:** Retrieves all scheduled appointments. Validates the data against stored records and ensures correct response formatting.

2. **Filtered Appointments**

   - **Endpoint:** `/api/appointments/filter/`
   - **Method:** GET
   - **Description:** Fetches appointments filtered by attributes like meeting type. Confirms the filters are applied correctly and the results are accurate.

3. **Create Appointment**

   - **Endpoint:** `/api/appointments/`
   - **Method:** POST
   - **Description:** Allows the creation of a new appointment. Ensures input data is validated and successfully stored in the system.

4. **Update Appointment**

   - **Endpoint:** `/api/appointments/{id}/`
   - **Method:** PUT
   - **Description:** Updates details of an existing appointment, such as the disease field. Validates the response and database changes.

5. **Delete Appointment**
   - **Endpoint:** `/api/appointments/{id}/`
   - **Method:** DELETE
   - **Description:** Deletes a specific appointment by ID. Confirms the appointment's removal and checks for error messages if the ID does not exist.

---

## Testing Information

- **Framework Used:** Django REST Framework
- **Testing Suite:** `APITestCase` and `APIClient`
- **Key Features Tested:**
  - CRUD operations.
  - Validation for invalid data or non-existent IDs.
  - Filtering results by attributes.

## Django Project Overview

This Django project, named Synergy_Backend, serves as the backend for the CureHealth telehealth platform. The project is built using Django 4.2.6 and includes various apps such as `base`, `api`, `healthcare`, `phonenumber_field`, `rest_framework`, `rest_framework_simplejwt`, `corsheaders`, `channels`, `chatApp_2`, `verifyAuth`, `agora`, `chatApp`, and `email_Sender`.

## Django Settings

### Environment Variables

Ensure you have the following environment variables set:

- `SECRET_KEY`: Django secret key for security.
- `DEBUG`: Set to `True` for development, and `False` for production.
- `ALLOWED_HOSTS`: List of valid host/domain names.

### Installed Apps

- `base`, `api`, `healthcare`, `phonenumber_field`, `rest_framework`, `rest_framework_simplejwt.token_blacklist`, `corsheaders`, `rest_framework_simplejwt`, `channels`, `chatApp_2`, `verifyAuth`, `agora`, `chatApp`, `email_Sender`.

### JWT Authentication Settings

- JWT access token lifetime: 5 minutes.
- JWT refresh token lifetime: 90 days.

### Middleware

- Middleware includes security, session, common, CSRF, authentication, messages, clickjacking, and CORS.

### Database

- Default SQLite database is configured for development.

### Password Validation

- Password validators ensure secure user passwords.

### Internationalization

- Language code set to "en-us" with UTC timezone.

### Static Files

- Static files served from the "static/" directory.

### Default Auto Field

- Default primary key field type is `BigAutoField`.

### Authentication User Model

- Custom user model is set to "healthcare.NewUser".

### CORS Settings

- CORS is configured to allow all origins with credentials.

### Email Settings

- Email backend, host, port, user, password, and server email are configured for sending emails.

### Channel Layers

- Channels are configured for handling WebSockets using Redis.

### Caching

- Redis is configured for caching purposes.

### Admins

- Admins are set with their names and email addresses.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/valmikGit/CureHealth-BackEnd
   ```

2. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Apply Migrations:**

   ```bash
   python manage.py migrate
   ```

4. **Run the Development Server:**

   ```bash
   python manage.py runserver
   ```

5. **Access the Admin Panel:**
   - Open your browser and go to `http://localhost:8000/admin/` to access the Django admin panel.

## Environment Variables

Ensure the following environment variables are set:

- `SECRET_KEY`: Django secret key for security.
- `DEBUG`: Set to `True` for development, and `False` for production.
- `ALLOWED_HOSTS`: List of valid host/domain names.
- `REDIS_URL`: URL for Redis.

## Contributions

- [Vaibhav Mittal](https://github.com/Vebstere)
- [Krish Dave](https://github.com/KrishDave1)
- [Valmik Belgaonkar](https://github.com/valmikGit)
- [Chirag MV](https://github.com/ChiragMV)

## Contact Us

For any additional information or inquiries, please contact us on our website [gmail](synergybackend12@gmail.com).

## Testing

The report for Testing is in this repository which has 34 tests for API's relating to doctor, newUser, Patient, Intermediary and Appointmemts. The report name is SE_Testing.tex which is a latex source file and the PDF is SE_TESTING_Report.
