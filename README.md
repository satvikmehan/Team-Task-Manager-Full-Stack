# 🚀 Team Task Manager (Django + DRF)

A backend system where users can create projects, assign tasks, and track progress with **role-based access control (Admin/Member)**.

Deployed live using Railway.

---

## 🌐 Live Demo

👉 https://web-production-b507d.up.railway.app/

---

## 📦 Features

### 🔐 Authentication

* JWT-based login system
* Secure token-based access
* Signup creates **Member** by default
* Only Admin can manage roles

---

### 📁 Project Management

* Admin can create projects
* Add/remove members to projects
* Each project has:

  * Owner
  * Team members

---

### ✅ Task Management

* Create tasks within projects
* Assign tasks to team members
* Status tracking:

  * TODO
  * IN_PROGRESS
  * DONE

---

### 📊 Dashboard

* Total tasks
* Completed tasks
* Pending tasks
* Overdue tasks
* Status breakdown

---

### 🔒 Role-Based Access Control

| Action             | Admin | Member                 |
| ------------------ | ----- | ---------------------- |
| Create Project     | ✅     | ❌                      |
| Add Members        | ✅     | ❌                      |
| Create Task        | ✅     | ❌                      |
| Update Task Status | ❌     | ✅ (assigned user only) |

---

## 🛠️ Tech Stack

* Backend: Django + Django REST Framework
* Authentication: JWT (SimpleJWT)
* Database: PostgreSQL (Railway)
* Deployment: Railway
* Server: Gunicorn

---

## 🔌 API Endpoints

### 🔐 Auth

* `POST /accounts/signup/`
* `POST /accounts/login/`

---

### 📁 Projects

* `POST /projects/create/`
* `GET /projects/`
* `POST /projects/{id}/add-members/`

---

### ✅ Tasks

* `POST /tasks/create/`
* `PATCH /tasks/{id}/update/`
* `GET /tasks/`

---

### 📊 Dashboard

* `GET /tasks/dashboard/`

---

## 🔑 How to Use

### 1. Login

```json
POST /accounts/login/
{
  "username": "admin",
  "password": "1234"
}
```

---

### 2. Use Token

Add header:

```
Authorization: Bearer <access_token>
```

---

## ⚙️ Setup Locally

```bash
git clone <repo_url>
cd Team-Task-Manager

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

---

## 🚀 Deployment

Deployed on Railway with:

* PostgreSQL
* Environment variables
* Gunicorn
* Auto migrations via Procfile

---

## 🎥 Demo Video

👉 (Add your 2–5 min demo video link here)

---

## 📌 Notes

* Backend is API-first (frontend can be added easily)
* Designed for scalability and clean architecture
* Follows service-based logic separation

---

## 👨‍💻 Author

Satvik Mehan
GitHub: https://github.com/satvikmehan
