class tesla:
  def name(self):
    print('Tesla')
    return 1
  
def test_tesla_name0():
  t = tesla()
  assert t.name() == 0
  
def test_tesla_name1():
  t = tesla()
  assert t.name() == 1
