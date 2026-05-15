from django.apps import AppConfig


class BlogsInsightsConfig(AppConfig):
    name = 'blogs_insights'

    def ready(self):
        import blogs_insights.signals  # noqa: F401
