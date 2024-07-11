from django.db import models
from django.contrib.postgres.fields import ArrayField


class Chapter(models.Model):
    name = models.CharField(max_length=511, verbose_name="Название раздела")
    parent = models.ForeignKey("self", null=True, on_delete=models.PROTECT)
    
    class Meta:
        db_table = "chapters"
    
    def __str__(self):
        return f"{self.name}"


class Index(models.Model):
    name = models.CharField(max_length=511, verbose_name="Название показателя")
    measure = models.CharField(max_length=255, null=True, verbose_name="Единица измерения")
    chapter = models.ForeignKey("Chapter", null=True, on_delete=models.PROTECT, verbose_name="Раздел")
    
    class Meta:
        db_table = "indices"
    
    def __str__(self):
        return f"{self.name}"


class IndexPeriod(models.Model):
    name = models.CharField(max_length=255, verbose_name="Период индекса")

    class Meta:
        db_table = "index_periods"

    def __str__(self):
        return f"{self.name}"


class DatePeriod(models.Model):
    name = models.CharField(max_length=255, verbose_name="Дата индекса")
    index_period = models.ForeignKey("IndexPeriod", on_delete=models.PROTECT)

    class Meta:
        db_table = "date_periods"

    def __str__(self):
        return f"{self.name}"


class Dic(models.Model):
    dic_ids = ArrayField(models.IntegerField())
    dic_names = ArrayField(models.CharField(max_length=511))

    class Meta:
        db_table = "dics"


class IndexDics(models.Model):
    index = models.ForeignKey("Index", on_delete=models.PROTECT)
    dics = models.ForeignKey("Dic", on_delete=models.PROTECT)
    period = models.ForeignKey("IndexPeriod", on_delete=models.PROTECT)
    dates = ArrayField(models.IntegerField())

    class Meta:
        db_table = "indices_dics"


class Logs(models.Model):
    info = models.CharField(max_length=512)
    timestamp = models.DateTimeField(auto_now_add=True)
    