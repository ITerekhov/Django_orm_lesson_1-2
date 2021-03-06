from django.db import models
import datetime
from django.utils import timezone

SECONDS_IN_HOUR = 3600
SECONDS_IN_MINUTE = 60


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )

    def get_duration(self):
        if not self.leaved_at:
            delta = timezone.localtime(timezone.now()) - self.entered_at
        else:
            delta = self.leaved_at - self.entered_at
        duration = datetime.timedelta.total_seconds(delta)
        return int(duration)
    
    def format_duration(self):
        duration = self.get_duration()
        hours = duration // SECONDS_IN_HOUR
        minutes = (duration % SECONDS_IN_HOUR) // SECONDS_IN_MINUTE
        seconds = duration % SECONDS_IN_MINUTE
        return datetime.time(hours, minutes, seconds).strftime("%H:%M:%S")

    def is_visit_long(self, minutes=60):
        duration = self.get_duration()
        return (duration // SECONDS_IN_MINUTE) > minutes
