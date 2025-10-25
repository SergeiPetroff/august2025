import car.tesla as tesla

class tesla2025(tesla.tesla):
  def name(self):
    return 2025
  
def test_tesla2025():
  t2025 = tesla2025()
  assert t2025.name() == 2025