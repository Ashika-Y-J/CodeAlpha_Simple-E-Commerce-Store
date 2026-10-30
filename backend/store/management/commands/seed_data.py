from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Category, Product, ProductImage, Review
from orders.models import Order, OrderItem
from decimal import Decimal

class Command(BaseCommand):
    help = 'Seeds database with realistic e-commerce products, categories, reviews, and test accounts.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Starting ShopSphere database seeding...'))

        # 1. Create Superuser and Test User
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser('admin', 'admin@shopsphere.local', 'admin123')
            admin_user.first_name = 'ShopSphere'
            admin_user.last_name = 'Admin'
            admin_user.save()
            self.stdout.write(self.style.SUCCESS('Created superuser: admin (password: admin123)'))
        else:
            admin_user = User.objects.get(username='admin')

        if not User.objects.filter(username='customer').exists():
            customer_user = User.objects.create_user('customer', 'customer@example.com', 'customer123')
            customer_user.first_name = 'Alex'
            customer_user.last_name = 'Morgan'
            customer_user.save()
            if hasattr(customer_user, 'profile'):
                customer_user.profile.phone = '+1 (555) 234-5678'
                customer_user.profile.address = '742 Evergreen Terrace'
                customer_user.profile.city = 'Springfield'
                customer_user.profile.state = 'OR'
                customer_user.profile.postal_code = '97477'
                customer_user.profile.save()
            self.stdout.write(self.style.SUCCESS('Created test customer: customer (password: customer123)'))
        else:
            customer_user = User.objects.get(username='customer')

        # 2. Categories
        categories_data = [
            {
                'name': 'Electronics',
                'slug': 'electronics',
                'icon': 'fa-laptop',
                'description': 'Latest tech gadgets, smart wearables, and advanced computing accessories.',
                'image_url': 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=800&q=80',
            },
            {
                'name': 'Fashion & Apparel',
                'slug': 'fashion-apparel',
                'icon': 'fa-shirt',
                'description': 'Trendy streetwear, premium everyday essentials, and designer wear.',
                'image_url': 'https://images.unsplash.com/photo-1445205170230-053b83016050?auto=format&fit=crop&w=800&q=80',
            },
            {
                'name': 'Audio & Headphones',
                'slug': 'audio-headphones',
                'icon': 'fa-headphones',
                'description': 'Immersive noise-cancelling headphones, high-fidelity earbuds, and soundbars.',
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80',
            },
            {
                'name': 'Home & Living',
                'slug': 'home-living',
                'icon': 'fa-couch',
                'description': 'Modern interior decor, ergonomic furniture, and smart living comforts.',
                'image_url': 'https://images.unsplash.com/photo-1513694203232-719a280e022f?auto=format&fit=crop&w=800&q=80',
            },
            {
                'name': 'Fitness & Outdoor',
                'slug': 'fitness-outdoor',
                'icon': 'fa-dumbbell',
                'description': 'High-performance athletic gear, hydration, and outdoor lifestyle equipment.',
                'image_url': 'https://images.unsplash.com/photo-1517838277536-f5f99be501cd?auto=format&fit=crop&w=800&q=80',
            },
            {
                'name': 'Accessories',
                'slug': 'accessories',
                'icon': 'fa-glasses',
                'description': 'Handcrafted leather goods, luxury timepieces, and travel essentials.',
                'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80',
            },
        ]

        cat_instances = {}
        for cdata in categories_data:
            cat, _ = Category.objects.update_or_create(
                slug=cdata['slug'],
                defaults=cdata
            )
            cat_instances[cdata['slug']] = cat

        self.stdout.write(self.style.SUCCESS(f'Created {len(cat_instances)} categories.'))

        # 3. Products
        products_data = [
            {
                'category': cat_instances['audio-headphones'],
                'name': 'AuraPulse ANC Wireless Headphones',
                'slug': 'aurapulse-anc-wireless-headphones',
                'brand': 'SoundWave',
                'short_description': 'Hybrid active noise cancelling over-ear headphones with 45-hour battery life and spatial audio.',
                'description': 'Experience studio-grade acoustic clarity with the AuraPulse Pro. Engineered with custom 40mm titanium dynamic drivers and hybrid active noise cancellation that filters out up to 98% of ambient noise. Equipped with ultra-soft memory foam earcups, multi-point Bluetooth 5.3 connection, and quick-charging that grants 5 hours of playback from just a 10-minute charge.',
                'price': Decimal('179.99'),
                'old_price': Decimal('229.99'),
                'stock': 25,
                'is_featured': True,
                'is_deal': True,
                'badge': 'SALE',
                'rating': Decimal('4.85'),
                'reviews_count': 42,
                'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80',
                'gallery': [
                    'https://images.unsplash.com/photo-1484704849700-f032a568e944?auto=format&fit=crop&w=800&q=80',
                    'https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=800&q=80'
                ]
            },
            {
                'category': cat_instances['electronics'],
                'name': 'Horizon Ultra-Slim Smartwatch Series 6',
                'slug': 'horizon-ultraslim-smartwatch-series-6',
                'brand': 'Chronos',
                'short_description': 'Always-on AMOLED display with comprehensive ECG, heart rate, SPO2 tracker, and GPS.',
                'description': 'Redefine everyday fitness tracking with the Chronos Horizon Series 6. Features a vibrant 1.78-inch curved AMOLED display wrapped in an aerospace-grade aluminum casing. Water-resistant up to 50 meters, with over 100 dedicated workout modes, sleep staging analysis, and seamless smartphone notifications for iOS and Android.',
                'price': Decimal('149.50'),
                'old_price': Decimal('199.00'),
                'stock': 18,
                'is_featured': True,
                'is_deal': False,
                'badge': 'HOT',
                'rating': Decimal('4.70'),
                'reviews_count': 38,
                'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80',
                'gallery': [
                    'https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?auto=format&fit=crop&w=800&q=80'
                ]
            },
            {
                'category': cat_instances['electronics'],
                'name': 'Lumix Mechanical RGB Keyboard',
                'slug': 'lumix-mechanical-rgb-keyboard',
                'brand': 'KeyCraft',
                'short_description': 'Hot-swappable mechanical keyboard with custom linear switches, PBT keycaps, and RGB.',
                'description': 'The ultimate typing experience designed for coders and gamers alike. Features pre-lubed mechanical switches with gold contacts for buttery smooth keystrokes. Includes per-key customizable RGB backlighting, aircraft aluminum frame, and sound-dampening acoustic silicone padding for whisper-soft bottom outs.',
                'price': Decimal('89.99'),
                'old_price': Decimal('119.99'),
                'stock': 30,
                'is_featured': True,
                'is_deal': False,
                'badge': 'POPULAR',
                'rating': Decimal('4.90'),
                'reviews_count': 56,
                'image_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=800&q=80',
                'gallery': [
                    'https://images.unsplash.com/photo-1595225476474-87563907a212?auto=format&fit=crop&w=800&q=80'
                ]
            },
            {
                'category': cat_instances['fashion-apparel'],
                'name': 'Vintage Washed Denim Trucker Jacket',
                'slug': 'vintage-washed-denim-trucker-jacket',
                'brand': 'UrbanHeritage',
                'short_description': '100% organic heavyweight denim jacket with copper hardware and relaxed fit.',
                'description': 'A timeless wardrobe staple tailored from durable 13oz ring-spun cotton denim. Finished with subtle vintage fading, dual button-flap chest pockets, welt hand-warmer pockets, and adjustable waist tabs for a tailored silhouette. Machine washable and designed to age gracefully with wear.',
                'price': Decimal('74.00'),
                'old_price': Decimal('98.00'),
                'stock': 15,
                'is_featured': False,
                'is_deal': True,
                'badge': 'SALE',
                'rating': Decimal('4.65'),
                'reviews_count': 23,
                'image_url': 'https://images.unsplash.com/photo-1576995853123-5a10305d93c0?auto=format&fit=crop&w=800&q=80',
                'gallery': [
                    'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?auto=format&fit=crop&w=800&q=80'
                ]
            },
            {
                'category': cat_instances['fashion-apparel'],
                'name': 'Apex Minimalist Everyday Leather Sneakers',
                'slug': 'apex-minimalist-everyday-leather-sneakers',
                'brand': 'StrideLab',
                'short_description': 'Full-grain Italian nappa leather sneakers with orthopedic cushioned footbeds.',
                'description': 'Elevate your casual footwear with clean, monochromatic craftsmanship. Hand-stitched with supple Italian leather and lined with breathable calfskin. The vulcanized rubber outsole provides steady traction on slick surfaces while the antimicrobial memory foam insole guarantees all-day walking support.',
                'price': Decimal('119.00'),
                'old_price': Decimal('149.00'),
                'stock': 20,
                'is_featured': True,
                'is_deal': False,
                'badge': 'BESTSELLER',
                'rating': Decimal('4.80'),
                'reviews_count': 64,
                'image_url': 'https://images.unsplash.com/photo-1549298916-b41d501d3772?auto=format&fit=crop&w=800&q=80',
                'gallery': [
                    'https://images.unsplash.com/photo-1560769629-975ec94e6a86?auto=format&fit=crop&w=800&q=80'
                ]
            },
            {
                'category': cat_instances['home-living'],
                'name': 'Nordic Ceramic Minimalist Table Lamp',
                'slug': 'nordic-ceramic-minimalist-table-lamp',
                'brand': 'AuraLiving',
                'short_description': 'Matte textured stoneware lamp with natural linen shade and touch-dimmer.',
                'description': 'Bring cozy Scandinavian serenity into your bedroom or workspace. Crafted from textured sand stoneware with earthy undertones and paired with a hand-woven linen drum shade. Equipped with 3-level touch-sensitive touch dimming, compatible with standard E26 smart LED bulbs.',
                'price': Decimal('59.90'),
                'old_price': Decimal('79.00'),
                'stock': 12,
                'is_featured': True,
                'is_deal': False,
                'badge': 'NEW',
                'rating': Decimal('4.75'),
                'reviews_count': 19,
                'image_url': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=800&q=80',
                'gallery': []
            },
            {
                'category': cat_instances['audio-headphones'],
                'name': 'SonicBlast 360 Waterproof Bluetooth Speaker',
                'slug': 'sonicblast-360-waterproof-bluetooth-speaker',
                'brand': 'SoundWave',
                'short_description': 'IPX7 waterproof portable speaker with punchy bass, 24-hr playtime, and pairing mode.',
                'description': 'Take festival-grade sound wherever adventure leads. Delivers 360-degree omnidirectional acoustics powered by dual passive bass radiators. Ruggedized rubber bumpers protect against drops, and the IPX7 waterproof casing can withstand full submersion in water for 30 minutes.',
                'price': Decimal('64.99'),
                'old_price': Decimal('89.99'),
                'stock': 35,
                'is_featured': False,
                'is_deal': True,
                'badge': '28% OFF',
                'rating': Decimal('4.60'),
                'reviews_count': 31,
                'image_url': 'https://images.unsplash.com/photo-1545454675-3531b543be5d?auto=format&fit=crop&w=800&q=80',
                'gallery': []
            },
            {
                'category': cat_instances['accessories'],
                'name': 'Monaco Sapphire Chronograph Watch',
                'slug': 'monaco-sapphire-chronograph-watch',
                'brand': 'Chronos Luxe',
                'short_description': 'Precision Japanese quartz movement with anti-reflective sapphire crystal glass.',
                'description': 'A masterclass in horological refinement. Crafted with a 41mm 316L stainless steel case, genuine top-grain calfskin leather strap, and a deep sunburst dial. Features date complication, split-second chronograph sub-dials, and 100M water resistance.',
                'price': Decimal('210.00'),
                'old_price': Decimal('285.00'),
                'stock': 8,
                'is_featured': True,
                'is_deal': False,
                'badge': 'PREMIUM',
                'rating': Decimal('4.95'),
                'reviews_count': 77,
                'image_url': 'https://images.unsplash.com/photo-1524805444758-089113d48a6d?auto=format&fit=crop&w=800&q=80',
                'gallery': [
                    'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?auto=format&fit=crop&w=800&q=80'
                ]
            },
            {
                'category': cat_instances['fitness-outdoor'],
                'name': 'ThermoShield Double-Wall Vacuum Flask 1L',
                'slug': 'thermoshield-double-wall-vacuum-flask-1l',
                'brand': 'TrailPeak',
                'short_description': 'Keeps beverages icy cold for 24 hours or piping hot for 12 hours. BPA free.',
                'description': 'Constructed from premium pro-grade 18/8 stainless steel that prevents flavor transfer. Equipped with a condensation-free powder coat finish, silicone carry loop, and leak-proof wide mouth lid compatible with standard ice cubes.',
                'price': Decimal('32.50'),
                'old_price': Decimal('42.00'),
                'stock': 50,
                'is_featured': False,
                'is_deal': False,
                'badge': '',
                'rating': Decimal('4.88'),
                'reviews_count': 92,
                'image_url': 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=800&q=80',
                'gallery': []
            },
            {
                'category': cat_instances['accessories'],
                'name': 'Voyager Waxed Canvas & Leather Backpack',
                'slug': 'voyager-waxed-canvas-leather-backpack',
                'brand': 'UrbanHeritage',
                'short_description': 'Water-repellent 16oz canvas backpack with padded 16-inch laptop compartment.',
                'description': 'Engineered for metropolitan commuters and weekend adventurers. Boasts heavy-duty 16oz weatherproof waxed cotton canvas accented with vegetable-tanned bridle leather trims. Includes a padded zippered laptop pocket, luggage trolley sleeve, and magnetic quick-snap closures.',
                'price': Decimal('98.00'),
                'old_price': Decimal('135.00'),
                'stock': 14,
                'is_featured': True,
                'is_deal': True,
                'badge': 'SALE',
                'rating': Decimal('4.78'),
                'reviews_count': 45,
                'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?auto=format&fit=crop&w=800&q=80',
                'gallery': []
            },
            {
                'category': cat_instances['home-living'],
                'name': 'ZenMist Ultrasonic Ultrasonic Diffuser',
                'slug': 'zenmist-ultrasonic-diffuser',
                'brand': 'AuraLiving',
                'short_description': 'Ceramic essential oil diffuser with ambient warm LED light and automatic shutoff.',
                'description': 'Infuse your home with calming aromatics. Utilizes whisper-quiet ultrasonic vibrations to disperse pure essential oils without heat, preserving therapeutic benefits. Features timer settings (1h, 3h, 6h, continuous) and soft amber mood illumination.',
                'price': Decimal('44.00'),
                'old_price': Decimal('55.00'),
                'stock': 22,
                'is_featured': False,
                'is_deal': False,
                'badge': '',
                'rating': Decimal('4.68'),
                'reviews_count': 29,
                'image_url': 'https://images.unsplash.com/photo-1608571423902-eed4a5ad8108?auto=format&fit=crop&w=800&q=80',
                'gallery': []
            },
            {
                'category': cat_instances['electronics'],
                'name': 'ErgoLift Aluminum Adjustable Laptop Stand',
                'slug': 'ergolift-aluminum-adjustable-laptop-stand',
                'brand': 'KeyCraft',
                'short_description': 'Solid CNC aluminum desk riser with heat dissipation vents and silicone anti-slip pads.',
                'description': 'Elevate your screen to eye level to alleviate neck fatigue and improve posture. Crafted from a single piece of sandblasted aluminum alloy, offering rock-solid stability for laptops from 11 up to 17 inches. Foldable design slips easily into your laptop bag.',
                'price': Decimal('39.99'),
                'old_price': Decimal('49.99'),
                'stock': 40,
                'is_featured': False,
                'is_deal': False,
                'badge': 'BEST VALUE',
                'rating': Decimal('4.82'),
                'reviews_count': 53,
                'image_url': 'https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?auto=format&fit=crop&w=800&q=80',
                'gallery': []
            }
        ]

        for pdata in products_data:
            gallery = pdata.pop('gallery', [])
            prod, created = Product.objects.update_or_create(
                slug=pdata['slug'],
                defaults=pdata
            )
            # Create extra gallery images
            for img_url in gallery:
                ProductImage.objects.get_or_create(
                    product=prod,
                    image_url=img_url
                )

            # Create sample review
            if not prod.reviews.exists():
                Review.objects.create(
                    product=prod,
                    user=customer_user,
                    rating=5,
                    title='Exceeded my expectations!',
                    comment='Outstanding build quality and fast delivery. Exactly as described on ShopSphere.'
                )

        self.stdout.write(self.style.SUCCESS(f'Created {len(products_data)} products with images and reviews.'))

        # 4. Create a Sample Past Order for customer
        if not Order.objects.filter(user=customer_user).exists():
            sample_product = Product.objects.first()
            sample_order = Order.objects.create(
                user=customer_user,
                first_name='Alex',
                last_name='Morgan',
                email='customer@example.com',
                phone='+1 (555) 234-5678',
                address_line1='742 Evergreen Terrace',
                city='Springfield',
                state='OR',
                postal_code='97477',
                country='United States',
                subtotal=sample_product.price,
                shipping_cost=Decimal('0.00'),
                tax_amount=round(sample_product.price * Decimal('0.05'), 2),
                total_amount=sample_product.price + round(sample_product.price * Decimal('0.05'), 2),
                payment_method='card',
                payment_status='Paid',
                order_status='Delivered'
            )
            OrderItem.objects.create(
                order=sample_order,
                product=sample_product,
                product_name=sample_product.name,
                product_image=sample_product.display_image,
                price=sample_product.price,
                quantity=1,
                total_price=sample_product.price
            )
            self.stdout.write(self.style.SUCCESS(f'Created sample order #{sample_order.order_number}'))

        self.stdout.write(self.style.SUCCESS('ShopSphere database seeding completed successfully!'))

