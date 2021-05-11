from django import forms

from .models import Patient

class PatientForm(forms.ModelForm):

    class Meta:
        model = Patient
        fields = ('id', 'name','Aadhar_num','contact_number','date_of_birth','gender','email',)
