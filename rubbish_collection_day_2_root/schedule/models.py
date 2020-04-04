from django.db import models
from city_detail.models import Address


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
    mark_color = models.CharField(
        max_length=7,
        verbose_name="Kolor zaznaczenia w kalendarzu",
        unique=True,
        help_text="Podaj HEX zaczynająć od #. ",
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Frakcje śmieci"
        verbose_name = "Frakcja"


class RubbishDistrict(models.Model):
    CITY_TYPE_OPTION = [
        ("gmina", "Gmina"),
        ("miasto", "Miasto"),
    ]

    name = models.CharField(max_length=200, verbose_name="Nazwa")
    city_type = models.CharField(
        choices=CITY_TYPE_OPTION,
        default="gmina",
        verbose_name="Typ miejscowości",
        max_length=10,
    )
    rubbish_type = models.ForeignKey(
        RubbishType,
        related_name="districts",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name="Frakcja",
    )
    date = models.ManyToManyField(
        Date, related_name="districts", null=True, verbose_name="Daty"
    )
    address = models.ManyToManyField(
        Address,
        related_name="districts",
        null=True,
        verbose_name="Adres odbioru odpadów",
        help_text="Adresy należące do tego regionu.",
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Rejony odbioru odpadów"
        verbose_name = "Rejon"
        unique_together = ("name", "city_type", "rubbish_type")
