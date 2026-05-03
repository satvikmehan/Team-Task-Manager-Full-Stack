# 🚀 Team Task Manager (Full-Stack Django)

A full-stack application where users can create projects, assign tasks, and track progress with **role-based access control (Admin/Member)**. 
Featuring a modern, stunning **Glassmorphism UI**, the app provides a premium user experience out of the box.

Deployed live using Railway.

---

## 🌐 Live Demo

👉 https://web-production-b507d.up.railway.app/

---

## 📦 Features

### 🎨 Stunning Modern UI
*   **Glassmorphism & Gradients**: Premium frosted glass aesthetic with vibrant backgrounds.
*   **Responsive Design**: Works beautifully across desktop and mobile.
*   **Modern Typography & Interactions**: Fluid animations and sleek design elements.

### 🔐 Authentication
*   Session-based Web UI login & JWT-based REST APIs
*   Secure token-based access for APIs
*   Signup creates **Member** by default
*   Only Admin can manage roles

---

### 📁 Project Management
*   Admin can create, edit, and **delete** projects (Full CRUD)
*   Add/remove members to projects
*   Each project tracks its total task count dynamically
*   Each project has:
  * Owner
  * Team members

---

### ✅ Task Management
*   Create tasks within projects
*   Assign tasks to specific team members of a project
*   Status tracking:
  * TODO
  * IN_PROGRESS
  * DONE

---

### 📊 Project-First Dashboard
*   **Project Grid**: Displays assigned projects with their respective task counts.
*   **Drill-Down View**: Click a project to view tasks assigned specifically to you for that project.
*   **Stats Tracking**: Total tasks, completed tasks, and pending tasks.
*   **Smart Overdue Highlighting**: Tasks that are past their due date are automatically highlighted in red.

---

### 🔒 Role-Based Access Control

| Action                 | Admin | Member                 |
| ---------------------- | ----- | ---------------------- |
| Create/Edit/Delete Project | ✅     | ❌                      |
| Add/Remove Members     | ✅     | ❌                      |
| Create/Delete Task     | ✅     | ❌                      |
| Update Task Status     | ✅     | ✅ (assigned user only) |

---

## 🛠️ Tech Stack

* **Backend & Frontend**: Django (Templates + Views) + Django REST Framework
* **Styling**: Vanilla CSS (Modern Glassmorphism)
* **Authentication**: Django Sessions & JWT (SimpleJWT)
* **Database**: PostgreSQL (Railway) / SQLite (Local)
* **Deployment**: Railway
* **Server**: Gunicorn

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

## 🔑 How to Use the API

### 1. Login

```json
POST /accounts/login/
{
  "username": "admin",
  "password": "admin123"
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

* The application now features a fully integrated frontend built with Django templates, utilizing a modern Glassmorphism design system.
* Designed for scalability and clean architecture.
* Follows service-based logic separation.

---

## 👨‍💻 Author

Satvik Mehan
GitHub: https://github.com/satvikmehan
