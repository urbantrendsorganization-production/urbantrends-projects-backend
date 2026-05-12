# Urbantrends Blogs API — Frontend Handout

**Base URL (dev):** `http://localhost:8000`  
**Base URL (prod):** `https://blog-api.urbantrends.dev`  
**Content-Type:** `application/json` for all requests unless uploading files (use `multipart/form-data`)

---

## Authentication

All protected endpoints require a token in the `Authorization` header:

```
Authorization: Token <token>
```

The token is returned on login and registration. Store it in local storage or a cookie and attach it to every subsequent request.

---

## Auth Endpoints

These are provided by `dj-rest-auth` out of the box.

### Register
`POST /api/auth/registration/`

```json
// Request
{
  "email": "user@example.com",
  "password1": "strongpassword",
  "password2": "strongpassword"
}

// Response 201
{
  "key": "<auth-token>"
}
```

### Login
`POST /api/auth/login/`

```json
// Request
{
  "email": "user@example.com",
  "password": "strongpassword"
}

// Response 200
{
  "key": "<auth-token>"
}
```

### Logout
`POST /api/auth/logout/`  
Requires token. Invalidates the current token.

```json
// Response 200
{ "detail": "Successfully logged out." }
```

### Password Reset (request email)
`POST /api/auth/password/reset/`

```json
// Request
{ "email": "user@example.com" }
```

### Password Reset Confirm
`POST /api/auth/password/reset/confirm/`

```json
// Request
{
  "uid": "<uid from email link>",
  "token": "<token from email link>",
  "new_password1": "newpassword",
  "new_password2": "newpassword"
}
```

### Change Password
`POST /api/auth/password/change/`  
Requires token.

```json
// Request
{
  "old_password": "current",
  "new_password1": "newpassword",
  "new_password2": "newpassword"
}
```

### Google Login
`POST /api/auth/social/google/`

```json
// Request
{ "access_token": "<google-oauth-access-token>" }

// Response 200
{ "key": "<auth-token>" }
```

### Apple Login
`POST /api/auth/social/apple/`

```json
// Request
{ "access_token": "<apple-identity-token>" }

// Response 200
{ "key": "<auth-token>" }
```

---

## Account Endpoints

### Get / Update My Profile
`GET /api/accounts/me/`  
`PATCH /api/accounts/me/`  
Requires token.

```json
// GET Response 200
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "date_joined": "2025-01-10T09:00:00Z",
  "profile": {
    "bio": "Writer and tech enthusiast.",
    "avatar_url": "https://example.com/avatar.jpg",
    "website": "https://johndoe.com"
  }
}

// PATCH Request — send only the fields you want to update
{
  "first_name": "Jane",
  "profile": {
    "bio": "Updated bio here."
  }
}
```

> `email` and `date_joined` are read-only.

---

## Newsletter

### Subscribe
`POST /api/subscribe/`  
No token required — open to everyone.

```json
// Request
{ "email": "reader@example.com" }

// Response 201
{ "detail": "Successfully subscribed." }

// Response 400 (already subscribed)
{ "email": ["subscriber with this email already exists."] }
```

---

## Blog Endpoints (Authenticated Users)

### List Published Posts
`GET /api/blogs/`  
Requires token.

```json
// Response 200
[
  {
    "id": 1,
    "title": "Getting Started with Django",
    "slug": "getting-started-with-django",
    "excerpt": "A quick intro to Django for modern web apps.",
    "image": "/media/blog_images/cover.jpg",
    "user": { "id": 2, "email": "admin@urbantrends.dev", "first_name": "Edwin", "last_name": "" },
    "relevant_link": "https://docs.djangoproject.com",
    "is_published": true,
    "published_at": "2025-05-01T10:00:00Z",
    "created_at": "2025-04-30T08:00:00Z",
    "likes_count": 12,
    "comments_count": 4
  }
]
```

### Get Single Post
`GET /api/blogs/<slug>/`  
Requires token.

```json
// Response 200
{
  "id": 1,
  "title": "Getting Started with Django",
  "slug": "getting-started-with-django",
  "excerpt": "A quick intro...",
  "content": "Full markdown/HTML content here...",
  "image": "/media/blog_images/cover.jpg",
  "user": { "id": 2, "email": "admin@urbantrends.dev", "first_name": "Edwin", "last_name": "" },
  "relevant_link": "https://docs.djangoproject.com",
  "is_published": true,
  "published_at": "2025-05-01T10:00:00Z",
  "created_at": "2025-04-30T08:00:00Z",
  "updated_at": "2025-05-01T09:00:00Z",
  "likes_count": 12,
  "comments_count": 4,
  "is_liked": false,
  "comments": [
    {
      "id": 3,
      "user": { "id": 5, "email": "reader@example.com", "first_name": "Alice", "last_name": "" },
      "content": "Great article!",
      "created_at": "2025-05-02T11:30:00Z"
    }
  ]
}
```

> `is_liked` is `true` if the authenticated user has liked the post.

### List / Add Comments
`GET /api/blogs/<slug>/comments/`  
`POST /api/blogs/<slug>/comments/`  
Requires token.

```json
// POST Request
{ "content": "This is my comment." }

// POST Response 201
{
  "id": 10,
  "user": { "id": 1, "email": "user@example.com", "first_name": "John", "last_name": "" },
  "content": "This is my comment.",
  "created_at": "2025-05-10T14:00:00Z"
}
```

### Delete Own Comment
`DELETE /api/blogs/comments/<id>/`  
Requires token. Users can only delete their own comments. Returns `204 No Content`.

### Toggle Like
`POST /api/blogs/<slug>/like/`  
Requires token. Calling it once likes the post; calling it again unlikes it.

```json
// Response 201 — liked
{ "liked": true, "likes_count": 13 }

// Response 200 — unliked
{ "liked": false, "likes_count": 12 }
```

---

## Admin Endpoints

> Admin endpoints require the user to have **`is_staff = true`**. The token must belong to a staff user.

### Blog Stats Dashboard
`GET /api/admin/blogs/stats/`

```json
// Response 200
{
  "total_posts": 25,
  "published": 18,
  "drafts": 7,
  "total_likes": 342,
  "total_comments": 156,
  "top_liked": {
    "title": "10 Django Tips",
    "slug": "10-django-tips",
    "likes_count": 45
  },
  "top_commented": {
    "title": "React vs Vue",
    "slug": "react-vs-vue",
    "comments_count": 23
  }
}
```

### List All Posts (including drafts)
`GET /api/admin/blogs/`

Same shape as the user listing but includes unpublished (`is_published: false`) posts too.

### Create Post
`POST /api/admin/blogs/`  
Use `multipart/form-data` when uploading an image; `application/json` otherwise.

```json
// Request (JSON)
{
  "title": "My New Post",
  "excerpt": "A short summary shown in the list.",
  "content": "Full body content here...",
  "relevant_link": "https://example.com",
  "is_published": false
}

// Request (multipart) — include image field as file upload

// Response 201
{
  "title": "My New Post",
  "slug": "my-new-post",
  "excerpt": "...",
  "content": "...",
  "image": null,
  "relevant_link": "...",
  "is_published": false
}
```

> Setting `is_published: true` on create or update automatically sets `published_at` and triggers email notifications to all subscribers.

### Get / Edit / Delete Post
`GET /api/admin/blogs/<slug>/`  
`PATCH /api/admin/blogs/<slug>/`  
`DELETE /api/admin/blogs/<slug>/`

`GET` returns the full detail including comments (same shape as user detail view).  
`PATCH` accepts any subset of the writable fields.  
`DELETE` returns `204 No Content`.

---

## HTTP Status Code Reference

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 204 | Deleted successfully |
| 400 | Validation error — check response body for field errors |
| 401 | Missing or invalid token |
| 403 | Authenticated but not authorised (e.g. non-staff hitting admin endpoint) |
| 404 | Resource not found |

---

## URL Summary

| Method | Endpoint | Auth | Role |
|--------|----------|------|------|
| POST | `/api/auth/registration/` | — | Register |
| POST | `/api/auth/login/` | — | Login → get token |
| POST | `/api/auth/logout/` | Token | Logout |
| POST | `/api/auth/password/reset/` | — | Request password reset email |
| POST | `/api/auth/password/reset/confirm/` | — | Confirm password reset |
| POST | `/api/auth/password/change/` | Token | Change password |
| POST | `/api/auth/social/google/` | — | Google OAuth login |
| POST | `/api/auth/social/apple/` | — | Apple OAuth login |
| GET | `/api/accounts/me/` | Token | View profile |
| PATCH | `/api/accounts/me/` | Token | Update profile |
| POST | `/api/subscribe/` | — | Newsletter subscription |
| GET | `/api/blogs/` | Token | List published posts |
| GET | `/api/blogs/<slug>/` | Token | Post detail + comments |
| GET POST | `/api/blogs/<slug>/comments/` | Token | List / add comment |
| DELETE | `/api/blogs/comments/<id>/` | Token | Delete own comment |
| POST | `/api/blogs/<slug>/like/` | Token | Toggle like |
| GET | `/api/admin/blogs/stats/` | Staff token | Dashboard stats |
| GET POST | `/api/admin/blogs/` | Staff token | List all / create post |
| GET PATCH DELETE | `/api/admin/blogs/<slug>/` | Staff token | Manage single post |
