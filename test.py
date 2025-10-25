class Pizza:
  def __init__(self, ingredients):
    self.ingredients = ingredients

  @classmethod
  def margherita(cls):
    return cls(["mozzarella", "tomatoes"])
  
  @classmethod
  def pepperoni(cls):
    return cls(["mozzarella", "pepperoni"])
  
  @staticmethod
  def ass(x):
    print('ass', x)
  
pizza1 = Pizza.margherita()
pizza2 = Pizza.pepperoni()

print(pizza1, pizza2)

print(pizza1.ingredients)

Pizza.ass("hay")

pizza2.ass("milk")