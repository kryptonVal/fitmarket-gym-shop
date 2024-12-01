# Fitmarket Gym Shop


[image](https://github.com/kryptonVal/fitmarket-gym-shop/issues/2#issue-2708732346) (screenshot link)

Fitmarket Gym Shop is an online shop that offers a stylish and functional range of gym clothing designed for fitness enthusiasts. 
The shop features a diverse selection of activewear for both men, women, and kids. Products in the store includes  shoes, shirts, leggings, shorts, and sports bras. Each piece is crafted with high-quality materials that prioritize comfort and performance, ensuring that customers can look great while achieving their fitness goals.
The user can search products in the stroe site by product name. 

## Technology
This project is based on:

pycharm 2024.2.3,
Django	5.1.3,
mysqlclient	2.2.6

## Installation


1. Clone the repository:

* In Pycharm git clone URL https://github.com/kryptonVal/fitmarket-gym-shop.git

* Install the project dependencies:

pip install -r requirements.txt
asgiref 3.8.1
pillow 11.0.0
sqlparse 0.5.2
tzdata 2024.2


2. Create a virtual environment and install dependencies:

python -m venv venv

It will
Create a New Directory.
Copy Python Executable.
Create Site Packages Directory
Create Activation Scripts. These scripts are located in:
venv/Scripts/activate (on Windows)
venv/bin/activate (on macOS/Linux)

pip install -r requirements.txt

Create environment file:
 .env
insert following
DB_ENGINE= "django.db.backends.mysql"
DB_NAME="fitmarket_gym_shop"
DB_USER="root"
DB_PASSWORD="1234"
DB_HOST="localhost"
DB_PORT="3306"
SECRET_KEY = 'django-insecure-4b#a5qv_lp*qszyre)3t=&+aiq6mke&yh!_4a$!w!ax+2m%6ev'


3. Database Setup

Ensure MySQL is installed and running.

In MySQL Workbench create a MySQL database named fitmarket_gym_shop. (create schema)

Update the database configuration in .env with your MySQL credentials (user, password, root)

python manage.py makemigrations
python manage.py migrate

Start the development server

python manage.py runserver
server at http://127.0.0.1:8000/

## Views
In this project we use class_based views.


## Testing
In our Project, we ran test for Cart and  Orders. 
Using Pycharms test.py, we ran 5 tests: AddToCartTest, ViewCartTest, DeleteFromCartTest, CheckoutTest, and OrderSuccessTest.



## Credits
This project was made as a collaboration by

Valentine

Azeema Mehdi

Andrei Jerjomenko

Roman Tomusk

Tauri Luigand
