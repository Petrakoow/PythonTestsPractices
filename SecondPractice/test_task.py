import unittest
from task import Ingredient, Receipt

class TestIngredient(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.valid_ingredient_data = {
            "name": "Яйцо",
            "raw_weight": 80,
            "cooked_weight": 70,
            "cost": 20
        }
        cls.invalid_cost_data = -10
    
    def setUp(self):
        self.ingredient = Ingredient(
            self.valid_ingredient_data['name'],
            self.valid_ingredient_data['raw_weight'],
            self.valid_ingredient_data['cooked_weight'],
            self.valid_ingredient_data['cost']
        )

    def tearDown(self):
        del self.ingredient

    @classmethod
    def tearDownClass(cls):
        cls.valid_ingredient_data = None
        cls.invalid_cost_data = None

    def test_valid_ingredient(self):
        self.assertEqual(self.ingredient.name, "Яйцо")
        self.assertEqual(self.ingredient.raw_weight, 80)
        self.assertEqual(self.ingredient.cooked_weight, 70)
        self.assertEqual(self.ingredient.cost, 20)

    def test_invalid_raw_weight(self):
        with self.assertRaises(ValueError):
            Ingredient("Яйцо", -10, 70, 20)
        with self.assertRaises(ValueError):
            Ingredient("Яйцо", 0, 70, 20)
        with self.assertRaises(ValueError):
            Ingredient("Яйцо", "двадцать", 70, 20)

    def test_invalid_cooked_weight(self):
        with self.assertRaises(ValueError):
            Ingredient("Яйцо", 80, -10, 20)
        with self.assertRaises(ValueError):
            Ingredient("Яйцо", 80, 0, 20)
        with self.assertRaises(ValueError):
            Ingredient("Яйцо", 80, "двадцать", 20)

    def test_invalid_cost(self):
        with self.assertRaises(ValueError):
            Ingredient("Яйцо", 80, 70, self.invalid_cost_data)
        with self.assertRaises(ValueError):
            Ingredient("Яйцо", 80, 70, 2000)  # exceeds MAX_COST
        with self.assertRaises(ValueError):
            Ingredient("Яйцо", 80, 70, "двадцать")

    def test_zero_cost(self):
        ingredient = Ingredient("Яйцо", 80, 70, 0)
        self.assertEqual(ingredient.cost, 0)

    def test_boundary_cost(self):
        ingredient = Ingredient("Яйцо", 80, 70, 1000)  # MAX_COST
        self.assertEqual(ingredient.cost, 1000)

    def test_float_weights_and_cost(self):
        ingredient = Ingredient("Яйцо", 80.5, 70.5, 19.99)
        self.assertEqual(ingredient.raw_weight, 80.5)
        self.assertEqual(ingredient.cooked_weight, 70.5)
        self.assertEqual(ingredient.cost, 19.99)

    def test_name_as_non_string(self):
        with self.assertRaises(TypeError):
            Ingredient(123, 80, 70, 20)

    def test_empty_name(self):
        with self.assertRaises(ValueError):
            Ingredient("", 80, 70, 20)


class TestReceiptSurname(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.receipt_from_api_parfait = {
            "title": "Парфе с ягодами и сливками.",
            "ingredients_list": [
                ("Йогурт", 200, 180, 50),
                ("Сливки", 100, 90, 100),
                ("Ягоды", 150, 150, 120),
                ("Мёд", 50, 50, 80),
                ("Мюсли", 60, 60, 40)
            ]
        }
    
    def setUp(self):
        self.receipt_parfait = Receipt(
            self.receipt_from_api_parfait["title"],
            self.receipt_from_api_parfait["ingredients_list"]
        )

    def tearDown(self):
        del self.receipt_parfait

    @classmethod
    def tearDownClass(cls):
        cls.receipt_from_api_parfait = None

    def test_valid_receipt(self):
        self.assertEqual(self.receipt_parfait.name, "Парфе с ягодами и сливками.")
        self.assertEqual(len(self.receipt_parfait.ingredients), 5)

    def test_calc_cost(self):
        self.assertEqual(self.receipt_parfait.calc_cost(), 390) 
        self.assertEqual(self.receipt_parfait.calc_cost(2), 780) 

    def test_calc_weight(self):
        self.assertEqual(self.receipt_parfait.calc_weight(), 560)  
        self.assertEqual(self.receipt_parfait.calc_weight(raw=False), 530)  
        self.assertEqual(self.receipt_parfait.calc_weight(portions=2), 1120) 

    def test_invalid_ingredient_list(self):
        with self.assertRaises(ValueError):
            Receipt("Парфе", []) 
    
    def test_invalid_ingredient_list(self):
        with self.assertRaises(ValueError):
            Receipt("Парфе", [])
        with self.assertRaises(ValueError):
            Receipt("Парфе", [("Сахар", -100, 90, 50)])

    def test_receipt_with_single_ingredient(self):
        receipt_single = Receipt("Простой рецепт", [("Вода", 100, 100, 0)])
        self.assertEqual(receipt_single.calc_cost(), 0)
        self.assertEqual(receipt_single.calc_weight(), 100)

    def test_receipt_as_string(self):
        receipt_str = str(self.receipt_parfait)
        self.assertIn("Парфе с ягодами и сливками.", receipt_str)
        self.assertIn("Йогурт", receipt_str)
        self.assertIn("Мюсли", receipt_str)


class TestReceiptName(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.receipt_from_api_erundopel = {
            "title": "Ерундопель - Запечённое лакомство с секретом.",
            "ingredients_list": [
                ("Творог", 250, 230, 180),
                ("Сметана", 100, 95, 80),
                ("Яйца", 2, 2, 50),  
                ("Сахар", 80, 80, 40),
                ("Мука", 100, 100, 90),
                ("Ванилин", 1, 1, 5)
            ]
        }
        cls.invalid_ingredient_list = [("Мука", -100, 100, 90)]  
    
    def setUp(self):
        self.receipt_erundopel = Receipt(
            self.receipt_from_api_erundopel["title"],
            self.receipt_from_api_erundopel["ingredients_list"]
        )

    def tearDown(self):
        del self.receipt_erundopel

    @classmethod
    def tearDownClass(cls):
        cls.receipt_from_api_erundopel = None
        cls.invalid_ingredient_list = None

    def test_valid_receipt(self):
        self.assertEqual(self.receipt_erundopel.name, "Ерундопель - Запечённое лакомство с секретом.")
        self.assertEqual(len(self.receipt_erundopel.ingredients), 6)

    def test_invalid_receipt_name(self):
        with self.assertRaises(ValueError):
            Receipt("", self.receipt_from_api_erundopel["ingredients_list"])
        with self.assertRaises(ValueError):
            Receipt(123, self.receipt_from_api_erundopel["ingredients_list"])  

    def test_invalid_ingredient_list(self):
        with self.assertRaises(ValueError):
            Receipt("Невалидный рецепт", [])  
        with self.assertRaises(ValueError):
            Receipt("Невалидный рецепт", self.invalid_ingredient_list) 

    def test_invalid_receipt_with_invalid_ingredient(self):
        with self.assertRaises(ValueError):
            Receipt("Невалидный рецепт", [("Мука", -100, 100, 90)])  

    def test_receipt_with_duplicate_ingredients(self):
        duplicate_ingredients = [
            ("Творог", 250, 230, 180),
            ("Творог", 250, 230, 180)
        ]
        receipt = Receipt("Дублирующийся рецепт", duplicate_ingredients)
        self.assertEqual(len(receipt.ingredients), 2)

    def test_empty_ingredient_name(self):
        with self.assertRaises(ValueError):
            Receipt("Невалидный рецепт", [("", 100, 100, 50)])

    def test_receipt_as_string(self):
        receipt_str = str(self.receipt_erundopel)
        self.assertIn("Ерундопель - Запечённое лакомство с секретом.", receipt_str)
        self.assertIn("Творог", receipt_str)
        self.assertIn("Ванилин", receipt_str)

    def test_calc_cost(self):
        self.assertEqual(self.receipt_erundopel.calc_cost(), 445)
        self.assertEqual(self.receipt_erundopel.calc_cost(2), 890) 

    def test_calc_weight(self):
        self.assertEqual(self.receipt_erundopel.calc_weight(), 533)
        self.assertEqual(self.receipt_erundopel.calc_weight(raw=False), 508)  

    def test_receipt_with_single_ingredient(self):
        receipt_single = Receipt("Простой рецепт", [("Вода", 100, 100, 0)])
        self.assertEqual(receipt_single.calc_cost(), 0)
        self.assertEqual(receipt_single.calc_weight(), 100)

    def test_large_ingredient_list(self):
        large_ingredient_list = [("Ингредиент_" + str(i), 100, 90, 50) for i in range(100)]
        receipt_large = Receipt("Большой рецепт", large_ingredient_list)
        self.assertEqual(receipt_large.calc_cost(), 5000) 
        self.assertEqual(receipt_large.calc_weight(), 10000)  


if __name__ == "__main__":
    unittest.main()