from datacenter.models import Visit
from django.shortcuts import render


def storage_information_view(request):
    serialized_visits = []
    non_closed_visits = Visit.objects.filter(leaved_at=None)
    for visit in non_closed_visits:
        duration = visit.format_duration()
        data = {
            'who_entered': visit.passcard.owner_name,
            'entered_at': visit.entered_at,
            'duration': duration}
        serialized_visits.append(data)
    context = {
        'non_closed_visits': serialized_visits, 
    }
    return render(request, 'storage_information.html', context)
