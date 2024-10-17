from django.db import models

# Create your models here.

class Ingredient:
    MAX_COST = 1000

    def __init__(
        self,
        name: str,
        raw_weight: (int, float),
        cooked_weight: (int, float),
        cost: (int, float),
    ) -> None:
        self.name = name
        self.raw_weight = raw_weight
        self.cooked_weight = cooked_weight
        self.cost = cost

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Name must be a string.")
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        self._name = value

    @property
    def raw_weight(self):
        return self._raw_weight

    @raw_weight.setter
    def raw_weight(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Raw weight must be a number.")
        if value <= 0:
            raise ValueError("Raw weight must be positive.")
        self._raw_weight = value

    @property
    def cooked_weight(self):
        return self._cooked_weight

    @cooked_weight.setter
    def cooked_weight(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Cooked weight must be a number.")
        if value <= 0:
            raise ValueError("Cooked weight must be positive.")
        self._cooked_weight = value

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Cost must be a number.")
        if value < 0:
            raise ValueError("Cost must be non-negative.")
        if value > 1000:
            raise ValueError("Cost exceeds the maximum allowed value.")
        self._cost = value

    def __str__(self) -> str:
        return (
            f"---------------------\n"
            f"Ingredient: {self.name}\n"
            f"Raw Weight: {self.raw_weight}\n"
            f"Cooked Weight: {self.cooked_weight}\n"
            f"Cost: ${self.cost:.2f}\n"
            f"---------------------\n"
        )


class Receipt:
    _id_counter = 1
    def __init__(
        self, name: str, ingredient_list: list[tuple[str, float, float, float]]
    ):
        self.id = Receipt._id_counter
        Receipt._id_counter += 1
        self.name = name
        self.ingredients = [Ingredient(*ingredient) for ingredient in ingredient_list]

    @property
    def name(self):
        return self._name
    
    @property
    def id(self):
        return self._id;
    
    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("ID must be an integer.")
        if value <= 0:
            raise ValueError("ID must be a positive number.")
        self._id = value

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Recipe name must be a string.")
        if not value.strip():
            raise ValueError("Recipe name cannot be empty.")
        self._name = value

    @property
    def ingredients(self):
        return self._ingredients

    @ingredients.setter
    def ingredients(self, value: list[Ingredient]):
        if not isinstance(value, list):
            raise ValueError("Ingredients must be a list.")
        if not all(isinstance(ingredient, Ingredient) for ingredient in value):
            raise ValueError(
                "All items in the ingredient list must be instances of Ingredient."
            )
        if not value:
            raise ValueError("Ingredient list cannot be empty.")
        self._ingredients = value

    def calc_cost(self, portions=1):
        total_cost = sum(ingredient.cost for ingredient in self.ingredients)
        return total_cost * portions

    def calc_weight(self, portions=1, raw=True):
        if raw:
            total_weight = sum(ingredient.raw_weight for ingredient in self.ingredients)
        else:
            total_weight = sum(
                ingredient.cooked_weight for ingredient in self.ingredients
            )
        return total_weight * portions

    def __str__(self) -> str:
        ingredient_details = "\n".join(
            str(ingredient) for ingredient in self.ingredients
        )
        return (
            f"Recipe: {self.name}\n###All Receipt Ingredients###\n{ingredient_details}"
        )