# Generated by Django 3.1.6 on 2021-03-03 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmm', '0006_auto_20210302_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentround',
            name='clarification',
            field=models.CharField(blank=True, max_length=2000, null=True),
        ),
    ]