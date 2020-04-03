from django.db import models


# Create your models here.
class Date(models.Model):
    date = models.DateField(verbose_name="Data")

    def __str__(self):
        return f"{self.date}"

    class Meta:
        verbose_name_plural = "Daty"
        verbose_name = "Data"


class RubbishType(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nazwa frakcji")
    mark_color = models.CharField(max_length=7, verbose_name="Kolor zaznaczenia w kalendarzu")
