from calendar import HTMLCalendar
from datetime import timedelta
from .models import Event
from django.db.models import Q

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, events):
        filtered_events = events.filter(end_time__day__gte=day, start_time__day__lte=day)
        d = ''
        for event in filtered_events:
            d+= f'<li> {event.title} </li>'

        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'
    

    def formatweek(self, theweek, events):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True, user_id=1):
        events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month, user_id=user_id)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events)}\n'
        return cal

    def prev_month(d):
        prev_month = d.replace(day=1) - timedelta(days=1)
        return f"{prev_month.year}-{prev_month.month:02d}"

    def next_month(d):
        next_month = (d.replace(day=1) + timedelta(days=32)).replace(day=1)
        return f"{next_month.year}-{next_month.month:02d}"
