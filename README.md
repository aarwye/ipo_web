
# IPO Web Application & REST API — Bluestock Fintech Internship Project

A full-stack web application that displays both **admin-uploaded** and **live IPO data** fetched from the **Finnhub API**.
Built as part of the Bluestock Fintech Internship to demonstrate end-to-end full-stack development — covering backend design, REST API development, frontend integration, database configuration, testing, and CI/CD automation.

---

## 🚀 Project Overview

This project provides a platform to:

* View **IPO listings** (both internal/admin-uploaded and external live IPO data)
* Manage IPO records via Django Admin
* Fetch **real-time IPO data** from the [Finnhub API](https://finnhub.io/docs/api/ipo-calendar)
* View all IPOs in a responsive React interface using cards
* Perform CRUD operations via REST API
* Ensure **code quality and reliability** using automated testing and a **GitHub Actions CI pipeline**

---

## 🧠 Tech Stack

| Layer                | Technology                     | Purpose                              |
| -------------------- | ------------------------------ | ------------------------------------ |
| **Frontend**         | React.js                       | Responsive client-side UI            |
| **Backend**          | Django + Django REST Framework | API development                      |
| **Database**         | PostgreSQL                     | Data persistence                     |
| **External API**     | Finnhub API                    | Live IPO data integration            |
| **Version Control**  | Git & GitHub                   | Collaboration and version management |
| **Testing**          | Pytest, Django TestCase        | Unit & integration testing           |
| **CI/CD**            | GitHub Actions                 | Continuous Integration               |
| **API Testing Tool** | Postman                        | Manual API testing and documentation |

---

## ⚙️ Architecture

```
Client (React)
     ↓
REST API (Django REST Framework)
     ↓
PostgreSQL Database
     ↑
External API (Finnhub)
```

**Data Flow:**

1. React frontend sends requests to the Django backend.
2. Django fetches data from its own database and the Finnhub API.
3. Combined data is serialized and returned as JSON.
4. Frontend displays IPOs in styled cards.

---

## 🏗️ Project Structure

```
webapp/
│
├── backend/
│   ├── ipo_backend/            # Django project settings
│   ├── ipo_app/                # Main app containing models, views, serializers, tests
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/         # React UI components
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
│
└── .github/
    └── workflows/
        └── django-ci.yml       # CI workflow definition
```

---

## 🧩 Features

✅ **Backend**

* Django REST Framework-based CRUD APIs
* PostgreSQL integration
* Admin interface for IPO management
* Combined data endpoint (`/all-ipos/`) merging database & Finnhub API data

✅ **Frontend**

* Built with React.js
* Fetches IPO data from Django REST API
* Displays data in modern card layout
* Handles both local and external data seamlessly

✅ **External API Integration**

* Uses `finnhub-python` client
* Fetches IPO calendar data with fields like:

  * Name
  * Exchange
  * Number of Shares
  * Price
  * Status
  * Symbol

✅ **Testing**

* Unit tests for models and views
* Pytest and Django’s TestCase used
* Coverage integrated with CI

✅ **CI/CD**

* GitHub Actions workflow to:

  * Install dependencies
  * Run migrations
  * Execute tests
  * Validate code automatically on every push or PR

---

## ⚙️ Backend Setup (Django)

### 1️⃣ Create and Activate a Virtual Environment

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # (Windows)
# or
source venv/bin/activate  # (Mac/Linux)
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure PostgreSQL

Create a database (e.g., `ipo_db`) and update your `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ipo_db',
        'USER': 'postgres',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 4️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Create a Superuser (for Admin)

```bash
python manage.py createsuperuser
```

### 6️⃣ Run the Server

```bash
python manage.py runserver
```

---

## 🖥️ Frontend Setup (React)

### 1️⃣ Create React App

```bash
cd ../
npx create-react-app frontend
```

### 2️⃣ Install Axios

```bash
cd frontend
npm install axios
```

### 3️⃣ Example API Integration (inside `App.js`)

```javascript
import React, { useEffect, useState } from "react";
import axios from "axios";

const App = () => {
  const [ipos, setIpos] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/all-ipos/")
      .then(res => setIpos(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="container">
      <h1>IPO Listings</h1>
      <div className="ipo-grid">
        {ipos.map((ipo, index) => (
          <div className="ipo-card" key={index}>
            <h3>{ipo.name || ipo.company_name}</h3>
            <p><b>Price:</b> {ipo.price || ipo.price_band}</p>
            <p><b>Status:</b> {ipo.status}</p>
            <p><b>Date:</b> {ipo.date || ipo.open_date}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;
```

### 4️⃣ Start Frontend

```bash
npm start
```

Then visit [http://localhost:3000](http://localhost:3000)

---

## 🧾 API Endpoints

| Method | Endpoint      | Description                   |
| ------ | ------------- | ----------------------------- |
| GET    | `/ipos/`      | Get all IPOs from DB          |
| POST   | `/ipos/`      | Create a new IPO              |
| GET    | `/ipos/{id}/` | Retrieve IPO by ID            |
| PUT    | `/ipos/{id}/` | Update IPO                    |
| DELETE | `/ipos/{id}/` | Delete IPO                    |
| GET    | `/all-ipos/`  | Combined local + Finnhub IPOs |

---

## 🌐 External API Integration (Finnhub)

**File:** `ipo_app/views.py`

```python
import finnhub
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import IPO
from .serializers import IPOSerializer

@api_view(['GET'])
def all_ipos(request):
    # Local IPO data
    local_ipos = IPO.objects.all()
    local_data = IPOSerializer(local_ipos, many=True).data

    # External IPO data
    finnhub_client = finnhub.Client(api_key="YOUR_API_KEY")
    external_data = finnhub_client.ipo_calendar(_from="2025-01-01", to="2025-12-31")["ipoCalendar"]

    # Combine
    combined_data = local_data + external_data
    return Response(combined_data)
```

---

## 🧪 Testing

**Run tests locally:**

```bash
cd backend
pytest
# or
python manage.py test ipo_app
```

**Example test (tests.py):**

```python
from django.test import TestCase
from .models import IPO

class IPOModelTest(TestCase):
    def setUp(self):
        self.ipo = IPO.objects.create(company_name="TestCorp", status="Open")

    def test_str_method(self):
        self.assertEqual(str(self.ipo), "TestCorp")
```

---

## 🤖 Continuous Integration (CI/CD)

**Workflow File:** `.github/workflows/django-ci.yml`

**Purpose:**
Automatically tests every commit and pull request using GitHub Actions.

**Key steps:**

* Set up Python environment
* Start PostgreSQL service
* Install all dependencies
* Run Django migrations
* Execute all tests

✅ **You can verify it works**:

* Go to your GitHub repo → **Actions tab**
* Check “Django CI Pipeline”
* If it shows a green check ✅ → All tests passed

---

## 🧮 requirements.txt

```txt
Django==5.0.3
djangorestframework==3.15.1
django-cors-headers==4.3.1
psycopg2-binary==2.9.9
python-decouple==3.8
requests==2.32.3
finnhub-python==2.4.18
pytest==8.3.2
pytest-django==4.9.0
coverage==7.5.4
responses==0.25.3
```

---

## 🔍 API Testing with Postman

You can test your endpoints easily with Postman:

1. Open Postman → New Request
2. Method: `GET`
3. URL: `http://127.0.0.1:8000/all-ipos/`
4. Click “Send” → Should display IPO JSON data.

---

## 📊 Future Enhancements

* Add IPO detail view pages
* Implement search and filtering
* Deploy backend on Render / Railway
* Deploy frontend on Vercel / Netlify
* Add caching for faster API responses
* Integrate coverage reports into CI badges

---
