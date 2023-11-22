# Synergy_Backend ReadMe

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
   git clone <repository-url>
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

6. **Run WebSocket Server:**
   ```bash
   daphne Synergy_Backend.asgi:application --port 8001
   ```

7. **Access WebSocket Server:**
   - Open your browser and go to `ws://localhost:8001/` to access the WebSocket server.

## Environment Variables

Ensure the following environment variables are set:

- `SECRET_KEY`: Django secret key for security.
- `DEBUG`: Set to `True` for development, and `False` for production.
- `ALLOWED_HOSTS`: List of valid host/domain names.
- `REDIS_URL`: URL for Redis.
