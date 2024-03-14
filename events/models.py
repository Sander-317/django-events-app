from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime


class Location(models.Model):
    name = models.CharField("Location Name",max_length=255)
    address = models.CharField("Location Address",max_length=255)
    zip_code = models.CharField("Location Zip Code",max_length=20)
    phone_number = models.CharField("Location Phone Number",max_length=20)
    website = models.URLField("Location Website",max_length=255, blank=True)
    email = models.EmailField("Location Email", blank=True)
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    # owner = models.IntegerField("location owner", blank=False ,default=1)
    location_image = models.ImageField("location image", blank=True ,upload_to="images/")

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField("Event Name",max_length=255)
    event_date = models.DateTimeField("Event Date")
    location = models.ForeignKey(Location, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(" Event Description", null=True, blank=True)
    attendees = models.ManyToManyField(User, blank=True, related_name="attendee")
    approved = models.BooleanField("approved", default=False)
    event_image = models.ImageField("event image", blank=True ,upload_to="images/")

    def __str__(self):
        return self.name
    
    @property
    def Days_Till(self):
        today = date.today()
        days_till = self.event_date.date() - today
        days_till_stripped = str(days_till).split(",",1)[0]
        
        return days_till_stripped
    
    @property
    def Is_Past(self):
        today = date.today()
        if self.event_date.date() < today:
            thing = "past"
        else:
            thing = "up cumming"
        
        return thing
        
