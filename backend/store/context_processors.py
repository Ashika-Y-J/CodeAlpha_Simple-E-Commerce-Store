from .models import Category

def store_context(request):
    """Context processor for categories and global store metadata."""
    categories = Category.objects.filter(is_active=True)
    return {
        'all_categories': categories,
    }

