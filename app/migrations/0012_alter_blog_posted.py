# Generated by Django 4.1.7 on 2023-05-02 17:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_blog_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 5, 2, 20, 13, 32, 486820), verbose_name='Опубликована'),
        ),
    ]
