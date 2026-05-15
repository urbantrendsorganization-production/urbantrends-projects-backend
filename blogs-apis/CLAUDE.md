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

Dependencies live in `./venv/` (not committed). To regenerate: `venv/bin/pip freeze > requirements.txt`.

## Docker / Production

Production uses Docker + Gunicorn + Nginx. The `entrypoint.sh` runs `migrate`, `collectstatic`, then Gunicorn with 3 workers on port 8000. `docker-compose.yml` binds the backend to `127.0.0.1:8004` and spins up `postgres:16-alpine` on port 5437.

Switch to PostgreSQL by setting `USE_POSTGRES=true` in `.env` along with `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`.

## Architecture

**Django 6.0.5** REST API. Python 3.14.

### Apps

- **`accounts/`** — `UserProfile` (OneToOne → User, auto-created via signal), `Subscriber` (newsletter opt-in). Handles social login views, `MeView` (GET/PATCH current user), and `SubscribeView`. Signals send welcome emails on signup/subscribe.
- **`blogs/`** — `BlogPost` (auto-slug with collision avoidance, image upload, like/comment counts annotated on every queryset), `Comment`, `Like`. Signals send a new-post email to all `Subscriber` rows when a post is first published.
- **`blogs_insights/`** — `BlogsInsights` (OneToOne → BlogPost, stores `insight_title` + `insight_description`). The app is a stub: `views.py` is empty and it is not wired into the URL conf yet.

### Auth stack

- **`dj-rest-auth`** — login/logout/registration endpoints
- **`django-allauth`** — registration flow and social providers (Google, Apple)
- **`rest_framework.authentication.TokenAuthentication`** — default auth (not JWT)
- **`CsrfExemptSessionAuthentication`** (`accounts/authentication.py`) — replaces session auth to bypass CSRF

### Email

`accounts/email_service.py` wraps the **Resend** API (via `resend` SDK). Three transactional emails: welcome on signup, welcome on newsletter subscribe, and new-post notification broadcast to all subscribers. Set `RESEND_API_KEY` and `DEFAULT_FROM_EMAIL` in `.env`.

### URL layout

| Prefix | Handler |
|---|---|
| `/admin/` | Django admin |
| `/accounts/` | allauth internal (required for social redirects) |
| `/api/auth/` | dj-rest-auth |
| `/api/auth/registration/` | dj-rest-auth registration |
| `/api/auth/social/google/` | Google OAuth2 |
| `/api/auth/social/apple/` | Apple OAuth2 |
| `/api/accounts/me/` | `MeView` — GET/PATCH authenticated user + profile |
| `/api/subscribe/` | `SubscribeView` — newsletter opt-in |
| `/api/admin/blogs/` | `AdminBlogListCreateView` — `IsAdminUser` only |
| `/api/admin/blogs/<slug>/` | `AdminBlogDetailView` — `IsAdminUser` only |
| `/api/admin/blogs/stats/` | `AdminBlogStatsView` — aggregate counts |
| `/api/blogs/` | `BlogListView` — published posts, public |
| `/api/blogs/<slug>/` | `BlogDetailView` — public |
| `/api/blogs/<slug>/comments/` | `BlogCommentListCreateView` — read public, write authenticated |
| `/api/blogs/<slug>/like/` | `LikeToggleView` — authenticated, toggles like |
| `/api/blogs/comments/<pk>/` | `CommentDeleteView` — owner only |

### Key patterns

- `_annotated_qs()` in `blogs/views.py` annotates every `BlogPost` queryset with `likes_count` and `comments_count` via `Count(..., distinct=True)` — always use this helper instead of separate queries.
- `HttpsImageField` in `blogs/serializers.py` forces `https://` on media URLs (needed behind a reverse proxy).
- Admin vs public blog views are separated purely by permission class (`IsAdminUser` vs `AllowAny`/`IsAuthenticated`), not by separate URL namespaces.
- `BlogPost.slug` is auto-generated from the title on first save with a counter suffix for collisions.
- `published_at` is set by both `AdminBlogDetailView.perform_update` and `blogs/signals.py` — the signal is the canonical path for the public flow; the view handles the admin form flow.
