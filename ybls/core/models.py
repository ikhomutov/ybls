from django.db import models

from .constants import MATERIAL_TYPES


class Subject(models.Model):
    name = models.CharField(max_length=256)
    ibls_id = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        db_table = 'subjects'


class Lesson(models.Model):
    level = models.PositiveSmallIntegerField()
    index = models.PositiveSmallIntegerField()
    subject = models.ForeignKey(
        to=Subject,
        on_delete=models.PROTECT,
        related_name='lessons'
    )
    name = models.CharField(max_length=512)

    class Meta:
        db_table = 'lessons'
        ordering = ('index',)


class Content(models.Model):
    lesson = models.ForeignKey(
        to=Lesson,
        on_delete=models.CASCADE,
        related_name='contents'
    )
    order = models.PositiveSmallIntegerField(null=True, blank=True)
    name = models.CharField(max_length=256)

    class Meta:
        db_table = 'contents'
        ordering = ('order',)


class Material(models.Model):
    content = models.ForeignKey(
        to=Content,
        on_delete=models.CASCADE,
        related_name='materials'
    )
    order = models.PositiveSmallIntegerField(blank=True, null=True)
    type = models.PositiveSmallIntegerField(
        choices=MATERIAL_TYPES
    )
    data = models.JSONField()

    class Meta:
        db_table = 'materials'
        ordering = ('order',)
