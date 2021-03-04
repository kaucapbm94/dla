from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone

import logging
logger = logging.getLogger(__name__)


# Create your models here.
class Expert(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    chat_id = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class LanguageType(models.Model):
    name = models.TextField(blank=True, null=True)
    code = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ResourceType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ContentType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Result(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField(null=True, blank=True)
    title = models.TextField(null=True)
    url = models.CharField(max_length=2100)
    language_type = models.ForeignKey(LanguageType, models.DO_NOTHING)
    resource_type = models.ForeignKey(ResourceType, models.DO_NOTHING)
    content_type = models.ForeignKey(ContentType, models.DO_NOTHING)
    date = models.DateTimeField(null=True)

    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    expert = models.ForeignKey(Expert, models.DO_NOTHING, null=True)

    def __str__(self):
        return self.title if self.title != '' else self.url[:80]


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True, unique=True)
    description = models.TextField(blank=True, null=True)
    is_common = models.BooleanField(default=False, null=True)
    expert = models.ForeignKey('Expert', models.DO_NOTHING, null=True)

    def __str__(self):
        return self.name


class Specie(models.Model):
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField(blank=True, null=True)
    expert = models.ForeignKey(Expert, models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.name


class TonalType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField(blank=True, null=True)
    author_url = models.CharField(max_length=2100, null=True)
    result = models.ForeignKey(Result, on_delete=models.CASCADE, null=True)
    is_answer = models.BooleanField(null=True)
    language_type = models.ForeignKey(LanguageType, models.DO_NOTHING)
    resource_type = models.ForeignKey(ResourceType, models.DO_NOTHING, null=True)
    date = models.DateTimeField(null=True)
    specie = models.ForeignKey(Specie, models.DO_NOTHING, blank=True, null=True)
    tags = models.ManyToManyField(Tag, through='CommentTags')
    tonal_type = models.ForeignKey(TonalType, models.DO_NOTHING, blank=True, null=True)

    clarification = models.CharField(max_length=6000, null=True, blank=True)

    expert = models.ForeignKey(Expert, models.DO_NOTHING, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.text[:80]


class CommentTags(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, blank=True, null=True)
    is_present = models.BooleanField(null=True)

    def __str__(self):
        return self.comment.text[:80]


class CommentRound(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    comment = models.ForeignKey(Comment, models.CASCADE, blank=True, null=True)
    specie = models.ForeignKey(Specie, models.DO_NOTHING, blank=True, null=True)
    tags = models.ManyToManyField(Tag, through='CommentRoundTags', blank=True)
    tonal_type = models.ForeignKey(TonalType, models.DO_NOTHING, blank=True, null=True)

    clarification = models.CharField(max_length=2000, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    expert = models.ForeignKey(Expert, models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return self.comment.text[:80]


class CommentRoundTags(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, blank=True, null=True)
    comment_round = models.ForeignKey(CommentRound, on_delete=models.CASCADE, blank=True, null=True)
    is_present = models.BooleanField(null=True)

    def __str__(self):
        return self.comment_round.comment.text[:80] + ': ' + self.tag.name
