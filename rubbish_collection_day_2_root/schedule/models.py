from django.db import models
from solo.models import SingletonModel


# Create your models here.
class ScheduleConfiguration(SingletonModel):
    site_name = models.CharField(max_length=255, verbose_name="Nazwa strony")
    maintenance_mode = models.BooleanField(
        default=False, verbose_name="Przerwa techniczna"
    )
    year = models.CharField(max_length=4, verbose_name="Rok", unique=True)
    original_schedule = models.CharField(
        max_length=255,
        verbose_name="Link do harmonogramu",
        help_text="Link do harmonogramu opublikowanego na stronie Urzędu Miasta",
    )

    def __str__(self):
        return f"Konfiguracja strony: {self.site_name}"

    class Meta:
        verbose_name = "Konfiguracja harmonogramu"


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

    name = models.CharField(max_length=200, verbose_name="Nazwa rejonu")
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
        Date, related_name="districts", blank=True, verbose_name="Daty"
    )

    def __str__(self):
        return f"{self.city_type.capitalize()} - {self.rubbish_type}: {self.name}"

    class Meta:
        verbose_name_plural = "Rejony odbioru odpadów"
        verbose_name = "Rejon"
        unique_together = ("name", "city_type", "rubbish_type")
