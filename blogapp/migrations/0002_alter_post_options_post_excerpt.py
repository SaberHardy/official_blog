# Generated by Django 4.0.4 on 2022-05-25 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-publish']},
        ),
        migrations.AddField(
            model_name='post',
            name='excerpt',
            field=models.TextField(default='empty data'),
            preserve_default=False,
        ),
    ]
