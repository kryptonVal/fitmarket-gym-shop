# Fitmarket Gym Shop


[image](https://github.com/kryptonVal/fitmarket-gym-shop/issues/2#issue-2708732346) (screenshot link)

Fitmarket Gym Shop is a modern online store that offers a stylish and functional range of gym apparel, designed specifically for fitness enthusiasts. The platform provides a diverse selection of activewear for men, women, and kids, including:

👟 Shoes
👕 Shirts
🩳 Shorts
🧘‍♀️ Leggings
🏋️‍♀️ Sports Bras

All products are crafted with high-quality materials that prioritize comfort and performance, helping customers look great while achieving their fitness goals.

🔍 Users can search products by name directly on the site.

**🛠️ Technology Stack:**

This project was built using:

PyCharm 2024.2.3
Django 5.1.3
mysqlclient 2.2.6

🚀 **Installation & Setup:**

1. Clone the Repository
You can clone the project using Git in PyCharm or your terminal:

git clone https://github.com/kryptonVal/fitmarket-gym-shop.git
cd fitmarket-gym-shop

2. Create and Activate Virtual Environment
python -m venv venv

Activate the virtual environment:

Windows:
venv\Scripts\activate

macOS/Linux:
source venv/bin/activate

3. Install Dependencies
Install all required packages using the provided requirements.txt:

pip install -r requirements.txt

Key dependencies:

asgiref==3.8.1
pillow==11.0.0
sqlparse==0.5.2
tzdata==2024.2

4. Environment Configuration
Create a .env file in the root directory with the following content:

DB_ENGINE=django.db.backends.mysql
DB_NAME=fitmarket_gym_shop
DB_USER=root
DB_PASSWORD=1234
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=django-insecure-4b#a5qv_lp*qszyre)3t=&+aiq6mke&yh!_4a$!w!ax+2m%6ev

5. Database Setup
Ensure MySQL is installed and running.

Open MySQL Workbench or any preferred MySQL client
Create a database named: fitmarket_gym_shop

Run the following Django commands to apply migrations:

python manage.py makemigrations
python manage.py migrate

6. Start Development Server
python manage.py runserver

Your app will be running at:
http://127.0.0.1:8000/

**👀 Views**
This project uses class-based views throughout the application to handle logic and rendering efficiently.

**✅ Testing**
We have implemented unit tests for cart and order functionalities. Using test.py in PyCharm, the following tests were run:

AddToCartTest
ViewCartTest
DeleteFromCartTest
CheckoutTest
OrderSuccessTest

**👥 Credits**
This project is a collaborative effort by:

Valentine
Azeema Mehdi
Andrei Jerjomenko
Roman Tomusk
Tauri Luigand

