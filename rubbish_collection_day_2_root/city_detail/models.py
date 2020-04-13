from django.db import models
from schedule.models import RubbishDistrict


# Create your models here.
class City(models.Model):
    CITY_TYPE_OPTION = [
        ("gmina", "Gmina"),
        ("miasto", "Miasto"),
    ]

    name = models.CharField(max_length=40, verbose_name="Miejscowość")

    city_type = models.CharField(
        choices=CITY_TYPE_OPTION,
        default="gmina",
        verbose_name="Typ miejscowości",
        max_length=10,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Miejscowości"
        verbose_name = "Miejscowość"


class Street(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ulica")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Ulice"
        verbose_name = "Ulica"


class Address(models.Model):
    city = models.ForeignKey(
        City, on_delete=models.SET_NULL, null=True, verbose_name="Miasto"
    )
    street = models.ForeignKey(
        Street, on_delete=models.SET_NULL, null=True, verbose_name="Ulica"
    )

    rubbish_district = models.ManyToManyField(
        RubbishDistrict, related_name="addresses", verbose_name="Rejon",
    )

    def __str__(self):
        return f"{self.city.name}, {self.street.name}"

    class Meta:
        verbose_name_plural = "Adresy odbioru odpadów"
        verbose_name = "Adres odbioru odpadów"
        unique_together = ("city", "street")
