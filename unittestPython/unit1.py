import unittest 

class Test_coolify(unittest.TestCase):
  def test_name(self):
    name = "key"
    self.assertTrue(name.colify(name) == "key is cool")

if __name__ == '__main__':
  unittest.main()