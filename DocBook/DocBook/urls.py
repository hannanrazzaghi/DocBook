from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('booking.urls')),
]

admin.site.site_header = "DocBook Admin Panel"
admin.site.site_title = "DocBook Admin Panel"
admin.site.index_title = "Welcome to DocBook"