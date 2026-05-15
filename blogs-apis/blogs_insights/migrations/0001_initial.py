from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blogs', '0002_blogsinsights'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogsInsights',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('insight_title', models.CharField(max_length=200)),
                ('insight_description', models.TextField()),
                ('post', models.OneToOneField(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='insights',
                    to='blogs.blogpost',
                )),
            ],
        ),
    ]
