# Generated by Django 4.2.10 on 2024-05-14 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_post_title_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
