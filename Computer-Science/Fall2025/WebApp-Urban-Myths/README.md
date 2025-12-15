# **UCNJ FLask full-stack starter template**
This is a ready-to-use Flask full-stack starter project designed for instructional use at Union College of Union County, NJ. It includes a clean HTML structure using Jinja2 templating, a Flask app starter (app.py), and linked static assets (CSS, JS, images). Ideal for beginner to intermediate web application projects in a multi-page format.
---
## **Project Structure**

Template/
├── app/
|   ├── __init__.py
|   ├── db.py
|   ├── login.py
|   ├── register.py
|   ├── routes.py
│   ├── VirtualEnv/
│   │   └── README.md # Placeholder file to give instructions on virtual Environments
│   ├── static/
│   │   ├── css/
│   │   │   └── ucnj_style.css
│   │   ├── images/
│   │   │   └── favicon.ico
│   │   ├── js/
│   │   │   ├── flash.js
│   │   │   ├── login.js
│   │   │   ├── register.js
│   │   │   └── reset_password.js
│   ├── templates/
│   │   ├── base.html # Main layout used by all pages
│   │   ├── index.html # Homepage
│   │   ├── login.html
│   │   ├── registration.html
│   │   ├── feedback.html
│   │   └── about.html
├── database/
│   └── schema.sql
├── .env
├── .gitignore
├── config.py
├── README.md
└── run.py