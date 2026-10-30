from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q, Avg
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductListSerializer, ProductDetailSerializer, ReviewSerializer

class CategoryListAPIView(generics.ListAPIView):
    """API endpoint to list all active categories."""
    permission_classes = [AllowAny]
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


class ProductListAPIView(APIView):
    """API endpoint to list and filter products."""
    permission_classes = [AllowAny]

    def get(self, request):
        products = Product.objects.filter(is_available=True)

        # Category filter
        category_slug = request.GET.get('category')
        if category_slug:
            products = products.filter(category__slug=category_slug)

        # Search query
        query = request.GET.get('q', '').strip()
        if query:
            products = products.filter(
                Q(name__icontains=query) |
                Q(brand__icontains=query) |
                Q(description__icontains=query) |
                Q(short_description__icontains=query)
            )

        # Price range
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
        rating = request.GET.get('rating')
        if rating:
            try:
                products = products.filter(rating__gte=float(rating))
            except ValueError:
                pass

        # Featured / Deals flags
        if request.GET.get('featured') == 'true':
            products = products.filter(is_featured=True)
        if request.GET.get('deals') == 'true':
            products = products.filter(is_deal=True)

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
        else:
            products = products.order_by('-is_featured', '-created_at')

        limit = request.GET.get('limit')
        if limit:
            try:
                products = products[:int(limit)]
            except ValueError:
                pass

        serializer = ProductListSerializer(products, many=True)
        return Response({
            'count': len(serializer.data),
            'results': serializer.data
        })


class ProductDetailAPIView(APIView):
    """API endpoint to fetch a single product with gallery and related items."""
    permission_classes = [AllowAny]

    def get(self, request, slug):
        try:
            product = Product.objects.get(slug=slug, is_available=True)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductDetailSerializer(product)
        related = Product.objects.filter(category=product.category, is_available=True).exclude(id=product.id)[:4]
        related_serializer = ProductListSerializer(related, many=True)

        return Response({
            'product': serializer.data,
            'related_products': related_serializer.data
        })


class ProductReviewCreateAPIView(APIView):
    """API endpoint to add a review for a product."""
    def post(self, request, slug):
        try:
            product = Product.objects.get(slug=slug, is_available=True)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        rating = request.data.get('rating')
        title = request.data.get('title', '').strip()
        comment = request.data.get('comment', '').strip()

        if not rating or not comment:
            return Response({'error': 'Rating and comment are required'}, status=status.HTTP_400_BAD_REQUEST)

        # If user is not authenticated, check if user details provided or use anonymous customer
        user = request.user
        if not user.is_authenticated:
            from django.contrib.auth.models import User
            user = User.objects.filter(username='customer').first() or User.objects.first()

        try:
            review = Review.objects.create(
                product=product,
                user=user,
                rating=int(rating),
                title=title,
                comment=comment
            )
            # Recalculate average
            avg = product.reviews.aggregate(Avg('rating'))['rating__avg'] or 5.0
            product.rating = round(avg, 2)
            product.reviews_count = product.reviews.count()
            product.save()

            return Response({
                'success': True,
                'message': 'Review submitted successfully',
                'review': ReviewSerializer(review).data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

