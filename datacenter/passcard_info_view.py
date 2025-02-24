from datacenter.models import Visit, Passcard
from django.utils.timezone import localtime
from django.shortcuts import render, get_object_or_404
from datacenter.check_visit_info import get_duration, is_visit_long


def passcard_info_view(request, passcode):
    passcard = get_object_or_404(Passcard, passcode=passcode)
    visits = Visit.objects.filter(passcard=passcard).order_by('-entered_at')

    this_passcard_visits = [
        {
            'entered_at': localtime(visit.entered_at),
            'duration': get_duration(visit),
            'is_strange': is_visit_long(visit),
        }
        for visit in visits
    ]

    context = {
        'passcard': passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
