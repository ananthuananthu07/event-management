from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Count
from django.db.models import F  # Import F if it's used for database queries

from django.db.models import Count, Case, When, IntegerField


from event_app.forms import CustomRegistrationForm, CompanySearchForm, ReviewForm, AppointmentForm, GalleryPhotoForm, \
    MessageForm, BookingForm, PaymentOptionForm, DebitCardPaymentForm, NetBankingPaymentForm
from event_app.models import EventsClass, Categories, CompanyProfile, Review, Appointment, Notification, User, \
    GalleryPhoto, Message, Booking, Payment, MessageStatus
from . forms import EventsForm, CategoryForm, CompanyProfileForm
# Create your views here.

def create_notification(user, content):
    Notification.objects.create(user=user, content=content)

# CREATING NOTIFICATIONS VIEW


def create_message_notification(sender, recipient, content):
    if isinstance(recipient, User):  # Check if recipient is a User instance
        recipient_user = recipient
    elif isinstance(recipient, CompanyProfile):  # Check if recipient is a LawyerProfile instance
        recipient_user = recipient.user
    else:
        raise ValueError("Recipient must be either a User or LawyerProfile instance.")

    notification_content = f"You have a new message from {sender.username}: {content[:50]}..."
    Notification.objects.create(user=recipient_user, content=notification_content)

# REGISTRATION VIEW
def register_view(request):
    form = CustomRegistrationForm()
    if request.method == 'POST':
        form = CustomRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # breaking of automatic data access from form
            user.is_company = form.cleaned_data['is_company']
            user.is_customer = form.cleaned_data['is_customer']
            user.save()

            return redirect('login')
    return render(request, 'register.html', {'form': form})

# LOGIN VIEW
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_company:
                login(request, user)

                return redirect('index')
            elif user.is_customer:
                login(request, user)

                return redirect('index')
        return HttpResponse(request, 'Invalid credentials or user type')
    return render(request, 'login.html')

# LOG OUT VIEW
def log_out(request):
    logout(request)
    return redirect('index')

# INDEX PAGE
def event_index(request):
    return render(request, 'event_export/index.html')

# ABOUT/STORY PAGE
def event_about(request):
    return render(request, 'event_export/about.html')

# CONTACT US PAGE VIEW
def event_contact(request):
    return render(request, 'event_export/contact.html')

# SIG IN PAGE VIEW
def event_signin(request):
    return render(request, 'event_export/sign-in.html')

# SIGN UP VIEW
def event_signup(request):
    return render(request, 'event_export/sign-up.html')

# CATEGORY ADD VIEW
def events_type(request):
    if request.method == "POST":
        type_form = CategoryForm(request.POST, request.FILES)
        if type_form.is_valid():
            type_form.save()

    type_form = CategoryForm

    return render(request, 'event_export/type_add.html', {'type_form': type_form})

# CATEGORY DISPLAY VIEW
def event_categories(request):
    categories = Categories.objects.all()

    return render(request, 'event_export/category.html', {'categories': categories})

# CATEGORY ASSOCIATED COMPANIES VIEW

@login_required(login_url="login")
def category_companies(request, category_id):
    category = get_object_or_404(Categories, id=category_id)
    companies = category.company_profiles.all()
    return render(request, 'category_companies.html', {'category': category, 'companies': companies})

# COMPANY PROFILE BUILD/EDIT FORM


def edit_company_profile(request):
    try:
        company_profile = CompanyProfile.objects.get(user=request.user)
    except CompanyProfile.DoesNotExist:
        company_profile = None

    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES, instance=company_profile)
        if form.is_valid():
            # Save the lawyer profile
            company_profile = form.save(commit=False)
            company_profile.user = request.user
            company_profile.save()

            # Update user model fields with form data or defaults
            user = request.user
            user.first_name = form.cleaned_data.get('first_name', user.first_name)
            user.email = form.cleaned_data.get('email', user.email)
            user.save()

            return redirect('profile')  # Redirect to the lawyer's profile page
    else:
        initial_data = {
            'first_name': request.user.first_name,
            'email': request.user.email,

        }
        form = CompanyProfileForm(instance=company_profile, initial=initial_data)

    return render(request, 'event_export/company_profile_form.html', {'form': form, 'company_profile':company_profile})

# FETCHING COMPANIES


@login_required(login_url="login")
def companylist(request):
    companies = CompanyProfile.objects.all()

    return render(request,'event_export/company_display.html',{'companies':companies})

# COMPANIES DISPLAY/SEARCHING PAGE


@login_required(login_url="login")
def search_companies(request):
    if request.method == 'GET':
        form = CompanySearchForm(request.GET)
        if form.is_valid():
            comp_type = form.cleaned_data.get('comp_type')
            comp_location = form.cleaned_data.get('comp_location')

            # Create a base queryset
            results = CompanyProfile.objects.all()

            # Apply filters based on the form input
            if comp_type:
                results = results.filter(comp_type__event_name__icontains=comp_type)

            if comp_location:
                results = results.filter(comp_location__icontains=comp_location)

            # You can add more filters for other criteria

            return render(request, 'event_export/company_display.html', {'results': results, 'form': form})

    else:
        form = CompanySearchForm()

    return render(request, 'event_export/company_display.html', {'form': form})

# SINGLE COMPANY DISPLAY VIEW


@login_required(login_url="login")
def single_company_view(request, id):
    company = get_object_or_404(CompanyProfile, id=id)
    client = request.user

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.company = company
            review.reviewer = client
            review.save()
            # return redirect('companies')  # Redirect to a confirmation page or dashboard
    else:
        review_form = ReviewForm()

    reviews = Review.objects.filter(company=company).order_by('-created_at')

    return render(request, 'event_export/company_view.html', {'company': company, 'review_form': review_form, 'reviews': reviews})

# SUCCESS MESSAGE VIEW
def success_view(request):
    return render(request, 'event_export/success.html')

# GALLERY ADD VIEW

def add_gallery_photo(request):
    if request.method == 'POST':
        form = GalleryPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the current user's company profile
            company_profile = CompanyProfile.objects.get(user=request.user)

            # Create a new GalleryPhoto instance
            photo = form.save(commit=False)

            # Assign the company profile to the photo
            photo.company = company_profile

            # Save the photo
            photo.save()

            return redirect('profile')  # Redirect to the appropriate URL after successful submission
    else:
        form = GalleryPhotoForm()

    return render(request, 'event_export/add_gallery_photo.html', {'form': form})

# GALLERY DISPLAY VIEW
def display_gallery(request,company_id):
    company = get_object_or_404(CompanyProfile, id=company_id)
    gallery_photos = GalleryPhoto.objects.filter(company=company)
    return render(request, 'event_export/gallery.html', {'company': company, 'gallery_photos': gallery_photos})

# CHATTING WITH USER AND COMPANY

@login_required
def chat_with_company(request, company_id):
    company = get_object_or_404(CompanyProfile, id=company_id)
    messages = Message.objects.filter(sender=request.user, recipient=company.user) | Message.objects.filter(sender=company.user, recipient=request.user)
    messages = messages.order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = company.user
            message.is_company_user = True
            message.save()
            return redirect('chat_with_company', company_id=company_id)
    else:
        form = MessageForm()

    return render(request, 'event_export/chat_with_company.html', {'company': company, 'messages': messages, 'form': form})

# CONTACT LIST/CHAT HISTORY VIEW
@login_required
def contact_list(request):
    # Get distinct usernames of users who have sent messages to the logged-in company profile user
    displayed_usernames = Message.objects.filter(recipient=request.user).values_list('sender__username', flat=True).distinct()

    return render(request, 'event_export/contact_list.html', {'displayed_usernames': displayed_usernames})


@login_required
def reply_to_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            reply_message = form.save(commit=False)
            reply_message.sender = request.user
            reply_message.recipient = message.sender
            reply_message.save()
            return redirect('contact_list')
    else:
        form = MessageForm()
    return render(request, 'event_export/reply_message.html', {'form': form})


@login_required
def chat_with_user(request, username):
    user = get_object_or_404(User, username=username)
    messages = Message.objects.filter(
        (Q(sender=request.user, recipient=user) | Q(sender=user, recipient=request.user))
    ).order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = user
            message.save()
            return redirect('chat_with_user', username=username)
    else:
        form = MessageForm()

    return render(request, 'event_export/chat_with_user.html', {'user': user, 'messages': messages, 'form': form})


# BOOKING FORM


def book_with_company(request, company_id):
    company = get_object_or_404(CompanyProfile, id=company_id)
    event_category = company.comp_type

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.company_name = company.user  # Assign the company's user instance
            booking.comp_cat = company
            booking.customer_email = request.user.email  #LAST MODIFIED Add this line to store the customer's email

            booking.save()

            # Create a notification for the company user
            notification_content = f"You have a new booking from {booking.customer_name}"
            create_notification(company.user, notification_content)

            messages.success(request, 'Booking successfully created!')
            return redirect('select_payment_option', booking_id=booking.id)
        else:
            messages.error(request, 'Failed to create booking. Please correct the errors below.')
    else:
        form = BookingForm()

    return render(request, 'event_export/booking.html',
                  {'form': form, 'company_name': company.user.username, 'event_category': event_category})


# BOOKINGS DISPLAY


@login_required
def company_bookings(request):
    # Retrieve the company profile associated with the current user
    company_profile = get_object_or_404(CompanyProfile, user=request.user)

    # Filter the bookings based on the company profile
    bookings = Booking.objects.filter(company_name=company_profile.user)

    return render(request, 'company_bookings.html', {'company_bookings': bookings})

# BOOKING DELETE OPTION VIEW
@login_required
def booking_delete(request, pk):
    booking = Booking.objects.get(pk=pk)
    if request.method == 'POST':
        booking.delete()
        return redirect('company_bookings')
    return render(request, 'booking_confirm_delete.html', {'booking': booking})

# BOOKING SUCCESS MESSAGE VIEW
def booking_success(request, booking_id):
    booking = Booking.objects.get(id=booking_id)  # Retrieve the booking object
    return render(request, 'event_export/booking_success.html', {'booking': booking})


# PAYMENT VIEWS


def select_payment_option(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
    except Booking.DoesNotExist:
        return render(request, 'error.html', {'message': 'Booking not found'}, status=404)

    # Check if a payment entry already exists for the booking
    payment, created = Payment.objects.get_or_create(booking=booking)

    if request.method == 'POST':
        form = PaymentOptionForm(request.POST, instance=payment)
        if form.is_valid():
            try:
                form.save()
            except IntegrityError:
                return render(request, 'error.html', {'message': 'Integrity error occurred'}, status=500)
            return redirect('debit_card_payment' if payment.option == 'debit_card' else 'net_banking_payment', booking_id=booking_id)
    else:
        form = PaymentOptionForm(instance=payment)

    return render(request, 'select_payment_option.html', {'form': form, 'booking': booking})

# PAYMENT OPTION- DEBIT CARD VIEW
def debit_card_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    payment, created = Payment.objects.get_or_create(booking=booking)

    if request.method == 'POST':
        form = DebitCardPaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('payment_success')
    else:
        form = DebitCardPaymentForm(instance=payment)

    return render(request, 'debit_card_payment.html', {'form': form})

# PAYMENT OPTION-NET BANKING VIEW
def net_banking_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    payment, created = Payment.objects.get_or_create(booking=booking)

    if request.method == 'POST':
        form = NetBankingPaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            return redirect('payment_success')
    else:
        form = NetBankingPaymentForm(instance=payment)

    return render(request, 'net_banking_payment.html', {'booking': booking, 'form': form})

# PAYMENT SUCCESS MESSAGE VIEW
def payment_success(request):
    return render(request, 'payment_success.html')

# PAYMENT LIST DISPLAY

def display_payments(request):
    if request.user.is_authenticated and request.user.is_company:
        try:
            # Retrieve the company profile associated with the current user
            company_profile = get_object_or_404(CompanyProfile, user=request.user)

            # Retrieve all bookings of the company
            company_bookings = Booking.objects.filter(company_name=request.user)

            # Retrieve payments associated with the company's bookings
            company_payments = Payment.objects.filter(booking__in=company_bookings)

            return render(request, 'payments_list.html', {'company_payments': company_payments})
        except CompanyProfile.DoesNotExist:
            return render(request, 'error.html', {'error_message': 'Company profile not found'})
        except Payment.DoesNotExist:
            return render(request, 'error.html', {'error_message': 'No payments found for the selected company type'})
    else:
        return HttpResponseRedirect(reverse('index'))

# PAYMENT DELETE VIEW

def delete_payment(request, payment_id):
    # Retrieve the payment object
    payment = get_object_or_404(Payment, pk=payment_id)

    # Perform deletion logic
    payment.delete()

    # Redirect back to the payments page or any other desired page
    return redirect('payments')

# NOTIFICATIONS

def notifications(request):
    # Fetch unread notifications for the current user
    unread_notifications = Notification.objects.filter(user=request.user, is_read=False)

    return render(request, 'notifications.html', {'notifications': unread_notifications})


def notification_count(request):
    # Fetch the count of unread notifications for the current user
    notification_count = Notification.objects.filter(user=request.user, is_read=False).count()
    return JsonResponse({'notification_count': notification_count})


def mark_notification_read(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    notification.is_read = True
    notification.save()

    return redirect('notifications')

# USER PROFILE SECTIONS


def profile(request):
    # Assuming user data is available in the request or you can fetch it from the database
    user = request.user
    return render(request, 'event_export/profile.html', {'user': user})

# BOOKINGS SECTION


@login_required
def booking_history(request):
    # Retrieve the user's bookings based on the email
    user_bookings = Booking.objects.filter(customer_email=request.user.email)

    return render(request, 'user_bookings.html', {'bookings': user_bookings})


@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.delete()
        return redirect('booking_history')
    return redirect('booking_history')

# CHATS SECTION
def view_chats(request):
    # Get the messages where the sender is the current user
    sent_messages = Message.objects.filter(sender=request.user)

    # Mark all messages as read when the user views their chat history
    request.session['read_messages'] = [msg.id for msg in sent_messages]

    # Retrieve the company names associated with the recipients of these messages
    company_names = CompanyProfile.objects.filter(user__in=sent_messages.values('recipient'))

    context = {'company_names': company_names}
    return render(request, 'view_chats.html', context)


def unread_message_count(request):
    # Get the IDs of read messages from the session
    read_message_ids = request.session.get('read_messages', [])
    # Calculate the count of unread messages
    unread_count = Message.objects.filter(sender=request.user).exclude(id__in=read_message_ids).count()
    return JsonResponse({'unread_message_count': unread_count})


