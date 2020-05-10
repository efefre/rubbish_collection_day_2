import factory
from schedule.models import ScheduleConfiguration


class ScheduleConfigurationFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = ScheduleConfiguration

    site_name = 'Test Page'
    maintenance_mode = False
    year = 2020
    original_schedule = 'www.original.localhost.pl'
