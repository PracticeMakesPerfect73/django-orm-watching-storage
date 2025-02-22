from datacenter.models import Visit, Passcard
from django.utils.timezone import localtime, now
from django.shortcuts import render, get_object_or_404
import datetime


def format_duration(duration):
    seconds = duration.total_seconds()
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f'{int(hours)}ч {int(minutes)}м'


def is_visit_long(visit, minutes=60):
    if visit.leaved_at is not None:
        end_time = visit.leaved_at
    else:
        end_time = now()
    return (localtime(end_time) - localtime(visit.entered_at)) >= datetime.timedelta(minutes=minutes)


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard).order_by('-entered_at')

    this_passcard_visits = [
        {
            'entered_at': localtime(visit.entered_at),
            'duration': format_duration((visit.leaved_at or now())
                                        - visit.entered_at),
            'is_strange': is_visit_long(visit),
        }
        for visit in visits
    ]

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
