# Generated by Django 4.2.10 on 2024-05-14 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_featuredpost_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='featuredpost',
            name='pic',
        ),
        migrations.AddField(
            model_name='featuredcategory',
            name='pic',
            field=models.ImageField(blank=True, upload_to='featuredpic/'),
        ),
    ]
