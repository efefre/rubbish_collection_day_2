from schedule.models import ScheduleConfiguration


def get_link_to_original_schedule(request):
    config = ScheduleConfiguration.get_solo()
    return {
        "link_to_original_schedule": config.original_schedule
    }
