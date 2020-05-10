import datetime
import factory
from schedule.models import ScheduleConfiguration, Date


class ScheduleConfigurationFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = ScheduleConfiguration

    site_name = 'Test Page'
    maintenance_mode = False
    year = 2020
    original_schedule = 'www.original.localhost.pl'


class DateFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = Date

    date = factory.fuzzy.FuzzyDate(
        datetime.date(2020, 1, 1),
        datetime.date(2021, 3, 31),
    )
