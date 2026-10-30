# Re-exported for root reference; backend implementation is located in backend/accounts/admin.py
from django.contrib import admin
try:
    from backend.accounts.models import Profile
    @admin.register(Profile)
    class ProfileAdmin(admin.ModelAdmin):
        list_display = ('user', 'phone', 'city', 'country', 'created_at')
        search_fields = ('user__username', 'user__email', 'phone', 'city')
except Exception:
    pass

