from datacenter.models import Visit
from django.shortcuts import render
from django.utils.timezone import localtime
from datacenter.check_visit_info import get_duration


def storage_information_view(request):
    current_visitors = Visit.objects.filter(leaved_at__isnull=True)
    non_closed_visits = [
        {
            'who_entered': visitor.passcard,
            'entered_at': localtime(visitor.entered_at),
            'duration': get_duration(visitor),
        }
        for visitor in current_visitors
    ]

    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
