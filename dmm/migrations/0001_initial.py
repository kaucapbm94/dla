# Generated by Django 3.1.6 on 2021-02-12 11:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.TextField(blank=True, null=True)),
                ('author_url', models.CharField(max_length=2100, null=True)),
                ('is_answer', models.BooleanField(null=True)),
                ('date', models.DateTimeField(null=True)),
                ('clarification', models.CharField(max_length=6000, null=True)),
                ('create_date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Expert',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200, null=True)),
                ('chat_id', models.IntegerField(null=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='LanguageType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, null=True)),
                ('code', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ResourceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TonalType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_common', models.BooleanField(default=False, null=True)),
                ('expert', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dmm.expert')),
            ],
        ),
        migrations.CreateModel(
            name='Specie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('expert', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dmm.expert')),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('text', models.TextField(null=True)),
                ('title', models.TextField(null=True)),
                ('url', models.CharField(max_length=2100)),
                ('date', models.DateTimeField(null=True)),
                ('create_date', models.DateTimeField()),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dmm.contenttype')),
                ('expert', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dmm.expert')),
                ('language_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dmm.languagetype')),
                ('resource_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dmm.resourcetype')),
            ],
        ),
        migrations.CreateModel(
            name='CommentRound',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('clarification', models.CharField(max_length=2000, null=True)),
                ('create_date', models.DateTimeField(null=True)),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dmm.comment')),
                ('expert', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dmm.expert')),
                ('specie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dmm.specie')),
                ('tags', models.ManyToManyField(to='dmm.Tag')),
                ('tonal_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dmm.tonaltype')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='expert',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dmm.expert'),
        ),
        migrations.AddField(
            model_name='comment',
            name='language_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='dmm.languagetype'),
        ),
        migrations.AddField(
            model_name='comment',
            name='resource_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dmm.resourcetype'),
        ),
        migrations.AddField(
            model_name='comment',
            name='result',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dmm.result'),
        ),
        migrations.AddField(
            model_name='comment',
            name='specie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dmm.specie'),
        ),
        migrations.AddField(
            model_name='comment',
            name='tags',
            field=models.ManyToManyField(to='dmm.Tag'),
        ),
        migrations.AddField(
            model_name='comment',
            name='tonal_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='dmm.tonaltype'),
        ),
    ]
