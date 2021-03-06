# Generated by Django 4.0.4 on 2022-06-08 11:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blogapp', '0003_post_like_count_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='thumbs',
            field=models.ManyToManyField(blank=True, default=None, related_name='thumbs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='post',
            name='thumbsdown',
            field=models.IntegerField(default='0'),
        ),
        migrations.AddField(
            model_name='post',
            name='thumbsup',
            field=models.IntegerField(default='0'),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.BooleanField(default=True)),
                ('post', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='postid', to='blogapp.post')),
                ('user', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='userid', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
