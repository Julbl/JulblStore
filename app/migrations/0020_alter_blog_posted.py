# Generated by Django 4.1.7 on 2023-05-02 19:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0019_remove_blog_author_remove_blog_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 5, 2, 22, 53, 6, 876578), verbose_name='Опубликована'),
        ),
    ]
