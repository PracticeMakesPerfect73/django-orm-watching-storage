from datacenter.models import Visit, Passcard
from django.shortcuts import render
from django.utils.timezone import localtime, now


def get_duration(visit):
    delta = now() - visit.entered_at
    return delta


def format_duration(duration):
    seconds = duration.total_seconds()
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return f'{int(hours)}ч {int(minutes)}м'


def storage_information_view(request):
    current_visitors = Visit.objects.filter(leaved_at__isnull=True, passcard__is_active=True)
    non_closed_visits = []
    for visitor in current_visitors:
        duration = get_duration(visitor)
        non_closed_visits.append({
            'who_entered': visitor.passcard,
            'entered_at': localtime(visitor.entered_at),
            'duration': format_duration(duration),
        })

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
