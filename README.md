🗂️ Task Manager

  Task Manager is a Django-based web application for managing team tasks.
  Team members can create tasks, assign them to others, track deadlines, priorities, and completion status.
  
  🔗 Live demo:
  👉 You can test the app here: https://task-manager-pgom.onrender.com

🚀 Features

  User registration and authentication
  
  Users have positions (Developer, QA, Manager)
  
  Create, update, delete tasks
  
  Assign tasks to multiple users
  
  Task types, priorities, and deadlines
  
  Mark tasks as completed
  
  Welcome page for unauthenticated users
  
  Admin panel

⚙️ Local Setup
  git clone https://github.com/your-username/task-manager.git
  cd task-manager
  python -m venv .venv
  .venv\Scripts\activate
  pip install -r requirements.txt
  python manage.py migrate
  python manage.py runserver