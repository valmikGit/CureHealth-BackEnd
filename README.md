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

### 4. Video Calling (Agora Integration)

- Integrates Agora SDK for seamless video calling functionality.
- Enables direct communication between patients and doctors.

### 5. Chat Functionality

- Implements chat functionality using Django Channels and Redis.
- Supports real-time communication between users and healthcare professionals.

### 6. RESTful API

- Utilizes Django Rest Framework for building a RESTful API.
- Implements various endpoints to support frontend functionalities.

### 7. CORS and Security

- Configures CORS headers to allow cross-origin resource sharing.
- Implements middleware for security measures such as CSRF protection.

### 8. Admin Panel

- Provides a customizable admin panel for easy management of data.
- Allows administrators to monitor and manage the application efficiently.

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
