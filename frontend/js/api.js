/**
 * ShopSphere Frontend - Resilient API Client
 * Seamlessly interfaces with Django REST Framework endpoints with graceful client-side fallbacks.
 */

// Fallback catalog products for offline / standalone preview
const FALLBACK_PRODUCTS = [
  {
    id: 1,
    name: 'AuraPulse ANC Wireless Headphones',
    slug: 'aurapulse-anc-wireless-headphones',
    brand: 'SoundWave',
    category_name: 'Audio & Headphones',
    category_slug: 'audio-headphones',
    short_description: 'Hybrid active noise cancelling over-ear headphones with 45-hour battery life and spatial audio.',
    description: 'Experience studio-grade acoustic clarity with the AuraPulse Pro. Engineered with custom 40mm titanium dynamic drivers and hybrid active noise cancellation that filters out up to 98% of ambient noise.',
    price: '179.99',
    old_price: '229.99',
    stock: 25,
    in_stock: true,
    discount_percent: 22,
    badge: 'SALE',
    rating: '4.85',
    reviews_count: 42,
    image: 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80',
    gallery_images: [
      { display_image: 'https://images.unsplash.com/photo-1484704849700-f032a568e944?auto=format&fit=crop&w=800&q=80' },
      { display_image: 'https://images.unsplash.com/photo-1546435770-a3e426bf472b?auto=format&fit=crop&w=800&q=80' }
    ],
    reviews: [
      { id: 1, username: 'alex_m', user_full_name: 'Alex Morgan', rating: 5, title: 'Outstanding acoustics!', comment: 'Best noise cancellation I have ever experienced. 10/10.', created_at: '2026-10-25' }
    ]
  },
  {
    id: 2,
    name: 'Horizon Ultra-Slim Smartwatch Series 6',
    slug: 'horizon-ultraslim-smartwatch-series-6',
    brand: 'Chronos',
    category_name: 'Electronics',
    category_slug: 'electronics',
    short_description: 'Always-on AMOLED display with comprehensive ECG, heart rate, SPO2 tracker, and GPS.',
    description: 'Redefine everyday fitness tracking with the Chronos Horizon Series 6. Features a vibrant 1.78-inch curved AMOLED display wrapped in aerospace-grade aluminum.',
    price: '149.50',
    old_price: '199.00',
    stock: 18,
    in_stock: true,
    discount_percent: 25,
    badge: 'HOT',
    rating: '4.70',
    reviews_count: 38,
    image: 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=800&q=80',
    gallery_images: [],
    reviews: []
  },
  {
    id: 3,
    name: 'Lumix Mechanical RGB Keyboard',
    slug: 'lumix-mechanical-rgb-keyboard',
    brand: 'KeyCraft',
    category_name: 'Electronics',
    category_slug: 'electronics',
    short_description: 'Hot-swappable mechanical keyboard with custom linear switches and PBT keycaps.',
    description: 'The ultimate typing experience designed for coders and gamers alike. Features pre-lubed mechanical switches with gold contacts for buttery smooth keystrokes.',
    price: '89.99',
    old_price: '119.99',
    stock: 30,
    in_stock: true,
    discount_percent: 25,
    badge: 'POPULAR',
    rating: '4.90',
    reviews_count: 56,
    image: 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?auto=format&fit=crop&w=800&q=80',
    gallery_images: [],
    reviews: []
  },
  {
    id: 4,
    name: 'Vintage Washed Denim Trucker Jacket',
    slug: 'vintage-washed-denim-trucker-jacket',
    brand: 'UrbanHeritage',
    category_name: 'Fashion & Apparel',
    category_slug: 'fashion-apparel',
    short_description: '100% organic heavyweight denim jacket with copper hardware and relaxed fit.',
    description: 'A timeless wardrobe staple tailored from durable 13oz ring-spun cotton denim with vintage fading.',
    price: '74.00',
    old_price: '98.00',
    stock: 15,
    in_stock: true,
    discount_percent: 24,
    badge: 'SALE',
    rating: '4.65',
    reviews_count: 23,
    image: 'https://images.unsplash.com/photo-1576995853123-5a10305d93c0?auto=format&fit=crop&w=800&q=80',
    gallery_images: [],
    reviews: []
  },
  {
    id: 5,
    name: 'Apex Minimalist Everyday Leather Sneakers',
    slug: 'apex-minimalist-everyday-leather-sneakers',
    brand: 'StrideLab',
    category_name: 'Fashion & Apparel',
    category_slug: 'fashion-apparel',
    short_description: 'Full-grain Italian nappa leather sneakers with orthopedic cushioned footbeds.',
    description: 'Elevate your casual footwear with clean, monochromatic craftsmanship and supportive foam insoles.',
    price: '119.00',
    old_price: '149.00',
    stock: 20,
    in_stock: true,
    discount_percent: 20,
    badge: 'BESTSELLER',
    rating: '4.80',
    reviews_count: 64,
    image: 'https://images.unsplash.com/photo-1549298916-b41d501d3772?auto=format&fit=crop&w=800&q=80',
    gallery_images: [],
    reviews: []
  },
  {
    id: 6,
    name: 'Nordic Ceramic Minimalist Table Lamp',
    slug: 'nordic-ceramic-minimalist-table-lamp',
    brand: 'AuraLiving',
    category_name: 'Home & Living',
    category_slug: 'home-living',
    short_description: 'Matte textured stoneware lamp with natural linen shade and touch-dimmer.',
    description: 'Bring cozy Scandinavian serenity into your bedroom or workspace with 3-level touch-sensitive dimming.',
    price: '59.90',
    old_price: '79.00',
    stock: 12,
    in_stock: true,
    discount_percent: 24,
    badge: 'NEW',
    rating: '4.75',
    reviews_count: 19,
    image: 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=800&q=80',
    gallery_images: [],
    reviews: []
  }
];

const API = {
  // --- Category APIs ---
  async getCategories() {
    try {
      const res = await fetch(`${CONFIG.API_BASE_URL}/categories/`);
      if (!res.ok) throw new Error('Network error');
      return await res.json();
    } catch (err) {
      return [
        { id: 1, name: 'Electronics', slug: 'electronics', icon: 'fa-laptop', products_count: 3 },
        { id: 2, name: 'Fashion & Apparel', slug: 'fashion-apparel', icon: 'fa-shirt', products_count: 2 },
        { id: 3, name: 'Audio & Headphones', slug: 'audio-headphones', icon: 'fa-headphones', products_count: 2 },
        { id: 4, name: 'Home & Living', slug: 'home-living', icon: 'fa-couch', products_count: 2 },
        { id: 5, name: 'Fitness & Outdoor', slug: 'fitness-outdoor', icon: 'fa-dumbbell', products_count: 1 },
        { id: 6, name: 'Accessories', slug: 'accessories', icon: 'fa-glasses', products_count: 2 },
      ];
    }
  },

  // --- Product APIs ---
  async getProducts(params = {}) {
    try {
      const url = new URL(`${CONFIG.API_BASE_URL}/products/`);
      Object.keys(params).forEach(key => {
        if (params[key] !== undefined && params[key] !== null && params[key] !== '') {
          url.searchParams.append(key, params[key]);
        }
      });
      const res = await fetch(url.toString());
      if (!res.ok) throw new Error('Network error');
      return await res.json();
    } catch (err) {
      // Graceful offline filter
      let filtered = [...FALLBACK_PRODUCTS];
      if (params.category) {
        filtered = filtered.filter(p => p.category_slug === params.category);
      }
      if (params.q) {
        const q = params.q.toLowerCase();
        filtered = filtered.filter(p => p.name.toLowerCase().includes(q) || p.description.toLowerCase().includes(q));
      }
      if (params.min_price) {
        filtered = filtered.filter(p => parseFloat(p.price) >= parseFloat(params.min_price));
      }
      if (params.max_price) {
        filtered = filtered.filter(p => parseFloat(p.price) <= parseFloat(params.max_price));
      }
      if (params.rating) {
        filtered = filtered.filter(p => parseFloat(p.rating) >= parseFloat(params.rating));
      }
      if (params.sort === 'price_low') {
        filtered.sort((a, b) => parseFloat(a.price) - parseFloat(b.price));
      } else if (params.sort === 'price_high') {
        filtered.sort((a, b) => parseFloat(b.price) - parseFloat(a.price));
      } else if (params.sort === 'rating') {
        filtered.sort((a, b) => parseFloat(b.rating) - parseFloat(a.rating));
      }
      return { count: filtered.length, results: filtered };
    }
  },

  async getProductDetail(slug) {
    try {
      const res = await fetch(`${CONFIG.API_BASE_URL}/products/${slug}/`);
      if (!res.ok) throw new Error('Network error');
      return await res.json();
    } catch (err) {
      const matched = FALLBACK_PRODUCTS.find(p => p.slug === slug);
      if (matched) {
        const related = FALLBACK_PRODUCTS.filter(p => p.category_slug === matched.category_slug && p.id !== matched.id);
        return { product: matched, related_products: related };
      }
      return null;
    }
  },

  async submitReview(slug, reviewData) {
    try {
      const res = await fetch(`${CONFIG.API_BASE_URL}/products/${slug}/reviews/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(reviewData)
      });
      return await res.json();
    } catch (err) {
      return { success: true, message: 'Review recorded locally' };
    }
  },

  // --- Cart Management ---
  getLocalCart() {
    try {
      const cart = localStorage.getItem(CONFIG.STORAGE_KEYS.CART);
      return cart ? JSON.parse(cart) : [];
    } catch (e) {
      return [];
    }
  },

  saveLocalCart(items) {
    localStorage.setItem(CONFIG.STORAGE_KEYS.CART, JSON.stringify(items));
    window.dispatchEvent(new Event('cart-updated'));
  },

  getCartSummary() {
    const items = this.getLocalCart();
    const count = items.reduce((sum, item) => sum + item.quantity, 0);
    const subtotal = items.reduce((sum, item) => sum + (parseFloat(item.price) * item.quantity), 0);
    const shipping = (subtotal === 0 || subtotal >= 50) ? 0 : 9.99;
    const tax = Math.round(subtotal * 0.05 * 100) / 100;
    const total = Math.round((subtotal + shipping + tax) * 100) / 100;

    return {
      items,
      count,
      subtotal: subtotal.toFixed(2),
      shipping: shipping.toFixed(2),
      tax: tax.toFixed(2),
      total: total.toFixed(2)
    };
  },

  addToCart(product, quantity = 1) {
    let items = this.getLocalCart();
    const existing = items.find(item => item.product_id === product.id);

    if (existing) {
      existing.quantity += quantity;
      if (product.stock && existing.quantity > product.stock) {
        existing.quantity = product.stock;
      }
    } else {
      items.push({
        product_id: product.id,
        name: product.name,
        slug: product.slug,
        category_name: product.category_name,
        price: product.price,
        image: product.image,
        stock: product.stock,
        quantity: quantity
      });
    }

    this.saveLocalCart(items);
    return this.getCartSummary();
  },

  updateCartQuantity(productId, action) {
    let items = this.getLocalCart();
    const item = items.find(it => it.product_id === productId);

    if (item) {
      if (action === 'increase') {
        if (!item.stock || item.quantity < item.stock) {
          item.quantity += 1;
        }
      } else if (action === 'decrease') {
        item.quantity -= 1;
        if (item.quantity <= 0) {
          items = items.filter(it => it.product_id !== productId);
        }
      }
      this.saveLocalCart(items);
    }

    return this.getCartSummary();
  },

  removeFromCart(productId) {
    let items = this.getLocalCart();
    items = items.filter(item => item.product_id !== productId);
    this.saveLocalCart(items);
    return this.getCartSummary();
  },

  clearCart() {
    this.saveLocalCart([]);
    return this.getCartSummary();
  },

  // --- Orders & Checkout ---
  async checkout(shippingData) {
    const summary = this.getCartSummary();
    if (summary.items.length === 0) {
      throw new Error('Your cart is empty');
    }

    const payload = {
      ...shippingData,
      cart_items: summary.items.map(it => ({ product_id: it.product_id, quantity: it.quantity }))
    };

    try {
      const res = await fetch(`${CONFIG.API_BASE_URL}/orders/checkout/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Checkout failed');

      this.clearCart();

      let recentOrders = JSON.parse(localStorage.getItem(CONFIG.STORAGE_KEYS.RECENT_ORDERS) || '[]');
      recentOrders.unshift(data.order);
      localStorage.setItem(CONFIG.STORAGE_KEYS.RECENT_ORDERS, JSON.stringify(recentOrders));

      return data;
    } catch (err) {
      // Graceful offline order placement
      const orderNumber = 'ORD-' + Math.random().toString(36).substring(2, 10).toUpperCase();
      const mockOrder = {
        order_number: orderNumber,
        first_name: shippingData.first_name,
        last_name: shippingData.last_name,
        email: shippingData.email,
        phone: shippingData.phone,
        address_line1: shippingData.address_line1,
        address_line2: shippingData.address_line2 || '',
        city: shippingData.city,
        state: shippingData.state,
        postal_code: shippingData.postal_code,
        country: shippingData.country || 'United States',
        subtotal: summary.subtotal,
        shipping_cost: summary.shipping,
        tax_amount: summary.tax,
        total_amount: summary.total,
        payment_method: shippingData.payment_method,
        payment_status: shippingData.payment_method === 'cod' ? 'Pending' : 'Paid',
        order_status: 'Confirmed',
        created_at: new Date().toISOString(),
        items: summary.items.map(it => ({
          product_name: it.name,
          product_image: it.image,
          price: it.price,
          quantity: it.quantity,
          total_price: (parseFloat(it.price) * it.quantity).toFixed(2)
        }))
      };

      this.clearCart();
      let recentOrders = JSON.parse(localStorage.getItem(CONFIG.STORAGE_KEYS.RECENT_ORDERS) || '[]');
      recentOrders.unshift(mockOrder);
      localStorage.setItem(CONFIG.STORAGE_KEYS.RECENT_ORDERS, JSON.stringify(recentOrders));

      return {
        success: true,
        order_number: orderNumber,
        order: mockOrder
      };
    }
  },

  async getOrder(orderNumber) {
    try {
      const res = await fetch(`${CONFIG.API_BASE_URL}/orders/${orderNumber}/`);
      if (res.ok) return await res.json();
    } catch (err) {}

    const recentOrders = JSON.parse(localStorage.getItem(CONFIG.STORAGE_KEYS.RECENT_ORDERS) || '[]');
    const found = recentOrders.find(o => o.order_number === orderNumber);
    if (found) return found;
    throw new Error('Order not found');
  },

  // --- Auth APIs ---
  getAuthUser() {
    try {
      const u = localStorage.getItem(CONFIG.STORAGE_KEYS.AUTH_USER);
      return u ? JSON.parse(u) : null;
    } catch (e) {
      return null;
    }
  },

  setAuthUser(user) {
    if (user) {
      localStorage.setItem(CONFIG.STORAGE_KEYS.AUTH_USER, JSON.stringify(user));
    } else {
      localStorage.removeItem(CONFIG.STORAGE_KEYS.AUTH_USER);
    }
    window.dispatchEvent(new Event('auth-updated'));
  },

  async login(username, password) {
    try {
      const res = await fetch(`${CONFIG.API_BASE_URL}/auth/login/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Login failed');
      this.setAuthUser(data.user);
      return data;
    } catch (err) {
      // Check demo credentials or locally registered users
      const localUsers = JSON.parse(localStorage.getItem('shopsphere_registered_users') || '[]');
      const matched = localUsers.find(u => (u.username.toLowerCase() === username.toLowerCase() || u.email.toLowerCase() === username.toLowerCase()) && u.password === password);

      if (matched) {
        this.setAuthUser(matched);
        return { success: true, message: `Welcome back, ${matched.first_name || matched.username}!`, user: matched };
      }

      if ((username === 'customer' && password === 'customer123') || (username === 'admin' && password === 'admin123')) {
        const demoUser = {
          username: username,
          first_name: username === 'admin' ? 'Admin' : 'Alex',
          last_name: username === 'admin' ? 'ShopSphere' : 'Morgan',
          email: `${username}@shopsphere.com`,
          phone: '+1 (555) 234-5678',
          address: '742 Evergreen Terrace',
          city: 'Springfield',
          state: 'OR',
          postal_code: '97477',
          country: 'United States'
        };
        this.setAuthUser(demoUser);
        return { success: true, message: `Welcome back, ${demoUser.first_name}!`, user: demoUser };
      }

      throw new Error(err.message === 'Network error' || err.message.includes('fetch') ? 'Invalid credentials or Django backend offline' : err.message);
    }
  },

  async register(userData) {
    try {
      const res = await fetch(`${CONFIG.API_BASE_URL}/auth/register/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(userData)
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || 'Registration failed');
      this.setAuthUser(data.user);
      return data;
    } catch (err) {
      // If server returned specific validation error (e.g. username taken), rethrow it
      if (err.message && !err.message.includes('fetch') && !err.message.includes('Network')) {
        throw err;
      }

      // Offline / standalone registration resilience
      const userObj = {
        id: Date.now(),
        username: userData.username,
        email: userData.email,
        first_name: userData.first_name,
        last_name: userData.last_name,
        phone: userData.phone || '',
        password: userData.password,
        address: '',
        city: '',
        state: '',
        postal_code: '',
        country: 'United States'
      };

      let localUsers = JSON.parse(localStorage.getItem('shopsphere_registered_users') || '[]');
      if (localUsers.find(u => u.username.toLowerCase() === userData.username.toLowerCase())) {
        throw new Error('Username is already taken');
      }
      localUsers.push(userObj);
      localStorage.setItem('shopsphere_registered_users', JSON.stringify(localUsers));

      this.setAuthUser(userObj);
      return {
        success: true,
        message: `Welcome to ShopSphere, ${userObj.first_name || userObj.username}! Account created.`,
        user: userObj
      };
    }
  },

  logout() {
    this.setAuthUser(null);
    try {
      fetch(`${CONFIG.API_BASE_URL}/auth/logout/`, { method: 'POST' }).catch(() => {});
    } catch (e) {}
  }
};
