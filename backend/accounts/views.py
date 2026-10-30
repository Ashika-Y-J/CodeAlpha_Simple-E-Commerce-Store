from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, UserLoginForm, ProfileUpdateForm
from orders.models import Order

def register_view(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('store:home')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Set phone on profile if provided
            phone = form.cleaned_data.get('phone')
            if phone and hasattr(user, 'profile'):
                user.profile.phone = phone
                user.profile.save()

            messages.success(request, f'Welcome to ShopSphere, {user.first_name or user.username}! Your account has been created.')
            login(request, user)
            return redirect('store:home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """User login view with username or email support."""
    if request.user.is_authenticated:
        return redirect('store:home')

    next_url = request.GET.get('next') or request.POST.get('next') or 'store:home'

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Check if user entered email instead of username
            user_obj = None
            if '@' in username_or_email:
                try:
                    user_match = User.objects.get(email__iexact=username_or_email)
                    username_or_email = user_match.username
                except User.DoesNotExist:
                    pass

            user = authenticate(request, username=username_or_email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                return redirect(next_url)
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})


def logout_view(request):
    """Log out user and redirect to homepage."""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('store:home')


@login_required
def profile_view(request):
    """User profile overview and editable details."""
    profile = request.user.profile
    orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            # Update User fields
            request.user.first_name = form.cleaned_data.get('first_name')
            request.user.last_name = form.cleaned_data.get('last_name')
            new_email = form.cleaned_data.get('email')
            if new_email and new_email != request.user.email:
                if not User.objects.filter(email=new_email).exclude(id=request.user.id).exists():
                    request.user.email = new_email
                else:
                    messages.warning(request, 'Email address already in use by another account.')
            request.user.save()

            form.save()
            messages.success(request, 'Your profile details have been updated successfully.')
            return redirect('accounts:profile')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = ProfileUpdateForm(instance=profile, initial=initial)

    context = {
        'form': form,
        'orders': orders,
        'order_count': Order.objects.filter(user=request.user).count(),
    }
    return render(request, 'accounts/profile.html', context)
