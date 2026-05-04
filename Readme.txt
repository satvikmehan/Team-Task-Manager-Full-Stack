TEAM TASK MANAGER
=================

A full-stack application where users can create projects, assign tasks, and track progress with role-based access control. Featuring a modern, stunning Glassmorphism UI, the app provides a premium user experience out of the box.


SUBMISSION
----------

- Live App: https://web-production-b507d.up.railway.app/
- GitHub Repository: https://github.com/satvikmehan/Team-Task-Manager-Full-Stack
- Demo Video: 


OVERVIEW
--------

This project is a full-stack task management application that features:

- Authentication with Web UI login and JWT APIs
- Project and team management
- Task assignment and status tracking
- Role-based access control for Admin and Member users
- A project-first dashboard with task counts and overdue highlighting
- Deployment using Railway

The application uses Django for both backend (Templates + Views) and API (Django REST Framework), with a Vanilla CSS frontend featuring modern Glassmorphism and PostgreSQL for relational data management.


FEATURES
--------

- Session-based Web UI login & secure token-based JWT APIs
- Signup creates Member by default
- Admin can create, edit, and delete projects
- Add/remove members to projects
- Create, assign, update, and delete tasks
- Track task status with TODO, IN_PROGRESS, and DONE
- Project Grid dashboard displaying assigned projects with task counts
- Stats tracking: total, completed, and pending tasks
- Smart Overdue Highlighting for past-due tasks


ROLES
-----

ADMIN
- Create, edit, and delete projects
- Add or remove members to a project
- Manage user roles
- Create and delete tasks
- Update task status

MEMBER
- Access projects they belong to
- Update task status (assigned user only)
- View project tasks and dashboards


TECH STACK
----------

- Backend & Frontend: Django (Templates + Views) + Django REST Framework
- Styling: Vanilla CSS (Modern Glassmorphism)
- Database: PostgreSQL (Railway) / SQLite (Local)
- Authentication: Django Sessions & JWT (SimpleJWT)
- Server: Gunicorn
- Deployment: Railway


PROJECT STRUCTURE
-----------------

Team-Task-Manager/
├── accounts/          # Authentication and user management
├── core/              # Main Django project settings
├── projects/          # Project management logic and views
├── tasks/             # Task management logic and views
├── templates/         # HTML templates (Glassmorphism UI)
├── manage.py          # Django entry point
├── requirements.txt   # Python dependencies
├── Procfile           # Railway deployment config
└── README.md


DATABASE DESIGN
---------------

The backend uses PostgreSQL (on production) and SQLite (locally) with Django's ORM for strong data relationships.

Main entities:
- User
- Project
- Task

Relationships:
- One project has an Owner and Team members
- One project can have many tasks
- One task can be assigned to one user


API SUMMARY
-----------

AUTH
- POST /accounts/signup/
- POST /accounts/login/

PROJECTS
- GET /projects/
- POST /projects/create/
- POST /projects/{id}/add-members/

TASKS
- GET /tasks/
- POST /tasks/create/
- PATCH /tasks/{id}/update/

DASHBOARD
- GET /tasks/dashboard/


LOCAL SETUP
-----------

1. Clone the repository:
git clone https://github.com/satvikmehan/Team-Task-Manager-Full-Stack.git
cd Team-Task-Manager-Full-Stack

2. Setup environment:
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

3. Run migrations and start server:
python manage.py migrate
python manage.py runserver


DEPLOYMENT
----------

The app is deployed on Railway with:

- PostgreSQL database service
- Environment variables configured
- Gunicorn for serving the WSGI application
- Auto migrations via Procfile

ENVIRONMENT VARIABLES:
DATABASE_URL=${{Postgres.DATABASE_URL}}
SECRET_KEY=your_secret_here
DEBUG=False
ALLOWED_HOSTS=web-production-b507d.up.railway.app


UI NOTES
--------

The frontend features a fully integrated modern Glassmorphism design system:

- Premium frosted glass aesthetic with vibrant backgrounds.
- Fluid animations and sleek design elements.
- Responsive design that works beautifully across desktop and mobile.


WHAT I WOULD IMPROVE NEXT
-------------------------

- Kanban drag-and-drop task board
- Team avatars and profile settings
- Activity timeline and notifications
- Search and filters for tasks
- Email invite workflow


AUTHOR
------

- Satvik Mehan
- GitHub: https://github.com/satvikmehan
