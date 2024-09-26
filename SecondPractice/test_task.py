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


class TestReceipt(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.valid_receipt_data = [("Яйцо", 80, 70, 20), ("Бекон", 200, 100, 300)]
        cls.receipt_name = "Яичница с беконом"
    
    def setUp(self):
        self.receipt = Receipt(self.receipt_name, self.valid_receipt_data)

    def tearDown(self):
        del self.receipt

    @classmethod
    def tearDownClass(cls):
        cls.valid_receipt_data = None
        cls.receipt_name = None

    def test_valid_receipt(self):
        self.assertEqual(self.receipt.name, self.receipt_name)
        self.assertEqual(len(self.receipt.ingredients), 2)

    def test_invalid_receipt_name(self):
        with self.assertRaises(ValueError):
            Receipt("", [("Яйцо", 80, 70, 20)])  # empty name
        with self.assertRaises(ValueError):
            Receipt(123, [("Яйцо", 80, 70, 20)])  # non-string name

    def test_invalid_ingredient_list(self):
        with self.assertRaises(ValueError):
            Receipt("Яичница", [])  # empty ingredient list
        with self.assertRaises(ValueError):
            Receipt("Яичница", [("Яйцо", 80, 70, 20), ("Недопустимый", -10, 70, 20)])  # invalid ingredient

    def test_calc_cost(self):
        self.assertEqual(self.receipt.calc_cost(), 320)  # 20 + 300
        self.assertEqual(self.receipt.calc_cost(2), 640)  # 320 * 2

    def test_calc_weight(self):
        self.assertEqual(self.receipt.calc_weight(), 280)  # 80 + 200
        self.assertEqual(self.receipt.calc_weight(raw=False), 170)  # 70 + 100
        self.assertEqual(self.receipt.calc_weight(portions=2), 560)  # 280 * 2
        
    def test_receipt_with_single_ingredient(self):
        receipt = Receipt("Яичница", [("Яйцо", 80, 70, 20)])
        self.assertEqual(receipt.calc_cost(), 20)
        self.assertEqual(receipt.calc_weight(), 80)
        self.assertEqual(receipt.calc_weight(raw=False), 70)

    def test_receipt_with_float_ingredients(self):
        receipt = Receipt("Смузи", [("Банан", 150.5, 130.5, 60.5), ("Клубника", 100.2, 90.2, 40.2)])
        self.assertAlmostEqual(receipt.calc_cost(), 100.7)  # 60.5 + 40.2
        self.assertAlmostEqual(receipt.calc_weight(), 250.7)  # 150.5 + 100.2

    def test_receipt_name_case_insensitivity(self):
        receipt = Receipt("ЯИЧНИЦА", [("Яйцо", 80, 70, 20), ("Бекон", 200, 100, 300)])
        self.assertEqual(receipt.name.lower(), "яичница".lower())  # Check case insensitivity

if __name__ == "__main__":
    unittest.main()
