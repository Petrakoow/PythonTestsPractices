### Практическая работа №5 (Часть 3) - Django проект для управления рецептами

В этой части практической работы мы создаём и тестируем важную функциональность для управления рецептами. Задание включает изменения в структуре тестов, создание тестов для маршрутов и проверки контента.

### Описание задания

В данном проекте были добавлены тесты для проверки:

- Корректной работы маршрутов для страниц рецептов, деталей рецепта и страницы "О каталоге".
- Правильного создания объектов и их атрибутов.
- Верности расчёта веса блюда при задании ингредиентов в различных единицах измерения.
- Сортировки ингредиентов по алфавиту.

Также была улучшена модель `Ingredient` с учётом единиц измерения и конверсии для различных единиц (например, ложки, стаканы). Были добавлены соответствующие тесты.

### Основные этапы выполнения работы

1. **Рефакторинг структуры тестов**: Тесты были перемещены в подкаталог `tests`, и теперь разделены на два файла: `test_routes.py` и `test_content.py`.
2. **Добавление тестов**: Написаны тесты для проверки работы маршрутов, создания объектов, расчёта веса блюда и вывода списка ингредиентов в алфавитном порядке.
3. **Использование единиц измерения**: В модель `Ingredient` добавлен внешний ключ на модель `Unit` для конверсии ингредиентов в граммы.

---

### Код

#### Модели

Модель `Ingredient` была обновлена с добавлением поля для единицы измерения:

```python
from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

class Unit(models.Model):
    name = models.CharField(max_length=20, unique=True)
    conversion_to_grams = models.FloatField(validators=[MinValueValidator(0.1)])

    def __str__(self):
        return self.name
    
class Ingredient(models.Model):
    title = models.CharField(max_length=255, validators=[RegexValidator(regex=r'^[A-Za-zА-Яа-яёЁ\s]+$')])
    raw_weight = models.FloatField(validators=[MinValueValidator(0.1)])
    cooked_weight = models.FloatField(validators=[MinValueValidator(0.1)])
    cost = models.FloatField(validators=[MinValueValidator(0.1)])
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.title} (Raw: {self.raw_weight} g, Cooked: {self.cooked_weight} g, Cost: ${self.cost})'

    def save(self, *args, **kwargs):
        if self.unit:
            self.raw_weight *= self.unit.conversion_to_grams
            self.cooked_weight *= self.unit.conversion_to_grams
        super().save(*args, **kwargs)
```

#### Админ

Панель администратора была настроена для управления единицами измерения:

```python
from django.contrib import admin
from .models import Ingredient, Recipe, Unit

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'conversion_to_grams']

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['title', 'raw_weight', 'cooked_weight', 'cost', 'unit']
```

#### Тесты

Тесты были разделены на два файла: `test_routes.py` и `test_content.py`.

**test_routes.py**

Тесты маршрутов проверяют правильность доступности страниц и ответов:

```python
from django.test import TestCase
from django.urls import reverse

class TestRoutes(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_page(self):
        recipe = Recipe.objects.create(title="Парфе")
        response = self.client.get(reverse('recipe_detail', args=[recipe.pk]))
        self.assertEqual(response.status_code, 200)
```

**test_content.py**

Тесты содержимого проверяют правильность данных, расчётов и валидации:

```python
from django.test import TestCase
from recipe_catalog.models import Ingredient, Recipe, Unit

class TestRecipeWeightCalculation(TestCase):
    def setUp(self):
        self.spoon = Unit.objects.create(name='Spoon', conversion_to_grams=20)
        self.glass = Unit.objects.create(name='Glass', conversion_to_grams=250)

    def test_recipe_total_weight_in_grams(self):
        ingredient_flour = Ingredient.objects.create(title="Мука", raw_weight=100, cooked_weight=90, cost=50)
        ingredient_sugar = Ingredient.objects.create(title="Сахар", raw_weight=200, cooked_weight=180, cost=60, unit=self.glass)
        recipe = Recipe.objects.create(title="Торт")
        recipe.ingredients.set([ingredient_flour, ingredient_sugar])

        total_weight = recipe.total_weight_in_grams()
        self.assertEqual(total_weight, 100 + (200 * 250))  # Вес с учётом конверсии стаканов в граммы
```

### Описание полей

#### Модель `Ingredient`
- **title** — Название ингредиента.
- **raw_weight** — Вес ингредиента до приготовления.
- **cooked_weight** — Вес ингредиента после приготовления.
- **cost** — Стоимость ингредиента.
- **unit** — Единица измерения, может быть `Spoon`, `Glass` или любая другая единица с конверсией в граммы.

#### Модель `Recipe`
- **title** — Название рецепта.
- **ingredients** — Список ингредиентов, привязанных к рецепту.

### Заключение

Эта часть практической работы демонстрирует улучшение функциональности Django проекта с добавлением новых возможностей для работы с ингредиентами и их единицами измерения, а также создание и тестирование маршрутов и логики отображения данных на страницах.