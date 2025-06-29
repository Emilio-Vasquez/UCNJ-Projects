# **UCNJ Flask Full-Stack Starter Template**

This is a ready-to-use Flask full-stack starter project designed for instructional use at Union College of Union County, NJ. It includes a clean HTML structure using Jinja2 templating, a Flask app starter (`app.py`), and linked static assets (CSS, JS, images). Ideal for beginner to intermediate web application projects in a multi-page format.

---

## **Project Structure**

```
Template (you should rename this folder to your own specific project)/
├── app.py
├── .env # For environment variables (secret keys, so on...)
├── .gitignore # Hides .env and virtual environment from Git
├── requirements.txt # Add Python packages here, you can freeze your environment and pipe the libraries into this file
├── VirtualEnv/ # (Recommended) Virtual environment folder, you can rename it or create a new one: python -m venv MyVenv
│
├── templates/
│ ├── base.html # Main layout used by all pages
│ ├── index.html # Homepage
│ ├── login.html # (Placeholder for specific project instructions)
│ ├── registration.html# (Placeholder for specific project instructions)
│ ├── feedback.html # (Placeholder for specific project instructions)
│ └── about.html # (Placeholder for specific project instructions)
│
├── static/
│ ├── css/
│ │ └── styles.css # Custom styles
│ ├── js/
│ │ └── script.js # JavaScript logic
│ └── images/ # Static image assets
```

## **Setup Instructions**

> **This Flask template lives inside the `Template/` folder of the full UCNJ-Projects repository.**  
> For a full breakdown of the structure, walkthrough, and usage examples, visit:
> [https://github.com/Emilio-Vasquez/UCNJ-Projects-Template](https://github.com/Emilio-Vasquez/UCNJ-Projects-Template)
