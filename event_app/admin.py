from django.contrib import admin
from .models import (EventsClass, Categories, User, CompanyProfile, Review, Appointment, Notification,
                     GalleryPhoto, Message, Booking, Payment, MessageStatus)

# Register your models here.
admin.site.register(EventsClass)
admin.site.register(Categories)
# admin.site.register(Company)
# admin.site.register(History)
admin.site.register(User)
admin.site.register(CompanyProfile)
admin.site.register(Review)
admin.site.register(Appointment)
admin.site.register(Notification)
admin.site.register(GalleryPhoto)
admin.site.register(Message)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(MessageStatus)
