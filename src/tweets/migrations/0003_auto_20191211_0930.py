# Generated by Django 3.0 on 2019-12-11 09:30

from django.db import migrations, models
import tweets.models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0002_auto_20191211_0546'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='content',
            field=models.CharField(max_length=250, validators=[tweets.models.validate_content]),
        ),
    ]
