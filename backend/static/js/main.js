/**
 * ShopSphere - Interactive E-Commerce Client Scripts
 */

document.addEventListener('DOMContentLoaded', () => {
  initToasts();
  initAjaxAddToCart();
  initCartPageControls();
  initProductDetailGallery();
  initDetailTabs();
  initCheckoutPaymentMethods();
  initMobileMenu();
});

/* ============================================================
   Helper: Get CSRF Token from cookie or DOM
   ============================================================ */
function getCsrfToken() {
  const tokenInput = document.querySelector('[name=csrfmiddlewaretoken]');
  if (tokenInput) {
    return tokenInput.value;
  }
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, 10) === 'csrftoken=') {
        cookieValue = decodeURIComponent(cookie.substring(10));
        break;
      }
    }
  }
  return cookieValue;
}

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
  
  // Trigger animation
  requestAnimationFrame(() => {
    toast.classList.add('show');
  });

  // Remove after 3.5 seconds
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => {
      if (toast.parentNode) {
        toast.parentNode.removeChild(toast);
      }
    }, 300);
  }, 3500);
}

function initToasts() {
  // Auto-dismiss Django alerts after 5 seconds
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(alert => {
    setTimeout(() => {
      alert.style.opacity = '0';
      alert.style.transform = 'translateY(-10px)';
      alert.style.transition = 'all 0.4s ease';
      setTimeout(() => alert.remove(), 400);
    }, 5000);
  });
}

/* ============================================================
   AJAX Add to Cart
   ============================================================ */
function initAjaxAddToCart() {
  document.addEventListener('submit', async (e) => {
    const form = e.target.closest('.ajax-add-cart-form');
    if (!form) return;

    e.preventDefault();
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalContent = submitBtn ? submitBtn.innerHTML : '';
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
    }

    try {
      const formData = new FormData(form);
      const url = form.getAttribute('action');
      const response = await fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
        }
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          updateCartBadge(data.cart_count);
          showToast(data.message || 'Item added to your shopping cart!', 'success');
        }
      } else {
        // Fallback: submit standard form if AJAX fails
        form.submit();
      }
    } catch (err) {
      console.error('Add to cart error:', err);
      form.submit();
    } finally {
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalContent;
      }
    }
  });
}

function updateCartBadge(count) {
  const badges = document.querySelectorAll('.cart-badge');
  badges.forEach(badge => {
    badge.textContent = count;
    badge.classList.remove('badge-bounce');
    void badge.offsetWidth; // trigger reflow
    badge.classList.add('badge-bounce');
  });
}

/* ============================================================
   Cart Page Controls (Update & Remove via AJAX)
   ============================================================ */
function initCartPageControls() {
  const cartTable = document.querySelector('.cart-table');
  if (!cartTable) return;

  // Quantity updates
  cartTable.addEventListener('click', async (e) => {
    const btn = e.target.closest('.cart-qty-btn');
    if (!btn) return;

    e.preventDefault();
    const action = btn.dataset.action; // 'increase' or 'decrease'
    const productId = btn.dataset.productId;
    const url = `/cart/update/${productId}/`;
    const csrfToken = getCsrfToken();

    const formData = new FormData();
    formData.append('action', action);
    formData.append('csrfmiddlewaretoken', csrfToken);

    try {
      const response = await fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          const row = document.getElementById(`cart-row-${productId}`);
          if (data.item_quantity <= 0) {
            if (row) row.remove();
          } else {
            const qtyInput = row.querySelector('.cart-qty-val');
            const totalCell = row.querySelector('.cart-item-total');
            if (qtyInput) qtyInput.textContent = data.item_quantity;
            if (totalCell) totalCell.textContent = `$${data.item_total}`;
          }

          updateCartBadge(data.cart_count);
          updateSummary(data);

          if (data.cart_count === 0) {
            location.reload(); // Refresh to render the modern empty-state card
          }
        }
      }
    } catch (err) {
      console.error('Update cart error:', err);
    }
  });

  // Remove item
  cartTable.addEventListener('click', async (e) => {
    const removeBtn = e.target.closest('.cart-remove-btn');
    if (!removeBtn) return;

    e.preventDefault();
    const productId = removeBtn.dataset.productId;
    const url = `/cart/remove/${productId}/`;
    const csrfToken = getCsrfToken();

    const formData = new FormData();
    formData.append('csrfmiddlewaretoken', csrfToken);

    try {
      const response = await fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          const row = document.getElementById(`cart-row-${productId}`);
          if (row) {
            row.style.opacity = '0';
            row.style.transform = 'scale(0.95)';
            row.style.transition = 'all 0.3s ease';
            setTimeout(() => {
              row.remove();
              if (data.cart_count === 0) {
                location.reload();
              }
            }, 300);
          }
          updateCartBadge(data.cart_count);
          updateSummary(data);
          showToast(data.message, 'success');
        }
      }
    } catch (err) {
      console.error('Remove cart error:', err);
    }
  });
}

function updateSummary(data) {
  const subtotalEl = document.getElementById('summary-subtotal');
  const shippingEl = document.getElementById('summary-shipping');
  const taxEl = document.getElementById('summary-tax');
  const totalEl = document.getElementById('summary-total');

  if (subtotalEl) subtotalEl.textContent = `$${data.subtotal}`;
  if (shippingEl) {
    shippingEl.textContent = parseFloat(data.shipping) === 0 ? 'FREE' : `$${data.shipping}`;
  }
  if (taxEl) taxEl.textContent = `$${data.tax}`;
  if (totalEl) totalEl.textContent = `$${data.total}`;
}

/* ============================================================
   Product Detail Gallery Switcher
   ============================================================ */
function initProductDetailGallery() {
  const thumbs = document.querySelectorAll('.thumb-item');
  const mainImage = document.getElementById('main-product-img');

  if (!thumbs.length || !mainImage) return;

  thumbs.forEach(thumb => {
    thumb.addEventListener('click', () => {
      thumbs.forEach(t => t.classList.remove('active'));
      thumb.classList.add('active');

      const newSrc = thumb.dataset.image;
      if (newSrc) {
        mainImage.style.opacity = '0.3';
        setTimeout(() => {
          mainImage.src = newSrc;
          mainImage.style.opacity = '1';
        }, 150);
      }
    });
  });

  // Quantity +/- on detail page
  const qtyMinus = document.getElementById('detail-qty-minus');
  const qtyPlus = document.getElementById('detail-qty-plus');
  const qtyInput = document.getElementById('detail-qty-input');

  if (qtyMinus && qtyPlus && qtyInput) {
    qtyMinus.addEventListener('click', () => {
      let val = parseInt(qtyInput.value) || 1;
      if (val > 1) {
        qtyInput.value = val - 1;
      }
    });
    qtyPlus.addEventListener('click', () => {
      let val = parseInt(qtyInput.value) || 1;
      const max = parseInt(qtyInput.getAttribute('max')) || 99;
      if (val < max) {
        qtyInput.value = val + 1;
      }
    });
  }
}

/* ============================================================
   Product Detail Tabs (Description / Specs / Reviews)
   ============================================================ */
function initDetailTabs() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  if (!tabBtns.length) return;

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetId = btn.dataset.tab;

      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));

      btn.classList.add('active');
      const targetContent = document.getElementById(targetId);
      if (targetContent) {
        targetContent.classList.add('active');
      }
    });
  });
}

/* ============================================================
   Checkout Payment Methods Interaction
   ============================================================ */
function initCheckoutPaymentMethods() {
  const paymentOptions = document.querySelectorAll('.payment-card-option');
  const cardFields = document.getElementById('card-fields-box');
  const upiFields = document.getElementById('upi-fields-box');

  if (!paymentOptions.length) return;

  paymentOptions.forEach(option => {
    option.addEventListener('click', () => {
      paymentOptions.forEach(opt => opt.classList.remove('selected'));
      option.classList.add('selected');

      const radio = option.querySelector('input[type="radio"]');
      if (radio) {
        radio.checked = true;
        const val = radio.value;
        if (cardFields) cardFields.style.display = val === 'card' ? 'block' : 'none';
        if (upiFields) upiFields.style.display = val === 'upi' ? 'block' : 'none';
      }
    });
  });
}

/* ============================================================
   Mobile Navigation Menu Drawer
   ============================================================ */
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

