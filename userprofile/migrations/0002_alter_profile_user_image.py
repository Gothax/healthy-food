# Generated by Django 5.0.2 on 2024-05-03 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user_image',
            field=models.ImageField(blank=True, default='default_profile_image.png', null=True, upload_to='user_images/'),
        ),
    ]