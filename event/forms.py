from django import forms
from .models import Event, EventDetails

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ( "event_id","name","start_date","end_date","time","description","organizer",
                  "max_count","budget","venue")
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date",}),
            "end_date": forms.DateInput(attrs={"type": "date",}),
            "time": forms.TimeInput(attrs={"type": "time",}),
            "description": forms.Textarea(attrs={"rows": 4, "cols": 15}),
        }
        
class EventStatusForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("status",)

class EventUpdateForm(forms.ModelForm):
    class Meta:
        model = EventDetails
        fields = ("event", "report_details", "feedback_text", "rating", "participant_count", "image")

        report_details = forms.FileField(required=False)
        feedback_text = forms.FileField(required=False)
        rating = forms.FileField(required=False)
        participant_count = forms.FileField(required=False)
        image = forms.ImageField(required=False)
        widgets = {
            "report_details": forms.ClearableFileInput(attrs={"multiple": False}),
            "feedback_text": forms.ClearableFileInput(attrs={"multiple": False}),
            "rating": forms.ClearableFileInput(attrs={"multiple": False}),
            "participant_count": forms.ClearableFileInput(attrs={"multiple": False}),
            "image": forms.ClearableFileInput(attrs={"multiple": False}),
        }