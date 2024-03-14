from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from .models import Event, Location
from django.contrib.auth.models import User 
from datetime import datetime
from .forms import LocationForm, EventForm, EventFormAdmin
from django.http import HttpResponseRedirect, HttpResponse , FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator
from django.contrib import messages
import os

 
import csv
import pytz


def my_dashboard(request,):
    if request.user.is_authenticated:
        attending_events = Event.objects.filter(attendees=request.user.id).order_by("event_date")
        planned_events = Event.objects.filter(manager=request.user.id)
        owned_location = Location.objects.filter(owner= request.user.id)
        
        
        return_page = "my-dashboard"
        
        return render(request, "events/my_dashboard.html", {"attending_events": attending_events, 
                                                            "planned_events":planned_events, 
                                                            "return_page":return_page, 
                                                            "owned_location":owned_location,
                                                            "return_page": return_page,
                                                            })
    else:
        messages.success(request, ("access denied"))
        return redirect("home")
    
    


def events_by_location(request, location_id, return_page ):
    location = Location.objects.get(id=location_id)
    events = location.event_set.all().order_by("-event_date")
    
    if events:
        return render(request,"events/events_by_location.html", {"location_id":location_id,  "location": location, "events":events}, )
    else:
        messages.success(request, ("location has no events"))
        return redirect(return_page)
       

def attendees_by_event(request, event_id,):
    event = Event.objects.get(id=event_id)
    
    attendees = event.attendees.all()
    if attendees:
        return render(request,"events/attendees_by_event.html", {"event_id":event_id,  "event": event, "attendees":attendees})
    else:
        messages.success(request, ("event has no attendees"))
        return redirect("my-dashboard",request.user.id)
    


def admin_panel(request):
    events = Event.objects.all().order_by("-event_date")
    location_list = Location.objects.all()
    event_count = Event.objects.count()
    location_count = Location.objects.count()
    user_count = User.objects.count()
    return_page = 'admin-panel'

    if request.user.is_superuser:
        if request.method == "POST":
            id_list = request.POST.getlist("approved-checkbox")
            events.update(approved=False)
            for event_id in id_list:
                Event.objects.filter(pk=int(event_id)).update(approved=True)
            
            messages.success(request, ("approval updated"))
            return redirect(return_page)
        else:
            return render(request, "events/admin_panel.html", {"events":events, 
                                                               "event_count":event_count, 
                                                               "location_count":location_count, 
                                                               "user_count":user_count, 
                                                               "location_list":location_list,
                                                               "return_page":return_page
                                                               })
    else:
        messages.success(request, ("access denied"))
        return redirect("home")
   
def attend_event(request, event_id, return_page):
    new_attendee = request.user.pk
    event = Event.objects.get(id=event_id)
    event.attendees.add(new_attendee)
    event.save()

    messages.success(request,(f"you attended {event}") )
    return redirect(return_page)
    
def cancel_event(request, event_id, return_page):
    new_attendee = request.user.pk
    event = Event.objects.get(id=event_id)
    event.attendees.remove(new_attendee)
    event.save()

    messages.success(request,(f"you canceled {event}") )
    return redirect(return_page)
    




    



def location_pdf(request):
    buf = io.BytesIO()
    c = canvas.Canvas(buf ,pagesize=letter, bottomup=0)
    text_object = c.beginText()
    text_object.setTextOrigin(inch,inch)
    text_object.setFont("Helvetica", 14)

    locations = Location.objects.all()
    lines = []
    for location in locations:
        text_object.textLine(location.name)
        text_object.textLine(location.address)
        text_object.textLine(location.zip_code)
        text_object.textLine(location.phone_number)
        text_object.textLine(location.website)
        text_object.textLine(location.email)
        text_object.textLine("")

    c.drawText(text_object)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename="location.pdf")

def location_csv(request):

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=locations.csv"

    writer = csv.writer(response)
    
   
    locations = Location.objects.all()
    writer.writerow(
            [
                "name",
                "address",
                "zip_code",
                "phone_number",
                "website",
                "email",
            ]
        )
    for location in locations:
            writer.writerow(
                [
                    location.name,
                    location.address,
                    location.zip_code,
                    location.phone_number,
                    location.website,
                    location.email,
                ]
            )

    
    return response


def location_txt(request):
    response = HttpResponse(content_type="text/plain")
    response["Content-Disposition"] = "attachment; filename=location.txt"
    locations = Location.objects.all()

    lines = []
    for location in locations:
        lines.append(
            f"{location.name}\n"
            f"{location.address}\n"
            f"{location.zip_code}\n"
            f"{location.phone_number}\n"
            f"{location.website}\n"
            f"{location.email}\n\n\n"
        )
    response.writelines(lines)
    return response


def search(request,):
    return_page = 'search-location'
    if request.method == "POST":
        new_searched = request.POST["searched"]
        locations = Location.objects.filter(name__contains=new_searched)
        events = Event.objects.filter(name__contains=new_searched)
        return render(
            request,
            "events/search.html",
            {"searched": new_searched, "locations": locations, "events": events, "return_page":return_page},
        )

    else:
        return render(
            request,
            "events/search.html",
        )


def show_location(request, location_id, return_page):
    location = Location.objects.get(pk=location_id)
    location_owner = User.objects.get(pk=location.owner.pk)
    
    return render(request, "events/show_location.html", {"location": location,
                                                          "location_owner": location_owner,
                                                          "return_page": return_page
                                                          })


def all_locations(request):
    # location_list = Location.objects.all().order_by("name")
    # location_list = Location.objects.all()
    pagination = Paginator(Location.objects.all(),25)
    page = request.GET.get("page")
    pages = pagination.get_page(page)
    nums = "a" * pages.paginator.num_pages
    return_page = 'list-locations'

    return render(
        request, "events/location_list.html", { "pages":pages, "nums":nums , "return_page":return_page}
        
    )


def my_location(request):
    return_page = 'my-location'
    if request.user.is_authenticated:
        
        
        pagination = Paginator(Location.objects.filter(owner=request.user.id),5)
        
        page = request.GET.get("page")
        pages = pagination.get_page(page)
        nums = "a" * pages.paginator.num_pages
        return render(request, "events/my_location.html", { "pages":pages, "nums":nums, "return_page":return_page,})
    else:
        messages.success(request, ("access denied"))
        return redirect("home")
    
def all_events(request):
    
    show_pagination = True
    events = Event.objects.all().order_by("event_date")
    up_coming_events = []
    for event in events:
        
        if event.Days_Till > "0 ":
            up_coming_events.append(event)
    
    pagination = Paginator(up_coming_events,5)
    # pagination = Paginator(Event.objects.all().order_by("event_date"),50)
    page = request.GET.get("page")
    pages = pagination.get_page(page)
    nums = "a" * pages.paginator.num_pages
    return_page = "list-events"
    
    if request.user.id == None:
        current_user_events = []
    else:
        current_user_events = Event.objects.filter(attendees=request.user)
    
    return render(request, "events/events_list.html", { "current_user_events":current_user_events, "pages":pages, "nums":nums, "return_page":return_page, "show_pagination": show_pagination})

def my_events(request):
    if request.user.is_authenticated:
        show_pagination = True
        pagination = Paginator(Event.objects.filter(attendees=request.user.id).order_by("event_date"),5)
        page = request.GET.get("page")
        pages = pagination.get_page(page)
        nums = "a" * pages.paginator.num_pages
        current_user_events = Event.objects.filter(attendees=request.user)
        return_page = "my-events"
    
        
        return render(request, "events/my_events.html", {"current_user_events":current_user_events, "pages":pages, "nums":nums, "return_page":return_page, "show_pagination": show_pagination})
    else:
        messages.success(request, ("access denied"))
        return redirect("home")

def show_event(request, event_id, return_page):
    event = Event.objects.get(pk=event_id)

    return render(request, "events/show_event.html", {"event": event, "return_page":return_page})



def add_location(request):
    submitted = False
    if request.method == "POST":
        
        form = LocationForm(request.POST,request.FILES)
        if form.is_valid():
            location = form.save(commit=False)
            location.owner = request.user
            location.save()
            messages.success(request,("location added"))
            return redirect("list-locations")
            
    else:
        form = LocationForm
        if "submitted" in request.GET:
            submitted = True

    return render(
        request,
        "events/add_location.html",
        {"form": form, "submitted": submitted},
    )

def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request,("event added"))
                return redirect("list-events")
                # return HttpResponseRedirect("/events/add/?submitted=True")


        else:
            form = EventForm(request.POST,request.FILES)
            # print(request.user)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
                messages.success(request,("event added"))
                return redirect("list-events")
                # return HttpResponseRedirect("/events/add/?submitted=True")

    else:
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm
        if "submitted" in request.GET:
            submitted = True

    return render(
        request, "events/add_event.html", {"form": form, "submitted": submitted}
    )



def update_location(request, location_id, return_page):
    location = Location.objects.get(pk=location_id)
    file_to_delete = location.location_image
    form = LocationForm(request.POST or None, request.FILES or None, instance=location)
    
    if form.is_valid():
        if len(request.FILES)  == 0 :
            form.save()
        elif len(request.FILES) > 0:
            if file_to_delete == "":
                form.save()
            else:
                print(file_to_delete.path)
                os.remove(file_to_delete.path)
                form.save()

        messages.success(request,("location updated"))
        return redirect(return_page)
    
    return render(
        request,
        "events/update_location.html",
        {"location": location, "form": form},
    )

def update_event(request, event_id,return_page):
    event = Event.objects.get(pk=event_id)
    file_to_delete = event.event_image
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, request.FILES or None, instance=event)
    else:
        form = EventForm(request.POST or None, request.FILES or None, instance=event)
    if form.is_valid():
        if len(request.FILES)  == 0 :
            form.save()
        elif len(request.FILES) > 0:
            if file_to_delete == "":
                form.save()
            else:
                print(file_to_delete.path)
                os.remove(file_to_delete.path)
                form.save()
        messages.success(request,("event updated"))
        return redirect(return_page)
    return render(
        request,
        "events/update_event.html",
        {"event": event, "form": form},
    )












def delete_event(request, event_id, return_page):
    event = Event.objects.get(pk=event_id)
    if request.user == event.manager: 
        event.delete()
        messages.success(request,("event deleted"))
        return redirect(return_page)
    else:
        messages.success(request,("you are not authorized to delete this"))
        return redirect(return_page)

def delete_location(request, location_id, return_page):
    location = Location.objects.get(pk=location_id)

    if request.user == location.owner:
        location.delete()
        messages.success(request,("location deleted"))
        return redirect(return_page)
    else:
        messages.success(request,("you are not authorized to delete this"))
        return redirect(return_page)


def home(request, year=int(datetime.now().year), month=datetime.now().strftime("%B")):
    
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)
    cal = HTMLCalendar(firstweekday=0).formatmonth(year, month_number)
    timezone = pytz.timezone("Europe/Amsterdam")
    now = datetime.now(timezone).strftime(" %H:%M %A %-d %B %Y")
    
    return_page = "home"
    events_list = Event.objects.filter(
        event_date__year = year,
        event_date__month = month_number,

    )
    

    return render(
        request,
        "events/home.html",
        {
            
            "year": year,
            "month": month,
            "month_number": month_number,
            "cal": cal,
            "time": now,
            "events_list": events_list,
            "return_page": return_page,
            
        },
    )


def add_location_data_to_database(request):
    from .models import  Location
    with open("events/data.csv", "r", newline="") as csv_file:
        spamreader = csv.reader(csv_file, delimiter=',', )
        for row in spamreader:
            location = Location(name=row[0], address=row[1], zip_code=row[2], phone_number=row[3], website=row[4], email=row[5], )
            location.save()
            print(location)

