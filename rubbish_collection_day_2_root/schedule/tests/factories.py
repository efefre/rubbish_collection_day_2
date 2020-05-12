import datetime
import factory
import factory.fuzzy
from schedule.models import (ScheduleConfiguration, Date,
                             RubbishType, RubbishDistrict)
from city_detail.models import City, Street, Address


class ScheduleConfigurationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ScheduleConfiguration

    site_name = "Test Page"
    maintenance_mode = False
    year = 2020
    original_schedule = "www.original.localhost.pl"


class DateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Date

    date = factory.fuzzy.FuzzyDate(
        datetime.date(2020, 1, 1), datetime.date(2021, 3, 31),
    )


class RubbishTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RubbishType

    name = factory.Iterator(
        ["All Rubbish", "Bio Rubbish", "Recycled Rubbish",
         "Ash", "Big Rubbish"],
        cycle=False,
    )
    mark_color = factory.Iterator(
        ["#F45B70", "#70CEAE", "#6095BD", "#9E9E9E", "#BC8F71"], cycle=False
    )
    css_name = factory.Iterator(
        ["all", "bio", "rec", "ash", "big"], cycle=False
    )


class RubbishDistrictFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = RubbishDistrict

    name = "Rejon 1"
    city_type = "miasto"
    rubbish_type = factory.SubFactory(RubbishTypeFactory)

    @factory.post_generation
    def date(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for day in extracted:
                self.date.add(day)


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City

    name = "Wołomin"
    city_type = "miasto"


class StreetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Street

    name = factory.Iterator(["Polna", "Ogrodowa"], cycle=False)


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    city = factory.SubFactory(CityFactory)
    street = factory.SubFactory(StreetFactory)
