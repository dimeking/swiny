import unittest
from hyphenate import hyphenate_word
 
class TestHyphenate(unittest.TestCase):
 
    def setUp(self):
        pass
 
    def test_hyphenate_example(self):
        parts = hyphenate_word("example")
        print(parts)
        self.assertEqual(len(parts), 3)
 
    def test_hyphenate_flower(self):
        parts = hyphenate_word("output")
        print(parts)
        self.assertEqual(len(parts), 2)
  
if __name__ == '__main__':
    unittest.main()