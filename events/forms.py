from django import forms
from django.forms import ModelForm
from .models import Location, Event
from bootstrap_datepicker_plus.widgets import DateTimePickerInput ,DatePickerInput
class LocationForm(ModelForm):
    class Meta:
        model = Location
        fields = ('name', 'address', 'zip_code', 'phone_number', 'website', 'email', "location_image")
        labels = {
            'name': "",
            'address': "",
            'zip_code': "",
            'phone_number': "",
            'website': "",
            'email': "",
            "location_image":"",

        }
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter location name"}),
            'address': forms.TextInput(attrs={"class": "form-control","placeholder": "Enter location address" }),
            'zip_code': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter location zip code"}),
            'phone_number': forms.TextInput(attrs={"class": "form-control","placeholder": "Enter location phone number"}),
            'website': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter location website"}),
            'email': forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter location email"}),
            'location_image': forms.FileInput({"class": "form-control", "placeholder": "upload image"}),
            }


class EventFormAdmin(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 
                  'location', 'manager', 
                  'attendees', 
                  'description',
                  'event_image', 
                  )
        labels = {
            'name': "",
            'event_date': "YYYY-MM-DD HH:MM:SS",
            'location': "location",
            'manager': "manager",
            'attendees': "attendees",
            'description': "",
            'event_image':"", 
            }
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter event name"}), 
            # 'event_date': DatePickerInput() ,
            # 'event_date': DateTimePickerInput(attrs={"class": "form-control bootstrap-datepicker", "placeholder": "Enter event date " ,"name":"date",}) ,
            'event_date': forms.DateTimeInput(attrs={"class": "form-control bootstrap-datepicker", "placeholder": "Enter event date"}) ,
            'location': forms.Select(attrs={"class": "form-select", "placeholder": "Enter event name"}), 
            'manager': forms.Select(attrs={"class": "form-select", "placeholder": "Enter event name"}), 
            'attendees': forms.SelectMultiple(attrs={"class": "form-control", "placeholder": "Enter event name"}), 
            'description': forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter event description"}),
            'event_image': forms.FileInput(attrs={"class": "form-control", "placeholder": "upload image"}),

        }

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 
                  'location',  
                #   'attendees', 
                  'description',
                  'event_image' , 
                  )
        labels = {
            'name': "",
            'event_date': "YYYY-MM-DD HH:MM:SS",
            'location': "location",
           
            # 'attendees': "attendees",
            'description': "",
            'event_image' : "",
            }
        widgets = {
            'name': forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter event name"}), 
            'event_date': forms.DateTimeInput(attrs={"class": "form-control", "placeholder": "Enter event date"}) ,
            'location': forms.Select(attrs={"class": "form-select", "placeholder": "Enter event name"}), 
            
            # 'attendees': forms.SelectMultiple(attrs={"class": "form-control", "placeholder": "Enter event name"}), 
            'description': forms.Textarea(attrs={"class": "form-control", "placeholder": "Enter event description"}),
            'event_image': forms.FileInput(attrs={"class": "form-control", "placeholder": "upload image"}),

        }
