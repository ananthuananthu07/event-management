from datetime import datetime
from django.conf import settings

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    is_company = models.BooleanField(default=False)     # TICK OR NON_TICK
    is_customer = models.BooleanField(default=False)


def default_profile_pic():
    return "comp_images/d7.jpg"


class EventsClass(models.Model):
    title = models.CharField(max_length=100,null=True)
    description = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True, upload_to='event_images')

    def __str__(self):
        return self.title


class Categories(models.Model):
    event_name = models.CharField(max_length=100, null=True)
    event_des = models.CharField(max_length=500, null=True)
    event_image = models.ImageField(null=True, upload_to='category_images')
    event_prize = models.IntegerField(null=True)

    def __str__(self):
        return self.event_name


class CompanyProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='comp_profile')
    comp_type = models.ForeignKey(Categories, on_delete=models.CASCADE,related_name='company_profiles', null=True)
    comp_location = models.CharField(max_length=100, null=True)
    comp_id = models.IntegerField(null=True)
    comp_image = models.ImageField(upload_to='comp_images',default=default_profile_pic)
    comp_contact = models.CharField(max_length=12, null=True)
    comp_bio = models.TextField(null=True)
    comp_agent = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.user)


class Review(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Message from {self.reviewer.username}"


class Appointment(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    date = models.DateTimeField()
    details = models.TextField(null=True,blank=False)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'Appointment with {self.company.user.username} on {self.date}'


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class GalleryPhoto(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='gallery_photos')
    image = models.ImageField(upload_to='img_gallery')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.company}"


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_company_user = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}"


class Booking(models.Model):
    company_name = models.ForeignKey(User, on_delete=models.CASCADE)
    comp_cat = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100, null=True)
    customer_number = models.CharField(max_length=15, null=True)
    customer_email = models.EmailField()
    district = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=200, null=True)
    landmark = models.CharField(max_length=200, null=True)
    date = models.DateField()
    duration = models.PositiveIntegerField(null=True)
    food_type_choices = [
        ('Boffey', 'Boffey'),
        ('A la carte', 'A la carte'),
        ('Default', 'Default'),
    ]
    food_type = models.CharField(max_length=20, choices=food_type_choices)
    dj_party_needed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer_name}'s Booking"


# PAYMENT MODEL


class Payment(models.Model):
    PAYMENT_OPTIONS = [
        ('debit_card', 'Debit Card'),
        ('net_banking', 'Net Banking'),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    option = models.CharField(max_length=20, choices=PAYMENT_OPTIONS)
    card_holder_name = models.CharField(max_length=100, blank=True, null=True)
    card_number = models.CharField(max_length=16, blank=True, null=True)
    cvv_number = models.CharField(max_length=3, blank=True, null=True)
    expiry_date = models.CharField(max_length=5, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=14, blank=True, null=True)
    ifsc_code = models.CharField(max_length=15, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    email = models.EmailField(blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        if self.booking:
            return f"{self.booking.customer_name}'s Payment"
        else:
            return "Unassociated Payment"


class MessageStatus(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.user


