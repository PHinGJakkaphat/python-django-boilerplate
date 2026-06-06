# 🐍 Django Boilerplate

> **Django 5+ REST API boilerplate** — พร้อม Custom User Model, PostgreSQL, drf-spectacular (ReDoc / Swagger), Logging, Debug Toolbar และ base utilities สำหรับเริ่มต้นโปรเจกต์ได้เลย

---

## 📋 สารบัญ

- [Tech Stack](#-tech-stack)
- [โครงสร้างโปรเจกต์](#-โครงสร้างโปรเจกต์)
- [การติดตั้งและเริ่มต้นใช้งาน](#-การติดตั้งและเริ่มต้นใช้งาน)
- [Environment Variables](#-environment-variables)
- [การรัน Server](#-การรัน-server)
- [API Documentation](#-api-documentation)
- [Custom Utilities](#-custom-utilities)
- [การเพิ่ม App ใหม่](#-การเพิ่ม-app-ใหม่)
- [การรัน Tests](#-การรัน-tests)
- [Logging](#-logging)

---

## 🛠 Tech Stack

| Package | Version | หน้าที่ |
|---|---|---|
| **Django** | ≥ 5.0 | Web framework |
| **djangorestframework** | ≥ 3.15 | REST API |
| **drf-spectacular** | ≥ 0.28 | OpenAPI schema (ReDoc + Swagger) |
| **psycopg2-binary** | ≥ 2.9 | PostgreSQL adapter |
| **python-decouple** | ≥ 3.8 | Environment variable management |
| **django-debug-toolbar** | ≥ 4.4 | Debug panel |
| **Pillow** | ≥ 10.0 | Image / avatar support |

---

## 📁 โครงสร้างโปรเจกต์

```
django-boilerplate/
├── accounts/               # Custom User Model + Auth endpoints
│   ├── models.py           # User model (email-based login)
│   ├── managers.py         # UserManager
│   ├── views.py            # Login, Logout, Me, Change Password
│   ├── urls.py
│   ├── docs.py             # OpenAPI schema constants (swagger_auto_schema)
│   ├── forms.py
│   └── admin.py
│
├── common/                 # Shared utilities
│   ├── serializers.py      # BaseSerializer / BaseModelSerializer (รองรับ Meta.examples)
│   ├── openapi_helper.py   # swagger_auto_schema wrapper + openapi_response
│   └── pagination.py       # CustomPageNumberPagination
│
├── config/                 # Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── tests/
│   ├── cases/              # Test cases แยกตาม app
│   └── fixtures/           # Test fixtures
│
├── logs/                   # Log files (auto-generated)
│   ├── django.log
│   ├── errors.log
│   └── security.log
│
├── static/                 # Static files
├── .env.example            # ตัวอย่าง environment variables
├── requirements.txt
└── manage.py
```

---

## 🚀 การติดตั้งและเริ่มต้นใช้งาน

### 1. Clone โปรเจกต์

```bash
git clone <repository-url>
cd django-boilerplate
```

### 2. สร้าง Virtual Environment

```bash
# สร้าง venv
python -m venv venv

# Activate (Linux / macOS)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### 3. ติดตั้ง Dependencies

```bash
pip install -r requirements.txt
```

### 4. ตั้งค่า Environment Variables

```bash
# Copy ไฟล์ตัวอย่าง
cp .env.example .env
```

จากนั้นแก้ไข `.env` ตามสภาพแวดล้อมของคุณ (ดู [Environment Variables](#-environment-variables))

### 5. สร้าง Database

```bash
# สร้าง database ใน PostgreSQL ก่อน
psql -U postgres -c "CREATE DATABASE django_boilerplate;"
```

### 6. รัน Migrations

```bash
python manage.py migrate
```

### 7. สร้าง Superuser (Admin)

```bash
python manage.py createsuperuser
```

> ระบบใช้ **email** เป็น username field — กรอก email และ password

---

## 🔑 Environment Variables

คัดลอกจาก `.env.example` แล้วแก้ไขค่าต่าง ๆ:

```env
# ============================================================
# Security
# ============================================================
SECRET_KEY=your-very-secret-key-here-replace-me   # ⚠️ เปลี่ยนค่านี้ทุกครั้ง
DEBUG=True

# Allowed Hosts (comma-separated)
ALLOWED_HOSTS=127.0.0.1,localhost

# ============================================================
# Database (PostgreSQL)
# ============================================================
DB_ENGINE=django.db.backends.postgresql
DB_NAME=django_boilerplate
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# ============================================================
# Static & Media
# ============================================================
STATIC_URL=/static/
MEDIA_URL=/media/

# ============================================================
# Timezone
# ============================================================
TIME_ZONE=Asia/Bangkok
```

> **สร้าง SECRET_KEY ใหม่:**
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

---

## ▶️ การรัน Server

```bash
python manage.py runserver
```

| URL | หน้าที่ |
|---|---|
| `http://127.0.0.1:8000/admin/` | Django Admin |
| `http://127.0.0.1:8000/api/docs/redoc/` | ReDoc API Docs |
| `http://127.0.0.1:8000/api/docs/swagger/` | Swagger UI |
| `http://127.0.0.1:8000/api/schema/` | OpenAPI JSON Schema |
| `http://127.0.0.1:8000/__debug__/` | Debug Toolbar |

---

## 📚 API Documentation

โปรเจกต์ใช้ **drf-spectacular** สำหรับ generate OpenAPI schema อัตโนมัติ

### Endpoints ที่มีอยู่แล้ว (`accounts/`)

| Method | Path | หน้าที่ |
|---|---|---|
| `GET` | `/accounts/health/` | Health check |
| `POST` | `/accounts/login/` | Login ด้วย email + password |
| `POST` | `/accounts/logout/` | Logout |
| `GET` | `/accounts/me/` | ดึงข้อมูล profile ตัวเอง |
| `PATCH` | `/accounts/me/` | แก้ไข profile |
| `POST` | `/accounts/change-password/` | เปลี่ยน password |

### การเพิ่ม API Schema ให้ View

ใช้ `swagger_auto_schema` จาก `common.openapi_helper` ในไฟล์ `docs.py`:

```python
# myapp/docs.py
from common.openapi_helper import openapi_response, swagger_auto_schema
from myapp.serializers import MySerializer

GET_LIST = {
    "method": "GET",
    "operation_id": "List Items",
    "operation_description": "Returns a list of items.",
    "responses": {
        200: openapi_response(MySerializer, "Success"),
    },
    "tags": ["items"],
}
```

```python
# myapp/views.py
from common.openapi_helper import swagger_auto_schema
from myapp.docs import GET_LIST

class MyView(APIView):
    @swagger_auto_schema(**GET_LIST)
    def get(self, request):
        ...
```

---

## 🔧 Custom Utilities

### `BaseModelSerializer` — พร้อม `Meta.examples`

ใช้แทน `rest_framework.serializers.ModelSerializer` เพื่อให้กำหนด examples สำหรับ ReDoc ได้โดยตรงใน `class Meta`:

```python
from common.serializers import BaseModelSerializer

class UserSerializer(BaseModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name", "date_joined"]

        # ✅ Examples จะแสดงใน ReDoc / Swagger UI อัตโนมัติ
        examples = {
            "Standard User": {
                "summary": "ผู้ใช้ทั่วไป",
                "value": {
                    "id": 1,
                    "email": "jane@example.com",
                    "username": "jane_doe",
                    "first_name": "Jane",
                    "last_name": "Doe",
                    "date_joined": "2024-01-15T09:30:00Z",
                },
            },
        }
```

**Short-form** (example เดียว, flat dict):

```python
examples = {
    "id": 1,
    "email": "jane@example.com",
}
```

### `CustomPageNumberPagination`

Pagination สำเร็จรูป — response format:

```json
{
    "count": 100,
    "next": "http://api.example.com/items/?page=2",
    "previous": null,
    "results": [...]
}
```

### Logging

ใช้งาน logger ใน app ต่าง ๆ:

```python
import logging
logger = logging.getLogger("accounts")   # หรือชื่อ app ของคุณ

logger.info("User logged in: %s", user.email)
logger.error("Something went wrong", exc_info=True)
```

Log files จะอยู่ที่:
- `logs/django.log` — INFO ขึ้นไป
- `logs/errors.log` — ERROR ขึ้นไป
- `logs/security.log` — Security warnings

---

## 🏗 การเพิ่ม App ใหม่

```bash
python manage.py startapp myapp
```

จากนั้นเพิ่ม app ใน `config/settings.py`:

```python
LOCAL_APPS = [
    "accounts",
    "myapp",   # ✅ เพิ่มตรงนี้
]
```

เพิ่ม logger สำหรับ app ใหม่ใน `LOGGING` config (`config/settings.py`):

```python
"loggers": {
    ...
    "myapp": {
        "handlers": ["console", "django_file", "error_file"],
        "level": "DEBUG",
        "propagate": False,
    },
}
```

โครงสร้างแนะนำสำหรับ app ใหม่:

```
myapp/
├── models.py
├── serializers.py   # ใช้ BaseModelSerializer จาก common
├── views.py
├── urls.py
├── docs.py          # OpenAPI schema constants
├── admin.py
└── apps.py
```

---

## 🧪 การรัน Tests

```bash
# รัน test ทั้งหมด
python manage.py test tests

# รัน test เฉพาะ app
python manage.py test tests.cases.test_accounts_user

# รัน test พร้อม verbosity
python manage.py test tests --verbosity=2
```

Test files อยู่ใน `tests/cases/` — แยกตาม app

---

## 🔐 Production Checklist

ก่อน deploy ขึ้น production ให้ตรวจสอบ:

- [ ] `SECRET_KEY` เปลี่ยนเป็น key ใหม่ที่ไม่ได้ใช้ที่ไหนมาก่อน
- [ ] `DEBUG=False`
- [ ] `ALLOWED_HOSTS` ตั้งค่า domain จริง
- [ ] Database credentials ปลอดภัย
- [ ] รัน `python manage.py collectstatic`
- [ ] ตั้งค่า Email backend สำหรับ `mail_admins` handler
- [ ] ใช้ HTTPS + ตั้งค่า `SECURE_*` settings

---
