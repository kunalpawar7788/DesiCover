# Generated by Django 2.2.5 on 2020-05-31 11:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20200328_2203'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
