# WEB_Project — Криптовалютный трекер (CryptoPulse)

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?logo=flask&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-D71F00)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL%20%2F%20SQLite-DB-336791?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)

Веб-приложение на базе **Flask** и **SQLAlchemy** для мониторинга актуальных рыночных котировок криптовалют. Сервис включает полноценную систему регистрации и аутентификации пользователей, отказоустойчивую интеграцию со сторонними биржевыми API, локальное кэширование рыночных данных и поддержку запуска в изолированных Docker-контейнерах.

---

## Основной функционал

* **Регистрация и аутентификация:** создание учётных записей, валидация форм (`Flask-WTF`), безопасное хеширование паролей (`Werkzeug`) и управление пользовательскими сессиями.
* **Мониторинг котировок криптовалют:** получение актуальных курсов, рыночных показателей и динамики цен через внешние биржевые API (модуль `api_check.py`).
* **Отказоустойчивость и кэширование:** обработка сетевых таймаутов и ошибок стороннего API с сохранением и агрегацией снимков котировок в JSON-хранилище (`crypt_info/`) для бесперебойной отдачи данных.
* **Работа с базой данных через ORM:** объектно-реляционное отображение на базе `SQLAlchemy` с поддержкой как серверной СУБД **PostgreSQL** (при запуске через Docker Compose), так и локальной базы **SQLite** (`db/krypto.db`) для быстрой разработки.
* **Адаптивный веб-интерфейс:** серверный рендеринг шаблонов `Jinja2` с кастомной стилизацией страниц авторизации и главного дашборда.

---

## Технологический стек

* **Backend:** Python 3.11+, Flask, Flask-WTF, Werkzeug
* **База данных и ORM:** SQLAlchemy, PostgreSQL 15 / SQLite
* **Внешние интеграции и сеть:** `requests` / `httpx` (REST API интеграция, обработка таймаутов)
* **Frontend:** HTML5, CSS3 (`style.css`, `main_page_style.css`), шаблонизатор Jinja2
* **Инфраструктура:** Docker, Docker Compose, Git

---

## Архитектура и структура проекта

```text
WEB_Project/
├── crypt_info/                  # Кэшированные снимки котировок и ответов внешнего API
│   ├── crypto_2.json
│   └── crypto_3.json
├── data/                        # Слой работы с базой данных (SQLAlchemy ORM)
│   ├── __all_models.py          # Регистрация моделей ORM
│   ├── db_session.py            # Инициализация подключения, фабрика сессий и схемы БД
│   └── users.py                 # Модель пользователя (User) и методы работы с паролями
├── db/                          # Локальное хранилище базы данных (SQLite fallback)
│   └── krypto.db
├── forms/                       # Формы валидации пользовательского ввода (WTForms)
│   └── user.py                  # Формы регистрации и входа в систему
├── static/
│   └── css/                     # Таблицы стилей интерфейса
│       ├── main_page_style.css
│       └── style.css
├── templates/                   # HTML-шаблоны (Jinja2)
│   ├── log_reg_base.html        # Базовый шаблон страниц авторизации
│   ├── login.html               # Страница входа
│   ├── register.html            # Страница регистрации
│   └── main_page.html           # Главный дашборд с курсами криптовалют
├── api_check.py                 # Модуль интеграции со сторонним крипто-API и обновления котировок
├── main.py                      # Точка входа, маршрутизация (routes) и запуск Flask-сервера
├── Dockerfile                   # Инструкция сборки Docker-образа приложения
├── docker-compose.yml           # Оркестрация контейнеров (Flask App + PostgreSQL)
└── requirements.txt             # Зависимости Python
```

---

## Быстрый запуск проекта

### Вариант 1. Запуск в Docker (PostgreSQL + Flask) — рекомендуемый

1. Клонируйте репозиторий и перейдите в директорию проекта:
   ```bash
   git clone https://github.com/Mihanikus55/WEB_Project.git
   cd WEB_Project
   ```

2. Запустите сборку и контейнеры через Docker Compose:
   ```bash
   docker-compose up --build -d
   ```

3. Приложение автоматически инициализирует схему базы данных и будет доступно в браузере по адресу:
   ```text
   http://localhost:5000
   ```

### Вариант 2. Локальный запуск (для разработки)

1. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux / macOS
   venv\Scripts\activate         # Windows
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустите сервер приложения:
   ```bash
   python main.py
   ```

---

## Основные маршруты приложения

| Метод | Маршрут | Описание | Шаблон / Модуль |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Главная страница с таблицей актуальных котировок криптовалют | `main_page.html` |
| `GET, POST` | `/register` | Регистрация нового пользователя с валидацией формы и хешированием пароля | `register.html` / `forms/user.py` |
| `GET, POST` | `/login` | Аутентификация пользователя и открытие сессии | `login.html` / `forms/user.py` |
| `GET` | `/logout` | Завершение текущей сессии пользователя | `main.py` |