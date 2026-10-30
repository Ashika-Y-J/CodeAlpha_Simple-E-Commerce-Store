from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Avg
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Review

def home(request):
    """ShopSphere Homepage view."""
    categories = Category.objects.filter(is_active=True)[:6]
    featured_products = Product.objects.filter(is_available=True, is_featured=True)[:8]
    deal_products = Product.objects.filter(is_available=True, is_deal=True)[:4]
    new_arrivals = Product.objects.filter(is_available=True).order_by('-created_at')[:8]
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
        'deal_products': deal_products,
        'new_arrivals': new_arrivals,
    }
    return render(request, 'store/home.html', context)


def product_list(request, category_slug=None):
    """Product catalog with searching, filtering, and sorting."""
    category = None
    categories = Category.objects.filter(is_active=True)
    products = Product.objects.filter(is_available=True)

    # Category filter
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = products.filter(category=category)

    # Search filter
    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(description__icontains=query) |
            Q(short_description__icontains=query)
        )

    # Category filter via query parameter (if selected from dropdown)
    cat_param = request.GET.get('category')
    if cat_param and not category_slug:
        products = products.filter(category__slug=cat_param)

    # Price range filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Rating filter
    min_rating = request.GET.get('rating')
    if min_rating:
        try:
            products = products.filter(rating__gte=float(min_rating))
        except ValueError:
            pass

    # Sorting
    sort = request.GET.get('sort', 'featured')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'rating':
        products = products.order_by('-rating')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    else:  # featured / default
        products = products.order_by('-is_featured', '-created_at')

    # Pagination: 9 products per page
    total_count = products.count()
    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)

    context = {
        'category': category,
        'categories': categories,
        'products': products_page,
        'total_count': total_count,
        'query': query,
        'selected_sort': sort,
        'selected_category': cat_param or (category.slug if category else ''),
        'min_price': min_price or '',
        'max_price': max_price or '',
        'min_rating': min_rating or '',
    }
    return render(request, 'store/product_list.html', context)


def product_detail(request, slug):
    """Single product view with gallery, specifications, and reviews."""
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related_products = Product.objects.filter(
        category=product.category, is_available=True
    ).exclude(id=product.id)[:4]
    
    reviews = product.reviews.all().order_by('-created_at')

    # Handle review submission
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to leave a review.')
            return redirect('accounts:login')
        
        rating = request.POST.get('rating')
        title = request.POST.get('title', '').strip()
        comment = request.POST.get('comment', '').strip()

        if rating and comment:
            try:
                rating_val = int(rating)
                Review.objects.create(
                    product=product,
                    user=request.user,
                    rating=rating_val,
                    title=title,
                    comment=comment
                )
                
                # Recalculate average rating & count
                avg_rating = product.reviews.aggregate(Avg('rating'))['rating__avg'] or 5.0
                product.rating = round(avg_rating, 2)
                product.reviews_count = product.reviews.count()
                product.save()

                messages.success(request, 'Thank you! Your review has been submitted successfully.')
                return redirect('store:product_detail', slug=product.slug)
            except Exception as e:
                messages.error(request, f'Error submitting review: {e}')
        else:
            messages.error(request, 'Please provide both a star rating and your review comments.')

    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
    }
    return render(request, 'store/product_detail.html', context)
