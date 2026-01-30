# Fitmarket Gym Shop


[image](https://github.com/kryptonVal/fitmarket-gym-shop/issues/2#issue-2708732346) (screenshot link)

Fitmarket Gym Shop is a full-stack e-commerce web application built with Django and MySQL, designed to demonstrate practical software engineering skills including backend development, database design, testing, and clean architecture. The project simulates a real-world online retail platform for fitness apparel.

🎯 Project Purpose (Why this project)

This project was built to:

Apply computer science fundamentals in a real application

Practice backend development with Django

Implement scalable, maintainable architecture

Gain hands-on experience with databases, testing, and environment configuration

Simulate real e-commerce workflows (cart, checkout, orders)

🧩 Core Features

Product catalog with multiple categories (men, women, kids)

Product search by name

Shopping cart functionality (add, view, remove items)

Checkout and order confirmation flow

Server-side rendering with Django templates

Class-based views for maintainable logic

MySQL database integration

Unit tests for critical user flows

🛍️ Product Categories

Shoes

Shirts

Shorts

Leggings

Sports Bras

🏗️ Architecture & Engineering Practices

Framework: Django (MTV architecture)

Views: Class-Based Views (CBVs) for reuse and clarity

Database: MySQL with Django ORM

Environment Management: Virtual environments and .env configuration

Testing: Django unit tests for cart and order workflows

Version Control: Git & GitHub collaboration

🛠️ Tech Stack

Language: Python

Backend Framework: Django 5.1.3

Database: MySQL

IDE: PyCharm 2024.2.3

Key Dependencies

asgiref==3.8.1

mysqlclient==2.2.6

pillow==11.0.0

sqlparse==0.5.2

tzdata==2024.2

🚀 Getting Started
1. Clone the Repository
git clone https://github.com/kryptonVal/fitmarket-gym-shop.git
cd fitmarket-gym-shop

2. Create & Activate Virtual Environment
python -m venv venv


Activate:

Windows: venv\Scripts\activate

macOS/Linux: source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

4. Environment Configuration

Create a .env file in the project root:

DB_ENGINE=django.db.backends.mysql
DB_NAME=fitmarket_gym_shop
DB_USER=root
DB_PASSWORD=1234
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=your-secret-key


5. Database Setup

Ensure MySQL is running

Create database:

fitmarket_gym_shop


Apply migrations:

python manage.py makemigrations
python manage.py migrate

6. Run the Application
python manage.py runserver


Access at:
👉 http://127.0.0.1:8000/

✅ Testing

Unit tests were implemented for critical e-commerce functionality:

AddToCartTest

ViewCartTest

DeleteFromCartTest

CheckoutTest

OrderSuccessTest

Tests validate correctness of cart behavior and order flow using Django’s testing framework.

👥 Contributors

Valentine Okoye

Azeema Mehdi

Andrei Jerjomenko

Roman Tomusk

Tauri Luigand

🔮 Future Improvements

User authentication and profiles

Payment gateway integration

REST API endpoints

Frontend framework integration (React)

Performance and security enhancements
