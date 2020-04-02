from django.db import models


# Create your models here.
class City(models.Model):
    name = models.CharField(max_length=40, verbose_name="Miejscowość")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name')
        verbose_name_plural = "Miejscowości"
        verbose_name = "Miejscowość"
