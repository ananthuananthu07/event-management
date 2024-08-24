from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import EventsClass, Categories, CompanyProfile, Review, Appointment, GalleryPhoto, Message, Booking, \
    Payment
from event_app.models import User

#FORMS NEEDED FINE
class CustomRegistrationForm(UserCreationForm):
    is_company = forms.BooleanField(required=False,
                                    widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                                    label='Client')
    is_customer = forms.BooleanField(required=False,
                                     widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
                                     label='Advocate')

    first_name = (forms.CharField
                  (widget=forms.TextInput(attrs={'class': 'form-control my-2',
                                                 'placeholder': 'enter your name'})))

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control my-2',
                                                             'placeholder': 'enter your username'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control my-2',
                                                           'placeholder': 'enter your email id'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control my-2',
                                                                  'placeholder': 'enter your password'}))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control my-2',
                                                                  'placeholder': 'enter tour confirm password'}))

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'Full Name:',
        }

    def clean(self):
        cleaned_data = super().clean()
        is_company = cleaned_data.get('is_company', False)
        is_customer = cleaned_data.get('is_customer', False)

        if not is_company and not is_customer:
            raise forms.ValidationError('Please select your user type.')

        return cleaned_data


class EventsForm(forms.ModelForm):
    class Meta:
        model = EventsClass
        fields = '__all__'

        labels = {
            'title': 'Title:',
            'description': 'Description:',
            'image': 'Image:'
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Categories
        fields = '__all__'

        labels = {
            'event_type': 'Choose Event Type:',
            'event_name': 'Event Name:',
            'event_des': 'Event Description:',
            'event_image': 'Event Image:',
            'event_prize': 'Prize:'
        }


# -----------------COMPANY PROFILE FORM------------------------------------

class CompanyProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = CompanyProfile
        fields = [
            'first_name',  # Include the first name field
            'email',
            'comp_type',
            'comp_id',
            'comp_location',
            'comp_image',
            'comp_contact',
            'comp_bio',
            'comp_agent',

        ]


# forms.py

# -----------------form for Filtering lawyers------------------------------------


class CompanySearchForm(forms.Form):
    comp_type = forms.CharField(max_length=100, required=False)
    comp_location = forms.CharField(max_length=100, required=False)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment']
        labels = {'con': 'contact'}
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2, 'class': 'form-control my-2', 'placeholder': '', 'labels': ' '}),}


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'details']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date'].widget.attrs.update({'class': 'flatpickr'})


class GalleryPhotoForm(forms.ModelForm):
    class Meta:
        model = GalleryPhoto
        fields = ['image']


class MessageForm(forms.ModelForm):
    content = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Type your message here...'}))

    class Meta:
        model = Message
        fields = ['content']

# -----------------form for Booking------------------------------------

class BookingForm(forms.ModelForm):
    DISTRICT_CHOICES = [
        ('Alappuzha', 'Alappuzha'),
        ('Ernakulam', 'Ernakulam'),
        ('Idukki', 'Idukki'),
        ('Kannur', 'Kannur'),
        ('Kasargod', 'Kasargod'),
        ('Kollam', 'Kollam'),
        ('Kottayam', 'Kottayam'),
        ('Kozhikkod', 'Kozhikkod'),
        ('Malappuram', 'Malappuram'),
        ('Palakkad', 'Palakkad'),
        ('Pathanamthitta', 'Pathanamthitta'),
        ('Thrissur', 'Thrissur'),
        ('Trivandrum', 'Trivandrum'),
        ('Wayanad', 'Wayanad'),
        # Add more districts as needed
    ]

    district = forms.ChoiceField(choices=DISTRICT_CHOICES, required=True)

    class Meta:
        model = Booking
        fields = ['customer_name', 'customer_number', 'customer_email', 'district', 'location', 'landmark',
                  'date', 'duration', 'food_type', 'dj_party_needed']

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['district'].label = 'District'
        self.fields['dj_party_needed'].label = 'Require DJ Party?'
        self.fields['dj_party_needed'].widget = forms.RadioSelect(choices=((True, 'Yes'), (False, 'No')))


# PAYMENT FORMS

class PaymentOptionForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['option']


class DebitCardPaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['card_holder_name', 'card_number', 'cvv_number', 'expiry_date', 'email', 'mobile_number']


class NetBankingPaymentForm(forms.ModelForm):
    account_number = forms.CharField(label='Account Number', max_length=14,  # Adjusted max_length to 14
                                     widget=forms.TextInput(attrs={'maxlength': 14}))  # Adjusted maxlength to 14

    ifsc_code = forms.CharField(label='IFSC Code', max_length=15,
                                 widget=forms.TextInput(attrs={'maxlength': 15}))

    def clean_account_number(self):
        account_number = self.cleaned_data['account_number']
        if len(account_number) != 14:
            raise forms.ValidationError('Account number must be 14 characters long.')  # Adjusted error message
        return account_number

    def clean_ifsc_code(self):
        ifsc_code = self.cleaned_data['ifsc_code']
        if len(ifsc_code) != 15:
            raise forms.ValidationError('IFSC code must be 15 characters long.')
        return ifsc_code

    class Meta:
        model = Payment
        fields = ['bank_name', 'account_number', 'ifsc_code', 'email', 'mobile_number']
