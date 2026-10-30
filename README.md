# 🛍️ ShopSphere — Decoupled E-Commerce Platform

A professional, modern, fully functional e-commerce web platform architected with a **decoupled Client-Server structure**, separating the project cleanly into **`frontend/`** and **`backend/`**.

---

## 🏗️ Decoupled Architecture

```text
CodeAlpha_Simple E-Commerce Store/
├── frontend/                     # Pure HTML5 / CSS3 / JavaScript Client
│   ├── index.html                # Homepage with hero, categories, featured, deals
│   ├── products.html             # Catalog with department, price & rating filters
│   ├── product-detail.html       # Gallery switcher, specs tabs, reviews & ratings
│   ├── cart.html                 # Cart management (+/- qty, totals, promo code)
│   ├── checkout.html             # Shipping address & payment options (COD, Card, UPI)
│   ├── order-confirmation.html   # Animated checkmark, timeline tracker, printable invoice
│   ├── login.html                # User login with "Quick Demo Auto-Fill" buttons
│   ├── register.html             # User registration form with validation
│   ├── profile.html              # Account dashboard, shipping address & order history
│   ├── css/
│   │   └── style.css             # Design system with responsive variables & grid
│   └── js/
│       ├── config.js             # API base URL configuration (http://127.0.0.1:8000/api)
│       ├── api.js                # Reusable Fetch API client
│       └── main.js               # UI controller, cart badges, toasts, navigation
│
├── backend/                      # Python Django 5 & Django REST Framework
│   ├── manage.py                 # Django management CLI
│   ├── requirements.txt          # Python dependencies
│   ├── db.sqlite3                # Pre-seeded SQLite database
│   ├── shopsphere_core/          # Project settings, CORS config, and root URLs
│   │   ├── settings.py           # Configured with corsheaders & rest_framework
│   │   ├── api_urls.py           # REST API endpoints routing
│   │   └── urls.py               # Root URL configuration
│   ├── store/                    # Store app (models, admin, serializers, api_views)
│   │   └── management/commands/
│   │       └── seed_data.py      # Database seeding command
│   ├── cart/                     # Cart session logic, serializers & api_views
│   ├── orders/                   # Order & OrderItem models, serializers & api_views
│   ├── accounts/                 # Profile model, auth serializers & api_views
│   ├── static/                   # Static assets for Django Admin
│   └── templates/                # Django admin and template views
│
└── README.md                     # Documentation & setup instructions
```

---

## ⚡ REST API Endpoints (Backend)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/categories/` | List all active product categories |
| `GET` | `/api/products/` | Filter products by `category`, `q`, `min_price`, `max_price`, `rating`, `sort` |
| `GET` | `/api/products/<slug>/` | Single product details with gallery, reviews, and related items |
| `POST` | `/api/products/<slug>/reviews/` | Submit a product review and star rating |
| `GET` | `/api/cart/` | Retrieve current cart items, subtotal, shipping, tax, and total |
| `POST` | `/api/cart/add/` | Add a product and quantity to cart |
| `POST` | `/api/cart/update/` | Increase, decrease, or update line-item quantity |
| `POST` | `/api/cart/remove/` | Remove an item completely from cart |
| `POST` | `/api/cart/clear/` | Clear all items from cart |
| `POST` | `/api/orders/checkout/` | Process shipping address, payment method, decrement stock & create order |
| `GET` | `/api/orders/<order_number>/` | Retrieve order confirmation and itemized receipt |
| `POST` | `/api/auth/register/` | Register a new customer account |
| `POST` | `/api/auth/login/` | Authenticate customer or administrator |
| `POST` | `/api/auth/logout/` | End user session |
| `GET` | `/admin/` | Django Administration Panel (Full CRUD) |

---

## 🚀 How to Run in Visual Studio Code

### Step 1: Start the Backend (Django REST API)

1. Open the project folder `CodeAlpha_Simple E-Commerce Store` in VS Code.
2. Open the terminal (<kbd>Ctrl</kbd> + <kbd>`</kbd>).
3. Navigate into the `backend/` directory:
   ```powershell
   cd backend
   ```
4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
5. Apply database migrations and seed realistic sample products (already pre-loaded):
   ```powershell
   python manage.py migrate
   python manage.py seed_data
   ```
6. Start the Django development server:
   ```powershell
   python manage.py runserver
   ```
   The backend API will run at **`http://127.0.0.1:8000/`**.

---

### Step 2: Open and Run the Frontend

You can run the frontend in any of the following ways:

#### Option A: Using VS Code Live Server (Recommended)
1. Install the **Live Server** extension in VS Code (by *Ritwick Dey*).
2. Right-click on `frontend/index.html` in the VS Code file explorer.
3. Select **"Open with Live Server"**.
4. The frontend will launch at `http://127.0.0.1:5500/frontend/index.html`.

#### Option B: Direct in Browser
Simply double-click or drag `frontend/index.html` into your web browser (Chrome, Edge, Firefox, Safari).

#### Option C: Python Static HTTP Server
In a second terminal:
```powershell
cd frontend
python -m http.server 3000
```
Then visit **`http://127.0.0.1:3000/`**.

---

## 🔑 Demo & Admin Credentials

| Role | Username | Password | Notes |
|---|---|---|---|
| **Admin** | `admin` | `admin123` | Access backend admin portal at `http://127.0.0.1:8000/admin/` |
| **Customer** | `customer` | `customer123` | Pre-loaded address and order history |

> 💡 On `frontend/login.html`, click **"Fill Customer"** or **"Fill Admin"** to auto-fill the login form instantly!

---

## 🧪 Automated Testing

To run the backend test suite verifying all models, views, cart calculations, orders, and REST APIs:

```powershell
cd backend
python manage.py test
```
Result: **20 out of 20 tests pass (`OK`)**.
