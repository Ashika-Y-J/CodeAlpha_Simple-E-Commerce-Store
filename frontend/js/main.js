/**
 * ShopSphere Frontend - Client UI Controller
 */

document.addEventListener('DOMContentLoaded', () => {
  initNavbar();
  initCartCounter();
  initMobileMenu();
  
  window.addEventListener('cart-updated', updateNavbarCartBadge);
  window.addEventListener('auth-updated', initNavbarAuth);
});

/* ============================================================
   Toast Notification System
   ============================================================ */
function showToast(message, type = 'success') {
  let container = document.getElementById('toast-container');
  if (!container) {
    container = document.createElement('div');
    container.id = 'toast-container';
    document.body.appendChild(container);
  }

  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  const iconClass = type === 'success' ? 'fa-circle-check' : 'fa-circle-exclamation';
  toast.innerHTML = `
    <i class="fa-solid ${iconClass} toast-icon"></i>
    <span class="toast-message">${message}</span>
  `;

  container.appendChild(toast);

  requestAnimationFrame(() => {
    toast.classList.add('show');
  });

  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    }, 300);
  }, 3500);
}

/* ============================================================
   Navbar Initialization (Categories, Auth & Cart Badge)
   ============================================================ */
async function initNavbar() {
  initNavbarAuth();
  updateNavbarCartBadge();

  // Load categories in dropdown and category nav strip
  const categories = await API.getCategories();
  
  const searchSelect = document.getElementById('nav-search-category');
  if (searchSelect && categories.length > 0) {
    categories.forEach(cat => {
      const opt = document.createElement('option');
      opt.value = cat.slug;
      opt.textContent = cat.name;
      searchSelect.appendChild(opt);
    });
  }

  const navCategories = document.getElementById('category-nav-items');
  if (navCategories && categories.length > 0) {
    // Check if on catalog page with active category
    const urlParams = new URLSearchParams(window.location.search);
    const activeCat = urlParams.get('category');

    let html = `
      <a href="products.html" class="nav-item ${!activeCat ? 'active' : ''}">
        <i class="fa-solid fa-border-all"></i> All Products
      </a>
    `;
    categories.forEach(cat => {
      const isActive = activeCat === cat.slug;
      html += `
        <a href="products.html?category=${cat.slug}" class="nav-item ${isActive ? 'active' : ''}">
          <i class="fa-solid ${cat.icon || 'fa-tag'}"></i> ${cat.name}
        </a>
      `;
    });
    navCategories.innerHTML = html;
  }
}

function initNavbarAuth() {
  const user = API.getAuthUser();
  const authContainer = document.getElementById('navbar-auth-section');
  if (!authContainer) return;

  if (user) {
    authContainer.innerHTML = `
      <div class="user-menu">
        <a href="profile.html" class="action-link">
          <i class="fa-regular fa-user"></i>
          <span>${user.first_name || user.username}</span>
          <i class="fa-solid fa-chevron-down" style="font-size: 0.75rem;"></i>
        </a>
        <div class="user-dropdown">
          <a href="profile.html"><i class="fa-regular fa-id-badge"></i> My Profile</a>
          <a href="profile.html#orders"><i class="fa-solid fa-box-open"></i> Order History</a>
          <hr>
          <a href="#" id="nav-logout-btn"><i class="fa-solid fa-arrow-right-from-bracket"></i> Sign Out</a>
        </div>
      </div>
    `;

    document.getElementById('nav-logout-btn').addEventListener('click', (e) => {
      e.preventDefault();
      API.logout();
      showToast('Logged out successfully', 'info');
      setTimeout(() => {
        window.location.href = 'index.html';
      }, 500);
    });
  } else {
    authContainer.innerHTML = `
      <a href="login.html" class="action-link">
        <i class="fa-regular fa-user"></i>
        <span>Sign In</span>
      </a>
    `;
  }
}

function initCartCounter() {
  updateNavbarCartBadge();
}

function updateNavbarCartBadge() {
  const summary = API.getCartSummary();
  const badges = document.querySelectorAll('.cart-badge');
  badges.forEach(badge => {
    badge.textContent = summary.count;
    badge.classList.remove('badge-bounce');
    void badge.offsetWidth;
    badge.classList.add('badge-bounce');
  });
}

function initMobileMenu() {
  const toggleBtn = document.querySelector('.mobile-menu-toggle');
  const navContainer = document.querySelector('.category-nav');

  if (toggleBtn && navContainer) {
    toggleBtn.addEventListener('click', () => {
      navContainer.classList.toggle('open');
      if (navContainer.classList.contains('open')) {
        navContainer.style.display = 'block';
      } else {
        navContainer.style.display = '';
      }
    });
  }
}

/* ============================================================
   Product Card HTML Component
   ============================================================ */
function renderProductCard(p) {
  let badgeHtml = '';
  if (p.badge) {
    let badgeClass = 'badge-popular';
    if (p.badge.includes('SALE') || p.badge.includes('%')) badgeClass = 'badge-sale';
    else if (p.badge.includes('HOT')) badgeClass = 'badge-hot';
    else if (p.badge.includes('NEW')) badgeClass = 'badge-new';
    badgeHtml = `<span class="product-badge ${badgeClass}">${p.badge}</span>`;
  }

  const oldPriceHtml = p.old_price ? `<span class="product-old-price">$${p.old_price}</span>` : '';

  return `
    <div class="product-card">
      ${badgeHtml}
      <a href="product-detail.html?slug=${p.slug}" class="product-image-wrap">
        <img src="${p.image}" alt="${p.name}" loading="lazy">
      </a>
      <div class="product-content">
        <span class="product-category">${p.category_name}</span>
        <h3 class="product-title">
          <a href="product-detail.html?slug=${p.slug}">${p.name}</a>
        </h3>
        <div class="product-rating">
          <div class="stars">
            <i class="fa-solid fa-star"></i>
            <i class="fa-solid fa-star"></i>
            <i class="fa-solid fa-star"></i>
            <i class="fa-solid fa-star"></i>
            <i class="fa-solid fa-star-half-stroke"></i>
          </div>
          <span class="rating-count">(${p.rating})</span>
        </div>
        <div class="product-bottom">
          <div class="product-price-wrap">
            <span class="product-price">$${p.price}</span>
            ${oldPriceHtml}
          </div>
          <button type="button" class="btn-add-cart" onclick="handleQuickAddToCart(${JSON.stringify(p).replace(/"/g, '&quot;')})" title="Add to Cart">
            <i class="fa-solid fa-cart-plus"></i>
          </button>
        </div>
      </div>
    </div>
  `;
}

function handleQuickAddToCart(product) {
  API.addToCart(product, 1);
  showToast(`"${product.name}" added to cart!`, 'success');
}

