<p align="center">
    <a href="https://www.teknofest.az/">
        <img width="400" src="assets/Logo default.svg" />
    </a>
</p>

👋 Hi! This is a diet tracking app which enables users to create/modify and follow different diets in their day to day life with an easy to use interface!

---

## 🧐 Project philosophy

> This app was created for me and my girlfriend to try to motivate ourselves to follow a diet. Every dietary or meal planning app on the market didn't have what we wanted, or just cost a lot of money for the average college student so we decided to work on the solution on our own. I learned a lot about programming and development on the way and I hope you will find this project interesting!

---

## ✨ Getting Started

### 1. Get the prerequisites

_🛠 This project requires `pip` and `Python 3.6` or above_. See: [Python downloads](https://www.python.org/downloads/)

### 2. Clone the repository

```sh
git clone --depth=1 https://github.com/TypicalAM/sparesnack-new.git
```

### 3. Install the dependencies

```sh
python3 -m pip install -r requirements.txt
```

### 4. Set up keys and make migrations

- 👤 You need to make migrations and set up an authorized user

```sh
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py createsuperuser
```

### 5. Run the app!

🌟 To run in a local environment

```sh
python3 manage.py runserver
```

---

## 📸 Product images

<p align="center">
    <img src="assets/Day creation.png" />
</p>
