# Generated by Django 3.1.6 on 2021-02-18 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmm', '0010_auto_20210218_1638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='result',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
