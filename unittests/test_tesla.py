import car.tesla as tesla

def test_tesla_name1():
  t = tesla.tesla()
  assert t.name() == 1

def test_tesla_name100():
  t = tesla.tesla()
  assert t.name() == 100