from django.db import models


class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True, verbose_name="Время публикации")
    modified = models.DateTimeField(auto_now=True, verbose_name="Время изменения")

    class Meta:
        abstract = True


class Chapter(models.Model):
    name = models.CharField(max_length=511, verbose_name="Название раздела")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.CASCADE)


class Index(models.Model):
    name = models.CharField(max_length=511, verbose_name="Название показателя")
    chapter = models.ForeignKey("Chapter", on_delete=models.PROTECT, null=True, blank=True, verbose_name="Раздел")



