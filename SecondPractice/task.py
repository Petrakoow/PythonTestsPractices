class Ingredient:
    MAX_COST = 1000;
    def __init__(self, name: str, raw_weight: (int, float), cooked_weight: (int, float), cost: (int, float)) -> None:
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
