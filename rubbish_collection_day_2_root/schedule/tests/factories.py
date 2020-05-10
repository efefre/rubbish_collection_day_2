import datetime
import factory
from schedule.models import ScheduleConfiguration, Date, RubbishType


class ScheduleConfigurationFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = ScheduleConfiguration

    site_name = "Test Page"
    maintenance_mode = False
    year = 2020
    original_schedule = "www.original.localhost.pl"


class DateFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Date

    date = factory.fuzzy.FuzzyDate(
        datetime.date(2020, 1, 1), datetime.date(2021, 3, 31),
    )


class RubbishTypeFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = RubbishType

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
