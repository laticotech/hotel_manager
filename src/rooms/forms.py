from django import forms

class AvailabilityForm(forms.Form):
    room_name = forms.CharField(required=True)
    check_in = forms.DateTimeField(required=True, input_formats=['\Y-\m-\dT\H:\M'])
    check_out = forms.DateTimeField(required=True, input_formats=['\Y-\m-\dT\H:\M'])
