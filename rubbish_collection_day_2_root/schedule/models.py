from django.db import models
from solo.models import SingletonModel


# Create your models here.
class ScheduleConfiguration(SingletonModel):
    site_name = models.CharField(
        max_length=255, verbose_name="Nazwa strony", default="Calendar"
    )
    maintenance_mode = models.BooleanField(
        default=False, verbose_name="Przerwa techniczna"
    )
    year = models.IntegerField(verbose_name="Rok", unique=True, default=2020)
    original_schedule = models.CharField(
        max_length=255,
        verbose_name="Link do harmonogramu",
        help_text="Link do harmonogramu opublikowanego na stronie UM",
        default="localhost",
    )
    last_update = models.CharField(
        max_length=100, verbose_name="Nazwa strony", default="marzec 2020"
    )
    gtm_number = models.CharField(
        max_length=20, verbose_name="Identyfikator kontenera GTM", default="empty_number"
    )

    class Meta:
        verbose_name = "Konfiguracja harmonogramu"

    def __str__(self):
        return f"Konfiguracja strony: {self.site_name}"


class Date(models.Model):
    date = models.DateField(verbose_name="Data", unique=True)

    class Meta:
        verbose_name_plural = "Daty"
        verbose_name = "Data"

    def __str__(self):
        return f"{self.date}"


class RubbishType(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nazwa frakcji")
    mark_color = models.CharField(
        max_length=7,
        verbose_name="Kolor zaznaczenia w kalendarzu",
        unique=True,
        help_text="Podaj HEX zaczynająć od #. ",
    )
    css_name = models.CharField(
        max_length=3,
        verbose_name="Skrótowa nazwa frakcji",
        unique=True,
        help_text="Trzy litery związane z nazwą frakcji.",
    )

    class Meta:
        verbose_name_plural = "Frakcje śmieci"
        verbose_name = "Frakcja"

    def __str__(self):
        return f"{self.name}"


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

    class Meta:
        verbose_name_plural = "Rejony odbioru odpadów"
        verbose_name = "Rejon"
        unique_together = ("name", "city_type", "rubbish_type")

    def __str__(self):
        return f"{self.city_type.capitalize()} - {self.rubbish_type}: {self.name}"
