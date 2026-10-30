from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Profile

def format_user_data(user):
    profile = getattr(user, 'profile', None)
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_staff': user.is_staff,
        'phone': profile.phone if profile else '',
        'address': profile.address if profile else '',
        'city': profile.city if profile else '',
        'state': profile.state if profile else '',
        'postal_code': profile.postal_code if profile else '',
        'country': profile.country if profile else 'United States',
    }

class AuthRegisterAPIView(APIView):
    """API endpoint to register a new customer."""
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username = data.get('username', '').strip()
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        email = data.get('email', '').strip()
        phone = data.get('phone', '').strip()
        password = data.get('password', '')

        if not username or not email or not password:
            return Response({'error': 'Username, email, and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'error': 'An account with this email address already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        if hasattr(user, 'profile'):
            user.profile.phone = phone
            user.profile.save()

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return Response({
            'success': True,
            'message': 'Account registered successfully',
            'user': format_user_data(user)
        }, status=status.HTTP_201_CREATED)


class AuthLoginAPIView(APIView):
    """API endpoint to authenticate a user."""
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        username_or_email = data.get('username', '').strip()
        password = data.get('password', '')

        if not username_or_email or not password:
            return Response({'error': 'Please enter both username/email and password.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if email passed
        username = username_or_email
        if '@' in username_or_email:
            try:
                matched_user = User.objects.get(email__iexact=username_or_email)
                username = matched_user.username
            except User.DoesNotExist:
                pass

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({
                'success': True,
                'message': f'Welcome back, {user.first_name or user.username}!',
                'user': format_user_data(user)
            })
        else:
            return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)


class AuthLogoutAPIView(APIView):
    """API endpoint to log out."""
    permission_classes = [AllowAny]

    def post(self, request):
        logout(request)
        return Response({'success': True, 'message': 'Logged out successfully'})


class AuthProfileAPIView(APIView):
    """API endpoint to get or update profile."""
    def get(self, request):
        if not request.user.is_authenticated:
            # Default demo profile for decoupled frontend if no session active
            user = User.objects.filter(username='customer').first() or User.objects.first()
            return Response({'authenticated': False, 'user': format_user_data(user)})
        return Response({'authenticated': True, 'user': format_user_data(request.user)})

    def put(self, request):
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        new_email = data.get('email', user.email)
        if new_email and new_email != user.email:
            if not User.objects.filter(email=new_email).exclude(id=user.id).exists():
                user.email = new_email
        user.save()

        if hasattr(user, 'profile'):
            profile = user.profile
            profile.phone = data.get('phone', profile.phone)
            profile.address = data.get('address', profile.address)
            profile.city = data.get('city', profile.city)
            profile.state = data.get('state', profile.state)
            profile.postal_code = data.get('postal_code', profile.postal_code)
            profile.country = data.get('country', profile.country)
            profile.save()

        return Response({
            'success': True,
            'message': 'Profile updated successfully',
            'user': format_user_data(user)
        })

