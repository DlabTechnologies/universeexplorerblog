# Generated by Django 2.2.2 on 2020-06-12 22:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200612_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(blank=True),
        ),
    ]