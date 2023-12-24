# Generated by Django 2.2.28 on 2023-12-24 09:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0029_auto_20231223_2040'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('occupation', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('male', 'Мужской'), ('female', 'Женский')], max_length=255)),
                ('internet', models.CharField(choices=[('1', 'Каждый день'), ('2', 'Несколько раз в день'), ('3', 'Несколько раз в неделю'), ('4', 'Несколько раз в месяц')], max_length=255)),
                ('notice', models.BooleanField()),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'db_table': 'Feedbacks',
            },
        ),
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 12, 24, 12, 48, 49, 705306), verbose_name='Опубликована'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 12, 24, 12, 48, 49, 706307), verbose_name='Дата комментария'),
        ),
    ]