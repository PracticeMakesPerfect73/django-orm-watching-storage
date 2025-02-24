from django.utils.timezone import localtime, now
import datetime

SECONDS_IN_HOUR = 3600
SECONDS_IN_MINUTE = 60


def get_duration(visit):
    return format_duration(
        (visit.leaved_at or now()) - visit.entered_at
    )


def format_duration(duration):
    seconds = duration.total_seconds()
    hours = seconds // SECONDS_IN_HOUR
    minutes = (seconds % SECONDS_IN_HOUR) // SECONDS_IN_MINUTE
    return f'{int(hours)}ч {int(minutes)}м'


def is_visit_long(visit, minutes=60):
    end_time = visit.leaved_at or now()
    return (
        localtime(end_time) - localtime(visit.entered_at)
    ) >= datetime.timedelta(minutes=minutes)
