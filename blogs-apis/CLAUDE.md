# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

All commands assume the virtualenv is active (`source venv/bin/activate`).

```bash
# Run development server
python manage.py runserver

# Apply migrations
python manage.py migrate

# Create new migrations after model changes
python manage.py makemigrations

# Run all tests
python manage.py test

# Run tests for a specific app
python manage.py test accounts

# Django shell
python manage.py shell

# Create superuser
python manage.py createsuperuser
```

No `requirements.txt` exists — dependencies are installed directly into `./venv/`. To freeze: `venv/bin/pip freeze > requirements.txt`.

## Architecture

**Django 6.0.5** REST API. Python 3.14.

### Auth stack
Authentication is entirely delegated to third-party packages — there is no custom auth logic in `accounts/views.py`:

- **`dj-rest-auth`** provides login/logout/registration endpoints at `/api/auth/`
- **`django-allauth`** handles registration flow and social providers
- **`djangorestframework-simplejwt`** is installed but not yet wired up in `REST_FRAMEWORK` settings
- Social login for **Google** and **Apple** is configured in `urbantrends_blogs_apis/urls.py` as `SocialLoginView` subclasses

Default authentication uses `TokenAuthentication` (DRF token, not JWT). `CsrfExemptSessionAuthentication` in `accounts/authentication.py` replaces the default session auth to bypass CSRF checks — the `CsrfViewMiddleware` is also commented out in settings.

### URL layout
| Prefix | Handled by |
|---|---|
| `/admin/` | Django admin |
| `/api/auth/` | dj-rest-auth |
| `/api/auth/registration/` | dj-rest-auth registration |
| `/api/auth/social/google/` | Google OAuth2 |
| `/api/auth/social/apple/` | Apple OAuth2 |

### Database
SQLite (`db.sqlite3`) for development. `accounts/migrations/` is empty — no custom models yet.

### Project layout
- `urbantrends_blogs_apis/` — Django project config (settings, root URLs, wsgi/asgi)
- `accounts/` — user auth app; currently only contains the `CsrfExemptSessionAuthentication` helper and empty model/view stubs
- `venv/` — local virtualenv, not committed
