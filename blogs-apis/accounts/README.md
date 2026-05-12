# Accounts App

This application manages user authentication, registration, and social login integration for the Urbantrends Blogs API project.

## Features
- **User Registration**: API-based user registration.
- **Social Login**: Google and Apple authentication providers integrated via `django-allauth`.
- **Token Authentication**: Uses `dj-rest-auth` for token-based API authentication.

## API Endpoints
- `/api/auth/registration/`: User registration endpoint.
- `/api/auth/login/`: User login endpoint.
- `/api/auth/logout/`: User logout endpoint.
- `/api/auth/social/`: Social authentication providers.

## Configuration
Authentication is configured in `urbantrends_blogs_apis/settings.py` using `allauth` and `dj-rest-auth`.
