
from django.urls import path 
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('<int:year>/<str:month>/', views.home, name="home"),
    path("events/", views.all_events, name="list-events"),
    # path("events/search", views.search_events, name="search-events"),
    path("events/my_events", views.my_events, name="my-events"),
    path("events/my_locations", views.my_location, name="my-location"),
    path("events/<event_id>/<return_page>", views.show_event, name="show-event"),
    path("events/add/", views.add_event, name="add-event"),
    path("events/delete/<event_id>/<return_page>", views.delete_event, name="delete-event"),
    path("events/update/<event_id>/<return_page>", views.update_event, name="update-event"),
    path("locations/", views.all_locations, name="list-locations"),
    path("locations/search/", views.search, name="search-location"),
    path("locations/<location_id>/<return_page>", views.show_location, name="show-location"),
    path("add_location/", views.add_location, name="add-location"),
    path("locations/update/<location_id>/<return_page>", views.update_location, name="update-location"),
    path("locations/delete/<location_id>/<return_page>", views.delete_location, name="delete-location"),
    path("location/txt_file", views.location_txt, name="location-txt"),
    path("location/csv_file", views.location_csv, name="location-csv"),
    path("location/pdf_file", views.location_pdf, name="location-pdf"),
    path("attend_event/<event_id>/<return_page>", views.attend_event, name="attend-event"),
    path("cancel_event/<event_id>/<return_page>", views.cancel_event, name="cancel-event"),
    path("admin_panel", views.admin_panel, name="admin-panel"),
    path("events_by_location/<int:location_id>/<return_page>", views.events_by_location, name="events-by-location"),
    path("my_dashboard/", views.my_dashboard, name="my-dashboard"),
    # path("location/pdf_file", views.add_location_data_to_database, name="location-pdf"),
   path("attendees_by_location/<event_id>", views.attendees_by_event, name="attendees-by-location")
]
