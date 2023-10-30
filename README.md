# vk-data-collector

---

## Обзор
`vk-data-collector` - это приложение на Django, разработанное в рамках проекта Petersburg Mood Project. Приложение предназначено для сбора и анализа данных из VKontakte (VK), популярного социального сервиса в России.

## Установка

### Предварительные требования
- Python 3.8 или выше
- pip (инсталлятор пакетов Python)

### Шаги
1. Клонирование репозитория:
    ```bash
    git clone https://github.com/petersburg-mood-project/vk-data-collector.git
    cd vk-data-collector
    ```

2. Создание виртуального окружения и его активация:
    ```bash
    python -m venv venv
    source venv/bin/activate  # На Windows используйте `venv\Scripts\activate`
    ```

3. Установка требуемых зависимостей:
    ```bash
    pip install -r requirements.txt
    ```

4. Настройка параметров базы данных в `vk_data_collector/settings.py`.

5. Выполнение миграции базы данных:
    ```bash
    python manage.py migrate
    ```

6. Создание суперпользователя для административного интерфейса Django:
    ```bash
    python manage.py createsuperuser
    ```

## Использование

1. Запуск сервера разработки Django:
    ```bash
    python manage.py runserver
    ```

2. Откройте веб-браузер и перейдите по адресу [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) для доступа к административному интерфейсу Django.

3. Войдите с учетными данными суперпользователя, которые вы создали ранее.

4. Через административный интерфейс вы можете управлять сбором данных VK.

## Конфигурация

- Учетные данные VK API: для сбора данных из VK вам нужно настроить учетные данные VK API в `vk_data_collector/settings.py`.

## Участие в проекте

Не стесняйтесь отправлять проблемы и запросы на перенос, мы всегда рады улучшить проект с помощью сообщества.
