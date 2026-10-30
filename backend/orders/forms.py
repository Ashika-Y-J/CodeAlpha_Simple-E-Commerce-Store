from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'address_line1', 'address_line2', 'city', 'state',
            'postal_code', 'country', 'payment_method', 'order_notes'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'John', 'required': True}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Doe', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'john.doe@example.com', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+1 (555) 000-0000', 'required': True}),
            'address_line1': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '123 Main Street, Apt 4B', 'required': True}),
            'address_line2': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Suite, floor, etc. (optional)'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'New York', 'required': True}),
            'state': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'NY', 'required': True}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '10001', 'required': True}),
            'country': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'United States', 'required': True}),
            'payment_method': forms.RadioSelect(attrs={'class': 'payment-radio'}),
            'order_notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Special delivery instructions or notes (optional)'}),
        }

