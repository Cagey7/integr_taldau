from django.db import models
from django.contrib.postgres.fields import ArrayField


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="Время публикации")
    modified = models.DateTimeField(auto_now=True, verbose_name="Время изменения")

    class Meta:
        abstract = True


class Chapter(models.Model):
    name = models.CharField(max_length=511, verbose_name="Название раздела")
    parent = models.ForeignKey("self", null=True, on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.name}"


class Index(models.Model):
    name = models.CharField(max_length=511, verbose_name="Название показателя")
    chapter = models.ForeignKey("Chapter", null=True, on_delete=models.PROTECT, verbose_name="Раздел")
    
    def __str__(self):
        return f"{self.name}"


class IndexPeriod(models.Model):
    name = models.CharField(max_length=255, verbose_name="Период индекса")

    def __str__(self):
        return f"{self.name}"


class DatePeriod(models.Model):
    name = models.CharField(max_length=255, verbose_name="Дата индекса")
    index_period = models.ForeignKey("IndexPeriod", on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name}"


class Dic(models.Model):
    dic_ids = ArrayField(models.IntegerField())
    dic_names = ArrayField(models.CharField(max_length=511))
    term_ids = ArrayField(models.IntegerField())


class IndixDics(models.Model):
    index = models.ForeignKey("Index", on_delete=models.PROTECT)
    dics = models.ForeignKey("Dic", on_delete=models.PROTECT)
    period = models.ForeignKey("IndexPeriod", on_delete=models.PROTECT)
    dates = ArrayField(models.IntegerField())
