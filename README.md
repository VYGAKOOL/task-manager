# 🗂️ Task Manager

Task Manager is a web application built with Django that helps teams manage tasks efficiently.
Users can create tasks, assign them to team members, track progress, and mark tasks as completed.

---

## 🚀 Features

- User authentication (Sign up / Login)
- Task creation and editing
- Assign tasks to multiple users
- Task prioritization and deadlines
- Mark tasks as completed
- Simple and clean UI

---

## 🌐 Live Demo

You can test the application here:  
👉 https://task-manager-pgom.onrender.com

**Demo credentials:**  
- Username: "alice"  
- Password: "alice123"

---

## ⚙️ Local Setup

```bash
git clone https://github.com/VYGAKOOL/task-manager
cd task-manager
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
