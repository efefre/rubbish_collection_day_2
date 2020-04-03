from django.db import models


# Create your models here.
class Date(models.Model):
    date = models.DateField(verbose_name="Data")

    def __str__(self):
        return f"{self.date}"

    class Meta:
        verbose_name_plural = "Daty"
        verbose_name = "Data"
