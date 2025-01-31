# FastAPI Backend - For the kissan connect
# Note 

- There is complete env file and the db also uploaded for the use case of the development for the new developer . To help the new developer i have made followed the practice to let the new developer enjoy the beauty of the backend . Happy learnig .
## 🚀 Overview
This is the backend API for **Kissan Connect**, a platform designed to connect farmers and buyers. It provides user authentication, product listing, bidding system, order management, notifications, and an insurance module.

## 📌 Features
- User authentication (Signup/Login with role-based access)
- Product listing and management
- Bidding system for buyers and farmers
- Order confirmation and tracking
- Notifications for bids, orders, and updates
- Insurance management (apply, claim)

---

## 🏗️ Setup Instructions

### 1️⃣ Prerequisites
Ensure you have the following installed:
- Python 3.10+
- FastAPI
- SQLite (or PostgreSQL for production)
- Uvicorn

### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 3️⃣ Run the Application
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 4️⃣ Database Setup
Ensure the database is created:
```bash
sqlite3 backend.db "PRAGMA table_info(users);"
```

---

## 📌 API Endpoints

### 🔐 Authentication
| Method | Endpoint | Body | Description |
|--------|---------|------|-------------|
| POST | `/auth/signup` | `{ full_name, email, phone, password, role }` | Register a new user |
| POST | `/auth/login` | `{ username, password }` | Login and get JWT token |
| GET | `/auth/me` | Headers: `Authorization: Bearer {token}` | Get current user details |

### 📦 Products
| Method | Endpoint | Body | Description |
|--------|---------|------|-------------|
| POST | `/products/` | `{ name, price, quantity, image_url }` | List a new product (farmer only) |
| GET | `/products/` | None | Fetch all available products |

### ⚖️ Bidding System
| Method | Endpoint | Body | Description |
|--------|---------|------|-------------|
| GET | `/bids/` | None | Fetch bids received by a farmer |
| POST | `/bids/place` | `{ product_id, amount }` | Place a bid on a product (buyer) |
| PUT | `/bids/{bid_id}/update?status=accepted` | Query: `status=accepted/rejected` | Accept or reject a bid |

### 📦 Orders
| Method | Endpoint | Body | Description |
|--------|---------|------|-------------|
| POST | `/orders/confirm` | `{ bid_id }` | Confirm an accepted bid and create an order |
| GET | `/orders/` | None | Get all orders for a user |

### 🔔 Notifications
| Method | Endpoint | Body | Description |
|--------|---------|------|-------------|
| GET | `/notifications/` | None | Fetch notifications for the logged-in user |

### 🛡️ Insurance
| Method | Endpoint | Body | Description |
|--------|---------|------|-------------|
| GET | `/insurance/` | None | Fetch available insurance plans (filtered by role) |
| POST | `/insurance/apply` | `{ insurance_id }` | Apply for an insurance plan |
| POST | `/insurance/claim` | `{ insurance_id, reason }` | Claim an insurance plan |

---

## 🛠️ Testing with Postman
1. Import the API collection into Postman.
2. Set `Authorization` as `Bearer {access_token}` for protected routes.
3. Test different functionalities like user signup, bidding, and insurance.

---


## 🔍 Troubleshooting
### ✅ Common Issues
- **Login failure:** Ensure the credentials are correct and the database has users.
- **Unauthorized requests:** Include the `Authorization` header in requests.
- **Database not updating:** Run `sqlite3 backend.db` and check data consistency.

---

## 📜 License
This project is licensed under **MIT License**.

---

## 🙌 Contributors
- **Shit_code** - Lead Developer

For any issues, feel free to open a GitHub issue or contact us. 🚀
