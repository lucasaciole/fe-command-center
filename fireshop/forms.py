from django import forms
from .models import Event
from tempus_dominus.widgets import DateTimePicker

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'date', 'has_party_planning']
        widgets = {'date': DateTimePicker(options={
            'format': 'D/M/YYYY H:mm:ss'
            })}
