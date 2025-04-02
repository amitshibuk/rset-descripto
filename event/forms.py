from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ( "event_id","name","start_date","end_date","time","description","organizer",
                  "max_count","budget","venue")
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date",}),
            "end_date": forms.DateInput(attrs={"type": "date",})
        }
        
class EventStatusForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("status",)