# Generated by Django 3.0 on 2019-12-17 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0008_tweet_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweet',
            name='image',
        ),
    ]
