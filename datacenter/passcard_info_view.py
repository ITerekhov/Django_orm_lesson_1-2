from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    serialized_visits = []
    visits = Visit.objects.filter(passcard=passcard)
    for visit in visits:
        duration = visit.format_duration()
        visit_details = {
            'entered_at': visit.entered_at,
            'duration': duration,
            'is_strange': visit.is_visit_long()}
        serialized_visits.append(visit_details)
    context = {
        'passcard': passcard,
        'this_passcard_visits': serialized_visits
    }
    return render(request, 'passcard_info.html', context)
