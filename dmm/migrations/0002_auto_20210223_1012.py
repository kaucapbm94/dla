# Generated by Django 3.1.6 on 2021-02-23 04:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dmm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='result',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='dmm.result'),
        ),
        migrations.AlterField(
            model_name='commentround',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dmm.comment'),
        ),
    ]
