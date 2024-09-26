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
    def __init__(
        self, name: str, ingredient_list: list[tuple[str, float, float, float]]
    ):
        self.name = name
        self.ingredients = [Ingredient(*ingredient) for ingredient in ingredient_list]

    @property
    def name(self):
        return self._name

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

# (П)етраков-> (П)арфе - Входные аргументы для второй практической работы

if __name__ == "__main__":
    receipt_from_api = {
        "title": "Яичница с беконом и помидорами.",
        "ingredients_list": [
            ("Яйцо", 80, 70, 20),
            ("Бекон", 200, 100, 300),
            ("Помидор", 100, 80, 200),
        ],
    }

    receipt = Receipt(receipt_from_api["title"], receipt_from_api["ingredients_list"])
    print(
        f"Общий вес сырого продукта: {receipt.calc_weight()}\nОбщий вес готового продукта: {receipt.calc_weight(raw=False)}\n"
    )
    print(receipt.__str__())
