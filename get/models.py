# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.postgres.fields import ArrayField

class Chapters(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=511)
    parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'chapters'


class DatePeriods(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    index_period = models.ForeignKey('IndexPeriods', on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'date_periods'


class Dics(models.Model):
    dic_ids = ArrayField(models.IntegerField())
    dic_names = ArrayField(models.CharField(max_length=511))
    term_ids = ArrayField(models.IntegerField())

    class Meta:
        managed = False
        db_table = "dics"


class IndexPeriods(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'index_periods'


class Indices(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=511)
    chapter = models.ForeignKey(Chapters, on_delete=models.PROTECT, blank=True, null=True)
    measure = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'indices'


class IndicesDics(models.Model):
    id = models.BigAutoField(primary_key=True)
    dates = ArrayField(models.IntegerField())  # This field type is a guess.
    dics = models.ForeignKey(Dics, on_delete=models.PROTECT)
    index = models.ForeignKey(Indices, on_delete=models.PROTECT)
    period = models.ForeignKey(IndexPeriods, on_delete=models.PROTECT)

    class Meta:
        managed = False
        db_table = 'indices_dics'
