import resend
from django.conf import settings

resend.api_key = settings.RESEND_API_KEY
FROM = settings.DEFAULT_FROM_EMAIL


def _send(*, to: str | list, subject: str, html: str) -> None:
    resend.Emails.send({
        "from": f"Urbantrends <{FROM}>",
        "to": to if isinstance(to, list) else [to],
        "subject": subject,
        "html": html,
    })


# ── templates ────────────────────────────────────────────────────────────────

def _base(content: str) -> str:
    return f"""
    <div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;color:#1a1a1a;">
      <div style="background:#000;padding:24px 32px;">
        <h1 style="color:#fff;margin:0;font-size:22px;letter-spacing:1px;">URBANTRENDS</h1>
      </div>
      <div style="padding:32px;">
        {content}
      </div>
      <div style="padding:16px 32px;border-top:1px solid #eee;font-size:12px;color:#888;text-align:center;">
        © Urbantrends · <a href="mailto:{FROM}" style="color:#888;">Unsubscribe</a>
      </div>
    </div>
    """


# ── public API ────────────────────────────────────────────────────────────────

def send_welcome_email(user) -> None:
    name = user.get_full_name() or user.email.split("@")[0]
    _send(
        to=user.email,
        subject="Welcome to Urbantrends!",
        html=_base(f"""
            <h2 style="margin-top:0;">Hey {name}, welcome aboard!</h2>
            <p>We're glad you joined Urbantrends. You'll find the latest insights,
            stories, and trends from our blog right here.</p>
            <p>Stay tuned — great content is on its way.</p>
            <p style="margin-top:32px;">— The Urbantrends Team</p>
        """),
    )


def send_subscription_welcome_email(email: str) -> None:
    _send(
        to=email,
        subject="You're subscribed to Urbantrends!",
        html=_base(f"""
            <h2 style="margin-top:0;">You're on the list!</h2>
            <p>Thanks for subscribing to <strong>Urbantrends</strong>. You'll be
            the first to know when we publish new stories and updates.</p>
            <p style="margin-top:32px;">— The Urbantrends Team</p>
        """),
    )


def send_new_blog_email(blog, subscribers: list[str]) -> None:
    if not subscribers:
        return
    excerpt = blog.excerpt or (blog.content[:160] + "…" if len(blog.content) > 160 else blog.content)
    html = _base(f"""
        <h2 style="margin-top:0;">New on Urbantrends</h2>
        <h3 style="color:#111;">{blog.title}</h3>
        <p style="color:#555;">{excerpt}</p>
        <a href="https://urbantrends.dev/blogs/{blog.slug}"
           style="display:inline-block;margin-top:16px;padding:12px 24px;
                  background:#000;color:#fff;text-decoration:none;border-radius:4px;">
          Read the full post
        </a>
        <p style="margin-top:32px;font-size:12px;color:#999;">
          You're receiving this because you subscribed to Urbantrends updates.
        </p>
    """)
    # Send individually so subscribers don't see each other's addresses
    for email in subscribers:
        _send(to=email, subject=f"New post: {blog.title}", html=html)
