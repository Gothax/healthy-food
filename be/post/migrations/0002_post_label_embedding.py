# Generated by Django 5.0.6 on 2024-06-24 20:54

import pgvector.django
import post.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='label_embedding',
            field=pgvector.django.VectorField(default=post.models.default_embedding, dimensions=1536),
        ),
    ]