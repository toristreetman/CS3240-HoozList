# Generated by Django 4.1.1 on 2022-12-05 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_userprofile_comments_received_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
