<p align="center">
    <a href="#">
        <img width="400" src="assets/Logo default.svg" />
    </a>
</p>

👋 Hi! This is a diet tracking app which enables users to create/modify and follow different diets in their day-to-day life with an easy-to-use interface!

---

## 🧐 Project philosophy

> This app was created for me and my girlfriend to try to motivate ourselves to follow a diet. Every dietary or meal planning app on the market didn't have what we wanted, or just cost a lot of money for the average college student, so we decided to work on the solution on our own. I learned a lot about programming and development on the way and I hope you will find this project interesting!

---

## ✨ Getting Started

### 1. Get the prerequisites

_🛠 This project requires `pip` and `Python 3.6` or above_. See: [Python downloads](https://www.python.org/downloads/). Additionally, two packages require further setup - those are:

- `Psycopg2` - installation [instructions](https://www.psycopg.org/docs/install.html#install-from-source)
- `Pillow` - installation [instructions](https://pillow.readthedocs.io/en/stable/installation.html)

### 2. Clone the repository and enter it

```sh
git clone --depth=1 https://github.com/TypicalAM/SpareSnack.git && cd SpareSnack
```

### 3. Install the dependencies

```sh
python3 -m pip install -r requirements.txt
```

### 4. Set up keys and make migrations


- 🔐 You need to set up some additional data for the application to work correctly, most of those are special environment variables like:

```sh
# core/settings.py variables
DEBUG=1
SECRET_KEY=my_secret_secret_key
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]

# core/settings.py/DATABASES configuration
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=my_db
SQL_USER=TypicalAM
SQL_PASSWORD=my_secret_password
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
```

You can also modify the existing configuration to not require having a `postgres` database with the `DATABASE` variable.

- Next, we have to make migrations and migrate the database

```sh
python3 manage.py makemigrations
python3 manage.py migrate
```

### 5. Run the app!

🌟 To run in a local environment

```sh
python3 manage.py runserver
```

## ✨ Starting the app in a container

If you have a possibility to run docker containers on your machine, you can also run the dev version of this product directly in the container using the provided `Dockerfile`. If you want to also use the `postgres` database engine however, you must also set up an image for a `postgres` database. A well-written guide I've found to do this is [here](https://testdriven.io/blog/dockerizing-django-with-postgres-gunicorn-and-nginx/).

## ❓ How do I even use it?

Glad you asked, there are four main components to the app:
- You have **Recipes**, which go in **Meals**. Each **Day** consists of five **Meals**.
- If you really liked a **Day** you can save it in a **Diet**, which can be public or private. If it is public everyone is able to see it and **import** it into their day. Importing is a process which involves *reusing* the days which have already been created to make the most out of your well-prepared **Days**.
- After creating an account (I won't steal your details) you can go into the **My Day** tab to see all the possible options that you have.
- Initially, it would be useful to also fill the database with ingredients, because it's hard to include them in this package since that would be a lot of data.

---

## 📸 Product images

<p align="center">
    <img src="assets/Day creation 2.png" />
</p>
<p align="center">
    <img src="assets/Meal browse.png" />
</p>
<p align="center">
    <img src="assets/Meal create.png" />
</p>
