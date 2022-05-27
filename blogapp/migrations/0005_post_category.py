# Generated by Django 4.0.4 on 2022-05-27 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0004_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, to='blogapp.category'),
        ),
    ]
