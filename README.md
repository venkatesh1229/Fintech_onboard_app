# PayOnboard — Fintech Merchant Onboarding Platform

A full-stack merchant onboarding application built with **React**, **FastAPI**, and **MySQL**.

---

## Project Structure

```
fintech-onboarding/
├── backend/                    ← FastAPI Python backend
│   ├── app/
│   │   ├── main.py             ← App entry point, route registration
│   │   ├── config.py           ← Environment variables / settings
│   │   ├── database.py         ← SQLAlchemy DB connection + session
│   │   ├── models.py           ← Database table definitions (ORM)
│   │   ├── schemas.py          ← Request/response validation (Pydantic)
│   │   ├── auth.py             ← JWT token create/decode
│   │   ├── dependencies.py     ← Route guards (get_current_user, get_current_admin)
│   │   ├── routes/
│   │   │   ├── auth_routes.py         ← Register, Login, Admin Login
│   │   │   ├── application_routes.py  ← Submit, Get Status
│   │   │   ├── admin_routes.py        ← View all, Update status
│   │   │   └── upload_routes.py       ← Document file upload
│   │   ├── utils/
│   │   │   └── hashing.py      ← bcrypt password hash/verify
│   │   └── middleware/
│   │       └── cors.py         ← Allow React frontend calls
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/                   ← React frontend
│   └── src/
│       ├── App.js              ← Root component (BrowserRouter + AuthProvider)
│       ├── index.js            ← React DOM mount
│       ├── context/
│       │   └── AuthContext.jsx ← Global auth state (login/logout/token)
│       ├── services/
│       │   └── api.js          ← All axios API calls (auto JWT injection)
│       ├── routes/
│       │   └── AppRoutes.jsx   ← All URL route definitions
│       ├── components/
│       │   └── ProtectedRoute.jsx ← Route guard (redirects if not logged in)
│       ├── pages/
│       │   ├── Register.jsx        ← Merchant registration form
│       │   ├── Login.jsx           ← Merchant login
│       │   ├── AdminLogin.jsx      ← Admin login
│       │   ├── MerchantDashboard.jsx ← Merchant home
│       │   ├── ApplyForm.jsx       ← Submit application + upload docs
│       │   ├── StatusPage.jsx      ← Application status tracker
│       │   ├── AdminDashboard.jsx  ← Admin: all applications
│       │   └── ApplicationDetails.jsx ← Admin: review + update status
│       └── styles/
│           ├── global.css      ← CSS variables, reset, utilities
│           ├── auth.css        ← Login/Register page styles
│           └── dashboard.css   ← Dashboard, table, upload styles
│
└── database/
    └── schema.sql              ← MySQL table creation script
```

---

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- MySQL 8.0+

---

### 1. Database Setup

```bash
# Create database and tables
mysql -u root -p < database/schema.sql
```

---

### 2. Backend Setup

```bash
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env: set DATABASE_URL and SECRET_KEY

# Run the FastAPI server
uvicorn app.main:app --reload --port 8000
```

API will be available at: `http://localhost:8000`  
Interactive API docs: `http://localhost:8000/docs`

---

### 3. Frontend Setup

```bash
cd frontend

# Install Node dependencies
npm install

# Start React development server
npm start
```

Frontend will open at: `http://localhost:3000`

---

## API Endpoints

| Method | URL | Description | Auth |
|--------|-----|-------------|------|
| POST | `/api/auth/register` | Merchant registration | Public |
| POST | `/api/auth/login` | Merchant login → JWT | Public |
| POST | `/api/auth/admin/login` | Admin login → JWT | Public |
| POST | `/api/application/submit` | Submit application | Merchant JWT |
| GET  | `/api/application/status` | Get own status | Merchant JWT |
| POST | `/api/upload/document` | Upload document file | Merchant JWT |
| GET  | `/api/admin/applications` | List all applications | Admin JWT |
| GET  | `/api/admin/applications/{id}` | Application detail | Admin JWT |
| PUT  | `/api/admin/applications/{id}/status` | Update status | Admin JWT |

---

## How JWT Authentication Works

1. User logs in → backend returns a **JWT token**
2. Frontend stores token in **localStorage**
3. Every API request includes: `Authorization: Bearer <token>`
4. Backend decodes the token to identify the user/role
5. Protected routes reject requests with missing/invalid tokens

---

## Default Admin Account

Email: `admin@company.com`  
Password: `admin123`  
*(Change these immediately in production!)*

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, React Router v6, Axios |
| Backend | FastAPI, SQLAlchemy, Pydantic |
| Database | MySQL 8 |
| Auth | JWT (python-jose), bcrypt (passlib) |
| Styling | Custom CSS with CSS Variables |
