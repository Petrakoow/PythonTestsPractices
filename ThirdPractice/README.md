## Результат работы

![Result work](img/index.png)

![Result work](img/about.png)

![Result work](img/receipt.png)

### Создание виртуального окружения

1. Переход в каталог проекта:
   ```bash
   cd ~/super_django_prj
   ```

2. Создание виртуального окружения:
   ```bash
   python3.12 -m venv .venv
   ```
   Эта команда создает виртуальное окружение `.venv` для изоляции зависимостей проекта.

3. Активация виртуального окружения:
   ```bash
   source .venv/bin/activate
   ```
   Активация виртуального окружения.

4. Обновление менеджера пакетов `pip`:
   ```bash
   python -m pip install --upgrade pip
   ```
   Здесь `pip` обновляется до последней версии для установки зависимостей.

5. Установка Django:
   ```bash
   pip install Django==4.2.16
   ```
   Устанавливаем Django версии 4.2.16 в виртуальном окружении.

### Создание Django-проекта

**Команда** `django-admin startproject recipe_project`

Команда `django-admin startproject recipe_project` используется для создания нового Django-проекта. В моем случае она создает проект с именем `recipe_project`.

После выполнения команды создаются следующие файлы и каталоги:

- **recipe_project/** — основная директория проекта, содержащая файлы конфигурации проекта.
  - **__init__.py** — пустой файл, который указывает, что этот каталог является модулем Python.
  - **settings.py** — файл конфигурации проекта, в котором находятся настройки базы данных, приложений и других параметров Django.
  - **urls.py** — файл, в котором определяется маршрутизация URL для проекта.
  - **asgi.py** — файл для настройки ASGI-приложения, используемого для асинхронного взаимодействия.
  - **wsgi.py** — файл для настройки WSGI-приложения, необходимого для развертывания проекта на веб-серверах.
  
- **manage.py** — утилита командной строки для управления проектом, используемая для выполнения различных команд, таких как запуск сервера разработки, миграции базы данных и другие. 

### Пробный запуск проекта

После запуска команды `python manage.py runserver`, Django запустил сервер разработки, который отслеживает изменения в файлах и автоматически их применяет. Сервер начал работать по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/), однако было выявлено, что у проекта есть 18 непримененных миграций для встроенных приложений Django, таких как `admin`, `auth`, `contenttypes` и `sessions`. Эти миграции нужно применить командой `python manage.py migrate`, чтобы проект работал корректно.

 - Решение: миграции `python manage.py migrate`

### Создание первого приложения

Для создания приложения в Django была использована команда:

```bash
python manage.py startapp recipe_catalog
```

Эта команда создала структуру файлов и папок для нового приложения `recipe_catalog`. Приложение будет использоваться для реализации функционала каталога рецептов. После выполнения команды структура проекта выглядит следующим образом:

```
.
├── db.sqlite3               # База данных проекта
├── manage.py                # Основной скрипт для управления проектом
├── recipe_catalog           # Папка созданного приложения
│   ├── __init__.py          # Указывает, что это пакет Python
│   ├── admin.py             # Настройки административной панели
│   ├── apps.py              # Конфигурация приложения
│   ├── migrations           # Папка для миграций базы данных
│   │   └── __init__.py      # Указывает, что это пакет для миграций
│   ├── models.py            # Определение моделей для базы данных
│   ├── tests.py             # Тесты приложения
│   └── views.py             # Логика обработки запросов
└── recipe_project           # Основная конфигурация проекта
    ├── __init__.py
    ├── asgi.py              # Настройки для ASGI-сервера
    ├── settings.py          # Настройки проекта
    ├── urls.py              # Маршрутизация проекта
    └── wsgi.py              # Настройки для WSGI-сервера
```

Теперь можно добавлять модели, представления и другие компоненты, чтобы реализовать необходимый функционал для каталога рецептов.

### Регистрация приложения

После создания приложения `recipe_catalog`, его необходимо зарегистрировать в проекте, чтобы Django знал о его существовании и мог обрабатывать его модели, маршруты и другую логику.

Для этого в файле `settings.py`, который находится в папке `recipe_project`, было добавлено следующее:

```python
INSTALLED_APPS = [
    'recipe_catalog.apps.RecipeCatalogConfig',  # Регистрация приложения recipe_catalog
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

Здесь строка `'recipe_catalog.apps.RecipeCatalogConfig'` указывает Django, что нужно использовать конфигурацию приложения, которая описана в файле `apps.py`. Теперь Django будет учитывать `recipe_catalog` при запуске и в ходе выполнения проекта.

### Протокол HTTP(S)

HTTP (HyperText Transfer Protocol) — это сетевой протокол прикладного уровня, разработанный для передачи гипертекстовых документов в формате HTML между клиентом и сервером. Со временем HTTP стал универсальным инструментом для взаимодействия между различными узлами как в глобальной сети, так и в локальных веб-инфраструктурах. Используя HTTP(S), веб-приложения могут обмениваться данными, загружать контент и поддерживать сессию с пользователями.

Этот протокол лежит в основе разработки большинства современных веб-приложений, таких как наше приложение для управления рецептами, созданное с помощью Django.

### Подключение путей в проекте Django

В данном шаге я настраиваю маршрутизацию для приложения `recipe_catalog`. Это позволяет связать URL-адреса с соответствующими представлениями (views), которые будут обрабатывать запросы и возвращать нужный контент пользователям.

Внутри файла `recipe_catalog/urls.py` я создаю пути для главной страницы (`index`), страницы с подробной информацией о рецепте (`recipe_detail`), и страницы «О нас» (`about`):

```python
from django.urls import path
from .views import about, index, recipe_detail

urlpatterns = [
    path('', index, name='index'),
    path('recipe/<int:pk>/', recipe_detail, name='recipe_detail'),
    path('about/', about, name='about')
]
```

Затем в основном файле конфигурации проекта `recipe_project/urls.py` я подключаю маршруты приложения `recipe_catalog` через функцию `include()`:

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('recipe_catalog.urls')),
]
```

Это позволяет передавать управление URL-адресами в отдельное приложение и организовывать код более структурировано.

### Привязка шаблонов страниц

В файле конфигурации `settings.py` я настроил систему шаблонов Django, указав директорию для хранения шаблонов проекта. 

Добавил следующее:
- Путь к папке с шаблонами `TEMPLATES_DIR = BASE_DIR / 'templates'`, чтобы шаблоны хранились в директории `templates` в корне проекта.
- Включил параметр `'DIRS': [TEMPLATES_DIR]` в настройках шаблонов, чтобы Django знал, где искать пользовательские шаблоны.
- Активировал параметр `'APP_DIRS': True`, чтобы позволить Django искать шаблоны и в директориях приложений.
- Обработчики контекста, такие как `'django.template.context_processors.request'`, были добавлены для корректной обработки данных, передаваемых в шаблоны. 

Эта настройка помогает связывать логику и HTML-страницы для отображения в браузере.

Дальше добавляем директорию `templates/recipe_catalog` и добавляем туда страницу `index.html`

### Добавление модели

- Берём модель из практической работы №2 и добавляем в `models.py`

- Создаем файл constants.py, в который кладем коллекцию наших рецептов

### Редактирование views

- добавляем hook на обработку запросов, получаем по id нужный рецепт и отдаем его в ответе на отображение

- `about(request)`: Возвращает шаблон страницы "О проекте" (`about.html`).

- `index(request)`: Отображает главную страницу каталога рецептов. Шаблон `index.html` рендерится с контекстом, содержащим все рецепты из константы `recipes`.

- `recipe_detail(request, pk)`: Отвечает за отображение детальной информации о конкретном рецепте. 
    - Ищет рецепт по его `id` (передается через `pk`).
    - Если рецепт не найден, вызывает исключение `Http404`.
    - Вычисляет и отображает общий вес ингредиентов в сыром (`raw=True`) и приготовленном виде (`raw=False`) для одной порции.
    - Результаты передаются в шаблон `recipe.html` вместе с рецептом для отображения пользователю.

```python
def recipe_detail(request, pk):
    recipe = next((r for r in recipes if r.id == pk), None)
    if recipe is None:
        raise Http404("Recipe does not exist")
    
    total_raw_weight = recipe.calc_weight(raw=True, portions=1)
    total_cooked_weight = recipe.calc_weight(raw=False, portions=1)
    
    return render(
        request=request,
        template_name='recipe_catalog/recipe.html',
        context={
            'recipe': recipe,
            'total_raw_weight': total_raw_weight,
            'total_cooked_weight': total_cooked_weight,
        }
    )
```
