# vk-data-collector

---

## Обзор | Overview
`vk-data-collector` - это приложение на Django, разработанное в рамках проекта [Прогнозирование социального самочувствия с целью оптимизации функционирования экосистемы городских цифровых сервисов Санкт-Петербурга](https://rscf.ru/project/23-28-10069/). Приложение предназначено для сбора и анализа данных из VKontakte (VK), популярного социального сервиса в России.
`vk-data-collector` is a Django-based application developed as part of the project [Forecasting Social Well-being to Optimize the Ecosystem of Urban Digital Services in St. Petersburg](https://rscf.ru/project/23-28-10069/). The application is designed to collect and analyze data from VKontakte (VK), a popular social networking service in Russia.

## Установка | Installation

### Предварительные требования | Prerequisites
- Python 3.8 или выше | Python 3.8 or later 
- pip (инсталлятор пакетов Python) | pip (Python package installer)

### Шаги | Steps
1. Клонирование репозитория: | Clone the repository:  
    ```bash
    git clone https://github.com/petersburg-mood-project/vk-data-collector.git
    cd vk-data-collector
    ```

2. Создание виртуального окружения и его активация: | Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # На Windows используйте `venv\Scripts\activate`
    ```

3. Установка требуемых зависимостей: | Install required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Настройка параметров базы данных в `vk_data_collector/settings.py` | Configure database settings in vk_data_collector/settings.py

5. Выполнение миграции базы данных: | Apply database migrations:
    ```bash
    python manage.py migrate
    ```

6. Создание суперпользователя для административного интерфейса Django: | Create a superuser for Django admin interface:
    ```bash
    python manage.py createsuperuser
    ```

## Использование | Usage

1. Запуск сервера разработки Django: | Run Django's development server:
    ```bash
    python manage.py runserver
    ```

2. Откройте веб-браузер и перейдите по адресу [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) для доступа к административному интерфейсу Django.
   Open a web browser and navigate to http://127.0.0.1:8000/admin to access the Django admin interface.

4. Войдите с учетными данными суперпользователя, которые вы создали ранее.
   Log in with the superuser credentials created earlier.

5. Через административный интерфейс вы можете управлять сбором данных VK.
   Use the admin interface to manage VK data collection.

## Конфигурация | Configuration

- Учетные данные VK API: для сбора данных из VK вам нужно настроить учетные данные VK API в `vk_data_collector/settings.py`.
- VK API credentials: To collect data from VK, set up the VK API credentials in `vk_data_collector/settings.py`.

## Участие в проекте | Contribution

Не стесняйтесь отправлять проблемы и запросы на перенос, мы всегда рады улучшить проект с помощью сообщества.
Feel free to submit issues and pull requests; we welcome community contributions to improve the project.
